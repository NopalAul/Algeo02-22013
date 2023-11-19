# Tugas Besar II Aljabar Linear dan Geometri (IF2123)
## Kelompok 13: 3 Musketeers
- Denise Felicia Tiowanni	13522013
- Muhammad Naufal Aulia	    13522074
- Abdullah Mubarak	        13522101

## Table of Contents
* [Tentang Website](#website-sistem-temu-balik-gambar)
* [Screenshots](#technologies-used)
* [Dependencies](#dependencies)
* [Screenshots](#screenshots)
* [Setup](#setup)


## Website Sistem Temu Balik Gambar <a href="website-sistem-temu-balik-gambar"></a>
Website Reverse Image Search
> Sistem temu balik gambar berbasis website yang diimplementasikan menggunakan pendekatan klasifikasi berbasis konten dengan aljabar vektor.
Sistem temu balik gambar memungkinkan kita untuk dengan mudah mencari, mengakses, dan mengelola koleksi gambar. Kita dapat mengeksplorasi informasi visual yang tersimpan di berbagai platform, termasuk pencarian gambar pribadi, analisis gambar medis untuk diagnosis, pencarian ilustrasi ilmiah, hingga mencari produk.
<!-- > Live demo [_here_](https://www.example.com).If you have the project hosted somewhere, include the link here. -->
Berikut video mengenai website:
[nonton ini dulu ga sih](https://youtu.be/kTaZdwUF400?si=oeym0EgkqAKwQucP)


## Dependencies <a href="dependencies"></a>
- Python 3.x
- Nodejs
- virtualenv `pip install virtualenv`


## Screenshots <a href="screenshots"></a>
![Example screenshot](./img/screenshot.png)
<!-- If you have screenshots you'd like to share, include them here. -->


## Setup <a href="setup"></a>
1. Clone repository ini dengan 
    ```
    git clone https://github.com/NopalAul/Algeo02-22013
    ```
2. Di dalam direktori tersebut, buat virtual environment dengan
    ```
    python -m venv myenv
    ```
3. Aktivasi virtual environment dengan
    - Windows:
        ```
        myenv\Scripts\activate
        ```
    - macOS & Linux:
        ```
        source myenv/bin/activate
        ```
4. Install dahulu requierements dengan melakukan 
    ```
    pip install -r requirements.txt
    ```
5. Pindah ke direktori *website* dengan `cd src/website`
6. Install requierements website dengan command <code>npm install</code>
7. Jalankan website dengan <code>npm start</code>
8. Buka terminal baru, aktivasi lagi virtual environment, pindah ke direktori *backend* dengan `cd src/backend`
9. Jalankan file python dengan <code>python app.py</code>
10. Buka <code>http://localhost:3000</code> pada peramban dan website sudah dapat digunakan