import React from "react";

const ImagePreview = ({ uploadedImage }) => {
  return (
    <div className="image-preview">
      {uploadedImage && (
        <img
          src={URL.createObjectURL(uploadedImage)}
          alt="Uploaded"
          width="200" // Adjust the width as needed
          height="200" // Adjust the height as needed
        />
      )}
    </div>
  );
};

export default ImagePreview;
