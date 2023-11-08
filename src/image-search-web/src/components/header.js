import React from 'react';
import './styles.css';

const Header = ({ children }) => {
    return (
        <div className="bg-gray-100 flex items-center py-12">
            <div className='max-w-md mx-auto w-full'>
                <h1 className='text-rose-950 text-center text-5xl font-bold mb-5'>REVERSE IMAGE SEARCH</h1>
                {children}
            </div>
        </div>
    )
}

export default Header