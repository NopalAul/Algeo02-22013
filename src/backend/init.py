# import glob
# import cv2

# from tekstur import *
# from warna import warna_csv

# # Ekstrak warna
# warna_csv()

# # Ekstrak tekstur
# output_tekstur = open("fitur/tekstur.csv", "w")
# for imagePath in glob.glob("../../img/dataset/*"):
#     imageID = imagePath[imagePath.rfind("\\") + 1:]
#     image = cv2.imread(imagePath)

#     # ekstraksi fitur gambar
#     fitur_tekstur = CBIR_tekstur(image)
#     fitur_tekstur = [str(f) for f in fitur_tekstur]
#     output_tekstur.write("%s,%s\n" % (imageID, ",".join(fitur_tekstur)))

# output_tekstur.close()


# print("Ekstraksi selesai!")


import glob
import cv2
import time
from multiprocessing import Pool, cpu_count

from tekstur import *
from warna import warna_csv


def ekstrak_tekstur(imagePath):
    imageID = imagePath[imagePath.rfind("\\") + 1:]
    image = cv2.imread(imagePath)
    fitur_tekstur = CBIR_tekstur(image)
    fitur_tekstur = [str(f) for f in fitur_tekstur]
    
    return imageID, fitur_tekstur

if __name__ == "__main__":
    start_time = time.time()

    with Pool() as pool:
        warna_csv()     # Ekstrak warna
        image_path = glob.glob("../../img/dataset/*")   
        results = pool.map(ekstrak_tekstur, image_path)     # Ekstrak tekstur

    # Write ke csv
    output_tekstur = open("fitur/tekstur.csv", "w")
    for imageID, fitur_tekstur in results:
        output_tekstur.write("%s,%s\n" % (imageID, ",".join(fitur_tekstur)))

    output_tekstur.close()

    end_time = time.time()
    execution_time = end_time - start_time
    print("Ekstraksi selesai!")
    print(f"Ekstraksi selesai dalam {execution_time:.2f} detik")