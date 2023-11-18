import cv2
# from numba import njit
from numpy import array
from math import sqrt, pow
from timeit import default_timer as timer

start = timer()
gambar1 = cv2.imread('../../src/nyoba_nopal/dataset/0.jpg')
gambar2 = cv2.imread('../../src/nyoba_nopal/dataset/1.jpg')

# print(gambar1,end=' djdjdjd')
# print(gambar2)
# gambar1 = array(gambar1)
# gambar2 = array(gambar2)

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

def coba1(image):
    # Resize image ke ukuran terkecil (for performance purpose)
    row, col = image.shape[0], image.shape[1]
    histogram = [0 for i in range(72*16)]
    # Crop out the window and calculate the histogram
    # Number of pieces Horizontally 
    W_SIZE  = 4
    # Number of pieces Vertically to each Horizontal  
    H_SIZE = 4
    c = 0
    for ih in range(0, H_SIZE ):
        for iw in range(0, W_SIZE ):
            vector = [0 for i in range(3)]
            x = col/W_SIZE * iw 
            y = row/H_SIZE * ih
            h = (row / H_SIZE)
            w = (col / W_SIZE )
            # print(x,y,h,w)
            img1 = image[int(y):int(y+h), int(x):int(x+w)]
            # print(h,w)
            for i in range(0,round(h)):
                for j in range(0,round(w)):
                    index = (ih*4+iw)*72 + rgb_to_index(img1[i][j][0],img1[i][j][1],img1[i][j][2])
                    # print(rgb_to_index(img1[i][j][0],img1[i][j][1],img1[i][j][2]),end=" ")
                    histogram[index]+=1
                    c+=1
    return histogram

# Konversi RGB space ke HSV space, lalu ke histogram (kuantifikasi)
def rgb_to_index(r,g,b):
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

print(coba1(gambar1))
print(coba1(gambar2))
# print(gambar1.shape)
# print(cosine_sim(coba1(gambar1),coba1(gambar2)))
end = timer()
print(end - start)