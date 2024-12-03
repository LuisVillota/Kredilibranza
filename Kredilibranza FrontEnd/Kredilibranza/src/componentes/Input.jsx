import React from 'react';

const Input = ({ type, id, placeholder, value, onChange, className, ...props }) => {
  return (
    <input
      type={type}
      id={id}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className={`border p-2 rounded ${className}`}
      {...props}
    />
  );
};

export default Input;
