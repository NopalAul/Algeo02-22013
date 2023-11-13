from math import pow,sqrt
import csv

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
    # return results[:limit]

# usage ex:
# inputF = [126.14295651908023,0.1672657734818665,9.00105046776379,7.455525318003914,0.013465695481830138,0.9786704881314865]
# option = "texture"
# print("hasil:", find(inputF,option))
