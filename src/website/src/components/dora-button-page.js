import React from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';
import standingdora from './rsc/dodo_icon.png'; 

const DoraButtonPage = () => {
    const navigate = useNavigate();

    const handleBackClick = () => {
      navigate('/'); // home page
    };

    const handleNobita = () => {
      navigate('/nobi-button-page');
    };

    return (
      <div className="button-page-container">
        <button className="back-button" onClick={handleBackClick}>
          Home
        </button>
        <button className="back-dora-button" onClick={handleNobita}>
          How to Use
        </button>
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