import React from 'react';

const Attribution = () => {
  return (
    <div className="absolute bottom-2 sm:bottom-4 left-1/2 transform -translate-x-1/2 px-4 z-20">
      <button
        className="attribution-glow-btn text-red-300 text-xs sm:text-sm tracking-wide font-orbitron px-3 md:px-4 py-1 md:py-2 rounded-lg border-2 border-red-500 bg-red-900 bg-opacity-50 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-red-300 focus:ring-offset-2"
        style={{ boxShadow: '0 0 16px 3px #7f1d1dcc, 0 0 8px 2px #ef444488' }}
        tabIndex={0}
        type="button"
        aria-label="Astrothunder attribution"
      >
        PLAY ASTROTHUNDER BY TRAVIS SCOTT
      </button>
      <style>{`
        .attribution-glow-btn {
          background: rgba(127,29,29,0.5) !important;
          color: #fca5a5 !important;
          font-weight: 700 !important;
          box-shadow: 0 0 16px 3px #7f1d1dcc, 0 0 8px 2px #ef444488;
        }
        .attribution-glow-btn:hover, .attribution-glow-btn:focus {
          background: rgba(127,29,29,0.7) !important;
          color: #fff1f2 !important;
          box-shadow: 0 0 32px 8px #ef4444cc, 0 0 16px 4px #7f1d1d99;
          transform: scale(1.05);
        }
      `}</style>
    </div>
  );
};

export default Attribution; 