#--------- File app.py: proses utama (main) ---------#
# Import library
from flask import Flask, request, redirect, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import os
import csv
import shutil
import urllib.request 
import subprocess
import base64
import requests
from bs4 import BeautifulSoup
from timeit import default_timer as timer

# Import dari file
from tekstur import *
from finder import *


app = Flask(__name__)
CORS(app)


########## Upload dataset (folder) ##########
@app.route('/dataset', methods=['POST'])
def upload():
    # Reset dataset
    if os.path.exists('../../img/dataset') == True :
        shutil.rmtree('../../img/dataset')
        os.makedirs('../../img/dataset')

    images = request.files.getlist('imagefiles[]')
    for image in images:
        image_path = "../../img/" + image.filename
        image.save(image_path)
    
    # Ekstraksi fitur image dataset
    command = "python3 init.py"
    subprocess.run(command, shell=True)
    command = "python init.py"
    subprocess.run(command, shell=True)

    print("Ekstraksi selesai!") # delete
    return jsonify(message="Dataset selesai diekstrak")


########## Upload gambar yang mau dicari ##########
@app.route('/search', methods=['POST', 'GET'])
def search():
    start = timer()

    # Bersihkan direktori
    if os.path.exists('../../img/retrieve') == True :
        shutil.rmtree('../../img/retrieve')
        shutil.rmtree('../../img/uploaded')

    if os.path.exists('../../img/uploaded') == True :
        shutil.rmtree('../../img/uploaded')
    # Akses image file dan selected option dari  form data
    image = request.files['imagefile']
    selected_option = request.form['selectedOption']

    # Opsi
    # Membandingkan cosine similarity tekstur gambar query dengan dataset
    if selected_option == 'texture':
        os.makedirs('../../img/uploaded', exist_ok=True)
        image_path = "../../img/uploaded/" + image.filename
        image.save(image_path)

        imageInput = cv2.imread("../../img/uploaded/"+image.filename)
        fitur_tekstur = CBIR_tekstur(imageInput)
        hasil_tekstur = find(fitur_tekstur,selected_option)

        os.makedirs('../../img/retrieve', exist_ok=True) 
        for (nilai, IDhasil) in hasil_tekstur:
            hasil = cv2.imread("../../img/dataset/"+IDhasil)
            cv2.imwrite("../../img/retrieve/" + str(nilai*100) + ".jpeg", hasil)
        

    # Membandingkan cosine similarity warna gambar query dengan dataset
    elif selected_option == 'color':
        os.makedirs('../../img/uploaded', exist_ok=True)
        image_path = "../../img/uploaded/" + image.filename
        image.save(image_path)

        command = "python3 warna_individual.py"
        subprocess.run(command, shell=True)
        command = "python warna_individual.py"
        subprocess.run(command, shell=True)
    
    # Timer
    end = timer()
    durasi = round((end - start), 2)
    print("durasi: ", durasi) # delete

    # Durasi csv
    os.makedirs('durasi', exist_ok=True)
    output_durasi = open("durasi/durasi.csv", "w")
    output_durasi.write("%s\n"%durasi)
    output_durasi.close()
    return redirect('/durasi')

########## Mengembalikan durasi pencarian ##########
@app.route('/durasi')
def durasi():
    output_durasi = "durasi/durasi.csv"
    with open(output_durasi) as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    waktu = (data[0])[0]
    print("dudur: ", (data[0])[0]) # delete
    return jsonify({'data': waktu})

########## Mengembalikan similar image ke frontend ##########
@app.route('/retrieve-images')
def retrieve_images():
    retrieve_folder = "../../img/retrieve/"
    image_urls = []

    # Sort nilai image di folder dari yang tertinggi
    for filename in sorted(os.listdir(retrieve_folder), key=lambda x: int(x.split('.')[0]), reverse=True):
        if filename.endswith(".jpeg"):
            image_urls.append(f'/img/retrieve/{filename}')

    return jsonify(image_urls)

@app.route('/img/<path:path>')
def send_report(path):
    return send_from_directory('../../img', path)

def getdata(url):  
    r = requests.get(url)  
    return r.text  

@app.route('/scrape', methods=['POST'])
def scrape():
    if os.path.exists('../../img/dataset') == True :
        shutil.rmtree('../../img/dataset')
        os.makedirs('../../img/dataset')

    if 'url' not in request.form:
        print("0 ")
        return "No URL provided."
    
    url = request.form['url']
    print(url)
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html5lib")
    links = soup.select('div img')

    x = 0
    for f in links:
        print(f["src"])
        img_data = requests.get(f['src']).content
        with open('../../img/dataset/' + str(x) + '.jpg', 'wb') as handler: 
            handler.write(img_data)
        x+=1

    command = "python3 init.py"
    subprocess.run(command, shell=True)
    command = "python init.py"
    subprocess.run(command, shell=True)

    print("Ekstraksi selesai!") # delete
    return jsonify(message="Dataset selesai diekstrak")

@app.route('/camera', methods=['POST'])
def capture():
    # Bersihkan direktori
    if os.path.exists('../../img/retrieve') == True :
        shutil.rmtree('../../img/retrieve')
        shutil.rmtree('../../img/uploaded')

    if os.path.exists('../../img/uploaded') == True :
        shutil.rmtree('../../img/uploaded')
    
    # Akses image file
    image = request.files['image']

    os.makedirs('../../img/uploaded', exist_ok=True)
    image_path = "../../img/uploaded/" + "ganteng.jpg"
    image.save(image_path)

    return jsonify(message="Foto telah diupload")


if __name__ == '__main__':
    app.run(port=3005, debug=True, threaded=False)