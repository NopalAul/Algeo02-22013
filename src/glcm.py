import numpy as np

def create_glcm_matrix(image, d=1, angle=0):
    # quantization levels
    levels = np.max(image) + 1

    # inisialisasi matrix dengan 0
    framework_matrix = np.zeros((levels, levels), dtype=np.uint32)

    # dimensi dari gambarnya
    rows, cols = image.shape

    # isi matrixnya
    for i in range(rows):
        for j in range(cols):
                x1, y1 = i, j

                # perpindahan vektor berdasarkan sudut
                if angle == 0:
                    x2, y2 = i + 0, j + d
                elif angle == 90:
                    x2, y2 = ...
                elif angle == 45:
                    x2, y2 = ...
                elif angle == 135:
                    x2, y2 = ...

                if 0 <= x1 < rows and 0 <= y1 < cols and 0 <= x2 < rows and 0 <= y2 < cols:
                    pixel1 = image[x1, y1]
                    pixel2 = image[x2, y2]
                    framework_matrix[pixel1, pixel2] += 1

    return framework_matrix

# bikin matriks simetriknya
def create_symmetric_glcm(glcm_matrix):
    symmetric_glcm = glcm_matrix + glcm_matrix.T
    return symmetric_glcm

# normalisasi matriks
def normalize_glcm(glcm_matrix):
    normalized_glcm = glcm_matrix / np.sum(glcm_matrix)
    return normalized_glcm

# tes
image = np.array([[0, 0, 1],
                  [1, 2, 3],
                  [2, 3, 2]])

# image = np.array([[1, 1, 5, 6, 8],
#                   [2, 3, 5, 7, 1],
#                   [4, 5, 7, 1, 2],
#                   [8, 5, 1, 2, 5]])

glcm_matrix = create_glcm_matrix(image, d=1, angle=0)
symmetric_glcm = create_symmetric_glcm(glcm_matrix)
normalized_glcm = normalize_glcm(symmetric_glcm)

print("GLCM Matrix:")
print(glcm_matrix)
print("Symmetric GLCM Matrix:")
print(symmetric_glcm)
print("Normalized GLCM Matrix:")
print(normalized_glcm)
