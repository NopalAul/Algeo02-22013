import React, { useState } from 'react';
import axios from 'axios';

import './search-field.css';

const SearchField = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    axios.post('http://127.0.0.1:5000/upload', formData)
      .then(response => {
        console.log(response.data);
        // handle success or update UI as needed
      })
      .catch(error => {
        console.error('Error uploading file', error);
        // handle error or update UI accordingly
      });
  };

  return (
    <div className="custom-file-input-container flex items-center">
      <label htmlFor="fileInput" className="custom-file-input" style={{ fontFamily: 'Comic Sans MS, cursive' }}>
        Choose a file
      </label>
      <input
        type="file"
        id="fileInput"
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
      <button
        className="upload-search-button"
        style={{ fontFamily: 'Comic Sans MS, cursive' }}
        onClick={handleUpload}
      >
        Upload & Search
      </button>
    </div>
  );
};

export default SearchField;