import "./styles.css";

import React, { useState } from 'react';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Dataset = () => {

    const [selectedFile, setSelectedFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [extractionStatus, setExtractionStatus] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files);
    setExtractionStatus(null);
  };

  const handleUpload = () => {
    const formData = new FormData();
    for (let i = 0; i < selectedFile.length; i++) {
        formData.append(`imagefiles[]`, selectedFile[i]);
      }
    
    setLoading(true);

    axios.post('http://localhost:3005/dataset', formData)
        .then(response => {
            console.log(response.data);
            toast.success('Upload process completed!');
            setExtractionStatus(response.data.message);
            setTimeout(() => {
              setExtractionStatus(null);
          }, 3000);
        })
        .catch(error => {
            console.error('Error uploading file', error);
            toast.error('Error during upload :(');
            setExtractionStatus('Error during extraction');
            setTimeout(() => {
              setExtractionStatus(null);
          }, 3000);
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
        <h1 className="text-center text-red-600">{extractionStatus && (
                <p style={{ marginLeft: '10px', fontFamily: 'Comic Sans MS, cursive'}}>
                    {extractionStatus}
                </p>
            )}
        </h1>
        <ToastContainer
            position="top-center"
            autoClose={5000}
            className="toast-container-custom"
            bodyClassName="toast-content-custom"/>
      </>
    );
};

export default Dataset;
