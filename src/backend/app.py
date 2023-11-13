from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
from flask_cors import CORS
import taichi as ti
import cv2
import os
import csv
import shutil

from tekstur import *
from finder import *
from warna import *

app = Flask(__name__)
CORS(app)

@app.route('/')
def cekawal():
	if os.path.exists('../../img/retrieve') == True :
		shutil.rmtree('../../img/retrieve') # delete retrieve folder
        # shutil.rmtree('../../img/uploaded') # delete upload recent image
		# shutil.rmtree('static/tmp')
		return redirect('/home')
	else :
		return redirect('/home')

@app.route('/home', methods=['GET'])
def home():
    # dataset = os.listdir('../../img/dataset')
    
    if os.path.exists('../../img/retrieve') == True:
        nilai_gambar = os.listdir('../../img/retrieve')
        similar = sorted(os.listdir('../../img/retrieve'))[0]
        imageFind = os.listdir('../../img/uploaded') # udah gaperlu, dah didisplay 

        return render_template('index.html', nilai_gambar = sorted(nilai_gambar), imageFind = (imageFind), similar = (similar), page_status = 1) # page status, untuk nandain berubah tampilan
    else :
        return render_template("index.html", page_status = 2)

# upload dataset banyak
@app.route('/dataset', methods=['POST'])
def upload():
    images = request.files.getlist('imagefiles[]')
    # print('images', images)
    # print(request.files)
    for image in images:
        image_path = "../../img/" + image.filename
        image.save(image_path)
    return redirect("/home")

    # images = request.files.getlist('imagefiles')
    # for image in images:
    #     image_path = "../../img/dataset/" + image.filename
    #     image.save(image_path)
    
    # image = request.files['imagefile']
    # image_path = "../../img/dataset/" + image.filename
    # image.save(image_path)
    # return redirect("/home")

# UPLOAD_FOLDER = '../../img/uploaded'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # Ensure the 'uploads' folder exists
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# upload gambar yang mau dicari 
@app.route('/search', methods=['POST'])
def search():
    # image = request.files['imagefile']
    # # filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    # image_path = "../../img/uploaded/" + image.filename
    # image.save(image_path)
    
    # Access image file from form data
    image = request.files['imagefile']
    # Access selected option from form data
    selected_option = request.form['selectedOption']

    # Choose the appropriate image path based on the selected option
    if selected_option == 'texture':
        os.makedirs('../../img/uploaded', exist_ok=True)
        # os.makedirs('../../img/uploaded')
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
            simpanRetrieve = cv2.imwrite("../../img/retrieve/" + str(nilai) + str(i) + ".jpeg", hasil)
        
        return redirect("/home")

    elif selected_option == 'color':
        os.makedirs('../../img/uploaded', exist_ok=True)
        # os.makedirs('../../img/uploaded')
        image_path = "../../img/uploaded/" + image.filename
        image.save(image_path)
    
        imageInput = cv2.imread("../../img/uploaded/"+image.filename)
        fitur_tekstur = fitur(imageInput)
        hasil_tekstur = find(fitur_tekstur,selected_option)
        
        os.makedirs('../../img/retrieve', exist_ok=True) 
        i = 1 # i untuk penamaan
        for (nilai, IDhasil) in hasil_tekstur:
            i += 1
            print(nilai,IDhasil) # delete
            hasil = cv2.imread("../../img/dataset/"+IDhasil)
            simpanRetrieve = cv2.imwrite("../../img/retrieve/" + str(nilai) + str(i) + ".jpeg", hasil)
        
        return redirect("/home")


@app.route('/retrieve-images')
def retrieve_images():
    retrieve_folder = "../../img/retrieve/"
    image_urls = []

    for filename in os.listdir(retrieve_folder):
        if filename.endswith(".jpeg"):
            image_urls.append(f'/img/retrieve/{filename}')

    return jsonify(image_urls)

@app.route('/img/<path:path>')
def send_report(path):
    return send_from_directory('../../img', path)


    # # baca gambar yang diupload BISA GINI GA YA
    # imageFind = cv2.imread(f'../../img/uploaded/{image.filename}')

    # # ekstraksi fitur gambar
    # fitur_warna = None # import file .py, panggil fungsinya
    # fitur_tekstur = None # import file .py, panggil fungsinya
    # search_warna = None('fitur/warna.csv') # pake class, masukkan path .csv
    # search_tekstur = None('fitur/tekstur.csv') # pake class, masukkan path .csv
    # hasil_warna = search_warna.None(fitur_warna) # simpan hasil cosine, panggil fungsi
    # hasil_tekstur = search_tekstur.None(fitur_tekstur) # simpan hasil cosine, panggil fungsi

    # # direktori untuk hasil search
    # os.makedirs('../../img/retrieve') 

    # i = 1 # i untuk penamaan
    # for (nilai, IDhasil) in hasil_warna:
    #     i += 1
    #     hasil = cv2.imread("../../img/dataset/"+IDhasil)
    #     simpanRetrieve = cv2.imwrite("../../img/retrieve/" + str(nilai) + str(i) + ".jpeg", hasil)
    
    # return redirect("/home")

    


if __name__ == '__main__':
    app.run(port=3005, debug=True, threaded=False)