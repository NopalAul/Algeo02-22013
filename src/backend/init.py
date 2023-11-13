import glob
import cv2
import csv
import os

from tekstur import *
from warna import warna_csv

# Ekstrak warna
warna_csv()

# Ekstrak tekstur
output_tekstur = open("fitur/tekstur.csv", "w")
for imagePath in glob.glob("../../img/dataset/*"):
    imageID = imagePath[imagePath.rfind("\\") + 1:] # atau imageID = imagePath[imagePath.rfind("/") + 1:]

    image = cv2.imread(imagePath)

    # ekstraksi fitur gambar
    fitur_tekstur = CBIR_tekstur(image) # import file .py, panggil fungsinya

    fitur_tekstur = [str(f) for f in fitur_tekstur]
    output_tekstur.write("%s,%s\n" % (imageID, ",".join(fitur_tekstur)))

output_tekstur.close()


print("Job Done, Configuration initialized!")
