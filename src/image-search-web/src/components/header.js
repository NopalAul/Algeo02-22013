import React from 'react';
import CustomButton from './button';
import CustomButton2 from './button2';
import './styles.css';
import text from './rsc/text.png'; 

const Header = ({ children, onButtonClick }) => {
  return (
    <div className='bg-sky-300 flex items-center py-12 relative'>
      <CustomButton onClick={onButtonClick} />
      <CustomButton2 onClick={onButtonClick} />
      <div className='max-w-md mx-auto w-full' style={{ maxWidth: '700px', width: '80%' }}>
        <h1 className='text-sky-700 text-center text-5xl font-bold mb-5' style={{ fontFamily: 'Comic Sans MS, cursive', textShadow: '4px 4px 8px white' }}>REVERSE IMAGE SEARCH</h1>
        <img src={text} alt="doraemon text" style={{ width: '300px', height: 'auto', margin: '0 auto' }}/>
        {children}
      </div>
    </div>
  );
}

export default Header;
