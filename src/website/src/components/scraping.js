import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import './styles.css';

const Scraping = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('url', url);

      const response = await axios.post('http://localhost:3005/scrape', formData);
        console.log(response.data);
        toast.success('Scraping process completed!');
    } catch (error) {
        console.error('Error scraping data', error);
        toast.error('Error during scraping :(');
    } finally {
        setLoading(false);
        setUrl('');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '20vh' }}>
      <div>
        <h1 className='scrape-title'>Image Scraping</h1>
        <form onSubmit={handleSubmit}>
        <input
          placeholder='Enter URL...'
          className="custom-file-input" 
          style={{ fontFamily: 'Comic Sans MS, cursive'}}
          type="text" 
          value={url} 
          onChange={(e) => setUrl(e.target.value)} required />
          <button 
          className="search-button"
          style={{ fontFamily: 'Comic Sans MS, cursive'}}
          type="submit"> {loading ? 'Scraping...' : 'Scrape'} </button>
        </form>
      </div>
    </div>
  );
}

export default Scraping;