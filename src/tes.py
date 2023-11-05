import time
import cv2
from CBIR_tekstur import *

start_time = time.time()

image1 = cv2.imread('img/contoh/1001.jpg')
image2 = cv2.imread('img/contoh/1000.jpg')

print(f"{CBIR_tekstur(image1, image2)*100:.5f}%")

end_time = time.time()

execution_time = end_time - start_time
print(f"Program selesai dalam {execution_time:.2f} detik")