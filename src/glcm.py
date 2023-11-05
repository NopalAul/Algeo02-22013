import numpy as np
import math
from skimage.feature import graycomatrix, graycoprops # buat ngecek aja
from nyoba.cosine_similarity import cosine_sim

########## CONVERT WARNA TO GRAYSCALE ##########
def toGrayscale(image):
    grayscale_image = np.dot(image[..., :3], [0.29, 0.587, 0.114]).astype(np.uint8)
    return grayscale_image

########## FRAMEWORK MATRIKS ##########
def matrixGLCM(image, d=1, angle=0):
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
def createVector(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x):
    vector = np.array([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x])

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



