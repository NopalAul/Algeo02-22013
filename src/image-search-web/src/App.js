import React, { createContext, useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/header";
import SearchField from "./components/searchfield";
import Images from "./components/images";
import useAxios from "./hooks/useAxios";
import ToggleOptions from "./components/toggleoptions";
import ImagePreview from "./components/imagepreview";
import DoraButtonPage from "./components/dora-button-page";
import NobiButtonPage from "./components/nobi-button-page";

export const ImageContext = createContext();

function App() {
  const [searchImage, setSearchImage] = useState("");
  const { response, isLoading, error, fetchData } = useAxios(
    `search/photos?page=1&query=cats&client_id=${process.env.REACT_APP_ACCESS_KEY}`
  );
  const [selectedOption, setSelectedOption] = useState("texture");
  const [uploadedImage, setUploadedImage] = useState(null);

  const handleOptionChange = (option) => {
    setSelectedOption(option);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setUploadedImage(file);
  };

  const handleButtonClick = () => {
    console.log('Button clicked');
  }

  const value = {
    response,
    isLoading,
    error,
    fetchData,
    searchImage,
    setSearchImage,
  };

  return (
    <Router>
      <ImageContext.Provider value={value}>
        <Routes>
          <Route path="/" element={<Header onButtonClick={handleButtonClick}>
            <ToggleOptions onOptionChange={handleOptionChange} />
            <SearchField selectedOption={selectedOption} handleFileChange={handleFileChange}/>
          </Header>}>
            <Route index element={<>
              <ImagePreview uploadedImage={uploadedImage} />
              <Images />
            </>} />
          </Route>
          <Route path="/buttonpage" element={<DoraButtonPage />} />
          <Route path="/nobi-button-page" element={<NobiButtonPage />} />
        </Routes>
      </ImageContext.Provider>
    </Router>
  );
}

export default App;
