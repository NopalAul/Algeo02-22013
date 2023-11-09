import React, { useState, useEffect } from 'react';
import './skeleton.css';

const ImagePreview = ({ uploadedImage }) => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (uploadedImage) {
      const image = new Image();
      image.src = URL.createObjectURL(uploadedImage);

      image.onload = () => {
        setLoading(false);
      };
    } else {
      setLoading(false);
    }
  }, [uploadedImage]);

  return (
    <div className="image-preview">
      <div className={loading ? 'skeleton' : ''} />
      {uploadedImage && (
        <img
          src={URL.createObjectURL(uploadedImage)}
          alt="Preview"
          style={{ width: '100%', height: 'auto' }}
        />
      )}
    </div>
  );
};

export default ImagePreview;
