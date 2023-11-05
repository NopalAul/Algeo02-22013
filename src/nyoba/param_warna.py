import colorsys
import cv2
import numpy as np
from PIL import Image
from cosine_similarity import *

from numpy import array
img = Image.open(r'../../src/nyoba/hitamdoang.jpg')
img1 = Image.open(r'../../src/nyoba/mobilmerah.jpg')
if img.width*img.height > img1.height*img1.width:
    img = img.resize((img1.size[0], img1.size[1]))
else:
    img1 = img1.resize((img.size[0], img.size[1]))

ar = array(img)
ar1 = array(img1)

def cara1(m1, m2, row, col):
    sum = 0
    c = 0
    for i in range(10):
        for j in range(10):
            l = rgbToHistogram(m1[i][j][0],m1[i][j][1],m1[i][j][2])
            l1 = rgbToHistogram(m2[i][j][0],m2[i][j][1],m2[i][j][2])
            print(l,l1, cosine_sim(l,l1))
            sum += cosine_sim(l,l1)
            c += 1
    return sum/c

def cara2(m1, m2, row, col):
    x = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    y = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    print(row)
    print(col)
    for i in range(0,row,3):
        for j in range(0,col,3):
            x = rgbToHistogram(m1[i][j][0],m1[i][j][1],m1[i][j][2],x)
            y = rgbToHistogram(m2[i][j][0],m2[i][j][1],m2[i][j][2],y)
    return cosine_sim(x,y)

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


def rgbToHistogram(r,g,b,l):
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

print(f"cosine similarity : {cara2(ar,ar1, img.height, img.width)}")
# def hsvtohistogram2(imgg):
#     row = imgg.height
#     col = imgg.width
#     img = array(imgg)
#     for i in range(0,row,3):
#         for j in range(0,col,3):
#             img[i][j] = rgbToHistogram(img[i][j][0],img[i][j][1],img[i][j][2])
#     hist = cv2.calcHist(img, [0, 1, 2], None, [180,256,256], [0, 180, 0, 256, 0, 256])
#     hist = cv2.normalize(hist, hist)
#     return hist.flatten()

# def cara3(m1):
#     for i in range(len(m1)):
#         for j in range(len(m1)):
#             m1[i][j] = rgbToHistogram(m1[i][j][0],m1[i][j][1],m1[i][j][2])
#     return m1

# def cara4(ar):
#     hsv_histogram = HSVColorHistogram([8, 8, 8])
#     source_color_features = hsv_histogram.describe(ar)
#     source_color_features = np.around(np.array(source_color_features, dtype=np.float32), decimals=8)
#     return source_color_features

# print(cosine_sim(cara4(ar), cara4(ar1)))

# print(cara3(hsvtohistogram2(img), hsvtohistogram2(img1)))