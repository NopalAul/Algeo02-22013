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
                # sudut 0:
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
def CBIR_tekstur(image):
    ## BUAT VECTOR BERISI CONTRAST, HOMOGENEITY, DAN ENTROPY DARI IMAGE 1
    # sudut 0
    glcm_matrix_sudut0 = matrixGLCM(image, d=1)
    symmetric_glcm_sudut0 = symmetricGLCM(glcm_matrix_sudut0)
    normalized_glcm_sudut0 = normalizeGLCM(symmetric_glcm_sudut0)
    contrast_sudut0, homogeneity_sudut0, entropy_sudut0, dissimilarity_sudut0, energy_sudut0, correlation_sudut0 = extract_texture(normalized_glcm_sudut0)

    vector = createVector(contrast_sudut0, homogeneity_sudut0, entropy_sudut0, dissimilarity_sudut0, energy_sudut0, correlation_sudut0)

    return vector

########## MENGAMBIL SEMUA GAMBAR DALAM SATU FOLDER ##########
def imageInFolder(folder_path):
    image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.jpg')]
    return image_files

##########***** TES *****##########

if __name__ == '__main__':
    start_time = time.time()

    # list gambar target yang akan dibandingkan
    target_folder = 'img/dataset/'
    target_images = imageInFolder(target_folder)

    # baca semua gambar langsung terus simpen ke list, jadi ga ulang ulang cv2 imreadnya
    target_images_list = [cv2.imread(image_path) for image_path in target_images]

    # inisialisasi pool multiprocessing dengan jumlah prosesor yang tersedia
    num_processors = 8 # sesuaikan dengan jumlah prosesor yang tersedia
    pool = Pool(processes=num_processors)

    # bandingkan gambar referensi dengan gambar target secara paralel
    vectors = pool.starmap(CBIR_tekstur, [(image,) for image in target_images_list])

    # close pool multiprocessing
    pool.close()
    pool.join()

    # Hasil kesamaan citra
    for i, vektor in enumerate(vectors):
        # print(f"Kesamaan dengan gambar-{i+1}: {similarity * 100:.5f}%")
        print(f"vektor gambar-{i+1}: {vektor}%")

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Program selesai dalam {execution_time:.2f} detik")



