import React, { useState } from 'react';
import axios from 'axios';
import ToggleOptions from './toggleoptions';
import './styles.css'

const Search = ({ onSearchComplete }) => {

  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState('');
  const [selectedOption, setSelectedOption] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {

    const formData = new FormData();
    formData.append('imagefile', selectedFile);
    formData.append('selectedOption', selectedOption);

    setLoading(true);

    axios.post('http://localhost:3005/search', formData)
      .then(response => {
        console.log(response.data);
        setImageUrl(URL.createObjectURL(selectedFile));
        onSearchComplete();
      })
      .catch(error => {
        console.error('Error uploading file', error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div>
      <ToggleOptions onOptionChange={setSelectedOption} />
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
            onClick={handleUpload}
            disabled={loading}
        >
            {loading ? 'Searching...' : 'Search'}
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
