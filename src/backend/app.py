from flask import Flask, render_template, request, redirect, jsonify, send_from_directory, url_for
from flask_cors import CORS
import taichi as ti
import cv2
import os
import csv
import shutil
import glob
from timeit import default_timer as timer


from tekstur import *
from finder import *
# from warna import *

import subprocess
import traceback

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 10000 * 10000 * 10000

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
    # print('test')
    # try:
    images = request.files.getlist('imagefiles[]')
    for image in images:
        print(f"File size: {len(image.read())} bytes")
        image.seek(0)  # Reset the file pointer to the beginning
        image_path = "../../img/" + image.filename
        image.save(image_path)
    # except:
    #     traceback.print_stack() # delete
    # Ekstraksi fitur image dataset
    command = "python init.py"
    subprocess.run(command, shell=True)
    command = "python3 init.py"
    subprocess.run(command, shell=True)
    # warna_csv()
    # tekstur_csv()

    print("Ekstraksi selesai!") # delete
    return redirect("/home")


# Upload gambar yang mau dicari 
@app.route('/search', methods=['POST'])
def search():
    start = timer()
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
        # i = 1 # i untuk penamaan
        for (nilai, IDhasil) in hasil_tekstur:
            # i += 1
            hasil = cv2.imread("../../img/dataset/"+IDhasil)
            cv2.imwrite("../../img/retrieve/" + str(nilai*100) + ".jpeg", hasil)
        

    elif selected_option == 'color':
        os.makedirs('../../img/uploaded', exist_ok=True)
        image_path = "../../img/uploaded/" + image.filename
        image.save(image_path)

        command = "python warna_individual.py"
        subprocess.run(command, shell=True)
        command = "python3 warna_individual.py"
        subprocess.run(command, shell=True)
        # fitur()

    # Timer
    end = timer()
    durasi = end - start
    print("durasi: ", durasi)
    return redirect(url_for('retrieve_duration', var=durasi))

@app.route('/retrieve_duration/<var>')
def retrieve_duration(var):
    return jsonify({'durasi' : var})

# Mengembalikan similar image ke frontend
@app.route('/retrieve-images')
def retrieve_images():
    retrieve_folder = "../../img/retrieve/"
    image_urls = []

    def get_numeric_part(filename):
        # Extracts the numeric part of the filename
        return int(''.join(filter(str.isdigit, filename)))

    # Sort nilai image di folder dari yang tertinggi
    for filename in sorted(os.listdir(retrieve_folder), key=lambda x: int(x.split('.')[0]), reverse=True):
        if filename.endswith(".jpeg"):
            image_urls.append(f'/img/retrieve/{filename}')

    return jsonify(image_urls)

@app.route('/img/<path:path>')
def send_report(path):
    return send_from_directory('../../img', path)


    


if __name__ == '__main__':
    app.run(port=3005, debug=True, threaded=False)