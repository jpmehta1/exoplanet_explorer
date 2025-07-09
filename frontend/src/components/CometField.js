import React, { useMemo } from 'react';

const getRandom = (min, max) => Math.random() * (max - min) + min;

const CometField = () => {
  // Generate 2 comets with random properties
  const comets = useMemo(() => {
    return Array.from({ length: 2 }).map((_, i) => {
      const angle = getRandom(-30, 30);
      const duration = getRandom(3.5, 6); // seconds
      const delay = getRandom(0, 4); // seconds
      const startY = getRandom(10, 80); // vh
      const startX = getRandom(-10, 10); // vw offset
      return {
        id: i,
        angle,
        duration,
        delay,
        startY,
        startX,
      };
    });
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none" aria-hidden="true" style={{ zIndex: 5 }}>
      {comets.map((comet) => (
        <div
          key={comet.id}
          style={{
            position: 'absolute',
            left: `calc(${comet.startX}vw)`,
            top: `calc(${comet.startY}vh)`,
            width: '120px',
            height: '8px',
            transform: `rotate(${comet.angle}deg)`,
            overflow: 'visible',
            pointerEvents: 'none',
            zIndex: 5,
            animation: `cometFly ${comet.duration}s linear ${comet.delay}s infinite`,
          }}
        >
          {/* Tail */}
          <div
            style={{
              position: 'absolute',
              left: 0,
              top: '50%',
              width: '100px',
              height: '4px',
              background: 'linear-gradient(90deg, rgba(0,212,255,0.0) 0%, rgba(0,212,255,0.5) 60%, rgba(255,255,255,0.8) 100%)',
              filter: 'blur(2px)',
              borderRadius: '2px',
              transform: 'translateY(-50%)',
            }}
          />
          {/* Head */}
          <div
            style={{
              position: 'absolute',
              left: '100px',
              top: '50%',
              width: '16px',
              height: '16px',
              background: 'radial-gradient(circle, #fff 60%, #00d4ff 100%)',
              boxShadow: '0 0 16px 8px #00d4ff88',
              borderRadius: '50%',
              transform: 'translateY(-50%)',
              opacity: 0.95,
            }}
          />
        </div>
      ))}
    </div>
  );
};

export default CometField; 