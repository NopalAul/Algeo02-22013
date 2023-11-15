import "./styles.css";

import React, { useState } from 'react';
import axios from 'axios';

const Dataset = () => {

    const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files);
  };

  const handleUpload = () => {
    const formData = new FormData();
    for (let i = 0; i < selectedFile.length; i++) {
        formData.append(`imagefiles[]`, selectedFile[i]);
      }

    axios.post('http://localhost:3005/dataset', formData)
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.error('Error uploading file', error);
      });
  };


    return (
        <div className="custom-file-input-container flex items-center">
            <label htmlFor="datainput" className="custom-file-input" style={{ fontFamily: 'Comic Sans MS, cursive'}}>Choose a folder</label>
            <input
                type="file"
                id="datainput"
                directory=""
                webkitdirectory=""
                style={{ display: "none" }}
                multiple
                onChange={handleFileChange}
            />
            <button
                className="upload-search-button"
                style={{ fontFamily: 'Comic Sans MS, cursive'}}
                onClick={handleUpload}>
                Upload Dataset
            </button>
        </div>
    );
};

export default Dataset;