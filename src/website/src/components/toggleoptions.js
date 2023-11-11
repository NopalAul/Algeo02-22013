import React, { useState } from "react";
import './styles.css';

const ToggleOptions = ({ onOptionChange }) => {
  const [selectedOption, setSelectedOption] = useState("texture");

  const handleOptionChange = (option) => {
    setSelectedOption(option);
    onOptionChange(option);
  };

  return (
    <div className="toggle-options">
      <button
        className={selectedOption === "texture" ? "active" : ""}
        onClick={() => handleOptionChange("texture")}
      >
        Texture
      </button>
      <button
        className={selectedOption === "color" ? "active" : ""}
        onClick={() => handleOptionChange("color")}
      >
        Color
      </button>
    </div>
  );
};

export default ToggleOptions;