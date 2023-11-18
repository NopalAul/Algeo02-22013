#include <stdio.h>
#include <stdlib.h>

#include "boolean.h"
#include "matrix.h"
#include "liststatik.h"
#include <math.h>

ListStatik rgb_to_histogram(double r,double g,double b,ListStatik l){
    // normalisasi
    double max, min, delta,h,s,v;
    r = r/255;
    g = g/255;
    b = b/255;
    // nilai ekstrim
    delta = max - min;
    if (max == min){
        h = 0;
    }
    else if (max == r){
        h = remainder(((g-b)/delta),6);
    }
    else if (max == g){
        h = 60*(((b-r)/delta) + 2);
    }
    else{
        h = 60*(((r-g)/delta) + 4);
    }
    if (max != 0){
        s = (delta/max);
    }
    else {
        s = 0;
    }
    v = max;
    return hsvtohistogram(h,s,v,l);
}

ListStatik quantify_hsv(double h,double s,double v){
    ListStatik l;
    CreateListStatik(&l);
    if (360 >= h >= 316){
        h = 0;
    }
    else if (h <= 25){
        h = 1;
    }
    else if (h <= 40){
        h = 2;
    }
    else if (h <= 120){
        h = 3;
    }
    else if (h <= 190){
        h = 4;
    }
    else if (h <= 270){
        h = 5;
    }
    else if (h <= 295){
        h = 6;
    }
    else if (h < 316){
        h = 7;
    }
    if (s < 0.2){
        s = 0;
    }
    else if (s < 0.7){
        s = 1;
    }
    else if (s >= 0.7){
        s = 2;
    }
    if (v < 0.2){
        v = 0;
    }
    else if (v < 0.7){
        v = 1;
    }
    else if (v >= 0.7){
        v = 2;
    }
    ELMT(l,0) = h;
    ELMT(l,1) = s;
    ELMT(l,2) = v;
    return l;
}

ListStatik hsvtohistogram(double h,double s,double v, ListStatik l){
    int index;
    ListStatik l_hsv;
    CreateListStatik(&l_hsv);
    l_hsv = quantify_hsv(h,s,v);
    index = 24*ELMT(l_hsv, 2) + 8*ELMT(l_hsv, 1) + ELMT(l_hsv, 0);
    ELMT(l, index)++;
    return l;
}

double cosine_sim(ListStatik vector1,ListStatik vector2){
    double dot_prod = 0;
    // dot product
    for (int i=0;i<72;i++){
        dot_prod += ELMT(vector1,i)*ELMT(vector2,i);
    }
    // vector magnitude
    double mag_vector1 = 0;
    double mag_vector2 = 0;
    for (int i=0;i<72;i++){
        mag_vector1 += pow(ELMT(vector1,i),2);
    }
    for (int i=0;i<72;i++){
        mag_vector2 += pow(ELMT(vector2,i),2);
    }
    double mag_total = sqrt(mag_vector1)*sqrt(mag_vector2);
    return dot_prod/mag_total;
}


ListStatik matrixToHistogram(Matrix m){
    ListStatik histogram;
    int i = 0;
    CreateListStatik(&histogram);
    // Pencarian histogram per 3x3 blok gambar
    for (i=0;i<ROW_EFF(m);i++){
        for (int j=0;j<COL_EFF(m);j++){
            histogram = rgb_to_histogram(ELMT(ELMTM(m,i,j),0),ELMT(ELMTM(m,i,j),1),ELMT(ELMTM(m,i,j),2),histogram);
        }
    }
        
    // Komparasi cosine similarity kedua vektor histogram HSV
    return histogram;
}