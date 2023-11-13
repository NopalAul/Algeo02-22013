import React, { useState } from 'react';
import axios from 'axios';

import './styles.css'

const Search = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imageUrl, setImageUrl] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append('imagefile', selectedFile); //nama imagefile harus sama dgn app.py

    axios.post('http://localhost:3005/search', formData)
      .then(response => {
        console.log(response.data);
        setImageUrl(URL.createObjectURL(selectedFile));
        // Handle success or update UI as needed
      })
      .catch(error => {
        console.error('Error uploading file', error);
        // Handle error or update UI accordingly
      });
  };

  return (
    <div>
      <div className="ref-img-container">
        <label htmlFor="fileInput" className="ref-img" style={{ fontFamily: 'Comic Sans MS, cursive'}}>
          Insert an Image
        </label>
        <input
          type="file"
          id="fileInput"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
        <button
            className="search-button"
            style={{ fontFamily: 'Comic Sans MS, cursive'}}
            onClick={handleUpload}>
            Search
        </button>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50px' }}>
        {selectedFile && <p>{selectedFile.name}</p>}
      </div>
      {imageUrl && (
        <div>
        <img src={imageUrl} alt="Uploaded" style={{display: 'block', margin: 'auto', width: '50%', height: 'auto'}} />
      </div>
      )}
    </div>
  );
};

export default Search;
