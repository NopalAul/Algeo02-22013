import React, { useRef, useState, useEffect } from 'react';
import Webcam from 'react-webcam';

const AutoCaptureCamera = () => {
  const webcamRef = useRef(null);
  const [capturedImages, setCapturedImages] = useState([]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      capture();
    }, 5000); // Adjust the interval as needed (in milliseconds)

    return () => clearInterval(intervalId); // Cleanup on component unmount
  }, []);

  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImages(prevImages => [...prevImages, imageSrc]);
  };

  return (
    <div>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        style={{ width: '100%', height: 'auto' }}
      />
      <div>
        {capturedImages.map((image, index) => (
          <img key={index} src={image} alt={`Captured ${index}`} />
        ))}
      </div>
    </div>
  );
};

export default AutoCaptureCamera;