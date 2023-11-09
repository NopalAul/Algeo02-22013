import React from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';
import nobita from './rsc/button_nobi.png';

const NobiButton = ({ onClick }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate('/nobi-button-page');
        onClick(); // call on click
    };

    return (
        <button className="custom-button-2" onClick={handleClick}>
            <img src={nobita} alt="Button 1" />
        </button>
    );
}

export default NobiButton;
