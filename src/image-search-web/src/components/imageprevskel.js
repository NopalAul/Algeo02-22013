import React from "react";
import "./skeleton.css";

const ImagePreview = ({ uploadedImage }) => {
  return (
    <div className="image-preview">
      <div className="skeleton" />
      {uploadedImage && (
        <img
          src={URL.createObjectURL(uploadedImage)}
          alt="Uploaded"
          width="200"
          height="200"
        />
      )}
    </div>
  );
};

export default ImagePreview;
