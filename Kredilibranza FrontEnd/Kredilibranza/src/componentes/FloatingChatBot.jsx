import React, { useState } from 'react';
import ChatBotPage from './chatbot';
import './FloatingChatBot.css';

function FloatingChatBot() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChatBot = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      <div className="floating-chatbot" onClick={toggleChatBot}>
        {/* Puedes reemplazar este div con una imagen o un ícono de esfera */}
        <div className="sphere"></div>
      </div>
      {isOpen && (
        <div className="chatbot-window">
          <ChatBotPage />
          <button className="close-button" onClick={toggleChatBot}>×</button>
        </div>
      )}
    </>
  );
}

export default FloatingChatBot;
