#--------- File finder.py: proses pencarian dengan cosine similarity ---------#
# Import library
from math import pow,sqrt
import csv

########## Cosine Similarity ##########
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

########## Pembanding vektor gambar query dengan dataset ##########
output_tekstur = 'fitur/tekstur.csv'
output_warna = 'fitur/warna.csv'
def find(inputFeature, option):
    results = {}
    if option == 'texture':
        with open(output_tekstur) as f:
            reader = csv.reader(f)

            for row in reader:
                datasetFeature = [float(x) for x in row[1:]]
                d = cosine_sim(inputFeature, datasetFeature)
                results[row[0]] = d

            f.close()
    elif option == 'color':
        with open(output_warna) as f:
            reader = csv.reader(f)

            for row in reader:
                datasetFeature = [float(x) for x in row[1:]]
                d = cosine_sim(inputFeature, datasetFeature)
                results[row[0]] = d

            f.close()

    results = sorted([(v, k) for (k, v) in results.items()])

    return results
