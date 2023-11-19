import React, { useState, useRef, useEffect } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';

const Kamera = () => {
  const webcamRef = useRef(null);
  const [image, setImage] = useState(null);
  const [capturing, setCapturing] = useState(false);

  const captureHandler = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImage(imageSrc);

    // Convert the image to a Blob
    const blob = await fetch(imageSrc).then((res) => res.blob());

    // Create FormData and append the image Blob
    const formData = new FormData();
    formData.append('image', blob, 'captured_image.jpg');

    // Send image to the backend
    try {
      await axios.post('http://localhost:3005/camera', formData);
    } catch (error) {
      console.error('Error sending image to the server:', error);
    }
  };

  const startCapturing = () => {
    setCapturing(true);
  };

  const stopCapturing = () => {
    setCapturing(false);
  };

  // Auto-capture at a certain interval (e.g., every 10 seconds)
  useEffect(() => {
    const intervalId = setInterval(() => {
      captureHandler();
    }, 5000); // Adjust the interval as needed (in milliseconds)

    // Cleanup the interval on component unmount
    return () => clearInterval(intervalId);
  }, [capturing]);

  return (
    <div>
      {capturing && <Webcam audio={false} ref={webcamRef} screenshotFormat="image/jpeg" />}
      {!capturing && <button onClick={startCapturing}>Start Capturing</button>}
      {capturing && <button onClick={stopCapturing}>Stop Capturing</button>}
    </div>
  );
};

export default Kamera;