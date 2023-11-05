from glcm import *

def CBIR_tekstur(image1, image2):
    ## BUAT VECTOR BERISI CONTRAST, HOMOGENEITY, DAN ENTROPY DARI IMAGE 1
    # sudut 0
    glcm_matrix1_sudut0 = matrixGLCM(image1, d=1, angle=0)
    symmetric_glcm1_sudut0 = symmetricGLCM(glcm_matrix1_sudut0)
    normalized_glcm1_sudut0 = normalizeGLCM(symmetric_glcm1_sudut0)
    contrast1_sudut0, homogeneity1_sudut0, entropy1_sudut0, dissimilarity1_sudut0, energy1_sudut0, correlation1_sudut0 = extract_texture(normalized_glcm1_sudut0)
    # sudut 45
    glcm_matrix1_sudut45 = matrixGLCM(image1, d=1, angle=45)
    symmetric_glcm1_sudut45 = symmetricGLCM(glcm_matrix1_sudut45)
    normalized_glcm1_sudut45 = normalizeGLCM(symmetric_glcm1_sudut45)
    contrast1_sudut45, homogeneity1_sudut45, entropy1_sudut45, dissimilarity1_sudut45, energy1_sudut45, correlation1_sudut45 = extract_texture(normalized_glcm1_sudut45)
    # sudut 90
    glcm_matrix1_sudut90 = matrixGLCM(image1, d=1, angle=90)
    symmetric_glcm1_sudut90 = symmetricGLCM(glcm_matrix1_sudut90)
    normalized_glcm1_sudut90 = normalizeGLCM(symmetric_glcm1_sudut90)
    contrast1_sudut90, homogeneity1_sudut90, entropy1_sudut90, dissimilarity1_sudut90, energy1_sudut90, correlation1_sudut90 = extract_texture(normalized_glcm1_sudut90)
    # sudut 135
    glcm_matrix1_sudut135 = matrixGLCM(image1, d=1, angle=135)
    symmetric_glcm1_sudut135 = symmetricGLCM(glcm_matrix1_sudut135)
    normalized_glcm1_sudut135 = normalizeGLCM(symmetric_glcm1_sudut135)
    contrast1_sudut135, homogeneity1_sudut135, entropy1_sudut135, dissimilarity1_sudut135, energy1_sudut135, correlation1_sudut135 = extract_texture(normalized_glcm1_sudut135)

    vector1 = createVector(contrast1_sudut0, contrast1_sudut45, contrast1_sudut90, contrast1_sudut135,
                           homogeneity1_sudut0, homogeneity1_sudut45, homogeneity1_sudut90, homogeneity1_sudut135,
                           entropy1_sudut0, entropy1_sudut45, entropy1_sudut90, entropy1_sudut135,
                           dissimilarity1_sudut0, dissimilarity1_sudut45, dissimilarity1_sudut90, dissimilarity1_sudut135,
                           energy1_sudut0, energy1_sudut45, energy1_sudut90, energy1_sudut135,
                           correlation1_sudut0, correlation1_sudut45, correlation1_sudut90, correlation1_sudut135)

    ## BUAT VECTOR BERISI CONTRAST, HOMOGENEITY, DAN ENTROPY DARI IMAGE 2
    # sudut 0
    glcm_matrix2_sudut0 = matrixGLCM(image2, d=1, angle=0)
    symmetric_glcm2_sudut0 = symmetricGLCM(glcm_matrix2_sudut0)
    normalized_glcm2_sudut0 = normalizeGLCM(symmetric_glcm2_sudut0)
    contrast2_sudut0, homogeneity2_sudut0, entropy2_sudut0, dissimilarity2_sudut0, energy2_sudut0, correlation2_sudut0 = extract_texture(normalized_glcm2_sudut0)
    # sudut 45
    glcm_matrix2_sudut45 = matrixGLCM(image2, d=1, angle=45)
    symmetric_glcm2_sudut45 = symmetricGLCM(glcm_matrix2_sudut45)
    normalized_glcm2_sudut45 = normalizeGLCM(symmetric_glcm2_sudut45)
    contrast2_sudut45, homogeneity2_sudut45, entropy2_sudut45, dissimilarity2_sudut45, energy2_sudut45, correlation2_sudut45 = extract_texture(normalized_glcm2_sudut45)
    # sudut 90
    glcm_matrix2_sudut90 = matrixGLCM(image2, d=1, angle=90)
    symmetric_glcm2_sudut90 = symmetricGLCM(glcm_matrix2_sudut90)
    normalized_glcm2_sudut90 = normalizeGLCM(symmetric_glcm2_sudut90)
    contrast2_sudut90, homogeneity2_sudut90, entropy2_sudut90, dissimilarity2_sudut90, energy2_sudut90, correlation2_sudut90 = extract_texture(normalized_glcm2_sudut90)
    # sudut 135
    glcm_matrix2_sudut135 = matrixGLCM(image2, d=1, angle=135)
    symmetric_glcm2_sudut135 = symmetricGLCM(glcm_matrix2_sudut135)
    normalized_glcm2_sudut135 = normalizeGLCM(symmetric_glcm2_sudut135)
    contrast2_sudut135, homogeneity2_sudut135, entropy2_sudut135, dissimilarity2_sudut135, energy2_sudut135, correlation2_sudut135 = extract_texture(normalized_glcm2_sudut135)

    vector2 = createVector(contrast2_sudut0, contrast2_sudut45, contrast2_sudut90, contrast2_sudut135,
                           homogeneity2_sudut0, homogeneity2_sudut45, homogeneity2_sudut90, homogeneity2_sudut135,
                           entropy2_sudut0, entropy2_sudut45, entropy2_sudut90, entropy2_sudut135,
                           dissimilarity2_sudut0, dissimilarity2_sudut45, dissimilarity2_sudut90, dissimilarity2_sudut135,
                           energy2_sudut0, energy2_sudut45, energy2_sudut90, energy2_sudut135,
                           correlation2_sudut0, correlation2_sudut45, correlation2_sudut90, correlation2_sudut135)
   
    ## CARI NILAI COS THETA UNTUK TAU KEMIRIPAN
    cos_theta = cosine_sim(vector1, vector2)

    return cos_theta