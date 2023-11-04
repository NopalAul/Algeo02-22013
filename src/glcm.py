import numpy as np
import math
from skimage.feature import graycomatrix, graycoprops # buat ngecek aja

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
                elif angle == 90:
                    x2, y2 = i + d, j + 0
                elif angle == 45:
                    x2, y2 = i + d, j + d
                elif angle == 135:
                    x2, y2 = i + 0, j + d

                if 0 <= x1 < rows and 0 <= y1 < cols and 0 <= x2 < rows and 0 <= y2 < cols:
                    pixel1 = image[x1, y1]
                    pixel2 = image[x2, y2]
                    framework_matrix[pixel1, pixel2] += 1
                    # print("framework matrix:")
                    # print(framework_matrix)

    return framework_matrix

# bikin matriks simetriknya
def symmetricGLCM(glcm_matrix):
    symmetric_glcm = glcm_matrix + glcm_matrix.T
    return symmetric_glcm

# normalisasi matriks
def normalizeGLCM(glcm_matrix):
    normalized_glcm = glcm_matrix / np.sum(glcm_matrix)
    return normalized_glcm

# ekstraksi tekstur
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

# tes
image = np.array([[0, 0, 1],
                  [1, 2, 3],
                  [2, 3, 2]])

# image = np.array([[1, 1, 5, 6, 8],
#                   [2, 3, 5, 7, 1],
#                   [4, 5, 7, 1, 2],
#                   [8, 5, 1, 2, 5]])

glcm_matrix = matrixGLCM(image, d=1, angle=0)
symmetric_glcm = symmetricGLCM(glcm_matrix)
normalized_glcm = normalizeGLCM(symmetric_glcm)
contrast = contrast(normalized_glcm)
homogeneity = homogeneity(normalized_glcm)
entropy = entropy(normalized_glcm)

# glcm = graycomatrix(image, 
#                     distances=[1], 
#                     angles=[0], 
#                     levels=4,
#                     symmetric=True, 
#                     normed=True)

# print(glcm[:,:,0,0])

# contrast_test = graycoprops(glcm, prop='contrast')
# homogeneity_test = graycoprops(glcm, prop='homogeneity')

# print("Contrast:", contrast_test)
# print("Homogeneity:", homogeneity_test)

print("GLCM Matrix:")
print(glcm_matrix)
print("Symmetric GLCM Matrix:")
print(symmetric_glcm)
print("Normalized GLCM Matrix:")
print(normalized_glcm)
print("Contrast:")
print(contrast)
print("Homogeneity:")
print(homogeneity)
print("Entropy:")
print(entropy)


