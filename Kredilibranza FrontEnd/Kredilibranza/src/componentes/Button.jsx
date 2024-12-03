import React from 'react';

// Componente de Botón Reutilizable
const Button = ({ children, onClick, className, ...props }) => {
  return (
    <button onClick={onClick} className={className} {...props}>
      {children}
    </button>
  );
};

export default Button;
