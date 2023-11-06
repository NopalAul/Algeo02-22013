import numpy as np
import math
from skimage.feature import graycomatrix, graycoprops # buat ngecek aja
from cosine_similarity import cosine_sim
import time
import os
from multiprocessing import Pool
import cv2

########## CONVERT WARNA TO GRAYSCALE ##########
def toGrayscale(image):
    grayscale_image = np.dot(image[..., :3], [0.29, 0.587, 0.114]).astype(np.uint8)
    return grayscale_image

########## FRAMEWORK MATRIKS ##########
def matrixGLCM(image, d=1):
    # ubah jadi grayscale dulu
    image = toGrayscale(image)

    # quantization levels
    levels = np.max(image) + 1

    # inisialisasi matrix dengan 0
    framework_matrix = np.zeros((levels, levels))

    # dimensi dari gambarnya
    rows, cols = image.shape

    # isi matrixnya
    for i in range(rows):
        for j in range(cols):
                x1, y1 = i, j
                # perpindahan vektor berdasarkan sudut
                x2, y2 = i + 0, j + d

                if 0 <= x1 < rows and 0 <= y1 < cols and 0 <= x2 < rows and 0 <= y2 < cols:
                    pixel1 = image[x1, y1]
                    pixel2 = image[x2, y2]
                    framework_matrix[pixel1, pixel2] += 1
                    # print("framework matrix:")
                    # print(framework_matrix)

    return framework_matrix

########## MATRIKS SIMETRIK ##########
def symmetricGLCM(glcm_matrix):
    symmetric_glcm = glcm_matrix + glcm_matrix.T
    return symmetric_glcm

########## MATRIKS NORMALISASI ##########
def normalizeGLCM(glcm_matrix):
    normalized_glcm = glcm_matrix / np.sum(glcm_matrix)
    return normalized_glcm

########## EKSTRAKSI TEKSTUR ##########
def extract_texture(glcm_matrix):
    rows = glcm_matrix.shape[0]

    # buat cari i - j (untuk contrast, homogeneity, dissimilarity)
    diff_matrix = np.abs(np.arange(rows) - np.arange(rows)[:, np.newaxis])

    # 1. contrast
    contrast_result = np.sum(diff_matrix ** 2 * glcm_matrix)

    # 2. homogeneity
    homogeneity_result = np.sum(glcm_matrix / (1 + diff_matrix ** 2))
    
    # 3. entropy
    # cari elemen tidak nol, handle kasus log(0) di entropy
    non_zero_elements = glcm_matrix[glcm_matrix > 0]
    entropy_result = -np.sum(non_zero_elements * np.log(non_zero_elements))

    # 4. dissimilarity
    dissimilarity_result = np.sum(diff_matrix * glcm_matrix)

    # 5. energy
    energy_result = np.sqrt(np.sum(glcm_matrix ** 2))

    # 6. correlation
    i, j = np.meshgrid(np.arange(rows), np.arange(rows), indexing='ij')
    rata_rata_i = np.sum(i * glcm_matrix) / np.sum(glcm_matrix)
    rata_rata_j = np.sum(j * glcm_matrix) / np.sum(glcm_matrix)
    
    sd_i = np.sqrt(np.sum(((i - rata_rata_i) ** 2) * glcm_matrix) / np.sum(glcm_matrix))
    sd_j = np.sqrt(np.sum(((j - rata_rata_j) ** 2) * glcm_matrix) / np.sum(glcm_matrix))
    
    correlation_result = np.sum(glcm_matrix * ((i - rata_rata_i) * (j - rata_rata_j) / (sd_i * sd_j)))

    return contrast_result, homogeneity_result, entropy_result, dissimilarity_result, energy_result, correlation_result

########## COSINE SIMILARITY ##########
def createVector(a, b, c, d, e, f,):
    vector = np.array([a, b, c, d, e, f])

    return vector

