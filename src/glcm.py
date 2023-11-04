import numpy as np
import math
from skimage.feature import graycomatrix, graycoprops # buat ngecek aja
from nyoba.cosine_similarity import cosine_sim

########## FRAMEWORK MATRIKS ##########
def matrixGLCM(image, d=1, angle=0):
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
                if angle == 0:
                    x2, y2 = i + 0, j + d
                elif angle == 45:
                    x2, y2 = i + d, j + d
                elif angle == 90:
                    x2, y2 = i + d, j + 0
                elif angle == 135:
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
# 1. contrast
def contrast(glcm_matrix):
    rows = glcm_matrix.shape[0]
    hasil = 0
    for i in range(rows):
        for j in range(rows):
            hasil += (i - j)**2 * glcm_matrix[i, j]

    return hasil

# 2. homogeneity
def homogeneity(glcm_matrix):
    rows = glcm_matrix.shape[0]
    hasil = 0
    for i in range(rows):
        for j in range(rows):
            hasil += (glcm_matrix[i, j] / (1 + (i - j)**2))

    return hasil

# 3. entropy
def entropy(glcm_matrix):
    rows = glcm_matrix.shape[0]
    hasil = 0
    for i in range(rows):
        for j in range(rows):
            if (glcm_matrix[i][j] != 0):
                hasil += (glcm_matrix[i, j] * math.log(glcm_matrix[i, j]))

    return (-1*hasil)

# 4. dissimilarity
def dissimilarity(glcm_matrix):
    rows = glcm_matrix.shape[0]
    hasil = 0
    for i in range(rows):
        for j in range(rows):
            selisih = i-j
            if ((selisih) < 0):
                selisih *= -1
            hasil += (glcm_matrix[i, j] * selisih)

    return hasil

# 5. energy
def energy(glcm_matrix):
    rows = glcm_matrix.shape[0]
    hasil = 0
    for i in range(rows):
        for j in range(rows):
            hasil += (glcm_matrix[i, j]**2)

    return math.sqrt(hasil)

# 6. correlation
def correlation(glcm_matrix):
    rows = glcm_matrix.shape[0]
    
    sum_i = 0
    sum_j = 0
    for i in range(rows):
        for j in range(rows):
            sum_i += i * glcm_matrix[i][j]
            sum_j += j * glcm_matrix[i][j]

    rata_rata_i = sum_i / np.sum(glcm_matrix)
    rata_rata_j = sum_j / np.sum(glcm_matrix)

    sum_temp_i = 0
    for i in range(rows):
        for j in range(rows):
            sum_temp_i += ((i - rata_rata_i) ** 2) * glcm_matrix[i][j]

    sd_i = math.sqrt(sum_temp_i / np.sum(glcm_matrix))

    sum_temp_j = 0
    for i in range(rows):
        for j in range(rows):
            sum_temp_j += ((j - rata_rata_j) ** 2) * glcm_matrix[i][j]

    sd_j = math.sqrt(sum_temp_j / np.sum(glcm_matrix))

    hasil = 0
    for i in range(rows):
        for j in range(rows):
            hasil += (glcm_matrix[i][j] * ((i - rata_rata_i) * (j - rata_rata_j) / (sd_i * sd_j)))

    return hasil

########## COSINE SIMILARITY ##########
def createVector(contrast, homogeneity, entropy, dissimilarity, energy, correlation):
    vector = np.array([contrast, homogeneity, entropy, dissimilarity, energy, correlation])

    return vector

#******** TES ********#
# image1 = np.array([[0, 0, 1],
#                   [1, 2, 3],
#                   [2, 3, 2]])
                  
# image2 = np.array([[0, 0, 1],
#                   [1, 2, 3],
#                   [2, 3, 2]])

# glcm_matrix1 = matrixGLCM(image1, d=1, angle=0)
# symmetric_glcm1 = symmetricGLCM(glcm_matrix1)
# normalized_glcm1 = normalizeGLCM(symmetric_glcm1)
# contrast1 = contrast(normalized_glcm1)
# homogeneity1 = homogeneity(normalized_glcm1)
# entropy1 = entropy(normalized_glcm1)

# glcm_matrix2 = matrixGLCM(image2, d=1, angle=0)
# symmetric_glcm2 = symmetricGLCM(glcm_matrix2)
# normalized_glcm2 = normalizeGLCM(symmetric_glcm2)
# contrast2 = contrast(normalized_glcm2)
# homogeneity2 = homogeneity(normalized_glcm2)
# entropy2 = entropy(normalized_glcm2)

# vector1 = createVector(contrast1, homogeneity1, entropy1)
# vector2 = createVector(contrast2, homogeneity2, entropy2)

# correlation = correlation(normalized_glcm1)
# print("Correlation:", correlation)
# dissimilarity = dissimilarity(normalized_glcm1)
# print("Dissimilarity:", dissimilarity)
# energy = energy(normalized_glcm1)
# print("Energy:", energy)

# glcm = graycomatrix(image1, 
#                     distances=[1], 
#                     angles=[0], 
#                     levels=4,
#                     symmetric=True, 
#                     normed=True)

# print(glcm[:,:,0,0])

# contrast_test = graycoprops(glcm, prop='correlation')
# dissimilarity_test = graycoprops(glcm, prop='dissimilarity')
# energy_test = graycoprops(glcm, prop='energy')
# print("Correlation:", contrast_test)
# print("Dissimilarity:", dissimilarity_test)
# print("Energy:", energy_test)

# contrast_test = graycoprops(glcm, prop='contrast')
# homogeneity_test = graycoprops(glcm, prop='homogeneity')
# print("Contrast:", contrast_test)
# print("Homogeneity:", homogeneity_test)

# print("GLCM Matrix:")
# print(glcm_matrix1)
# print("Symmetric GLCM Matrix:")
# print(symmetric_glcm1)
# print("Normalized GLCM Matrix:")
# print(normalized_glcm1)
# print("Contrast:")
# print(contrast1)
# print("Homogeneity:")
# print(homogeneity1)
# print("Entropy:")
# print(entropy1)



