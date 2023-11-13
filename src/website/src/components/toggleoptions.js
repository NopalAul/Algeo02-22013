import React, { useState } from "react";
import "./styles.css";

const ToggleOptions = ({ onOptionChange }) => {
  const [selectedOption, setSelectedOption] = useState(null);

  const handleOptionChange = (option) => {
    setSelectedOption(option);
    onOptionChange(option);
  };

  return (
    <div className="toggle-options">
      <button
        className={`toggle-button ${selectedOption === "texture" ? "active" : ""}`}
        onClick={() => handleOptionChange("texture")}
      >
        Texture
      </button>
      <button
        className={`toggle-button ${selectedOption === "color" ? "active" : ""}`}
        onClick={() => handleOptionChange("color")}
      >
        Color
      </button>
    </div>
  );
};

export default ToggleOptions;
