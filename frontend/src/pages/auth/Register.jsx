import React from 'react';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const navigate = useNavigate();
  
  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h2>Registration is handled in Login page</h2>
      <button onClick={() => navigate('/login')}>Go to Login</button>
    </div>
  );
};

export default Register;