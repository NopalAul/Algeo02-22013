import cython
import cv2
from cosine_similarity import *
from numpy import *
from CBIR_warna3x3 import rgb_to_histogram



# ########## FOR TEST
# importing os module   
import os 
# Image directory 
directory = r'C:\Users\Naufal\Documents\003. TAHUN KEDUA\SEMESTER 3\ALGEO\TUBES 2\Algeo02-22013\src\nyoba_nopal'
os.chdir(directory) 


cpdef double coba1(unsigned char [:, :] image1, unsigned char [:, :] image2):
    # Resize image ke ukuran terkecil (for performance purpose)
    cdef int row1, col1, row2, col2
    row1 = image1.shape[0]
    col1 = image1.shape[1]
    row2 = image2.shape[0]
    col2 = image2.shape[1]

    if col1*row1 > col2*row2:
        image1 = cv2.resize(image1, (col2, row2))
        row1 = row2
        col1 = col2
    else:
        image2 = cv2.resize(image2, (col1, row1))
        row2 = row1
        col2 = col1

    # Inisialisasi histogram
    cdef int histogram1[72], histogram2[72]
    histogram1 = [0 for i in range(72)]
    histogram2 = [0 for i in range(72)]

    cdef double sum_cosine
    cdef int c
    sum_cosine = 0
    c = 0
    # Crop out the window and calculate the histogram
    cdef int W_SIZE, H_SIZE
    # Number of pieces Horizontally 
    W_SIZE  = 3 
    # Number of pieces Vertically to each Horizontal  
    H_SIZE = 3
    cdef int ih, iw
    cdef double x, y, h, w
    cdef int i, j
    for ih in range(0, H_SIZE ):
        for iw in range(0, W_SIZE ):
            x = col1/W_SIZE * iw 
            y = row1/H_SIZE * ih
            h = (row1 / H_SIZE)
            w = (col1 / W_SIZE )
            # print(x,y,h,w)
            # cdef unsigned char[:, :] img1, img2
            img1 = gambar1[int(y):int(y+h), int(x):int(x+w)]
            img2 = gambar2[int(y):int(y+h), int(x):int(x+w)]

            # loop untuk tiap piksel di 1/9 blocks of image
            for i in range(0,int(row1/3)):
                for j in range(0,int(col1/3)):
                    histogram1 = rgb_to_histogram(img1[i][j][0],img1[i][j][1],img1[i][j][2],histogram1)
                    histogram2 = rgb_to_histogram(img2[i][j][0],img2[i][j][1],img2[i][j][2],histogram2)

                    sum_cosine += cosine_sim(histogram1,histogram2)
                    c += 1

    return sum_cosine/c

