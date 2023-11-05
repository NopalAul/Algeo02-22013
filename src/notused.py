import numpy as np
import math

# convert warna to grayscale
def toGrayscale(image):
    height, width, _ = image.shape

    grayscale_image = np.zeros((height, width), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            # extract warna
            B, G, R = image[i, j]
            gray_value = int(0.29 * R + 0.587 * G + 0.114 * B)
            grayscale_image[i, j] = gray_value

    return grayscale_image

# buat extract texture, tp ini lama
def extract_texture(glcm_matrix):
    rows = glcm_matrix.shape[0]

    # 1. contrast
    contrast_result = 0
    for i in range(rows):
        for j in range(rows):
            contrast_result += (i - j) ** 2 * glcm_matrix[i, j]

    # 2. homogeneity
    homogeneity_result = 0
    for i in range(rows):
        for j in range(rows):
            homogeneity_result += (glcm_matrix[i, j] / (1 + (i - j) ** 2))
    
    # 3. entropy
    entropy_result = 0
    for i in range(rows):
        for j in range(rows):
            if glcm_matrix[i][j] != 0:
                entropy_result += (glcm_matrix[i, j] * math.log(glcm_matrix[i, j]))
    entropy_result *= -1

    # 4. dissimilarity
    dissimilarity_result = 0
    for i in range(rows):
        for j in range(rows):
            selisih = i - j
            if (selisih < 0):
                selisih *= -1
            dissimilarity_result += (glcm_matrix[i, j] * selisih)

    # 5. energy
    energy_result = 0
    for i in range(rows):
        for j in range(rows):
            energy_result += (glcm_matrix[i, j] ** 2)
    energy_result = math.sqrt(energy_result)

    # 6. correlation
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

    correlation_result = 0
    for i in range(rows):
        for j in range(rows):
            correlation_result += (glcm_matrix[i][j] * ((i - rata_rata_i) * (j - rata_rata_j) / (sd_i * sd_j)))

    return contrast_result, homogeneity_result, entropy_result, dissimilarity_result, energy_result, correlation_result