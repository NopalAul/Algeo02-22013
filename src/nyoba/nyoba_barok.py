import cv2
from PIL import Image
from cosine_similarity import *
from numpy import array


gambar1 = cv2.imread('0.jpg')
gambar2 = cv2.imread('mobilmerah.jpg')

def CBIR_warna(image1,image2):
    # Resize image ke ukuran terkecil (for performance purpose)

    
    row1, col1 = image1.shape[0], image1.shape[1]
    row2, col2 = image2.shape[0], image2.shape[1]

    if col1*row1 > col2*row2:
        image1 = cv2.resize(image1, (col2, row2))
        row1 = row2
        col1 = col2
    else:
        image2 = cv2.resize(image2, (col1, row1))
        row2 = row1
        col2 = col1

    # Ekstraksi image ke komponen RGB-nya
    RGBimage1 = array(image1)
    RGBimage2 = array(image2)

    # Inisialisasi histogram

    sum = 0
    c = 0
    # Pencarian histogram per 3x3 blok gambar
    for i in range(0,row1,3):
        for j in range(0,col1,3):
            histogram1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            histogram2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            k = i + 3
            l = j + 3
            if i + 3 > row1:
                k = row1
            if j + 3 > row1:
                l = col1
            for k in range(i,k):
                for l in range(j,l):
                    histogram1 = rgb_to_histogram(RGBimage1[k][l][2],RGBimage1[k][l][1],RGBimage1[k][l][0],histogram1)
                    histogram2 = rgb_to_histogram(RGBimage2[k][l][2],RGBimage2[k][l][1],RGBimage2[k][l][0],histogram2)
            sum += cosine_sim(histogram1,histogram2)
            c += 1
    
    # Komparasi cosine similarity kedua vektor histogram HSV
    return sum/c

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

def imagetohistogram(image):
    RGBimage = array(image)

    # Inisialisasi histogram
    histogram = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    # Pencarian histogram per 3x3 blok gambar
    row,col = image.shape[0], image.shape[1]
    for i in range(0,row,3):
        for j in range(0,col,3):
            histogram = rgb_to_histogram(RGBimage[i][j][2],RGBimage[i][j][1],RGBimage[i][j][0],histogram)
    
    # Komparasi cosine similarity kedua vektor histogram HSV
    return histogram

print(f"cosine similarity : {CBIR_warna(gambar1,gambar2)}")
# print(f"cosine similarity 2: {cosine_sim(imagetohistogram(gambar1),imagetohistogram(gambar2))}")