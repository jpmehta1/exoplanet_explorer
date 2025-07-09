import React, { useState } from 'react';
import StarField from './components/StarField';
import Planet from './components/Planet';
import PlanetRight from './components/PlanetRight';
import ChatInterface from './components/ChatInterface';
import WelcomeScreen from './components/WelcomeScreen';
import Title from './components/Title';
import Attribution from './components/Attribution';
import { askQuestion, handleApiError } from './utils/api';
import CometField from './components/CometField';
import SplashCursor from './components/SplashCursor';
import Aurora from './components/Aurora';

function App() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showInput, setShowInput] = useState(false);
  const [error, setError] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleSubmit = async () => {
    if (!query.trim()) return;
    setIsLoading(true);
    setError('');
    // Add user message
    setChatHistory((prev) => [...prev, { sender: 'user', message: query }]);
    setQuery(''); // Clear the input field right after submitting
    try {
      const data = await askQuestion(query);
      setChatHistory((prev) => [...prev, { sender: 'bot', message: data || 'No response received' }]);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const startExploring = () => {
    setShowInput(true);
    setError('');
    setChatHistory([]);
  };

  const resetToStart = () => {
    setShowInput(false);
    setQuery('');
    setChatHistory([]);
    setError('');
  };

  // Attach streaming API to window for use in handleSubmit
  React.useEffect(() => {
    import('./utils/api').then((mod) => {
      window.askQuestionStream = mod.askQuestionStream;
      window.handleApiError = mod.handleApiError;
    });
  }, []);

  return (
    <div className="min-h-screen relative overflow-hidden bg-black">
      <div style={{ position: 'absolute', top: 0, left: 0, width: '100vw', height: 'auto', zIndex: 50, opacity: 0.35, pointerEvents: 'none' }}>
        <Aurora />
      </div>
      <CometField />
      <StarField />
      <div style={{ position: 'absolute', top: '1.5rem', left: 0, width: '100vw', zIndex: 60 }}>
        <Title />
      </div>
      {/* Central orbital system */}
      <div className="absolute inset-0 flex items-center justify-center z-10" style={{marginLeft: '-40px'}}>
        <div className="relative w-96 h-96 md:w-[600px] md:h-[600px]">
          <div className="absolute inset-0 flex items-center justify-center">
            {/* Oval orbital gradient */}
            <div
              className="absolute bg-gradient-to-r from-blue-500 to-red-500 opacity-50 blur-2xl"
              style={{
                width: '500px',
                height: '450px',
                borderRadius: '50%',
                transform: 'scaleX(1.8)',
              }}
              aria-hidden="true"
            />
            {/* Left planet */}
            <Planet />
            {/* Right planet */}
            <PlanetRight />
            {/* Central planet background (scaled up) */}
            <div className="absolute inset-0 flex items-center justify-center z-10">
              <div className="w-[384px] h-[384px] md:w-[460.8px] md:h-[460.8px] rounded-full bg-gray-300 opacity-50" />
            </div>
            {/* Central chat interface (original size, centered, shifted upward) */}
            <div className="relative w-80 h-80 md:w-96 md:h-96 flex flex-col items-center justify-center p-6 md:p-8 z-20" style={{ marginTop: '-24px' }}>
              {!showInput ? (
                <WelcomeScreen onStartExploring={startExploring} />
              ) : (
                <ChatInterface
                  query={query}
                  setQuery={setQuery}
                  error={error}
                  isLoading={isLoading}
                  onSubmit={handleSubmit}
                  onKeyPress={handleKeyPress}
                  onReset={resetToStart}
                  chatHistory={chatHistory}
                />
              )}
            </div>
          </div>
        </div>
      </div>
      <Attribution />
    </div>
  );
}

export default App;