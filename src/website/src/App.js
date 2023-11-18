import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import React, { useState } from 'react';
import Header from "./components/header";
import Dataset from "./components/dataset";
import DoraButtonPage from "./components/dora-button-page";
import NobiButtonPage from "./components/nobi-button-page";
import Images from "./components/images";
import Search from "./components/search";
import Scraping from "./components/scraping";

function App() {
  const handleButtonClick = () => {
    console.log('Button clicked');
  }

  const [searchCompleted, setSearchCompleted] = useState(false);

  const handleSearchComplete = () => {
    setSearchCompleted(true);
  };

  return (
    <Router>
      <Routes>
        <Route 
          path="/" 
          element={
            <div>
              <Header onButtonClick={handleButtonClick}>
                <Search onSearchComplete={handleSearchComplete} />
                <Dataset />
                <Scraping />
              </Header>
              {searchCompleted && <Images />}
            </div>
          }
        />
        <Route path="/buttonpage" element={<DoraButtonPage />} />
        <Route path="/nobi-button-page" element={<NobiButtonPage />} />
      </Routes>
    </Router>
  );
}

export default App;