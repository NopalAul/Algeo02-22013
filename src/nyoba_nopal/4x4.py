import cv2
from cosine_similarity import *
from numpy import *

gambar1 = cv2.imread('../../src/nyoba_nopal/0.jpg')
gambar2 = cv2.imread('../../src/nyoba_nopal/mobilmerah.jpg')

# ########## FOR TEST
# importing os module   
import os 
# Image directory 
directory = r'C:\Users\Naufal\Documents\003. TAHUN KEDUA\SEMESTER 3\ALGEO\TUBES 2\Algeo02-22013\src\nyoba_nopal'
os.chdir(directory) 


def coba1(image):
    # Resize image ke ukuran terkecil (for performance purpose)
    row, col = image.shape[0], image.shape[1]
    print(row,col)

    # Inisialisasi histogram
    vector_hsv = [0 for i in range(32)]

    # Crop out the window and calculate the histogram
    # Number of pieces Horizontally 
    W_SIZE  = 4
    # Number of pieces Vertically to each Horizontal  
    H_SIZE = 4
    s=0
    for ih in range(0, H_SIZE ):
        for iw in range(0, W_SIZE ):
            vector = [0 for i in range(3)]
            x = col/W_SIZE * iw 
            y = row/H_SIZE * ih
            h = (row / H_SIZE)
            w = (col / W_SIZE )
            # print(x,y,h,w)
            img1 = gambar1[int(y):int(y+h), int(x):int(x+w)]
            # RGBimage1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            # cv2.imwrite("inihasil" + str(ih)+str(iw) +  ".png",img1)
            # vector_hsv = rgb_to_histogram(img1[ih][iw][0],img1[ih][iw][1],img1[ih][iw][2],vector_hsv)
            # histogram2 = rgb_to_histogram(img2[ih][iw][0],img2[ih][iw][1],img2[ih][iw][2],histogram2)

            # loop untuk tiap piksel di 1/9 blocks of image
            print(h,w)
            for i in range(0,round(h)-2):
                for j in range(0,round(w)-2):
                    # if j == 113 or i == 113:
                    #     print("ono")
                    vector[0] += rgb_to_histogram(img1[i][j][0],img1[i][j][1],img1[i][j][2])[0]
                    vector[1] += rgb_to_histogram(img1[i][j][0],img1[i][j][1],img1[i][j][2])[1]
                    vector[2] += rgb_to_histogram(img1[i][j][0],img1[i][j][1],img1[i][j][2])[2]
            
            i += 1
            j += 1
            vector[0] /= (i*j)
            vector[1] /= (i*j)
            vector[2] /= (i*j)
            vector_hsv[s:(s+2)] = vector
            s+=3

    return vector_hsv

# Konversi RGB space ke HSV space, lalu ke histogram (kuantifikasi)
def rgb_to_histogram(r,g,b):
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
    return quantify_hsv(h,s,v)

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


# print(f"cosine similarity : {CBIR_warna(gambar1,gambar2)}")
# print(f"cosine similarity 3x3: {CBIR_warna_33(gambar1,gambar2)}")
# print(f"cosine similarity 2: {CBIR_warna_noresize(gambar1,gambar2)}")
# coba1(gambar1)
print(f"cosine : {cosine_sim(coba1(gambar1),coba1(gambar2))}")
# CBIR_warna(gambar1,gambar2)
# coba1(gambar1,gambar2)

# import cython
# def printhsv(image):
#     histogram1 = [0 for i in range(72)]

#     row1, col1 = image.shape[0], image.shape[1]
#     RGBimage = array(image)
#     print(RGBimage)
#     for i in range(0,row1):
#         for j in range(0,col1):
#             hsv = rgb_to_hsv(RGBimage[i][j][0],RGBimage[i][j][1],RGBimage[i][j][2],histogram1)
    
#     print(hsv)

# printhsv(gambar1)