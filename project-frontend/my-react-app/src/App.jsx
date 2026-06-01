import React, { useState, useRef } from 'react';
import './App.css';


const NewsGuardian = () => {
  const [input, setInput] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const recognitionRef = useRef(null);
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm NewsGuardian. I can help you verify news credibility. You can either enter a news text or upload an image/screenshot of news content.",
      sender: 'bot'
    }
  ]);


  // 🎤 Start recording
const startRecording = () => {
  if (!('webkitSpeechRecognition' in window)) {
    alert("Speech Recognition not supported");
    return;
  }

  const recognition = new window.webkitSpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = true;

  recognition.onstart = () => setIsRecording(true);

  recognition.onresult = (event) => {
    let transcript = "";
    for (let i = 0; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript;
    }
    setInput(transcript);
  };

  recognition.onend = () => setIsRecording(false);
  recognition.onerror = () => setIsRecording(false);

  recognitionRef.current = recognition;
  recognition.start();
};

// 🛑 Stop recording
const stopRecording = () => {
  recognitionRef.current?.stop();
  setIsRecording(false);
};

// ❌ Clear voice
const clearVoice = () => {
  setInput('');
};



const handleSubmit = async (e) => {
  e.preventDefault();
  if (!input.trim() && !selectedImage) return;

 const userMessage = {
  id: Date.now(),
  text: input,
  sender: 'user',
  image: selectedImage
};

const loadingBotMessage = {
  id: Date.now() + 1,
  text: "Analyzing the content and verifying with trusted sources...",
  sender: 'bot'
};



  setMessages(prev => [...prev, userMessage, loadingBotMessage]);
  

  try {
    let res;

const formData = new FormData();

if (selectedImage) {
  formData.append("image", selectedImage);
}

if (input.trim()) {
  formData.append("query", input);
}

res = await fetch("http://127.0.0.1:8001/search", {
  method: "POST",
  body: formData
});

//  STEP 1: API ERROR CHECK
if (!res.ok) {
  throw new Error(`API Error: ${res.status}`);

}

  const data = await res.json();

   setInput('');
  setSelectedImage(null);

//  STEP 2: NULL / INVALID RESPONSE CHECK
if (!data || typeof data !== "object") {
  throw new Error("Invalid API response format");
}

const finalBotMessage = {
  id: Date.now() + 2,
  text: data.answer || "No clear conclusion found.",
  sender: 'bot',
  sources: data.sources || [],
  canExplain: data.sources && data.sources.length > 0
};



    setMessages(prev => {
  const filtered = prev.filter(msg => msg.text !== "Analyzing the content and verifying with trusted sources...");
  return [...filtered, finalBotMessage];
});

  } catch (error) {
    setMessages(prev => [
      ...prev.slice(0, -1),
      {
        id: messages.length + 3,
        text: "⚠️ Error contacting verification service.",
        sender: 'bot'
      }
    ]);
  }
};


  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      // Also auto-focus on input
      document.querySelector('.chat-input')?.focus();
    }
  };

  const clearImage = () => {
    setSelectedImage(null);
  };

  const requestExplanation = async (message) => {
  try {
    const loadingMessage = {
      id: Date.now(),
      text: "Generating detailed explanation using RAG...",
      sender: "bot"
    };

    setMessages(prev => [...prev, loadingMessage]);

    const res = await fetch("http://127.0.0.1:8001/explain", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        query: message.text,
        sources: message.sources || []
      })
    });

    if (!res.ok) {
      throw new Error("Explain API failed");
    }

    const data = await res.json();

    console.log("API RESPONSE:", data);

    setMessages(prev => [
      ...prev.slice(0, -1),
      {
        id: Date.now() + 1,
        text: data.explanation || "No explanation generated.",
        sender: "bot"
      }
    ]);

  } catch (error) {
    setMessages(prev => [
      ...prev.slice(0, -1),
      {
        id: Date.now() + 2,
        text: "⚠️ Error generating explanation.",
        sender: "bot"
      }
    ]);
  }
};

