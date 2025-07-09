import React, { useState } from 'react';

const PlanetRight = () => {
  const [hovered, setHovered] = useState(false);
  // 6s is normal, so faster is 6s / 1.65 ≈ 3.64s
  // 4s is normal, so faster is 4s / 1.65 ≈ 2.42s
  const floatDuration = hovered ? '3.64s' : '6s';
  const spinDuration = hovered ? '2.42s' : '4s';
  return (
    <div
      style={{
        position: 'absolute',
        right: '-231px',
        top: '50%',
        transform: 'translateY(-50%)',
        width: '112px',
        height: '112px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1,
        pointerEvents: 'auto', // allow hover
      }}
      aria-hidden="true"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {/* Blurry gradient background for planet */}
      <div
        className="w-24 h-24 md:w-28 md:h-28 rounded-full blur-md"
        style={{
          position: 'absolute',
          left: 0,
          top: 0,
          zIndex: 1,
          animation: `floatOnly ${floatDuration} ease-in-out infinite`,
          background: 'linear-gradient(180deg, #A82D1A 16%, #E24228 34%, #E77140 60%, #EB864E 70%, #EF9858 85%)',
          opacity: 0.6,
        }}
      />
      {/* Single planet */}
      <div
        className="w-16 h-16 md:w-20 md:h-20 rounded-full opacity-90 relative overflow-hidden"
        style={{
          zIndex: 2,
          animation: `floatOnly ${floatDuration} ease-in-out infinite`,
          background: 'linear-gradient(180deg, #E24228 0%, #E77140 100%)',
          opacity: 0.7,
        }}
      >
        {/* Horizontal strip */}
        <div
          className="absolute inset-0 rounded-full"
          style={{
            background:
              'linear-gradient(0deg, transparent 20%, rgba(255,255,255,0.2) 35%, rgba(255,255,255,0.1) 45%, rgba(255,255,255,0.2) 55%, transparent 70%)',
            animation: `spin ${spinDuration} linear infinite`,
          }}
        />
        {/* Surface spots */}
        <div
          className="absolute w-2 h-2 rounded-full opacity-60"
          style={{
            top: '20%',
            left: '30%',
            background: '#A82D1A',
            animation: `spin ${spinDuration} linear infinite`,
          }}
        />
        <div
          className="absolute w-1 h-1 rounded-full opacity-80"
          style={{
            bottom: '30%',
            right: '25%',
            background: '#E77140',
            animation: `spin ${spinDuration} linear infinite`,
          }}
        />
      </div>
    </div>
  );
};

export default PlanetRight; 