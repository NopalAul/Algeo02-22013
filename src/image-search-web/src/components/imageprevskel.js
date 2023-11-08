import React from "react";
import Skeleton from "./skeleton.css"; // Import the Skeleton component

const ImagePreview = ({ uploadedImage }) => {
  return (
    <div className="image-preview">
      <Skeleton /> {/* Always show the skeleton */}
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
