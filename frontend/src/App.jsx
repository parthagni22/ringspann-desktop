import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Dashboard from './pages/Dashboard';
import NewQuotation from './pages/NewQuotation';
import CustomerRequirements from './pages/CustomerRequirements';
import CommercialQuote from './pages/CommercialQuote';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/quotation/new" element={<NewQuotation />} />
        <Route path="/quotation/requirements/:projectId" element={<CustomerRequirements />} />
        <Route path="/quotation/commercial/:projectId" element={<CommercialQuote />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;