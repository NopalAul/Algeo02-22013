# import untuk ekstraksi fitur
import glob
import cv2
import csv
import os

output_warna = open("fitur/warna.csv", "w")
output_tekstur = open("fitur/tekstur.csv", "w")

for imagePath in glob.glob("../../img/dataset/*"):
    imageID = imagePath[imagePath.rfind("/") + 1:]
    image = cv2.imread(imagePath)

    # ekstraksi fitur gambar
    fitur_warna = None # import file .py, panggil fungsinya
    fitur_tekstur = None # import file .py, panggil fungsinya

    features = [str(f) for f in features]
    output_warna.write("%s,%s\n" % (imageID, ",".join(features)))
    output_tekstur.write("%s,%s\n" % (imageID, ",".join(features)))

output_warna.close()
output_tekstur.close()


print("Job Done, Configuration initialized!")
