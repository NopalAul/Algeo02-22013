from math import pow,sqrt

def cosine_sim(vector1,vector2):
    # dot product
    dot_prod = 0
    for i in range(len(vector1)):
        dot_prod += vector1[i]*vector2[i]
    # vector magnitude
    mag_vector1 = 0
    mag_vector2 = 0
    for i in range(len(vector1)):
        mag_vector1 += pow(vector1[i],2)
    for i in range(len(vector2)):
        mag_vector2 += pow(vector2[i],2)
    mag_total = sqrt(mag_vector1)*sqrt(mag_vector2)
    # result
    return dot_prod/mag_total

# usage:
# vector1 = [25,98,30]
# vector2 = [20,90,10]
# print(cosine_sim(vector1,vector2))