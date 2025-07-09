// Environment configuration
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// API timeout in milliseconds
export const API_TIMEOUT = 30000;

// Error message mapping
export const ERROR_MESSAGES = {
  TIMEOUT: 'Request timed out. Please try again.',
  NETWORK_ERROR: 'Network error. Please check your connection.',
  SERVER_ERROR: 'Server error. Please try again later.',
  NOT_FOUND: 'Service temporarily unavailable. Please try again later.',
  UNKNOWN: 'Something went wrong. Please try again.',
};

// User-friendly error handler
export const handleApiError = (error) => {
  console.error('API Error:', error);
  
  if (error.name === 'AbortError') {
    return ERROR_MESSAGES.TIMEOUT;
  }
  
  if (error.name === 'TypeError' && error.message.includes('fetch')) {
    return ERROR_MESSAGES.NETWORK_ERROR;
  }
  
  if (error.status === 404) {
    return ERROR_MESSAGES.NOT_FOUND;
  }
  
  if (error.status >= 500) {
    return ERROR_MESSAGES.SERVER_ERROR;
  }
  
  return ERROR_MESSAGES.UNKNOWN;
};

// API request wrapper with timeout
export const apiRequest = async (endpoint, options = {}) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);
  
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      const error = new Error(`HTTP error! status: ${response.status}`);
      error.status = response.status;
      throw error;
    }
    
    return await response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    throw error;
  }
};

// Specific API functions
export const askQuestion = async (query) => {
  return apiRequest('/ask', {
    method: 'POST',
    body: JSON.stringify({ query: query.trim() }),
  });
}; 

// Streaming API function for /ask endpoint
export const askQuestionStream = async (query, onChunk) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

  try {
    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: 'POST',
      body: JSON.stringify({ query: query.trim() }),
      headers: { 'Content-Type': 'application/json' },
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    if (!response.ok) {
      const error = new Error(`HTTP error! status: ${response.status}`);
      error.status = response.status;
      throw error;
    }
    // Stream the response
    const reader = response.body.getReader();
    let fullText = '';
    let decoder = new TextDecoder();
    let done = false;
    while (!done) {
      const { value, done: doneReading } = await reader.read();
      if (value) {
        let chunk = decoder.decode(value, { stream: true });
        // Try to parse JSON lines (backend streams JSON objects per line)
        chunk.split(/\r?\n/).forEach(line => {
          if (line.trim()) {
            try {
              const obj = JSON.parse(line);
              if (obj.response) {
                // Filter out <think>...</think> or 'thought process' sections
                let filtered = obj.response.replace(/<think>[\s\S]*?<\/think>/gi, '').replace(/\n{2,}/g, '\n').trim();
                if (filtered) {
                  onChunk(filtered);
                  fullText += filtered;
                }
              }
            } catch (e) {
              // Not a JSON line, ignore
            }
          }
        });
      }
      done = doneReading;
    }
    return fullText;
  } catch (error) {
    clearTimeout(timeoutId);
    throw error;
  }
}; 