const explainSingleSource = async (query, source) => {
  try {

    const loadingMessage = {
      id: Date.now(),
      text: `Analyzing ${source.title}...`,
      sender: "bot"
    };

    setMessages(prev => [...prev, loadingMessage]);

    const res = await fetch("http://127.0.0.1:8001/explain", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        query: query,
        sources: [source]
      })
    });

    if (!res.ok) {
      throw new Error("Explain API failed");
    }

    const data = await res.json();

    setMessages(prev => [
      ...prev.slice(0, -1),
      {
  id: Date.now() + 1,
  text: data.explanation,
  sender: "bot",

  sourceDetails: {
    title: source.title,
    trust_score: source.trust_score,
    credibility_reason: source.credibility_reason,
    url: source.url
  }
}
    ]);

  } catch (error) {

    setMessages(prev => [
      ...prev.slice(0, -1),
      {
        id: Date.now() + 2,
        text: "⚠️ Error analyzing source.",
        sender: "bot"
      }
    ]);
  }
};


  return (
    <div className="news-guardian-container">
      {/* Header */}
      <div className="news-guardian-header">
        <div className="logo-section">
          <h1 className="logo-title">NewsGuardian</h1>
          <p className="logo-subtitle">Truth in an Age of Information</p>
        </div>
      </div>

      {/* Chat Container */}
      <div className="chat-container">
        {/* Messages Area */}
        <div className="messages-area">
          {messages.map((message) => (
            <div 
              key={message.id} 
              className={`message ${message.sender}-message`}
            >
              <div className="message-content">
                {message.sender === 'bot' && (
                  <div className="bot-avatar">NG</div>
                )}
                <div className="message-text">

  {message.sourceDetails ? (

    <div>

      <div className="credibility-card">

        <div className="credibility-header">
          🔍 {message.sourceDetails.title}
        </div>

        <div className="credibility-score">
          Trust Score: {message.sourceDetails.trust_score}%
        </div>

        <div className="credibility-reason">
          {message.sourceDetails.credibility_reason}
        </div>

        <a
          href={message.sourceDetails.url}
          target="_blank"
          rel="noopener noreferrer"
          className="credibility-link"
        >
          Visit Source
        </a>

      </div>

      <div className="source-explanation-box">
        {message.text}
      </div>

    </div>

  ) : (

    <div>
      {message.text}
    </div>

  )}

  {/* Show image if user uploaded */}
  {message.image && message.sender === 'user' && (
    <div className="image-preview">
      <span>📎 {message.image.name}</span>
    </div>
  )}

  {/* Show sources if backend sent them */}
  {message.sources && message.sources.length > 0 && (
    <div className="sources-section">
      <strong>Sources:</strong>
      <ul>
        {message.sources.map((source, index) => (
          <li key={index} className="source-item">

  <a
    href={source.url}
    target="_blank"
    rel="noopener noreferrer"
  >
    {source.title || source.url}
  </a>

  <button
    className="source-info-btn"
    onClick={() =>
      explainSingleSource(message.text, source)
    }
  >
    ⓘ
  </button>

</li>
        ))}
      </ul>
    </div>
  )}

  {/* Explain Button */}
{message.canExplain && (
  <div className="explain-section">
    <button
      className="explain-btn"
      onClick={() => requestExplanation(message)}
    >
      Explain using multiple sources (RAG)
    </button>
  </div>
)}

</div>

              </div>
            </div>
          ))}
        </div>

        {/* Input Area */}
        <form className="input-area" onSubmit={handleSubmit}>
          {selectedImage && (
            <div className="selected-image">
              <span>📎 {selectedImage.name}</span>
              <button 
                type="button" 
                className="clear-image-btn"
                onClick={clearImage}
              >
                ×
              </button>
            </div>
          )}
          
          <div className="input-wrapper">
            <div className="input-actions">

  {/* 📎 Upload */}
  <label className="upload-btn" title="Upload image">
    📎
    <input
      type="file"
      accept="image/*"
      onChange={handleImageUpload}
      style={{ display: 'none' }}
    />
  </label>

  {/* 🎤 Voice Button */}
  <button
    type="button"
    onClick={isRecording ? stopRecording : startRecording}
    title="Voice input"
    style={{
      marginLeft: "8px",
      color: isRecording ? "red" : "black",
      fontSize: "18px",
      cursor: "pointer",
      background: "none",
      border: "none"
    }}
  >
    🎤
  </button>

  {/* ❌ Clear Voice */}
  {input && (
    <button
      type="button"
      onClick={clearVoice}
      title="Clear text"
      style={{
        marginLeft: "6px",
        fontSize: "16px",
        cursor: "pointer",
        background: "none",
        border: "none"
      }}
    >
      ❌
    </button>
  )}

</div>
            
            <input
              type="text"
              className="chat-input"
              placeholder="Enter the news or upload an image..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              autoFocus
            />
            
            <button 
              type="submit" 
              className="send-btn"
              disabled={!input.trim() && !selectedImage}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
          
          <div className="powered-by">
            <span>Powered by</span>
            <span className="tech-name">RAG-LLM</span>
          </div>
        </form>
      </div>
    </div>
  );
};

export default NewsGuardian;