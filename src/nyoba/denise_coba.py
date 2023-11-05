import cv2
from numpy import array
from cosine_similarity import *

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

def bgr_to_rgb(image):
    image_rgb = image.copy()
    image_rgb[:, :, 0] = image[:, :, 2]
    image_rgb[:, :, 2] = image[:, :, 0]
    return image_rgb

img = cv2.imread('src/nyoba/hitamdoang.jpg')
img = bgr_to_rgb(img)
img1 = cv2.imread('src/nyoba/mobilmerah.jpg')
img1 = bgr_to_rgb(img1)

# resize image
if img.shape[0] * img.shape[1] > img1.shape[0] * img1.shape[1]:
    img = cv2.resize(img, (img1.shape[1], img1.shape[0]))
else:
    img1 = cv2.resize(img1, (img.shape[1], img.shape[0]))

ar = array(img)
ar1 = array(img1)

print("ar, ar1")
print(ar[0][0], ar1[0][1])

print(f"cosine similarity: {cara2(img, img1, img.shape[0], img.shape[1])}")
