import React from 'react';
import { AlertTriangle } from 'lucide-react';

const Alert = ({ message }) => {
  if (!message) return null;

  return (
    <div className="alert">
      <AlertTriangle size={20} />
      <span>{message}</span>
    </div>
  );
};

export default Alert;
