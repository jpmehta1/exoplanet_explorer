import React from 'react';

const Title = () => {
  return (
    <div className="absolute top-4 sm:top-8 md:top-12 left-1/2 transform -translate-x-1/2 px-4 z-20">
      <h1 
        className="text-lg sm:text-xl md:text-2xl lg:text-3xl xl:text-4xl tracking-widest text-center font-orbitron"
        style={{ color: '#F3F4F6', fontFamily: 'Digital Numbers, monospace' }}
      >
        EXOPLANET EXPLORER
      </h1>
    </div>
  );
};

export default Title; 