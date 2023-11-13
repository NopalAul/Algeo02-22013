import cv2
import taichi as ti
import glob
from numpy import array,zeros
from timeit import default_timer as timer

start = timer()
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
def cosine_sim(vector1 : histogram, vector2 : histogram):
    # dot product
    dot_prod = 0
    ti.loop_config(parallelize=2, block_dim=1)
    for i in range(len(vector1)):
        dot_prod += vector1[i]*vector2[i]
    # vector magnitude
    mag_vector1 = 0
    mag_vector2 = 0

    ti.loop_config(parallelize=2, block_dim=1)
    for i in range(len(vector1)):
        mag_vector1 += ti.math.pow(vector1[i],2)
    
    ti.loop_config(parallelize=2, block_dim=1)
    for i in range(len(vector2)):
        mag_vector2 += ti.math.pow(vector2[i],2)
    
    mag_total = ti.math.sqrt(mag_vector1)*ti.math.sqrt(mag_vector2)
    # result
    
    result =  dot_prod/mag_total

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
    # print(f"[{g},{b},{delta},{g-b/delta}]", end=" ")

    # nilai HSV
    ## H
    # s = 0
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
    # [h,s,v] = quantify_hsv(h,s,v)
    # print(f"[{h},{s},{v}]", end=" ")
    index[None] = 24*hsv[2] + 8*hsv[1] + hsv[0]
    # print(index,end=" "

ih = ti.i32
iw = ti.i32
@ti.kernel
def coba1(gambar1:image1, hist : histogram):
    # Resize gambar1 ke ukuran terkecil (for performance purpose)
    h,w = gambar1.shape
    row, col = h,w
    # Crop out the window and calculate the histogram
    # Number of pieces Horizontally 
    W_SIZE  = 4
    # Number of pieces Vertically to each Horizontal  
    H_SIZE = 4
    ti.loop_config(serialize=True)
    for ih in range(0, H_SIZE ):
        for iw in range(0, W_SIZE ):
            x = col/W_SIZE * iw 
            y = row/H_SIZE * ih
            t = (row / H_SIZE)
            l = (col / W_SIZE )
            # print(x,y,h,w)
            # img1 = gambar1[int(y):int(y+h), int(x):int(x+w)]
            # print(h,w)
            y = ti.math.round(y,dtype = ti.i32)
            x = ti.math.round(x,dtype = ti.i32)

            for i in range(ti.math.round(t,dtype = ti.i32)):
                for j in range(ti.math.round(l,dtype = ti.i32)):
                    a = ti.i32(i+y)
                    b = ti.i32(j+x)
                    rgb_to_index(gambar1[a,b][0],gambar1[a,b][1],gambar1[a,b][2])
                    idx = (ih*4 + iw)*72 + index[None]
                    # print(ih,iw,end=" ")
                    hist[idx] += 1

# Konversi RGB space ke HSV space, lalu ke histogram (kuantifikasi)

# print(coba1(gambar1))
output_warna = open("fitur/warna.csv", "w")
# output_tekstur = open("fitur/tekstur.csv", "w")

def warna_csv():
    for imagePath in glob.glob("../../img/dataset/*"):
        imageID = imagePath[imagePath.rfind("\\") + 1:]
        image = cv2.imread(imagePath)
        coba1(image,hist)

        # ekstraksi fitur gambar
        fitur_warna = None # import file .py, panggil fungsinya
        fitur_tekstur = None # import file .py, panggil fungsinya

        features = [str(f) for f in hist]
        output_warna.write("%s,%s\n" % (imageID, ",".join(features)))

def satu_warna(image):
    coba1(image,hist)
    return hist

def fitur(image):
    hist = satu_warna(image)
    return hist

warna_csv()
# image = cv2.imread('../../img/dataset/0.jpg')
# print(satu_warna(image))

# output_warna.write("%s,%s\n" % (1, ",".join(features)))
# coba1(gambar1,hist)
# for i in hist:
#     if i != 0:
#         print(i)
# print(hist)
end = timer()
print(end - start)