import cv2
from cosine_similarity import *
from numpy import array

# gambar1 = cv2.imread('../../src/nyoba/0.jpg')
# gambar2 = cv2.imread('../../src/nyoba/mobilmerah.jpg')

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
    RGBimage1 = array(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
    RGBimage2 = array(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
    # print(RGBimage1)

    # Inisialisasi histogram
    histogram1 = [0 for i in range(72)]
    histogram2 = [0 for i in range(72)]

    # Pencarian histogram per 3x3 blok gambar
    i = 0
    j = 0
    while i < row1:
        while j < col1:
            histogram1 = rgb_to_histogram(RGBimage1[i][j][0],RGBimage1[i][j][1],RGBimage1[i][j][2],histogram1)
            histogram2 = rgb_to_histogram(RGBimage2[i][j][0],RGBimage2[i][j][1],RGBimage2[i][j][2],histogram2)
            j += 3
        i += 3
        
    
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

# Kuantifikasi nilai HSV
def quantify_hsv(h,s,v):
    if h >= 316:
        h = 0
    elif h <= 25:
        h = 1
    elif h <= 40:
        h = 2
    elif h <= 120:
        h = 3
    elif h <= 190:
        h = 4
    elif h <= 270:
        h = 5
    elif h <= 295:
        h = 6
    elif h <= 315:
        h = 7
    if s < 0.2:
        s = 0
    elif s < 0.7:
        s = 1
    elif s >= 0.7:
        s = 2
    if v < 0.2:
        v = 0
    elif v < 0.7:
        v = 1
    elif v >= 0.7:
        v = 2
    return [h,s,v]

# Simpan HSV terkuantifikasi ke list l sebagai histogram HSV
def hsvtohistogram(h,s,v,l):
    index = 24*v + 8*s + h
    l[index] += 1
    
    return l

def imagetohistogram(image):
    RGBimage = array(image)
    # print("noresize: ",RGBimage)
    # Inisialisasi histogram
    histogram = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    # Pencarian histogram per 3x3 blok gambar
    i = 0
    j = 0
    row,col = image.shape[0], image.shape[1]
    while i < row:
        while j < col:
    # for i in range(0,row1,3):
    #     for j in range(0,col1,3):
            histogram = rgb_to_histogram(RGBimage[i][j][0],RGBimage[i][j][1],RGBimage[i][j][2],histogram)
            j += 3
        i += 3
    
    # Komparasi cosine similarity kedua vektor histogram HSV
    return histogram

def CBIR_warna_noresize(image1,image2):
    return cosine_sim(imagetohistogram(image1),imagetohistogram(image2))

# print(f"cosine similarity : {CBIR_warna(gambar1,gambar2)}")
# print(f"cosine similarity 2: {CBIR_warna_noresize(gambar1,gambar2)}")