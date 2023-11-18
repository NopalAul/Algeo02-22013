#include <vector>
#include <iostream>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#include <array>
#include <bits/stdc++.h>
#include "math.h"
using namespace std;

// ########## CONVERT WARNA TO GRAYSCALE ##########
vector<float> imagetoarray(const char* filename){
    int width, height, channels;
    vector<float> m;
    const char* c = filename;
    unsigned char* image_data = stbi_load(c, &width, &height, &channels, 0);
    if (image_data == NULL) {
        printf("Error loading image.\n");
    }

    unsigned char* image_array = new unsigned char[width * height * channels];
    
    int j = 0, k = 1;
    memcpy(image_array, image_data, width * height * channels);
    for (int i = 0; i < width * height * channels; i+=3){
        // cout << int(image_array[i + 1]) << " ";
        m.push_back(int(image_array[i]) * 0.29);
        m.push_back(int(image_array[i+1]) * 0.587);
        m.push_back(int(image_array[i+2]) * 0.114);
        // cout << m[i] << " ";
        // cout << m[i] << " ";
    }
    return m;
}



// ########## FRAMEWORK MATRIKS ##########
void transpose(int A[][], int B[][]) 
{ 
    int i, j; 
    for (i = 0; i < N; i++) 
        for (j = 0; j < N; j++) 
            B[i][j] = A[j][i]; 
} 

void matrixGLCM(const char* filename, int d=1){
    int width, height, channels;
    vector<float> m;
    const char* c = filename;
    unsigned char* image_data = stbi_load(c, &width, &height, &channels, 0);
    if (image_data == NULL) {
        printf("Error loading image.\n");
    }

    unsigned char* image_array = new unsigned char[width * height * channels];
    
    int j = 0, k = 1, max = 0;
    memcpy(image_array, image_data, width * height * channels);
    for (int i = 0; i < width * height * channels; i+=3){
        // cout << int(image_array[i + 1]) << " ";
        m.push_back(int(image_array[i]) * 0.29 + int(image_array[i+1]) * 0.587 + int(image_array[i+2]) * 0.114);
        if (m[j] >= max){
            max = m[j];
        }
        j++;
        // cout << m[i] << " ";
        // cout << m[i] << " ";
    }
    float framework_matrix[max,max];
    int rows, cols = height, width,i, pixel1,pixel2;
    for (i=0;i<rows;i++){
        for (j=0;j<cols;j++){
            int x = i+0, y = j+d;
            if (0 <= i < rows && 0 <= j < cols && 0 <= x < rows && 0 <= y < cols){
                    pixel1 = m[i*j + j];
                    pixel2 = m[i*j + j + d];
                    framework_matrix[pixel1,pixel2] += 1;
            }
        }
    }
    // int matrix_transpose[max,max];
    float sum = 0;
    for (i = 0; i < max; i++) 
        for (j = 0; j < max; j++) 
            framework_matrix[i,j] += framework_matrix[j,i]; 
            sum += framework_matrix[i,j];
    for (i = 0; i < max; i++) 
        for (j = 0; j < max; j++) 
            framework_matrix[i,j] /= sum; 
    float list[6];

    // # buat cari i - j (untuk contrast, homogeneity, dissimilarity)
    float diff_matrix = fabs(np.arange(rows) - np.arange(rows)[:, np.newaxis]);

    // # 1. contrast
    list[0] = np.sum(diff_matrix ** 2 * glcm_matrix)

    // # 2. homogeneity
    list[1] = np.sum(glcm_matrix / (1 + diff_matrix ** 2));
    
    // # 3. entropy
    // # cari elemen tidak nol, handle kasus log(0) di entropy
    non_zero_elements = glcm_matrix[glcm_matrix > 0];
    list[2] = -np.sum(non_zero_elements * np.log(non_zero_elements));

    // # 4. dissimilarity
    list[3] = np.sum(diff_matrix * glcm_matrix);

    // # 5. energy
    list[4] = np.sqrt(np.sum(glcm_matrix ** 2));

    // # 6. correlation
    i, j = np.meshgrid(np.arange(rows), np.arange(rows), indexing='ij');
    rata_rata_i = np.sum(i * glcm_matrix) / np.sum(glcm_matrix);
    rata_rata_j = np.sum(j * glcm_matrix) / np.sum(glcm_matrix);
    
    sd_i = np.sqrt(np.sum(((i - rata_rata_i) ** 2) * glcm_matrix) / np.sum(glcm_matrix));
    sd_j = np.sqrt(np.sum(((j - rata_rata_j) ** 2) * glcm_matrix) / np.sum(glcm_matrix));
    
    list[5] = np.sum(glcm_matrix * ((i - rata_rata_i) * (j - rata_rata_j) / (sd_i * sd_j)));
}

