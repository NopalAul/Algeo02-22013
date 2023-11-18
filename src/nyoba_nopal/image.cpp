#include <vector>
#include <iostream>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#include <array>
#include "math.h"
using namespace std;

vector<int> quantify_hsv(double h,double s,double v){
    vector<int> l; 
    if (360 > h >= 316){
        h = 0;
    }
    else if (0 <= h <= 25){
        h = 1;
    }
    else if (25 < h <= 40){
        h = 2;
    }
    else if (40 < h <= 120){
        h = 3;
    }
    else if (120 < h <= 190){
        h = 4;
    }
    else if (190 < h <= 270){
        h = 5;
    }
    else if (270 < h <= 295){
        h = 6;
    }
    else if (295 < h < 316){
        h = 7;
    }
    if (0 <= s < 0.2){
        s = 0;
    }
    else if (0.2 <= s < 0.7){
        s = 1;
    }
    else if (1 >= s >= 0.7){
        s = 2;
    }
    if (0<= v < 0.2){
        v = 0;
    }
    else if (0.2 <= v < 0.7){
        v = 1;
    }
    else if (1 >= v >= 0.7){
        v = 2;
    }
    // cout << "[" << h << "," << s << "," << v << "]" << " ";
    l.push_back(h);
    l.push_back(s);
    l.push_back(v);
    return l;
}

vector<double> rgb_to_histogram(double r,double g,double b){
    // normalisasi
    int index;
    double delta,h,s,v;
    r = r/255;
    g = g/255;
    b = b/255;
    // nilai ekstrim
    double maks = max(r,g);
    maks = max(maks,b);
    double minim = min(r,g);
    minim = min(minim,b);
    delta = maks - minim;
    // cout << "[" << g <<","<< b <<","<< delta<<","<< g-b/delta <<"]"<< " ";
    if (maks == minim){
        h = 0;
    }
    else if (maks == r){
        h = 60*remainder(((g-b)/delta),6);
    }
    else if (maks == g){
        h = 60*(((b-r)/delta) + 2);
    }
    else{
        h = 60*(((r-g)/delta) + 4);
    }
    if (maks != 0){
        s = (delta/maks);
    }
    else {
        s = 0;
    }
    v = maks;
    vector<double> l;
    l.push_back(h);
    l.push_back(s);
    l.push_back(v);
    // cout << "[" << l[0] << "," << l[1] << "," << l[2] << "]" << " ";
    // l_hsv = quantify_hsv(h,s,v);
    // index = 24*l_hsv[2] + 8*l_hsv[1] + l_hsv[0];
    // cout << index << " ";
    return l;
}



double cosine_sim(vector<double> vector1,vector<double> vector2){
    double dot_prod = 0;
    // dot product
    for (int i=0;i<72;i++){
        if (vector1[i] == 0 || vector2[i] == 0) {
            dot_prod = 1;
        } else {
            dot_prod += vector1[i]*vector2[i];
        }
    }
    // vector magnitude
    double mag_vector1 = 0;
    double mag_vector2 = 0;
    for (int i=0;i<72;i++){
        mag_vector1 += pow(vector1[i],2);
    }
    for (int i=0;i<72;i++){
        mag_vector2 += pow(vector2[i],2);
    }
    double mag_total = sqrt(mag_vector1)*sqrt(mag_vector2);
    cout << dot_prod << " ";
    return dot_prod/mag_total;
}


double matrixToHistogram(vector<int> m, vector<int> m1){
    int i = 0,c=0;
    double sum = 0;
    cout << 20 <<"\n";

    // Pencarian histogram per 3x3 blok gambar
    // cout << cosine_sim(rgb_to_histogram(m[300],m[300+1], m[300+2]),rgb_to_histogram(m1[300],m1[300+1], m1[300+2])) << "\n";
    for (i=0;i<m.size();i+=3){
        sum += cosine_sim(rgb_to_histogram(m[i],m[i+1], m[i+2]),rgb_to_histogram(m1[i],m1[i+1], m1[i+2]));
        c++;
    }
    // cout << sum << "\n";
    return sum/c;
}

vector<int> imagetoarray(const char* filename){
    int width, height, channels;
    vector<int> m;
    const char* c = filename;
    unsigned char* image_data = stbi_load(c, &width, &height, &channels, 0);
    if (image_data == NULL) {
        printf("Error loading image.\n");
    }

    unsigned char* image_array = new unsigned char[width * height * channels];

    int j = 0, k = 1;
    memcpy(image_array, image_data, width * height * channels);
    for (int i = 0; i < width * height * channels; i++){
        // cout << int(image_array[i + 1]) << " ";
        m.push_back(int(image_array[i]));
        // cout << m[i] << " ";
    }
    return m;
}

int main(){
    cout << matrixToHistogram(imagetoarray("0.jpg"), imagetoarray("1.jpg"));
}
