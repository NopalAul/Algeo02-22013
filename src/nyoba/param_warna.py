import colorsys
from PIL import Image
from cosine_similarity import *

from numpy import array
img = Image.open(r'../../src/nyoba/mobilmerah.jpg')
img1 = Image.open(r'../../src/nyoba/160.jpg')
if img.width*img.height > img1.height*img1.width:
    img = img.resize((img1.size[0], img1.size[1]))
else:
    img1 = img1.resize((img.size[0], img.size[1]))

ar = array(img)
ar1 = array(img1)

print(ar[0][0], ar1[0][0])
def cara1(m1, m2, row, col):
    sum = 0
    c = 0
    for i in range(10):
        for j in range(10):
            l = rgbToHSV(m1[i][j][0],m1[i][j][1],m1[i][j][2])
            l1 = rgbToHSV(m2[i][j][0],m2[i][j][1],m2[i][j][2])
            print(l,l1, cosine_sim(l,l1))
            sum += cosine_sim(l,l1)
            c += 1
    return sum/c

def cara2(m1, m2, row, col):
    sum = 0
    c = 0
    # row -= row % 3
    # col -= col % 3
    for i in range(0,row,3):
        for j in range(0,col,3):
            l = rgbToHSV(m1[i][j][0],m1[i][j][1],m1[i][j][2])
            l1 = rgbToHSV(m2[i][j][0],m2[i][j][1],m2[i][j][2])
            sum += cosine_sim(l,l1)
            c += 1
    print("c: ", c) #########
    return sum/c

def rgbToHSV(r,g,b):
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
        s = (delta/cmax)*100
    else :
        s = 0
    ## V
    v = cmax*100
    return [h,s,v]

print(f"cosine similarity : {cara1(ar,ar1, img.height, img.width)}")
