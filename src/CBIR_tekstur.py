from glcm import *

def CBIR_tekstur(image1, image2):
    ## BUAT VECTOR BERISI CONTRAST, HOMOGENEITY, DAN ENTROPY DARI IMAGE 1
    glcm_matrix1 = matrixGLCM(image1, d=1, angle=0)
    symmetric_glcm1 = symmetricGLCM(glcm_matrix1)
    normalized_glcm1 = normalizeGLCM(symmetric_glcm1)
    contrast1 = contrast(normalized_glcm1)
    homogeneity1 = homogeneity(normalized_glcm1)
    entropy1 = entropy(normalized_glcm1)
    vector1 = createVector(contrast1, homogeneity1, entropy1)

    ## BUAT VECTOR BERISI CONTRAST, HOMOGENEITY, DAN ENTROPY DARI IMAGE 2
    glcm_matrix2 = matrixGLCM(image2, d=1, angle=0)
    symmetric_glcm2 = symmetricGLCM(glcm_matrix2)
    normalized_glcm2 = normalizeGLCM(symmetric_glcm2)
    contrast2 = contrast(normalized_glcm2)
    homogeneity2 = homogeneity(normalized_glcm2)
    entropy2 = entropy(normalized_glcm2)
    vector2 = createVector(contrast2, homogeneity2, entropy2)

    ## CARI NILAI COS THETA UNTUK TAU KEMIRIPAN
    cos_theta = cosine_sim(vector1, vector2)

    ## HITUNG PERSENTASE KEMIRIPAN
    similarity = cos_theta*100

    return similarity

image1 = np.array([[0, 0, 1],
                  [1, 2, 3],
                  [2, 3, 2]])
                  
image2 = np.array([[0, 0, 1],
                  [1, 2, 3],
                  [2, 3, 2]])

print(CBIR_tekstur(image1, image2))
