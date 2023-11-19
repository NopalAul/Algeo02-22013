import React, { useState, useRef, useEffect } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import './styles.css';

const Kamera = ({onStopCapture}) => {
  const webcamRef = useRef(null);
  const [image, setImage] = useState(null);
  const [capturing, setCapturing] = useState(false);
  const [isCaptured, setIsCaptured] = useState(false);

  const handleCamClick = () => {
    setCapturing(false);
    setIsCaptured(true);
    onStopCapture(true);
  }
  
  const captureHandler = async () => {
    if (webcamRef.current) {
        const imageSrc = webcamRef.current.getScreenshot();
        setImage(imageSrc);

        const blob = await fetch(imageSrc).then((res) => res.blob());

        const formData = new FormData();
        formData.append('image', blob, 'captured_image.jpg');

        try {
        await axios.post('http://localhost:3005/camera', formData);
        } catch (error) {
        console.error('Error sending image to the server:', error);
        }
    }
  };

  const startCapturing = () => {
    setCapturing(true);
  };

  useEffect(() => {
    const intervalId = setInterval(() => {
      captureHandler();
    }, 5000);

    return () => clearInterval(intervalId);
  }, [capturing]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '20vh' }}>
      <div>
        {isCaptured && image && <img src={image} alt="Captured" />}
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '10vh', marginTop: '10px' }}>
        {capturing && <Webcam audio={false} ref={webcamRef} screenshotFormat="image/jpeg" width={300} height={180} marginHeight={50} />}
        {!capturing && <button className="cam-button" onClick={startCapturing}>Start Capturing</button>}
        {capturing && <button className="cam-button" onClick={handleCamClick}>Stop Capturing</button>}
      </div>
    </div>
  );
};

export default Kamera;