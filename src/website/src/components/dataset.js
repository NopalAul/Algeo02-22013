import "./styles.css";

import React, { useState } from 'react';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Dataset = () => {

    const [selectedFile, setSelectedFile] = useState(null);
    const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files);
  };

  const handleUpload = () => {

    if (!selectedFile || selectedFile.length === 0) {
      toast.error('Please choose a file before uploading');
      return;
    }

    const formData = new FormData();
    for (let i = 0; i < selectedFile.length; i++) {
        formData.append(`imagefiles[]`, selectedFile[i]);
      }
    
    setLoading(true);

    axios.post('http://localhost:3005/dataset', formData)
        .then(response => {
            console.log(response.data);
            toast.success('Upload process completed!');
        })
        .catch(error => {
            console.error('Error uploading file', error);
            toast.error('Error during upload :(');
        })
        .finally(() => {
            setLoading(false);
        });
  };


    return (
      <>
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
                onClick={handleUpload}
                disabled={loading}
            >
                {loading ? 'Uploading...' : 'Upload Dataset'}
            </button>
            
        </div>
        <ToastContainer
            position="top-center"
            autoClose={5000}
            className="toast-container-custom"
            bodyClassName="toast-content-custom"/>
      </>
    );
};

export default Dataset;
