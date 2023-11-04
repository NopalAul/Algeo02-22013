import colorsys
from PIL import Image

from numpy import array
img = Image.open(r'../../src/nyoba/aww.jpg')
ar = array(img)

print(ar[3000][3000])

def cara1(m1, m2, row, col):
    row -= row % 3
    col -= col % 3
    for i in range(row):
        for j in range(col):
            l = rgbToHSV(m1[i][j][0],m1[i][j][1],m1[i][j][2])
            l1 = rgbToHSV(m2[i][j][0],m2[i][j][1],m2[i][j][2])
            

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

    return h,s,v



def rgbhsv_stackover(r, g, b):
    r /= 255
    g /= 255
    b /= 255
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc-minc) / maxc
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = 0.0+bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h * 360, s * 100, v * 100

r = 142
g = 244
b = 85
print(f"{r}, {g}, {b}")
print(f"{rgbToHSV(r,g,b)[0]}, ", end="")
print(f"{rgbToHSV(r,g,b)[1]}, ", end="")
print(f"{rgbToHSV(r,g,b)[2]}\n")

print("stackover method:")
print(f"{rgbhsv_stackover(r,g,b)[0]}, ", end="")
print(f"{rgbhsv_stackover(r,g,b)[1]}, ", end="")
print(f"{rgbhsv_stackover(r,g,b)[2]}")


