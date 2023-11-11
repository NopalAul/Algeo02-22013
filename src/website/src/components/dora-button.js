import React from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';
import doraemon from './rsc/button_dora.png';

const DoraButton = ({ onClick }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate('/buttonpage');
        onClick(); // Call the onClick function passed as prop
    };

    return (
        <button className="custom-button" onClick={handleClick}>
            <img src={doraemon} alt="Button 1" />
        </button>
    );
}

export default DoraButton;