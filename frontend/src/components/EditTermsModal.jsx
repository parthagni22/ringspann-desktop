import React, { useState, useEffect } from 'react';

const EditTermsModal = ({ isOpen, onClose, onSave, currentTerms }) => {
  const [terms, setTerms] = useState({
    payment: '100% against Proforma Invoice',
    priceBasis: 'Ex-Works Chakan, Pune Basis',
    pfCharges: '2% Extra on the Basic Price',
    insurance: 'Shall be borne by you',
    taxes: {
      igst: 'I-GST is applicable for Out of Maharashtra',
      cgstSgst: 'C-GST & S-GST is applicable within the State of Maharashtra',
      ugst: 'U-GST is applicable for Union Territory'
    },
    deliveryPeriod: '8 weeks from date of technically and commercially clear PO',
    warranty: '12 months from the date of commissioning or 18 months from the date of Invoice, whichever is earlier'
  });

  const [customTerms, setCustomTerms] = useState([]);
  const [dropdownOptions, setDropdownOptions] = useState({
    payment: [],
    priceBasis: [],
    pfCharges: [],
    insurance: [],
    deliveryPeriod: []
  });

  useEffect(() => {
    loadDropdownOptions();
    if (currentTerms) {
      parseCurrentTerms(currentTerms);
    }
  }, [currentTerms]);

  const loadDropdownOptions = async () => {
    try {
      const result = await window.eel.get_terms_dropdown_options()();
      if (result.success) {
        setDropdownOptions(result.data);
      }
    } catch (error) {
      console.error('Failed to load dropdown options:', error);
    }
  };

  const parseCurrentTerms = (termsText) => {
    if (!termsText) return;
    
    const lines = termsText.split('\n');
    const parsed = {
      payment: '',
      priceBasis: '',
      pfCharges: '',
      insurance: '',
      taxes: { igst: '', cgstSgst: '', ugst: '' },
      deliveryPeriod: '',
      warranty: ''
    };
    const customList = [];
    
    lines.forEach(line => {
      if (line.includes('Terms of Payment')) {
        parsed.payment = line.split(' - ')[1] || parsed.payment;
      } else if (line.includes('Price basis:')) {
        parsed.priceBasis = line.split(': ')[1] || parsed.priceBasis;
      } else if (line.includes('P&F Charges:')) {
        parsed.pfCharges = line.split(': ')[1] || parsed.pfCharges;
      } else if (line.includes('Insurance:')) {
        parsed.insurance = line.split(': ')[1] || parsed.insurance;
      } else if (line.startsWith('a)')) {
        parsed.taxes.igst = line.substring(3).trim();
      } else if (line.startsWith('b)')) {
        parsed.taxes.cgstSgst = line.substring(3).trim();
      } else if (line.startsWith('c)')) {
        parsed.taxes.ugst = line.substring(3).trim();
      } else if (line.includes('Delivery Period:')) {
        parsed.deliveryPeriod = line.split(': ')[1] || parsed.deliveryPeriod;
      } else if (line.includes('Warranty') || line.includes('Guarantee')) {
        parsed.warranty = line.split(': ')[1] || parsed.warranty;
      } else if (line.match(/^\d+\)/)) {
        // Custom term (8+)
        const num = parseInt(line.match(/^\d+/)[0]);
        if (num >= 8) {
          const parts = line.substring(line.indexOf(')') + 1).split(':');
          if (parts.length >= 2) {
            customList.push({
              id: Date.now() + num,
              title: parts[0].trim(),
              description: parts.slice(1).join(':').trim()
            });
          }
        }
      }
    });
    
    setTerms(prev => ({ ...prev, ...parsed }));
    setCustomTerms(customList);
  };

  const handleAddCustomTerm = () => {
    setCustomTerms([...customTerms, { id: Date.now(), title: '', description: '' }]);
  };

  const handleCustomTermChange = (id, field, value) => {
    setCustomTerms(customTerms.map(term => 
      term.id === id ? { ...term, [field]: value } : term
    ));
  };

  const handleRemoveCustomTerm = (id) => {
    setCustomTerms(customTerms.filter(term => term.id !== id));
  };

  const handleAddNewOption = async (field, newValue) => {
    if (!newValue.trim()) return;
    
    try {
      const result = await window.eel.add_terms_dropdown_option(field, newValue)();
      if (result.success) {
        setDropdownOptions(prev => ({
          ...prev,
          [field]: [...prev[field], newValue]
        }));
        setTerms(prev => ({ ...prev, [field]: newValue }));
      }
    } catch (error) {
      console.error('Failed to add option:', error);
    }
  };

  const handleSave = async () => {
    const formattedTerms = formatTermsForPDF();
    await onSave(formattedTerms);
    onClose();
  };

  const formatTermsForPDF = () => {
    let formatted = [
      `1) Terms of Payment - ${terms.payment}`,
      `2) Price basis: ${terms.priceBasis}`,
      `3) P&F Charges: ${terms.pfCharges}`,
      `4) Insurance: ${terms.insurance}`,
      `5) Taxes:`,
      `a) ${terms.taxes.igst}`,
      `b) ${terms.taxes.cgstSgst}`,
      `c) ${terms.taxes.ugst}`,
      `6) Delivery Period: ${terms.deliveryPeriod}`,
      `7) Warranty/Guarantee: ${terms.warranty}`
    ];

    customTerms.forEach((term, idx) => {
      if (term.title.trim() && term.description.trim()) {
        formatted.push(`${8 + idx}) ${term.title}: ${term.description}`);
      }
    });

    return formatted.join('\n');
  };

  const handleResetDefaults = () => {
    setTerms({
      payment: '100% against Proforma Invoice',
      priceBasis: 'Ex-Works Chakan, Pune Basis',
      pfCharges: '2% Extra on the Basic Price',
      insurance: 'Shall be borne by you',
      taxes: {
        igst: 'I-GST is applicable for Out of Maharashtra',
        cgstSgst: 'C-GST & S-GST is applicable within the State of Maharashtra',
        ugst: 'U-GST is applicable for Union Territory'
      },
      deliveryPeriod: '8 weeks from date of technically and commercially clear PO',
      warranty: '12 months from the date of commissioning or 18 months from the date of Invoice, whichever is earlier'
    });
    setCustomTerms([]);
  };

  if (!isOpen) return null;

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <div style={styles.header}>
          <h2 style={styles.title}>Edit Terms & Conditions</h2>
          <button onClick={onClose} style={styles.closeBtn}>×</button>
        </div>

        <div style={styles.content}>
          {/* Payment Terms */}
          <div style={styles.field}>
            <label style={styles.label}>1. Terms of Payment:</label>
            <select 
              value={terms.payment}
              onChange={(e) => {
                if (e.target.value === '__ADD_NEW__') {
                  const newVal = prompt('Enter new payment term:');
                  if (newVal) handleAddNewOption('payment', newVal);
                } else {
                  setTerms({...terms, payment: e.target.value});
                }
              }}
              style={styles.select}
            >
              {dropdownOptions.payment.map(opt => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
              <option value="100% against Proforma Invoice">100% against Proforma Invoice</option>
              <option value="50% Advance, 50% against Delivery">50% Advance, 50% against Delivery</option>
              <option value="30 Days Credit">30 Days Credit</option>
              <option value="__ADD_NEW__">+ Add New Option</option>
            </select>
          </div>

          {/* Price Basis */}
          <div style={styles.field}>
            <label style={styles.label}>2. Price basis:</label>
            <select 
              value={terms.priceBasis}
              onChange={(e) => {
                if (e.target.value === '__ADD_NEW__') {
                  const newVal = prompt('Enter new price basis:');
                  if (newVal) handleAddNewOption('priceBasis', newVal);
                } else {
                  setTerms({...terms, priceBasis: e.target.value});
                }
              }}
              style={styles.select}
            >
              {dropdownOptions.priceBasis.map(opt => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
              <option value="Ex-Works Chakan, Pune Basis">Ex-Works Chakan, Pune Basis</option>
              <option value="FOR Destination">FOR Destination</option>
              <option value="CIF">CIF</option>
              <option value="__ADD_NEW__">+ Add New Option</option>
            </select>
          </div>

          {/* P&F Charges */}
          <div style={styles.field}>
            <label style={styles.label}>3. P&F Charges:</label>
            <select 
              value={terms.pfCharges}
              onChange={(e) => {
                if (e.target.value === '__ADD_NEW__') {
                  const newVal = prompt('Enter new P&F charge:');
                  if (newVal) handleAddNewOption('pfCharges', newVal);
                } else {
                  setTerms({...terms, pfCharges: e.target.value});
                }
              }}
              style={styles.select}
            >
              {dropdownOptions.pfCharges.map(opt => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
              <option value="2% Extra on the Basic Price">2% Extra on the Basic Price</option>
              <option value="3% Extra on the Basic Price">3% Extra on the Basic Price</option>
              <option value="Included">Included</option>
              <option value="__ADD_NEW__">+ Add New Option</option>
            </select>
          </div>

          {/* Insurance */}
          <div style={styles.field}>
            <label style={styles.label}>4. Insurance:</label>
            <select 
              value={terms.insurance}
              onChange={(e) => {
                if (e.target.value === '__ADD_NEW__') {
                  const newVal = prompt('Enter new insurance term:');
                  if (newVal) handleAddNewOption('insurance', newVal);
                } else {
                  setTerms({...terms, insurance: e.target.value});
                }
              }}
              style={styles.select}
            >
              {dropdownOptions.insurance.map(opt => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
              <option value="Shall be borne by you">Shall be borne by you</option>
              <option value="Included in price">Included in price</option>
              <option value="To be arranged by buyer">To be arranged by buyer</option>
              <option value="__ADD_NEW__">+ Add New Option</option>
            </select>
          </div>

          {/* Taxes (Editable text) */}
          <div style={styles.field}>
            <label style={styles.label}>5. Taxes:</label>
            <div style={styles.subField}>
              <label style={styles.subLabel}>a) I-GST:</label>
              <input 
                type="text"
                value={terms.taxes.igst}
                onChange={(e) => setTerms({...terms, taxes: {...terms.taxes, igst: e.target.value}})}
                style={styles.input}
              />
            </div>
            <div style={styles.subField}>
              <label style={styles.subLabel}>b) C-GST & S-GST:</label>
              <input 
                type="text"
                value={terms.taxes.cgstSgst}
                onChange={(e) => setTerms({...terms, taxes: {...terms.taxes, cgstSgst: e.target.value}})}
                style={styles.input}
              />
            </div>
            <div style={styles.subField}>
              <label style={styles.subLabel}>c) U-GST:</label>
              <input 
                type="text"
                value={terms.taxes.ugst}
                onChange={(e) => setTerms({...terms, taxes: {...terms.taxes, ugst: e.target.value}})}
                style={styles.input}
              />
            </div>
          </div>

          {/* Delivery Period */}
          <div style={styles.field}>
            <label style={styles.label}>6. Delivery Period:</label>
            <select 
              value={terms.deliveryPeriod}
              onChange={(e) => {
                if (e.target.value === '__ADD_NEW__') {
                  const newVal = prompt('Enter new delivery period:');
                  if (newVal) handleAddNewOption('deliveryPeriod', newVal);
                } else {
                  setTerms({...terms, deliveryPeriod: e.target.value});
                }
              }}
              style={styles.select}
            >
              {dropdownOptions.deliveryPeriod.map(opt => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
              <option value="8 weeks from date of technically and commercially clear PO">8 weeks from clear PO</option>
              <option value="6 weeks from date of technically and commercially clear PO">6 weeks from clear PO</option>
              <option value="12 weeks from date of technically and commercially clear PO">12 weeks from clear PO</option>
              <option value="__ADD_NEW__">+ Add New Option</option>
            </select>
          </div>

          {/* Warranty */}
          <div style={styles.field}>
            <label style={styles.label}>7. Warranty/Guarantee:</label>
            <input 
              type="text"
              value={terms.warranty}
              onChange={(e) => setTerms({...terms, warranty: e.target.value})}
              style={styles.input}
            />
          </div>

          {/* Custom Terms */}
          <div style={styles.customSection}>
            <h3 style={styles.subtitle}>Custom Terms & Conditions</h3>
            {customTerms.map(term => (
              <div key={term.id} style={styles.customTermBlock}>
                <input 
                  type="text"
                  value={term.title}
                  onChange={(e) => handleCustomTermChange(term.id, 'title', e.target.value)}
                  placeholder="Enter title (e.g., Warranty Extension)"
                  style={styles.input}
                />
                <textarea
                  value={term.description}
                  onChange={(e) => handleCustomTermChange(term.id, 'description', e.target.value)}
                  placeholder="Enter description..."
                  style={styles.textarea}
                  rows="3"
                />
                <button 
                  onClick={() => handleRemoveCustomTerm(term.id)}
                  style={styles.removeBtn}
                >
                  Remove
                </button>
              </div>
            ))}
            <button onClick={handleAddCustomTerm} style={styles.addBtn}>
              + Add New Term
            </button>
          </div>
        </div>

        <div style={styles.footer}>
          <button onClick={handleResetDefaults} style={styles.resetBtn}>
            Reset to Defaults
          </button>
          <div style={styles.actionBtns}>
            <button onClick={handleSave} style={styles.saveBtn}>Save</button>
            <button onClick={onClose} style={styles.cancelBtn}>Cancel</button>
          </div>
        </div>
      </div>
    </div>
  );
};

const styles = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.5)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000
  },
  modal: {
    backgroundColor: 'white',
    borderRadius: '8px',
    width: '800px',
    maxHeight: '90vh',
    display: 'flex',
    flexDirection: 'column',
    boxShadow: '0 4px 20px rgba(0,0,0,0.3)'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '20px',
    borderBottom: '1px solid #ddd',
    backgroundColor: '#ff6600'
  },
  title: {
    margin: 0,
    color: 'white',
    fontSize: '20px'
  },
  closeBtn: {
    background: 'none',
    border: 'none',
    fontSize: '28px',
    color: 'white',
    cursor: 'pointer',
    padding: '0',
    width: '30px',
    height: '30px'
  },
  content: {
    padding: '20px',
    overflowY: 'auto',
    flex: 1
  },
  field: {
    marginBottom: '20px'
  },
  label: {
    display: 'block',
    fontWeight: 'bold',
    marginBottom: '8px',
    fontSize: '14px'
  },
  select: {
    width: '100%',
    padding: '8px',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '4px'
  },
  input: {
    width: '100%',
    padding: '8px',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '4px'
  },
  subField: {
    marginLeft: '20px',
    marginTop: '10px'
  },
  subLabel: {
    display: 'block',
    fontSize: '13px',
    marginBottom: '5px'
  },
  customSection: {
    marginTop: '30px',
    paddingTop: '20px',
    borderTop: '2px solid #eee'
  },
  subtitle: {
    fontSize: '16px',
    marginBottom: '15px'
  },
  customTermBlock: {
    marginBottom: '20px',
    padding: '15px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    backgroundColor: '#f9f9f9'
  },
  customTerm: {
    display: 'flex',
    gap: '10px',
    marginBottom: '10px',
    alignItems: 'center'
  },
  textarea: {
    width: '100%',
    padding: '8px',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    marginTop: '8px',
    marginBottom: '8px',
    fontFamily: 'Arial, sans-serif',
    resize: 'vertical'
  },
  removeBtn: {
    padding: '8px 15px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  addBtn: {
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    marginTop: '10px'
  },
  footer: {
    padding: '15px 20px',
    borderTop: '1px solid #ddd',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  resetBtn: {
    padding: '10px 20px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  actionBtns: {
    display: 'flex',
    gap: '10px'
  },
  saveBtn: {
    padding: '10px 30px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '15px'
  },
  cancelBtn: {
    padding: '10px 30px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '15px'
  }
};

export default EditTermsModal;