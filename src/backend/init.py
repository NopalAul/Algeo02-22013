import glob
import cv2

from tekstur import *
from warna import warna_csv

# Ekstrak warna
warna_csv()

# Ekstrak tekstur
output_tekstur = open("fitur/tekstur.csv", "w")
for imagePath in glob.glob("../../img/dataset/*"):
    imageID = imagePath[imagePath.rfind("\\") + 1:]
    image = cv2.imread(imagePath)

    # ekstraksi fitur gambar
    fitur_tekstur = CBIR_tekstur(image)
    fitur_tekstur = [str(f) for f in fitur_tekstur]
    output_tekstur.write("%s,%s\n" % (imageID, ",".join(fitur_tekstur)))

output_tekstur.close()


print("Ekstraksi selesai!")


# import glob
# import cv2
# from multiprocessing import Pool

# from tekstur import *
# from warna import warna_csv

# # Ekstrak warna
# warna_csv()

# # Ekstrak tekstur
# def extract_features(imagePath):
#     imageID = imagePath[imagePath.rfind("\\") + 1:]
#     image = cv2.imread(imagePath)

#     # ekstraksi fitur gambar
#     fitur_tekstur = CBIR_tekstur(image)
#     fitur_tekstur = [str(f) for f in fitur_tekstur]
    
#     return imageID, fitur_tekstur

# if __name__ == "__main__":
#     # Ekstrak warna
#     warna_csv()

#     # Ekstrak tekstur using multiprocessing.Pool
#     with Pool() as pool:
#         image_paths = glob.glob("../../img/dataset/*")
#         results = pool.map(extract_features, image_paths)

#     # Write results to the output file
#     output_tekstur = open("fitur/tekstur.csv", "w")
#     for imageID, fitur_tekstur in results:
#         output_tekstur.write("%s,%s\n" % (imageID, ",".join(fitur_tekstur)))

#     output_tekstur.close()

#     print("Ekstraksi selesai!")

# # output_tekstur = open("fitur/tekstur.csv", "w")
# # for imagePath in glob.glob("../../img/dataset/*"):
# #     imageID = imagePath[imagePath.rfind("\\") + 1:]
# #     image = cv2.imread(imagePath)

# #     # ekstraksi fitur gambar
# #     fitur_tekstur = CBIR_tekstur(image)
# #     fitur_tekstur = [str(f) for f in fitur_tekstur]
# #     output_tekstur.write("%s,%s\n" % (imageID, ",".join(fitur_tekstur)))


# # if __name__ == '__main__':
# #     # inisialisasi pool multiprocessing dengan jumlah prosesor yang tersedia
# #     num_processors = 5 # sesuaikan dengan jumlah prosesor yang tersedia
# #     pool = Pool(processes=num_processors)

# #     # bandingkan gambar referensi dengan gambar target secara paralel
# #     vectors = pool.starmap(CBIR_tekstur, [(image,) for image in target_images_list])

# #     # close pool multiprocessing
# #     pool.close()
# #     pool.join()

# # print("Ekstraksi selesai!")

# # output_tekstur.close()