int main(){
    // imagetoarray("0.jpg");
    for (int i; i < 512; i++){
        cout << imagetoarray("0.jpg")[i] << " ";
    }
    return 0;
}

// ########## MATRIKS SIMETRIK ##########
// def symmetricGLCM(glcm_matrix):
//     symmetric_glcm = glcm_matrix + glcm_matrix.T
//     return symmetric_glcm

// ########## MATRIKS NORMALISASI ##########
// def normalizeGLCM(glcm_matrix):
//     normalized_glcm = glcm_matrix / np.sum(glcm_matrix)
//     return normalized_glcm

// ########## EKSTRAKSI TEKSTUR ##########
// def extract_texture(glcm_matrix):
//     rows = glcm_matrix.shape[0]
//     list = [0 for i in range(6)]

//     # buat cari i - j (untuk contrast, homogeneity, dissimilarity)
//     diff_matrix = np.abs(np.arange(rows) - np.arange(rows)[:, np.newaxis])

//     # 1. contrast
//     list[0] = np.sum(diff_matrix ** 2 * glcm_matrix)

//     # 2. homogeneity
//     list[1] = np.sum(glcm_matrix / (1 + diff_matrix ** 2))
    
//     # 3. entropy
//     # cari elemen tidak nol, handle kasus log(0) di entropy
//     non_zero_elements = glcm_matrix[glcm_matrix > 0]
//     list[2] = -np.sum(non_zero_elements * np.log(non_zero_elements))

//     # 4. dissimilarity
//     list[3] = np.sum(diff_matrix * glcm_matrix)

//     # 5. energy
//     list[4] = np.sqrt(np.sum(glcm_matrix ** 2))

//     # 6. correlation
//     i, j = np.meshgrid(np.arange(rows), np.arange(rows), indexing='ij')
//     rata_rata_i = np.sum(i * glcm_matrix) / np.sum(glcm_matrix)
//     rata_rata_j = np.sum(j * glcm_matrix) / np.sum(glcm_matrix)
    
//     sd_i = np.sqrt(np.sum(((i - rata_rata_i) ** 2) * glcm_matrix) / np.sum(glcm_matrix))
//     sd_j = np.sqrt(np.sum(((j - rata_rata_j) ** 2) * glcm_matrix) / np.sum(glcm_matrix))
    
//     list[5] = np.sum(glcm_matrix * ((i - rata_rata_i) * (j - rata_rata_j) / (sd_i * sd_j)))

//     return list

// ########## COSINE SIMILARITY ##########
// # def createVector(a, b, c, d, e, f,):
// #     vector = np.array([a, b, c, d, e, f])

// #     return vector

// ########## CBIR-TEKSTUR ##########
// def CBIR_tekstur(image):
//     ## BUAT VECTOR BERISI CONTRAST, HOMOGENEITY, DAN ENTROPY DARI IMAGE 1
//     # sudut 0
//     glcm_matrix_sudut0 = matrixGLCM(image, d=1)
//     symmetric_glcm_sudut0 = symmetricGLCM(glcm_matrix_sudut0)
//     normalized_glcm_sudut0 = normalizeGLCM(symmetric_glcm_sudut0)
//     vector =  extract_texture(normalized_glcm_sudut0)
    
//     return vector

// image = cv2.imread("0.jpg")
// print(CBIR_tekstur(image))
// ########## MENGAMBIL SEMUA GAMBAR DALAM SATU FOLDER ##########
// def imageInFolder(folder_path):
//     image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.jpg')]
//     return image_files

// end = timer()
// print(end - start)

// ##########***** TES *****##########

// # if __name__ == '__main__':
// #     start_time = time.time()

// #     # list gambar target yang akan dibandingkan
// #     target_folder = 'img/dataset/'
// #     target_images = imageInFolder(target_folder)

// #     # baca semua gambar langsung terus simpen ke list, jadi ga ulang ulang cv2 imreadnya
// #     target_images_list = [cv2.imread(image_path) for image_path in target_images]

// #     # inisialisasi pool multiprocessing dengan jumlah prosesor yang tersedia
// #     num_processors = 8 # sesuaikan dengan jumlah prosesor yang tersedia
// #     pool = Pool(processes=num_processors)

// #     # bandingkan gambar referensi dengan gambar target secara paralel
// #     vectors = pool.starmap(CBIR_tekstur, [(image,) for image in target_images_list])

// #     # close pool multiprocessing
// #     pool.close()
// #     pool.join()

// #     # Hasil kesamaan citra
// #     for i, vektor in enumerate(vectors):
// #         # print(f"Kesamaan dengan gambar-{i+1}: {similarity * 100:.5f}%")
// #         print(f"vektor gambar-{i+1}: {vektor}%")

// #     end_time = time.time()

// #     execution_time = end_time - start_time
// #     print(f"Program selesai dalam {execution_time:.2f} detik")



