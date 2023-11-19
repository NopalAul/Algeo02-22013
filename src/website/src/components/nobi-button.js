import React from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';
import nobita from './rsc/button_nobi.png';

const NobiButton = ({ onClick }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate('/nobi-button-page');
        onClick();
    };

    return (
        <button className="custom-button-2 text-sky-800" onClick={handleClick}>
            <img src={nobita} alt="Button 1" />
            How to Use
        </button>
    );
}

export default NobiButton;
