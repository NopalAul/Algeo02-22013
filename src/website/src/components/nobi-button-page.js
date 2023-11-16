import React from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';
import standingdora from './rsc/dodo_icon.png'; 

const NobiButtonPage = () => {
    const navigate = useNavigate();

    const handleBackClick = () => {
      navigate('/'); // home page
    };

    const handleDoraemon = () => {
      navigate('/buttonpage');
    };

    return (
      <div className="button-page-container">
        <button className="back-button" onClick={handleBackClick}>
          Home
        </button>
        <button className="back-dora-button" onClick={handleDoraemon}>
          About us
        </button>
        <h2 className="page-title">ABOUT THIS WEBSITE</h2>
        <p className="page-content">
          Website ini adalah sebuah web sistem temu balik gambar yang diimplementasikan menggunakan pendekatan 
          klasifikasi berbasis konten dengan aljabar vektor. Dalam konteks ini, aljabar vektor digunakan untuk 
          menggambarkan dan menganalisis data menggunakan pendekatan klasifikasi berbasis konten (Content-Based 
          Image Retrieval atau CBIR), di mana sistem temu balik gambar bekerja dengan mengidentifikasi gambar 
          berdasarkan konten visualnya, seperti <strong> warna</strong> dan <strong>tekstur</strong>.
        </p>
        <h4 className="page-title">CARA KERJA</h4>
        <p className="page-content">
        <strong>1. </strong>Pengguna terlebih dahulu memasukkan dataset gambar dalam bentuk folder yang berisi kumpulan gambar.
        Dataset gambar ini diperlukan sebelum proses searching agar ada perbandingan untuk gambar yang ingin dicari. </p>
        <p className="page-content"> 
        <strong>2. </strong>Setelah dataset sudah dimasukkan, pengguna memasukkan sebuah gambar yang ingin di-search dari dataset. </p>
        <p className="page-content"> 
        <strong>3. </strong>Pilih opsi pencarian, ingin melakukan pencarian berdasarkan warna atau tekstur. </p>
        <p className="page-content"> 
        <strong>4. </strong>Tekan tombol search, program kemudian akan memproses, mencari gambar-gambar dari dataset yang memiliki kemiripan dengan gambar yang dimasukkan tadi. </p>
        <p className="page-content">
        <strong>5. </strong>Program akan menampilkan kumpulan gambar yang mirip, diurutkan dari yang memiliki kemiripan paling tinggi ke yang paling rendah. Setiap gambar yang muncul diberi persentase kemiripannya. </p> 
        <p className="page-content">
        <strong>6. </strong>Terdapat informasi terkait jumlah gambar yang muncul, dan waktu eksekusi programnya.
        </p>
        <img src={standingdora} alt="Standing Doraemon" className="bottom-corner-image" />
      </div>
    );
  }
  
  export default NobiButtonPage;