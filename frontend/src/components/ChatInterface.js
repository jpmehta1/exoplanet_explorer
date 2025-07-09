import React, { useRef, useEffect } from 'react';

const ChatBubble = ({ message, isUser }) => (
  <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-2`}>
    <div
      className={`max-w-[80%] px-4 py-2 rounded-2xl shadow-md text-sm font-orbitron ${
        isUser
          ? 'bg-gradient-to-br from-orange-400 via-amber-500 to-yellow-500 text-white self-end neon-glow-orange-bubble'
          : 'bg-gradient-to-br from-cyan-400 via-blue-500 to-indigo-600 text-white self-start neon-glow-cyan-bubble'
      }`}
      style={{
        borderBottomRightRadius: isUser ? '0.5rem' : '1.5rem',
        borderBottomLeftRadius: isUser ? '1.5rem' : '0.5rem',
      }}
    >
      {message}
    </div>
  </div>
);

const TypingIndicator = () => (
  <div className="flex items-center space-x-1 mb-2 ml-2">
    <span className="dot bg-cyan-300" />
    <span className="dot bg-cyan-300" />
    <span className="dot bg-cyan-300" />
    <style>{`
      .dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 4px;
        animation: blink 1.4s infinite both;
      }
      .dot:nth-child(2) { animation-delay: 0.2s; }
      .dot:nth-child(3) { animation-delay: 0.4s; }
      @keyframes blink {
        0%, 80%, 100% { opacity: 0.3; }
        40% { opacity: 1; }
      }
    `}</style>
  </div>
);

const ChatInterface = ({
  query,
  setQuery,
  error,
  isLoading,
  onSubmit,
  onKeyPress,
  onReset,
  chatHistory = [], // [{ sender: 'user'|'bot', message: string }]
}) => {
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatHistory, isLoading]);

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex-1 mb-3 md:mb-4 overflow-y-auto rounded-3xl backdrop-blur-md bg-black bg-opacity-90 border border-cyan-400 neon-glow-cyan p-3 text-white" style={{ boxShadow: '0 0 16px 2px #22d3ee55', minHeight: '260px', maxHeight: '400px' }}>
        {error ? (
          <ChatBubble message={error} isUser={false} />
        ) : chatHistory.length > 0 ? (
          chatHistory.map((msg, idx) => (
            <ChatBubble key={idx} message={msg.message} isUser={msg.sender === 'user'} />
          ))
        ) : (
          <ChatBubble message="Ask me anything about exoplanets..." isUser={false} />
        )}
        {isLoading && <TypingIndicator />}
        <div ref={chatEndRef} />
      </div>
      <div className="space-y-3 mt-2">
        <div className="flex items-end space-x-2">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={onKeyPress}
            placeholder="What would you like to know?"
            className="flex-1 bg-black bg-opacity-90 text-white placeholder-white text-sm p-3 rounded-full resize-none focus:outline-none focus:ring-2 focus:ring-cyan-300 font-orbitron neon-glow-cyan"
            style={{ minHeight: '40px', maxHeight: '80px', boxShadow: '0 0 8px 1px #22d3ee55' }}
            rows="2"
            disabled={isLoading}
            aria-label="Enter your question about exoplanets"
          />
          <button
            onClick={onSubmit}
            disabled={isLoading || !query.trim()}
            className="bg-orange-500 bg-opacity-80 hover:bg-opacity-100 disabled:bg-opacity-30 text-black px-4 py-2 rounded-full font-orbitron neon-glow-orange focus:outline-none focus:ring-2 focus:ring-orange-300 focus:ring-offset-2 transition-all duration-200"
            aria-label={isLoading ? 'Exploring exoplanet data...' : 'Submit question about exoplanets'}
            style={{ boxShadow: '0 0 8px 1px #f59e0b55', marginTop: '-16px' }}
          >
            {isLoading ? '...' : 'Send'}
          </button>
        </div>
        <div className="w-full flex justify-center">
          <button
            onClick={onReset}
            className="bg-black text-white py-1 text-xs rounded-lg transition-all duration-300 font-orbitron focus:outline-none focus:ring-2 focus:ring-purple-300 focus:ring-offset-2 max-w-xs w-40"
            aria-label="Return to welcome screen"
          >
            BACK TO START
          </button>
        </div>
      </div>
      <style>{`
        .neon-glow-cyan {
          box-shadow: 0 0 8px 2px #22d3ee88, 0 0 2px 1px #67e8f9;
        }
        .neon-glow-orange {
          box-shadow: 0 0 8px 2px #f59e0b88, 0 0 2px 1px #fbbf24;
        }
        .neon-glow-cyan-bubble {
          box-shadow: 0 0 8px 2px #38bdf8cc, 0 0 2px 1px #6366f1;
        }
        .neon-glow-orange-bubble {
          box-shadow: 0 0 8px 2px #fbbf24cc, 0 0 2px 1px #f59e0b;
        }
      `}</style>
    </div>
  );
};
export default ChatInterface; 