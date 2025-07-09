import React from 'react';

const WelcomeScreen = ({ onStartExploring }) => {
  return (
    <div className="text-center space-y-4 md:space-y-6">
      <div className="welcome-glow-border mb-3 md:mb-4" style={{ position: 'relative', display: 'inline-block' }}>
        <div className="rounded-lg p-3 md:p-4" style={{ background: 'rgba(26,26,26,0.85)', position: 'relative', zIndex: 2, minWidth: 220 }}>
          <p 
            className="text-white text-xs md:text-sm leading-relaxed font-orbitron font-semibold drop-shadow-lg"
            style={{fontFamily: 'Digital Numbers, monospace', letterSpacing: '0.02em', textShadow: '0 1px 8px #000, 0 0px 2px #fff8'}}
          >
            HELLO FELLOW EXPLORER! WHAT PART OF THE EXOPLANET ARCHIVE DO YOU WANT TO EXPLORE?
          </p>
        </div>
      </div>
      
      <button
        onClick={onStartExploring}
        className="peach-glow-btn px-4 md:px-6 py-2 md:py-3 rounded-lg transition-all duration-300 transform hover:scale-105 text-xs md:text-sm font-orbitron font-bold focus:outline-none focus:ring-2 focus:ring-orange-200 focus:ring-offset-2"
        style={{
          fontFamily: 'Digital Numbers, monospace',
          background: 'rgba(255,209,179,0.45)',
          color: '#111',
          boxShadow: '0 0 16px 3px #FFD1B3cc',
          fontWeight: 700,
        }}
        aria-label="Start exploring exoplanet data"
      >
        START TYPING
      </button>
      <style>{`
        .welcome-glow-border {
          position: relative;
          display: inline-block;
        }
        .welcome-glow-border::before {
          content: '';
          position: absolute;
          inset: -2px;
          border-radius: 0.6rem;
          z-index: 1;
          pointer-events: none;
          background: linear-gradient(270deg, #FFD1B3, #1A1A1A, #FFD1B3);
          background-size: 200% 200%;
          animation: borderGlowAnim 3s linear infinite;
          box-shadow: 0 0 32px 8px #FFD1B3, 0 0 16px 4px #FFD1B399;
          filter: blur(1.5px);
        }
        .peach-glow-btn {
          background: rgba(255,209,179,0.45) !important;
          color: #111 !important;
          font-weight: 700 !important;
          box-shadow: 0 0 16px 3px #FFD1B3cc;
        }
        .peach-glow-btn:hover {
          background: rgba(255,209,179,0.65) !important;
        }
        @keyframes borderGlowAnim {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
      `}</style>
    </div>
  );
};

export default WelcomeScreen; 