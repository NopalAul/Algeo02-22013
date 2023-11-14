from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
from flask_cors import CORS
import taichi as ti
import cv2
import os
import csv
import shutil
import glob

from tekstur import *
from finder import *
# from warna import *

import subprocess

app = Flask(__name__)
CORS(app)


@app.route('/home', methods=['GET'])
def home():
    # dataset = os.listdir('../../img/dataset')
    
    if os.path.exists('../../img/retrieve') == True:
        # nilai_gambar = os.listdir('../../img/retrieve')
        # similar = sorted(os.listdir('../../img/retrieve'))[0]
        # imageFind = os.listdir('../../img/uploaded') # udah gaperlu, dah didisplay 

        return render_template('index.html') # page status, untuk nandain berubah tampilan
    else :
        return render_template("index.html", page_status = 2)
    


# Upload dataset (folder)
@app.route('/dataset', methods=['POST'])
def upload():
    images = request.files.getlist('imagefiles[]')
    for image in images:
        image_path = "../../img/" + image.filename
        image.save(image_path)

    # # Ekstrak tekstur
    # output_tekstur = open("fitur/tekstur.csv", "w")
    # for imagePath in glob.glob("../../img/dataset/*"):
    #     imageID = imagePath[imagePath.rfind("\\") + 1:]
    #     image = cv2.imread(imagePath)

    #     fitur_tekstur = CBIR_tekstur(image) # ekstraksi tekstur per gambar
    #     fitur_tekstur = [str(f) for f in fitur_tekstur]
    #     output_tekstur.write("%s,%s\n" % (imageID, ",".join(fitur_tekstur)))

    # output_tekstur.close()
    # Ekstrak warna
    # warna_csv()
    command = "python init.py"
    subprocess.run(command, shell=True)

    print("Ekstraksi selesai!") # delete
    return redirect("/home")


# Upload gambar yang mau dicari 
@app.route('/search', methods=['POST'])
def search():
    # Bersihkan direktori
    if os.path.exists('../../img/retrieve') == True :
        shutil.rmtree('../../img/retrieve')
        shutil.rmtree('../../img/uploaded')

    # Akses image file dan selected option dari  form data
    image = request.files['imagefile']
    selected_option = request.form['selectedOption']

    # Opsi
    if selected_option == 'texture':
        os.makedirs('../../img/uploaded', exist_ok=True)
        image_path = "../../img/uploaded/" + image.filename
        image.save(image_path)

        imageInput = cv2.imread("../../img/uploaded/"+image.filename)
        fitur_tekstur = CBIR_tekstur(imageInput)
        hasil_tekstur = find(fitur_tekstur,selected_option)

        os.makedirs('../../img/retrieve', exist_ok=True) 
        i = 1 # i untuk penamaan
        for (nilai, IDhasil) in hasil_tekstur:
            i += 1
            hasil = cv2.imread("../../img/dataset/"+IDhasil)
            cv2.imwrite("../../img/retrieve/" + str(nilai) + str(i) + ".jpeg", hasil)
        
        return redirect("/home")

    elif selected_option == 'color':
        os.makedirs('../../img/uploaded', exist_ok=True)
        image_path = "../../img/uploaded/" + image.filename
        image.save(image_path)

        command = "python warna.py"
        subprocess.run(command, shell=True)
        # imageInput = cv2.imread("../../img/uploaded/"+image.filename)
        # fitur(imageInput) # masih error
        # command = "python warna.py"
        # subprocess.run(command, shell=True)

        # hasil_tekstur = find(fitur_tekstur,selected_option)
        
        # os.makedirs('../../img/retrieve', exist_ok=True) 
        # i = 1 # i untuk penamaan
        # for (nilai, IDhasil) in hasil_tekstur:
        #     i += 1
        #     print(nilai,IDhasil) # delete
        #     hasil = cv2.imread("../../img/dataset/"+IDhasil)
        #     cv2.imwrite("../../img/retrieve/" + str(nilai) + str(i) + ".jpeg", hasil)
        
        return redirect("/home")

# Mengembalikan similar image ke frontend
@app.route('/retrieve-images')
def retrieve_images():
    retrieve_folder = "../../img/retrieve/"
    image_urls = []

    # Sort nilai image di folder dari yang tertinggi
    for filename in sorted(os.listdir(retrieve_folder), reverse=True):
        if filename.endswith(".jpeg"):
            image_urls.append(f'/img/retrieve/{filename}')

    return jsonify(image_urls)

@app.route('/img/<path:path>')
def send_report(path):
    return send_from_directory('../../img', path)


    


if __name__ == '__main__':
    app.run(port=3005, debug=True, threaded=False)