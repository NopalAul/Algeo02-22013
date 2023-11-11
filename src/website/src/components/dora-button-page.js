import React from 'react';
import './page.css';
import standingdora from './rsc/dodo_icon.png'; 

const DoraButtonPage = () => {
    return (
      <div className="button-page-container">
        <h2 className="page-title">ABOUT 3 MUSKETEERS</h2>
        <p className="page-content">
          3 Musketeers adalah sebuah kelompok Tugas Besar II Aljabar Linear dan Geometri (IF2123) yang terdiri
          dari <strong> Denise Felicia Tiowanni (NIM 13522013)</strong>, <strong> Muhammad Naufal Aulia (NIM 13522074)</strong>, 
          dan <strong> Abdullah Mubarak (NIM 13522101)</strong>. Proyek untuk Tugas Besar II IF2123 kali ini adalah 'Website Sistem Temu Balik Gambar'
          yang diimplementasikan menggunakan pendekatan klasifikasi berbasis konten dengan aljabar vektor.
        </p>
        <img src={standingdora} alt="Standing Doraemon" className="bottom-corner-image" />
      </div>
    );
  }
  
  export default DoraButtonPage;