#--------- File app.py: proses utama (main) ---------#
# Import library
from flask import Flask, request, redirect, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import os
import csv
import shutil
import subprocess
import requests
import base64
import urllib.request
from bs4 import BeautifulSoup
from timeit import default_timer as timer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image

# Import dari file
from tekstur import *
from finder import *

app = Flask(__name__)
CORS(app)

########## Upload dataset (folder) ##########
@app.route('/dataset', methods=['POST'])
def upload():
    # Reset dataset
    images = request.files.getlist('imagefiles[]')
    dirName = images[0].filename.split('/')[0]
    if os.path.exists('../../img/dataset') == True :
        shutil.rmtree('../../img/dataset')

    # Buat direktori baru
    os.makedirs('../../img/' + dirName)

    print(dirName) # delete
    for image in images:
        image_path = "../../img/" + image.filename
        image.save(image_path)
    
    source_path = os.path.abspath('../../img/' + dirName)
    destination_path = os.path.abspath('../../img/dataset')
    os.rename(source_path, destination_path)

    # Ekstraksi fitur image dataset
    command = "python3 init.py"
    subprocess.run(command, shell=True)
    command = "python init.py"
    subprocess.run(command, shell=True)
    command = "python3 init.py"
    subprocess.run(command, shell=True)

    print("Ekstraksi selesai!") # delete
    return jsonify(message="Upload process completed!")


########## Upload gambar yang mau dicari ##########
@app.route('/search', methods=['POST', 'GET'])
def search():
    start = timer()

    # Bersihkan direktori
    if os.path.exists('../../img/retrieve') == True :
        shutil.rmtree('../../img/retrieve')
        shutil.rmtree('../../img/uploaded')

    # Akses image file dan selected option dari  form data
    isCaptured = request.form['isCaptured']
    print(isCaptured) # delete
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
            if(nilai >= 0.6):
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
        command = "python3 warna_individual.py"
        subprocess.run(command, shell=True)
        # fitur()

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

# generate pdf

pdf_counter = 1

def get_next_pdf_filename():
    global pdf_counter
    pdf_filename = f"../../img/pdf/result-{pdf_counter}.pdf"
    pdf_counter += 1
    return pdf_filename

def resize_image(image_path, width, height):
    img = Image.open(image_path)
    img = img.resize((width, height), Image.ANTIALIAS)
    
    resized_image_path = image_path.replace(".jpeg", "_resized.jpeg")
    img.save(resized_image_path, "JPEG")
    
    return resized_image_path

@app.route('/generate-pdf')
def generate_pdf():
    retrieve_folder = "../../img/retrieve/"

    # next unique PDF filename
    pdf_filename = get_next_pdf_filename()

    # create new PDF document
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # title to the first page
    c.setFont("Helvetica", 16)
    c.drawString(100, 750, "Search Result")

    y_position = 500  # initial y position
    page_number = 1

    for filename in sorted(os.listdir(retrieve_folder), key=lambda x: int(x.split('.')[0]), reverse=True):
        if filename.endswith(".jpeg"):
            image_path = os.path.join(retrieve_folder, filename)

            # check if the current y position exceeds the page height
            if y_position <= 50:
                # create new page
                c.showPage()
                page_number += 1
                y_position = 500  # reset y position for the new page

            # resize image
            resized_image_path = resize_image(image_path, width=200, height=150)

            # percentage
            percentage = filename[0:5]

            # add resize image to page
            c.drawImage(resized_image_path, 100, y_position, width=200, height=150)
            c.drawString(150, y_position - 20, f"{percentage}%")

            y_position -= 200

    c.save()

    return send_from_directory('../../img/pdf/', f'result-{pdf_counter-1}.pdf')
 
def getdata(url):  
    r = requests.get(url)  
    return r.text  

@app.route('/scrape', methods=['POST'])
def scrape():
    if os.path.exists('../../img/dataset') == True :
        shutil.rmtree('../../img/dataset')
        os.makedirs('../../img/dataset')

    if 'url' not in request.form:
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

    return jsonify(message="Image has successfully uploaded")

if __name__ == '__main__':
    app.run(port=3005, debug=True, threaded=False)