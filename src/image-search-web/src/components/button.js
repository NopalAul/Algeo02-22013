import React from 'react';
import './styles.css';
import doraemon from './rsc/button_dora.png';

const CustomButton = ({ onClick }) => {
  return (
    <button className="custom-button" onClick={onClick}>
      <img src={doraemon} alt="Button 1" />
    </button>
  );
}

export default CustomButton;