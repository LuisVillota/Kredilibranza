import React, { useState, useRef, useEffect } from 'react';
import './chatbot.css'; 

function ChatBotPage() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const handleSendMessage = async () => {
    if (inputValue.trim() === '') return;
    const userMessage = { role: 'user', content: inputValue };
    setMessages([...messages, userMessage]);
    setInputValue('');
    try {
      const botResponse = await getBotResponse(inputValue);
      setMessages((prevMessages) => [...prevMessages, botResponse]);
    } catch (error) {
      console.error('Error al obtener respuesta del bot:', error);
      setMessages((prevMessages) => [...prevMessages, { role: 'bot', content: 'Error al obtener respuesta del bot.' }]);
    }
  };

  const getBotResponse = async (message) => {
    try {
      const response = await fetch('http://localhost:8000/generate-answer/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: message }),
      });
      if (!response.ok) {
        throw new Error('Error en la respuesta del servidor');
      }
      const data = await response.json();
      return { role: 'bot', content: data.answer };
    } catch (error) {
      throw error;
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-container">
      <div className="chat-window">
        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              {message.content}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Escribe tu mensaje..."
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <button onClick={handleSendMessage}>Enviar</button>
        </div>
      </div>
    </div>
  );
}

export default ChatBotPage;
