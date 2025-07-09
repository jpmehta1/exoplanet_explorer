import React, { useMemo } from 'react';

const StarField = () => {
  // Memoize star generation to prevent recreation on every render
  const stars = useMemo(() => {
    return [...Array(250)].map((_, i) => ({
      id: i,
      left: Math.random() * 100,
      top: Math.random() * 100,
      width: 2 + Math.random() * 3,
      height: 2 + Math.random() * 3,
      pulseDelay: Math.random() * 3,
      pulseDuration: 2 + Math.random() * 4,
      blinkDelay: Math.random() * 4,
      blinkDuration: 1 + Math.random() * 1.2,
    }));
  }, []);

  return (
    <div className="absolute inset-0" aria-hidden="true">
      {stars.map((star) => (
        <div
          key={star.id}
          className="absolute bg-white rounded-full animate-pulse star-blink"
          style={{
            left: `${star.left}%`,
            top: `${star.top}%`,
            width: `${star.width}px`,
            height: `${star.height}px`,
            animationName: 'pulse, blinkStar',
            animationDelay: `${star.pulseDelay}s, ${star.blinkDelay}s`,
            animationDuration: `${star.pulseDuration}s, ${star.blinkDuration}s`,
            animationIterationCount: 'infinite, infinite',
            animationTimingFunction: 'ease-in-out, ease-in-out',
            filter: 'brightness(1.2)',
            opacity: 1,
          }}
        />
      ))}
    </div>
  );
};

export default StarField; 