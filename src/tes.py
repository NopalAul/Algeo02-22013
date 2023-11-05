import cv2
import time
import os
from CBIR_tekstur import *
from multiprocessing import Pool

# membandingkan dua gambar
def compareImages(image1, image2):
    return CBIR_tekstur(image1, image2)

# mendapatkan semua gambar dalam folder
def imageInFolder(folder_path):
    image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.jpg')]
    return image_files

if __name__ == '__main__':
    start_time = time.time()

    # load gambar referensi
    reference_image = cv2.imread('img/contoh/1000.jpg')

    # list gambar target yang akan dibandingkan
    target_folder = 'img/contoh/'
    target_images = imageInFolder(target_folder)

    # baca semua gambar langsung terus simpen ke list, jadi ga ulang ulang cv2 imreadnya
    target_images_list = [cv2.imread(image_path) for image_path in target_images]

    # inisialisasi pool multiprocessing dengan jumlah prosesor yang tersedia
    num_processors = 8 # sesuaikan dengan jumlah prosesor yang tersedia
    pool = Pool(processes=num_processors)

    # bandingkan gambar referensi dengan gambar target secara paralel
    similarities = pool.starmap(compareImages, [(reference_image, image) for image in target_images_list])

    # close pool multiprocessing
    pool.close()
    pool.join()

    # Hasil kesamaan citra
    for i, similarity in enumerate(similarities):
        print(f"Kesamaan dengan gambar-{i+1}: {similarity * 100:.5f}%")

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Program selesai dalam {execution_time:.2f} detik")
