#--------- File app.py: proses utama (main) ---------#
# Import library
from flask import Flask, request, redirect, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import os
import csv
import shutil
import subprocess
from timeit import default_timer as timer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image

c = canvas.Canvas("hello.pdf")
c.drawString(100, 100, "Welcome to Reportlab!")
c.showPage()
c.save()

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
    # except:
    #     traceback.print_stack() # delete
    # Ekstraksi fitur image dataset
    command = "python3 init.py"
    subprocess.run(command, shell=True)
    command = "python init.py"
    subprocess.run(command, shell=True)
    command = "python3 init.py"
    subprocess.run(command, shell=True)
    # warna_csv()
    # tekstur_csv()

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
@app.route('/generate-pdf')
def generate_pdf():
    retrieve_folder = "../../img/retrieve/"
    pdf_filename = "../../img/result.pdf"

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
                y_position = 500  # reset Y position for the new page

            # resize image
            resized_image_path = resize_image(image_path, width=200, height=150)

            # percentage
            percentage = filename[0:5]

            # add resize image to page
            c.drawImage(resized_image_path, 100, y_position, width=200, height=150)
            c.drawString(150, y_position - 20, f"{percentage}%")

            y_position -= 200

    c.save()

    return send_from_directory('../../img', 'result.pdf')

def resize_image(image_path, width, height):
    img = Image.open(image_path)
    img = img.resize((width, height), Image.ANTIALIAS)
    
    resized_image_path = image_path.replace(".jpeg", "_resized.jpeg")
    img.save(resized_image_path, "JPEG")
    
    return resized_image_path


if __name__ == '__main__':
    app.run(port=3005, debug=True, threaded=False)