########## CBIR-TEKSTUR ##########
def CBIR_tekstur(image1, image2):
    ## BUAT VECTOR BERISI CONTRAST, HOMOGENEITY, DAN ENTROPY DARI IMAGE 1
    # sudut 0
    glcm_matrix1_sudut0 = matrixGLCM(image1, d=1)
    symmetric_glcm1_sudut0 = symmetricGLCM(glcm_matrix1_sudut0)
    normalized_glcm1_sudut0 = normalizeGLCM(symmetric_glcm1_sudut0)
    contrast1_sudut0, homogeneity1_sudut0, entropy1_sudut0, dissimilarity1_sudut0, energy1_sudut0, correlation1_sudut0 = extract_texture(normalized_glcm1_sudut0)

    vector1 = createVector(contrast1_sudut0, homogeneity1_sudut0, entropy1_sudut0, dissimilarity1_sudut0, energy1_sudut0, correlation1_sudut0)

    ## BUAT VECTOR BERISI CONTRAST, HOMOGENEITY, DAN ENTROPY DARI IMAGE 2
    # sudut 0
    glcm_matrix2_sudut0 = matrixGLCM(image2, d=1)
    symmetric_glcm2_sudut0 = symmetricGLCM(glcm_matrix2_sudut0)
    normalized_glcm2_sudut0 = normalizeGLCM(symmetric_glcm2_sudut0)
    contrast2_sudut0, homogeneity2_sudut0, entropy2_sudut0, dissimilarity2_sudut0, energy2_sudut0, correlation2_sudut0 = extract_texture(normalized_glcm2_sudut0)

    vector2 = createVector(contrast2_sudut0, homogeneity2_sudut0, entropy2_sudut0, dissimilarity2_sudut0, energy2_sudut0, correlation2_sudut0)
   
    ## CARI NILAI COS THETA UNTUK TAU KEMIRIPAN
    cos_theta = cosine_sim(vector1, vector2)

    return cos_theta

#******** TES HITUNGAN/RUMUS BENER OR GA W/ BUILT-IN FUNCTIONS ********#

image2 = cv2.imread('img/contoh2/4478.jpg')

glcm_matrix2_sudut0 = matrixGLCM(image2, d=1)
symmetric_glcm2_sudut0 = symmetricGLCM(glcm_matrix2_sudut0)
normalized_glcm2_sudut0 = normalizeGLCM(symmetric_glcm2_sudut0)
contrast2_sudut0, homogeneity2_sudut0, entropy2_sudut0, dissimilarity2_sudut0, energy2_sudut0, correlation2_sudut0 = extract_texture(normalized_glcm2_sudut0)

print("FUNCTION BIKIN SENDIRI")
print("Contrast:", contrast2_sudut0)
print("Homogeneity:", homogeneity2_sudut0)
print("Dissimilarity:", dissimilarity2_sudut0)
print("Energy:", energy2_sudut0)
print("Correlation:", correlation2_sudut0)
print(" ")

image2x = cv2.imread('img/contoh2/4478.jpg', cv2.IMREAD_GRAYSCALE)
num_levels = np.max(image2x) + 1

glcm = graycomatrix(image2x, 
                    distances=[1], 
                    angles=[135], 
                    levels=num_levels,
                    symmetric=True, 
                    normed=True)

# print(glcm[:,:,0,0])

print("FUNCTION BUILD-IN")
correlation_test = graycoprops(glcm, prop='correlation')
dissimilarity_test = graycoprops(glcm, prop='dissimilarity')
energy_test = graycoprops(glcm, prop='energy')
contrast_test = graycoprops(glcm, prop='contrast')
homogeneity_test = graycoprops(glcm, prop='homogeneity')
print("Contrast:", contrast_test)
print("Homogeneity:", homogeneity_test)
print("Dissimilarity:", dissimilarity_test)
print("Energy:", energy_test)
print("Correlation:", correlation_test)