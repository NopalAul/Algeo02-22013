import cv2
# import coba_cython

gambar1 = cv2.imread('../../src/nyoba_nopal/0.jpg')
gambar2 = cv2.imread('../../src/nyoba_nopal/1.jpg')
print(f"cosine similarity : {coba_cython.coba1(gambar1,gambar2)}")
