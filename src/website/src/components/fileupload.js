import React, { useState } from 'react';
import './styles.css'

const FileInputButton = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    // handle file selection
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  return (
    <div className="ref-img-container">
      <label htmlFor="fileInput" className="ref-img" style={{ fontFamily: 'Comic Sans MS, cursive'}}>
        Insert an Image
      </label>
      <input
        type="file"
        onChange={handleFileChange}
        style={{ display: 'none' }}
        id="fileInput"
      />
      {selectedFile && <p>{selectedFile.name}</p>}
    </div>
  );
};

export default FileInputButton;
