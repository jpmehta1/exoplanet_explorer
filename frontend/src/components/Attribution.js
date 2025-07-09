import React from 'react';

const Attribution = () => {
  return (
    <div className="absolute bottom-2 sm:bottom-4 left-1/2 transform -translate-x-1/2 px-4 z-20">
      <div className="border-2 border-red-500 bg-red-900 bg-opacity-50 px-3 md:px-4 py-1 md:py-2 rounded-lg">
        <p 
          className="text-red-300 text-xs sm:text-sm tracking-wide font-orbitron"
          style={{fontFamily: 'Digital Numbers, monospace'}}
        >
          PLAY ASTROTHUNDER BY TRAVIS SCOTT
        </p>
      </div>
    </div>
  );
};

export default Attribution; 