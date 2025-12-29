import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const NewQuotation = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [quotationNumber, setQuotationNumber] = useState('');
  const [customerName, setCustomerName] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const currentUser = localStorage.getItem('currentUser');
    if (!currentUser) {
      navigate('/login');
      return;
    }
    setUser(JSON.parse(currentUser));
  }, [navigate]);

  const validateQuotationNumber = async (number) => {
    if (!number.trim()) {
      setErrors(prev => ({ ...prev, quotationNumber: 'Quotation number is required' }));
      return false;
    }

    try {
      const response = await window.eel.check_quotation_exists(number)();
      if (response.exists) {
        setErrors(prev => ({ ...prev, quotationNumber: 'This quotation number already exists' }));
        return false;
      }
      setErrors(prev => ({ ...prev, quotationNumber: '' }));
      return true;
    } catch (error) {
      return true;
    }
  };

  const handleQuotationNumberChange = (e) => {
    const value = e.target.value;
    setQuotationNumber(value);
    if (value.trim()) {
      validateQuotationNumber(value);
    }
  };

  const handleCustomerNameChange = async (e) => {
    const value = e.target.value;
    setCustomerName(value);
    setErrors(prev => ({ ...prev, customerName: '' }));

    if (value.trim().length >= 2) {
      try {
        const response = await window.eel.search_customers(value)();
        if (response.success) {
          setSuggestions(response.data);
          setShowSuggestions(true);
        }
      } catch (error) {
        console.error('Failed to fetch suggestions:', error);
      }
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  const selectCustomer = (customer) => {
    setCustomerName(customer.name);
    setShowSuggestions(false);
  };

  const handleProceed = async () => {
    setErrors({});

    if (!quotationNumber.trim()) {
      setErrors(prev => ({ ...prev, quotationNumber: 'Quotation number is required' }));
      return;
    }

    if (!customerName.trim()) {
      setErrors(prev => ({ ...prev, customerName: 'Customer name is required' }));
      return;
    }

    const isValid = await validateQuotationNumber(quotationNumber);
    if (!isValid) return;

    setLoading(true);
    try {
      const response = await window.eel.create_project(quotationNumber, customerName)();
      if (response.success) {
        navigate(`/quotation/requirements/${response.data.id}`);
      } else {
        setErrors({ general: response.error });
      }
    } catch (error) {
      setErrors({ general: 'Failed to create quotation' });
    } finally {
      setLoading(false);
    }
  };

  if (!user) return <div style={styles.loading}>Loading...</div>;

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <div style={styles.headerContent}>
          <h1 style={styles.headerTitle}>Ringspann Industrial Suite</h1>
          <div style={styles.headerRight}>
            <span style={styles.userBadge}>User: {user.username}</span>
            <span style={styles.statusBadge}>● Logged In</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div style={styles.mainContent}>
        <button onClick={() => navigate('/dashboard')} style={styles.backBtn}>
          &lt; Back
        </button>

        <div style={styles.formCard}>
          <h2 style={styles.formTitle}>New Quotation</h2>

          {errors.general && (
            <div style={styles.errorBox}>{errors.general}</div>
          )}

          <div style={styles.formGroup}>
            <label style={styles.label}>Quotation Number:</label>
            <input
              type="text"
              value={quotationNumber}
              onChange={handleQuotationNumberChange}
              onBlur={() => validateQuotationNumber(quotationNumber)}
              placeholder="Enter unique quotation number"
              style={errors.quotationNumber ? styles.inputError : styles.input}
            />
            {errors.quotationNumber && (
              <span style={styles.errorText}>{errors.quotationNumber}</span>
            )}
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Customer Name:</label>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                value={customerName}
                onChange={handleCustomerNameChange}
                onFocus={() => customerName.length >= 2 && setShowSuggestions(true)}
                placeholder="Enter or select customer name"
                style={errors.customerName ? styles.inputError : styles.input}
                autoComplete="off"
              />
              {showSuggestions && suggestions.length > 0 && (
                <div style={styles.suggestionsBox}>
                  {suggestions.map((customer) => (
                    <div
                      key={customer.id}
                      onClick={() => selectCustomer(customer)}
                      style={styles.suggestionItem}
                    >
                      {customer.name}
                    </div>
                  ))}
                </div>
              )}
            </div>
            {errors.customerName && (
              <span style={styles.errorText}>{errors.customerName}</span>
            )}
          </div>

          <button
            onClick={handleProceed}
            disabled={loading}
            style={styles.proceedBtn}
          >
            {loading ? 'Processing...' : 'Proceed to Customer Requirements'}
          </button>
        </div>
      </div>

      {/* Footer */}
      <div style={styles.footer}>
        <span>Enter quotation details to proceed.</span>
        <span style={styles.footerRight}>{new Date().toLocaleString()}</span>
      </div>
    </div>
  );
};

const styles = {
  container: { minHeight: '100vh', display: 'flex', flexDirection: 'column', background: '#f5f5f5' },
  header: { background: '#e85d04', padding: '16px 0', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  headerContent: { maxWidth: '1400px', margin: '0 auto', padding: '0 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  headerTitle: { color: 'white', fontSize: '28px', fontWeight: 'bold', margin: 0 },
  headerRight: { display: 'flex', gap: '15px' },
  userBadge: { background: 'white', color: '#333', padding: '6px 16px', borderRadius: '4px', fontSize: '14px' },
  statusBadge: { background: 'white', color: '#28a745', padding: '6px 16px', borderRadius: '4px', fontSize: '14px' },
  mainContent: { flex: 1, maxWidth: '1000px', margin: '40px auto', padding: '0 20px', width: '100%' },
  backBtn: { background: '#007bff', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '4px', cursor: 'pointer', fontSize: '14px', marginBottom: '20px' },
  formCard: { background: 'white', borderRadius: '8px', padding: '50px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  formTitle: { fontSize: '32px', fontWeight: 600, color: '#333', marginBottom: '40px', textAlign: 'center' },
  formGroup: { marginBottom: '30px' },
  label: { display: 'block', fontSize: '16px', fontWeight: 500, color: '#333', marginBottom: '8px' },
  input: { width: '100%', padding: '14px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box' },
  inputError: { width: '100%', padding: '14px', fontSize: '16px', border: '2px solid #dc3545', borderRadius: '4px', boxSizing: 'border-box' },
  errorText: { color: '#dc3545', fontSize: '14px', marginTop: '5px', display: 'block' },
  errorBox: { background: '#f8d7da', border: '1px solid #f5c6cb', color: '#721c24', padding: '12px', borderRadius: '4px', marginBottom: '20px' },
  suggestionsBox: { position: 'absolute', top: '100%', left: 0, right: 0, background: 'white', border: '1px solid #ccc', borderTop: 'none', borderRadius: '0 0 4px 4px', maxHeight: '200px', overflowY: 'auto', zIndex: 1000, boxShadow: '0 4px 6px rgba(0,0,0,0.1)' },
  suggestionItem: { padding: '12px', cursor: 'pointer', borderBottom: '1px solid #f0f0f0', transition: 'background 0.2s' },
  proceedBtn: { background: '#007bff', color: 'white', border: 'none', padding: '16px 32px', fontSize: '18px', fontWeight: 600, borderRadius: '4px', cursor: 'pointer', width: '100%', marginTop: '20px' },
  footer: { background: '#2c3e50', color: 'white', padding: '12px 20px', fontSize: '13px', display: 'flex', justifyContent: 'space-between' },
  footerRight: { textAlign: 'right' },
  loading: { display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', fontSize: '18px' },
};

export default NewQuotation;