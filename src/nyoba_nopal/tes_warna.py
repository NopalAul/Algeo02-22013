import cv2
import time
import os
# from CBIR_tekstur import *
from warna_nopal import *
from multiprocessing import Pool

# membandingkan dua gambar
def compareImages(image1, image2):
    return CBIR_warna(image1, image2)

# memuat gambar dari path file
def loadImage(image_path):
    return cv2.imread(image_path)

# mendapatkan semua gambar dalam folder
def imageInFolder(folder_path):
    image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.jpg')]
    return image_files

# TES
if __name__ == '__main__':
    start_time = time.time()

    # load gambar referensi
    reference_image = cv2.imread('../../img/244/0.jpg')

    # list gambar target yang akan dibandingkan
    target_folder = '../../img/244/'
    target_images = imageInFolder(target_folder)

    # inisialisasi pool multiprocessing dengan jumlah prosesor yang tersedia
    num_processors = 8 # prosesor denise
    pool = Pool(processes=num_processors)

    # bandingkan gambar referensi dengan gambar target secara paralel
    similarities = pool.starmap(compareImages, [(reference_image, loadImage(image_path)) for image_path in target_images])

    # close pool multiprocessing
    pool.close()
    pool.join()

    # Hasil kesamaan citra
    for i, similarity in enumerate(similarities):
        print(f"Kesamaan dengan gambar-{i+1}: {similarity * 100:.5f}%")

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Program selesai dalam {execution_time:.2f} detik")