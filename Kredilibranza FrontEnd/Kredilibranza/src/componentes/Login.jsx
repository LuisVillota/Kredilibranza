import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from './Button';
import Input from './Input';
import Label from './Label';
import { User, Lock, X } from 'lucide-react';
import './Login.css';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await fetch('http://localhost:8000/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username,
          password,
        }),
      });

      if (!response.ok) {
        throw new Error('Nombre de usuario o contraseña incorrectos');
      }

      const data = await response.json();
      localStorage.setItem('token', data.access_token);
      // Redirige a la página principal o a la que desees
      navigate('/');
    } catch (err) {
      setError(err.message);
    }
  };

  const handleClose = () => {
    navigate('/'); 
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <button
          className="close-button"
          aria-label="Cerrar"
          onClick={handleClose}
        >
          <X size={24} />
        </button>

        <h1 className="text-3xl font-bold text-center mb-8">Iniciar Sesión</h1>

        {error && <p className="error-message">{error}</p>}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="login-field">
            <Label htmlFor="username">Nombre de Usuario</Label>
            <div className="relative">
              <User className="icon" size={20} />
              <Input
                id="username"
                type="text"
                placeholder="tu_usuario"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="pl-10"
                required
              />
            </div>
          </div>
          <div className="login-field">
            <Label htmlFor="password">Contraseña</Label>
            <div className="relative">
              <Lock className="icon" size={20} />
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="pl-10"
                required
              />
            </div>
          </div>
          <Button type="submit" className="w-full">
            Iniciar Sesión
          </Button>
        </form>
      </div>
    </div>
  );

  
}
