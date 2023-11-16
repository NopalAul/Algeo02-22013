import os
import cv2
import taichi as ti
import glob
from numpy import array,zeros
from finder import *
from timeit import default_timer as timer

ti.init(arch=ti.cpu)

def bacaimage(path):
    return cv2.imread(path)

image1 = ti.types.ndarray(dtype = ti.math.vec3,ndim=2)
histogram = ti.types.ndarray(dtype=ti.i32,ndim=1)
index = ti.field(ti.i32, shape=())
hsv = ti.field(ti.i32, shape=(3))
dst = zeros(72,dtype=int)
hist = zeros(72*16)


@ti.func
def rgb_to_index(r : ti.f32,g : ti.f32, b : ti.f32):
    # normalisasi
    h = r/255
    s = g/255
    v = b/255
    # nilai ekstrim
    cmax = ti.max(h,s,v)
    cmin = ti.min(h,s,v)
    delta = cmax - cmin
    # nilai HSV
    ## H
    if cmax == cmin :
        h = 0
    elif cmax == r :
        h = 60*(((s-v)/delta) % 6)
    elif cmax == g :
        h = 60*(((v-h)/delta) + 2)
    else :
        h = 60*(((h-s)/delta) + 4)
    ## S
    if cmax != 0 :
        s = (delta/cmax)
    else :
        s = 0
    ## V
    v = cmax
    if 360 > h >= 316:
        hsv[0] = 0
    elif h == 0:
        hsv[0] = 0
    elif h <= 25:
        hsv[0] = 1
    elif h <= 40:
        hsv[0] = 2
    elif h <= 120:
        hsv[0] = 3
    elif h <= 190:
        hsv[0] = 4
    elif h <= 270:
        hsv[0] = 5
    elif h <= 295:
        hsv[0] = 6
    elif h < 316:
        hsv[0] = 7
    if s < 0.2:
        hsv[1] = 0
    elif s < 0.7:
        hsv[1] = 1
    elif s >= 0.7:
        hsv[1] = 2
    if v < 0.2:
        hsv[2] = 0
    elif v < 0.7:
        hsv[2] = 1
    elif v >= 0.7:
        hsv[2] = 2

    index[None] = 24*hsv[2] + 8*hsv[1] + hsv[0]

ih = ti.i32
iw = ti.i32
@ti.kernel
def rgb_to_histogram(gambar1:image1, hist : histogram):
    # Inisialisasi histogram
    for k in range(1152):
        hist[k] = 0

    # Height & weight
    h,w = gambar1.shape
    row, col = h,w

    # Ekstrak warna dari 4x4 blok gambar
    weight_size  = 4
    height_size = 4
    ti.loop_config(serialize=True)
    for ih in range(0, height_size ):
        for iw in range(0, weight_size ):
            x = col/weight_size * iw 
            y = row/height_size * ih
            t = (row / height_size)
            l = (col / weight_size )
            y = ti.math.round(y,dtype = ti.i32)
            x = ti.math.round(x,dtype = ti.i32)

            for i in range(ti.math.round(t,dtype = ti.i32)):
                for j in range(ti.math.round(l,dtype = ti.i32)):
                    a = ti.i32(i+y)
                    b = ti.i32(j+x)
                    rgb_to_index(gambar1[a,b][0],gambar1[a,b][1],gambar1[a,b][2])
                    idx = (ih*4 + iw)*72 + index[None]
                    hist[idx] += 1


def warna_csv():
    output_warna = open("fitur/warna.csv", "w")
    for imagePath in glob.glob("../../img/dataset/*"):
        imageID = imagePath[imagePath.rfind("\\") + 1:]
        image = cv2.imread(imagePath)
        rgb_to_histogram(image,hist)

        features = [str(f) for f in hist]
        output_warna.write("%s,%s\n" % (imageID, ",".join(features)))

def satu_warna(image):
    rgb_to_histogram(image,hist)
    return hist

def fitur():
    for imagePath in glob.glob("../../img/uploaded/*"):
        image = cv2.imread(imagePath)

    rgb_to_histogram(image,hist)
    selected_option = 'color'
    fitur_warna = [float(f) for f in hist]
    hasil_warna = find(fitur_warna,selected_option)
        
    os.makedirs('../../img/retrieve', exist_ok=True) 
    for (nilai, IDhasil) in hasil_warna:
        hasil = cv2.imread("../../img/dataset/"+IDhasil)
        if(nilai >= 0.6):
            cv2.imwrite("../../img/retrieve/" + str(nilai*100) + ".jpeg", hasil)

# fitur()
# warna_csv()
# image = cv2.imread('../../img/dataset/0.jpg')
# print(satu_warna(image))

# output_warna.write("%s,%s\n" % (1, ",".join(features)))
# rgb_to_histogram(gambar1,hist)
# for i in hist:
#     if i != 0:
#         print(i)
# print(hist)
# end = timer()
# print(end - start) # delete