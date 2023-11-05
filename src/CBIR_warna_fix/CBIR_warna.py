import cv2
from cosine_similarity import *
from numpy import array

gambar1 = cv2.imread('../../src/nyoba/0.jpg')
gambar2 = cv2.imread('../../src/nyoba/mobilmerah.jpg')

def CBIR_warna(image1,image2):
    # Resize image ke ukuran terkecil (for performance purpose)
    row1, col1 = image1.shape[0], image1.shape[1]
    row2, col2 = image2.shape[0], image2.shape[1]
    if col1*row1 > col2*row2:
        image1 = cv2.resize(image1, (row2, col2))
        row1 = row2
        col1 = col2
    else:
        image2 = cv2.resize(image2, (row1, col1))
        row2 = row1
        col2 = col1

    # Ekstraksi image ke komponen RGB-nya
    RGBimage1 = array(image1)
    RGBimage2 = array(image2)

    # Inisialisasi histogram
    histogram1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    histogram2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    # Pencarian histogram per 3x3 blok gambar
    # masih problem, di input gambar hitamdoang.jpg vs mobilmerah.jpg
    # print(row1)
    # print(col1)
    # i = 0
    # j = 0
    # while i < row1:
    #     while j < col1:
    for i in range(0,row1,3):
        for j in range(0,col1,3):
            histogram1 = rgb_to_histogram(RGBimage1[i][j][2],RGBimage1[i][j][1],RGBimage1[i][j][0],histogram1)
            histogram2 = rgb_to_histogram(RGBimage2[i][j][2],RGBimage2[i][j][1],RGBimage2[i][j][0],histogram2)
        #     j += 3
        # i += 3
    
    # Komparasi cosine similarity kedua vektor histogram HSV
    return cosine_sim(histogram1,histogram2)

# Konversi RGB space ke HSV space, lalu ke histogram (kuantifikasi)
def rgb_to_histogram(r,g,b,l):
    # normalisasi
    r = r/255
    g = g/255
    b = b/255

    # nilai ekstrim
    cmax = max(r,g,b)
    cmin = min(r,g,b)
    delta = cmax - cmin

    # nilai HSV
    ## H
    if cmax == cmin :
        h = 0
    elif cmax == r :
        h = 60*(((g-b)/delta) % 6)
    elif cmax == g :
        h = 60*(((b-r)/delta) + 2)
    else :
        h = 60*(((r-g)/delta) + 4)
    ## S
    if cmax != 0 :
        s = (delta/cmax)
    else :
        s = 0
    ## V
    v = cmax
    return hsvtohistogram(h,s,v,l)
    
# Kuantifikasi HSV space, simpan ke list l sebagai histogram HSV
def hsvtohistogram(h,s,v,l):
    if h >= 316:
        l[0] += 1
    elif h <= 25:
        l[1] += 1
    elif h <= 40:
        l[2] += 1
    elif h <= 120:
        l[3] += 1
    elif h <= 190:
        l[4] += 1
    elif h <= 270:
        l[5] += 1
    elif h <= 295:
        l[6] += 1
    elif h <= 315:
        l[7] += 1
    if s < 0.2:
        l[8] += 1
    elif s < 0.7:
        l[9] += 1
    elif s >= 0.7:
        l[10] += 1
    if v < 0.2:
        l[11] += 1
    elif v < 0.7:
        l[12] += 1
    elif v >= 0.7:
        l[13] += 1
    return l


print(f"cosine similarity : {CBIR_warna(gambar1,gambar2)}")