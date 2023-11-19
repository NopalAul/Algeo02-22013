import React, { useState, useRef, useEffect } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import './styles.css';

const Kamera = () => {
  const webcamRef = useRef(null);
  const [image, setImage] = useState(null);
  const [capturing, setCapturing] = useState(false);
  const [isCaptured, setIsCaptured] = useState(false);

  const captureHandler = async () => {
    if (webcamRef.current) {
        const imageSrc = webcamRef.current.getScreenshot();
        setImage(imageSrc);

        // convert the image to a blob
        const blob = await fetch(imageSrc).then((res) => res.blob());

        // create form dataa and append the image blob
        const formData = new FormData();
        formData.append('image', blob, 'captured_image.jpg');

        // send image to the backend
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

  const handleClick = () => {
    setCapturing(false);
    setIsCaptured(true);
  };

  // const stopCapturing = () => {
  //   setCapturing(false);
  // };

  // auto-capture at a certain interval (e.g., every 10 seconds)
  useEffect(() => {
    const intervalId = setInterval(() => {
      captureHandler();
    }, 5000); // adjust the interval as needed (in milliseconds)

    // cleanup the interval on component unmount
    return () => clearInterval(intervalId);
  }, [capturing]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '20vh' }}>
        <div>
            <h1 className='scrape-title'>Camera</h1>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '20vh', marginTop: '50px'}}>
            {capturing && <Webcam audio={false} ref={webcamRef} screenshotFormat="image/jpeg" width={300} height={180} marginHeight={50}/>}
            {!capturing && <button className="cam-button" onClick={startCapturing}>Start Capturing</button>}
            {capturing && <button className="cam-button" onClick={handleClick}>Stop Capturing</button>}
        </div>
    </div>
  );
};

export default Kamera;