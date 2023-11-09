import React from 'react';
import './styles.css';
import nobita from './rsc/button_nobi.png';

const CustomButton2 = ({ onClick }) => {
  return (
    <button className="custom-button-2" onClick={onClick}>
      <img src={nobita} alt="Button 1" />
    </button>
  );
}

export default CustomButton2;