import React from 'react';

const Checkbox = ({ id, className, ...props }) => {
  return (
    <input type="checkbox" id={id} className={className} {...props} />
  );
};

export default Checkbox;
