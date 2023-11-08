import cv2
from cosine_similarity import *
from numpy import *

gambar1 = cv2.imread('../../src/nyoba_nopal/0.jpg')
gambar2 = cv2.imread('../../src/nyoba_nopal/hitam.jpg')

# ########## FOR TEST
# importing os module   
import os 
# Image directory 
directory = r'C:\Users\Naufal\Documents\003. TAHUN KEDUA\SEMESTER 3\ALGEO\TUBES 2\Algeo02-22013\src\nyoba_nopal'
os.chdir(directory) 


def coba1(image1, image2):
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

    # Inisialisasi histogram
    histogram1 = [0 for i in range(72)]
    histogram2 = [0 for i in range(72)]

    sum_cosine = 0
    c = 0
    # Crop out the window and calculate the histogram
    # Number of pieces Horizontally 
    W_SIZE  = 3 
    # Number of pieces Vertically to each Horizontal  
    H_SIZE = 3
    for ih in range(0, H_SIZE ):
        for iw in range(0, W_SIZE ):
            x = col1/W_SIZE * iw 
            y = row1/H_SIZE * ih
            h = (row1 / H_SIZE)
            w = (col1 / W_SIZE )
            # print(x,y,h,w)
            img1 = gambar1[int(y):int(y+h), int(x):int(x+w)]
            img2 = gambar2[int(y):int(y+h), int(x):int(x+w)]
            # RGBimage1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            # histogram1 = rgb_to_histogram(img1[ih][iw][0],img1[ih][iw][1],img1[ih][iw][2],histogram1)
            # histogram2 = rgb_to_histogram(img2[ih][iw][0],img2[ih][iw][1],img2[ih][iw][2],histogram2)

            # loop untuk tiap piksel di 1/9 blocks of image
            for i in range(0,int(row1/3)):
                for j in range(0,int(col1/3)):
                    histogram1 = rgb_to_histogram(img1[i][j][0],img1[i][j][1],img1[i][j][2],histogram1)
                    histogram2 = rgb_to_histogram(img2[i][j][0],img2[i][j][1],img2[i][j][2],histogram2)

                    sum_cosine += cosine_sim(histogram1,histogram2)
                    c += 1

    return sum_cosine/c


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
    if 360 >= h >= 316:
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
    elif h < 316:
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
    [h,s,v] = quantify_hsv(h,s,v)
    index = 24*v + 8*s + h
    l[index] += 1
    
    return l


# print(f"cosine similarity : {CBIR_warna(gambar1,gambar2)}")
# print(f"cosine similarity 3x3: {CBIR_warna_33(gambar1,gambar2)}")
# print(f"cosine similarity 2: {CBIR_warna_noresize(gambar1,gambar2)}")

print(f"cosine similarity : {coba1(gambar1,gambar2)}")
# CBIR_warna(gambar1,gambar2)
# coba1(gambar1,gambar2)