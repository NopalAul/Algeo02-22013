import numpy as np
import taichi as ti
import cv2

ti.init(arch=ti.gpu)

# Constants
levels = 256  # Adjust this based on the maximum pixel intensity in your images
rows, cols = 512, 512  # Adjust this based on your image size
d = 1
histogram = ti.types.ndarray(dtype=ti.i32,ndim=1)

# Memory allocation
image = ti.field(dtype=ti.u8, shape=(rows, cols, 3))
framework_matrix = ti.field(dtype=ti.i32, shape=(levels, levels))

# Convert color to grayscale kernel
@ti.kernel
def toGrayscale_kernel():
    for i, j in ti.ndrange(rows, cols):
        grayscale_value = int(image[i, j, 0] * 0.29 + image[i, j, 1] * 0.587 + image[i, j, 2] * 0.114)
        image[i, j, 0] = grayscale_value
        image[i, j, 1] = grayscale_value
        image[i, j, 2] = grayscale_value

# GLCM computation kernel
@ti.kernel
def matrixGLCM_kernel():
    for i, j in ti.ndrange(rows, cols):
        x1, y1 = i, j
        x2, y2 = i + 0, j + d

        if 0 <= x1 < rows and 0 <= y1 < cols and 0 <= x2 < rows and 0 <= y2 < cols:
            pixel1 = image[x1, y1, 0]
            pixel2 = image[x2, y2, 0]
            ti.atomic_add(framework_matrix[pixel1, pixel2], 1)

# GLCM symmetric kernel
@ti.kernel
def symmetricGLCM_kernel():
    for i, j in ti.ndrange(levels, levels):
        framework_matrix[i, j] += framework_matrix[j, i]

# GLCM normalization kernel
@ti.kernel
def normalizeGLCM_kernel():
    total_sum = 0
    for i, j in ti.ndrange(levels, levels):
        total_sum += framework_matrix[i, j]
    for i, j in ti.ndrange(levels, levels):
        framework_matrix[i, j] /= total_sum

# Texture extraction kernel
@ti.kernel
def extract_texture_kernel() -> histogram:
    diff_matrix = ti.cast(ti.abs(ti.arange(levels) - ti.arange(levels)[:, None]), ti.f32)
    p = ti.ndarray(dtype=ti.i32, shape=(5))
    
    contrast_result = 0.0
    homogeneity_result = 0.0
    entropy_result = 0.0
    dissimilarity_result = 0.0
    energy_result = 0.0
    correlation_result = 0.0
    
    for i, j in ti.ndrange(levels, levels):
        contrast_result += diff_matrix[i, j] ** 2 * framework_matrix[i, j]
        homogeneity_result += framework_matrix[i, j] / (1 + diff_matrix[i, j] ** 2)
        
        if framework_matrix[i, j] > 0:
            entropy_result -= framework_matrix[i, j] * ti.log(framework_matrix[i, j])
        
        dissimilarity_result += diff_matrix[i, j] * framework_matrix[i, j]
        energy_result += framework_matrix[i, j] ** 2
        
        rata_rata_i = ti.cast(ti.sum(ti.arange(levels) * framework_matrix), ti.f32) / ti.cast(total_sum, ti.f32)
        rata_rata_j = ti.cast(ti.sum(ti.arange(levels) * framework_matrix), ti.f32) / ti.cast(total_sum, ti.f32)
        
        sd_i = ti.sqrt(ti.cast(ti.sum((ti.arange(levels) - rata_rata_i) ** 2 * framework_matrix), ti.f32) / ti.cast(total_sum, ti.f32))
        sd_j = ti.sqrt(ti.cast(ti.sum((ti.arange(levels) - rata_rata_j) ** 2 * framework_matrix), ti.f32) / ti.cast(total_sum, ti.f32))
        
        correlation_result += framework_matrix[i, j] * ((i - rata_rata_i) * (j - rata_rata_j) / (sd_i * sd_j))
    
    return contrast_result, homogeneity_result, entropy_result, dissimilarity_result, energy_result, correlation_result

# Example usage
def main():
    image_np = cv2.imread('dataset/0.jpg')  # Replace with the actual image path
    image.from_numpy(image_np)

    toGrayscale_kernel()
    matrixGLCM_kernel()
    symmetricGLCM_kernel()
    normalizeGLCM_kernel()
    result = extract_texture_kernel()

    print("Contrast:", result[0])
    print("Homogeneity:", result[1])
    print("Entropy:", result[2])
    print("Dissimilarity:", result[3])
    print("Energy:", result[4])
    print("Correlation:", result[5])