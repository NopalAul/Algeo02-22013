import React from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';
import doraemon from './rsc/button_dora.png';

const DoraButton = ({ onClick }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate('/buttonpage');
        onClick();
    };

    return (
        <button className="custom-button text-sky-800" onClick={handleClick}>
            <img src={doraemon} alt="Button 1" />
            About us
        </button>
    );
}

export default DoraButton;