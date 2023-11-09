import React from 'react';
import DoraButton from './dora-button';
import NobiButton from './nobi-button';
import './styles.css';
import text from './rsc/text.png'; 

const Header = ({ children, onButtonClick }) => {
    return (
        <div className='bg-sky-300 flex items-center py-12 relative'>
            <DoraButton onClick={() => onButtonClick("buttonpage")} />
            <NobiButton onClick={() => onButtonClick("nobibuttonpage")} />
            <div className='max-w-md mx-auto w-full' style={{ maxWidth: '700px', width: '80%' }}>
                <h1 className='text-sky-700 text-center text-5xl font-bold mb-5' style={{ fontFamily: 'Comic Sans MS, cursive', textShadow: '4px 4px 8px white', letterSpacing: '2px' }}>REVERSE IMAGE SEARCH</h1>
                <img src={text} alt="doraemon text" style={{ width: '300px', height: 'auto', margin: '0 auto' }}/>
                {children}
            </div>
        </div>
    );
}

export default Header;
