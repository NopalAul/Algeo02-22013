from flask import Flask, render_template, request, redirect
# from flask_cors import CORS
import cv2
import os
import csv
import shutil

app = Flask(__name__)
# CORS(app)

@app.route('/')
def cekawal():
	if os.path.exists('../../img/retrieve') == True :
		shutil.rmtree('../../img/retrieve') # delete retrieve folder
		# shutil.rmtree('static/tmp')
		return redirect('/home')
	else :
		return redirect('/home')

@app.route('/home', methods=['GET'])
def home():
    dataset = os.listdir('../../img/dataset')
    
    if os.path.exists('../../img/retrieve') == True:
        nilai_gambar = os.listdir('../../img/retrieve')
        similar = sorted(os.listdir('../../img/retrieve'))[0]
        imageFind = os.listdir('../../img/uploaded')

        return render_template('index.html', nilai_gambar = sorted(nilai_gambar), imageFind = (imageFind), similar = (similar), page_status = 1) # page status, untuk nandain berubah tampilan
    else :
        return render_template("index.html", page_status = 2)

# upload gambar yang mau dicari 
@app.route('/search', methods=['POST'])
def search():
    image = request.files['imagefile']
    image_path = "../../img/uploaded" + image.filename
    image.save(image_path)

    # baca gambar yang diupload BISA GINI GA YA
    imageFind = cv2.imread(f'../../img/uploaded/{image.filename}')

    # ekstraksi fitur gambar
    fitur_warna = None # import file .py, panggil fungsinya
    fitur_tekstur = None # import file .py, panggil fungsinya
    search_warna = None('fitur/warna.csv') # pake class, masukkan path .csv
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
    
    return redirect("/home")

    


if __name__ == '__main__':
    app.run(port=3000, debug=True)  