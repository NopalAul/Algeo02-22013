// src/App.js
import React, { useState } from 'react';
import axios from 'axios';

const Scraping = () => {
  const [url, setUrl] = useState(null);
  const [imageUrls, setImageUrls] = useState([]);

  const handleSubmit = () => {
    const formData = new FormData();
    formData.append('url', url);

    axios.post('http://localhost:3005/scrape', formData)
  };
  // const handleSubmit = async (e) => {
  //   e.preventDefault();

  //   try {
  //     const response = await axios.post('http://localhost:3005/scrape', { url });
  //     setImageUrls(response.data.image_urls);
  //   } catch (error) {
  //     console.error('Error:', error.message);
  //   }
  // };

  return (
    <div>
      <h1>Image Scraping with React</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Enter URL:
          <input type="text" value={url} onChange={(e) => setUrl(e.target.value)} required />
        </label>
        <button type="submit">Scrape</button>
      </form>

      {/* {imageUrls.length > 0 && (
        <div>
          <h2>Scraped Images</h2>
          {imageUrls.map((imageUrl, index) => (
            <img key={index} src={imageUrl} alt={`Scraped Image ${index}`} />
          ))}
        </div>
      )} */}
    </div>
  );
}

export default Scraping;