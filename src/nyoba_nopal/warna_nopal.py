import cv2
from numpy import array
from math import sqrt, pow
from timeit import default_timer as timer

start = timer()
gambar1 = cv2.imread('../../src/nyoba_nopal/0.jpg')
gambar2 = cv2.imread('../../src/nyoba_nopal/1.jpg')

def cosine_sim(vector1,vector2):
    # dot product
    dot_prod = 0
    for i in range(len(vector1)):
        dot_prod += vector1[i]*vector2[i]
    # vector magnitude
    mag_vector1 = 0
    mag_vector2 = 0
    for i in range(len(vector1)):
        mag_vector1 += pow(vector1[i],2)
    for i in range(len(vector2)):
        mag_vector2 += pow(vector2[i],2)
    mag_total = sqrt(mag_vector1)*sqrt(mag_vector2)
    # result
    
    return dot_prod/mag_total



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
    
    # print(f"[{g},{b},{delta},{g-b/delta}]", end=" ")

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
    if 360 > h >= 316:
        h = 0
    elif h == 0:
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
    # [h,s,v] = quantify_hsv(h,s,v)
    # print(f"[{h},{s},{v}]", end=" ")
    index = 24*v + 8*s + h
    # print(index,end=" "
    
    return index

def CBIR_warna(image1):
    # Resize image ke ukuran terkecil (for performance purpose)
    row1, col1 = image1.shape[0], image1.shape[1]
    # row2, col2 = image2.shape[0], image2.shape[1]

    # if col1*row1 > col2*row2:
    #     image1 = cv2.resize(image1, (col2, row2))
    #     row1 = row2
    #     col1 = col2
    # else:
    #     image2 = cv2.resize(image2, (col1, row1))
    #     row2 = row1
        # col2 = col1

    # Ekstraksi image ke komponen RGB-nya
    # RGBimage1 = array(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
    # RGBimage2 = array(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
    RGBimage1 = array(image1)
    # RGBimage2 = array(image2)
    # print(RGBimage1)

    # Inisialisasi histogram
    histogram1 = [0 for i in range(72)]
    # histogram2 = [0 for i in range(72)]

    # Pencarian histogram global method
    for i in range(0,row1,3):
        for j in range(0,col1,3):
            histogram1 [rgb_to_histogram(RGBimage1[i][j][0],RGBimage1[i][j][1],RGBimage1[i][j][2])]+=1
            # histogram2 [rgb_to_histogram(RGBimage2[i][j][0],RGBimage2[i][j][1],RGBimage2[i][j][2])]+=1

    # print(histogram1)
    # print(histogram2)
    
    # Komparasi cosine similarity kedua vektor histogram HSV
    return histogram1

print(CBIR_warna(gambar1))
end = timer()
print(end - start)