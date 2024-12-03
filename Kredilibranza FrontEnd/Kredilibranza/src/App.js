import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import NavBar from "./componentes/NavBar";
import Header from "./componentes/Header";
import Form from "./componentes/Form";
import Condiciones from "./componentes/Condiciones";
import Simulador from "./componentes/Simulador";
import QuienesSomos from "./componentes/QuienesSomos";
import Footer from "./componentes/Footer";
import ChatBotPage from "./componentes/chatbot";
import FloatingChatBot from "./componentes/FloatingChatBot"; // Importar el nuevo componente
import FileUpload from "./componentes/FileUpload";

import Login from "./componentes/Login"; 

import './componentes/Banner.css';
import './componentes/Footer.css';
import './componentes/Form.css';
import './componentes/NavBar.css';
import './componentes/QuienesSomos.css';
import './componentes/Simulador.css';
import './componentes/Condiciones.css';
import './componentes/chatbot.css';
import './componentes/FloatingChatBot.css'; // Importar los estilos del flotante

function PrivateRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <Router>
      <div>
        <NavBar />
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Header />
                <Form />
                <Condiciones />
                <Simulador />
                <QuienesSomos />
                <Footer />
              </>
            }
          />

          <Route path="/login" element={<Login />} />

          <Route path="/chatbot" element={<ChatBotPage />} />

          <Route
            path="/fileupload"
            element={
              <PrivateRoute>
                <FileUpload />
              </PrivateRoute>
            }/>
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
        <FloatingChatBot /> {/* Agregar el flotante fuera de las rutas para que aparezca en todas las páginas */}
      </div>
    </Router>
  );
}

export default App;
