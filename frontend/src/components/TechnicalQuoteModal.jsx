import React, { useState, useEffect } from 'react';

// Technical field definitions by part type
const TECHNICAL_FIELDS = {
  "Brake Quotation": [
    { label: "Ringspann Product Quantity", type: "number" },
    { label: "Model", type: "text" },
    { label: "Size", type: "number" },
    { label: "Type", type: "text" },
    { label: "Thruster/Cylinder size", type: "number" },
    { label: "Material", type: "text" },
    { label: "Accessories", type: "textarea" },
    { label: "Drum/Disc size", type: "number" },
    { label: "Brake Torque (Nm)", type: "number" },
    { label: "Theoretical Stopping time for selected brake (sec)", type: "number" },
    { label: "Technical Points", type: "textarea" }
  ],
  "Backstop Quotation": [
    { label: "Ringspann Product Quantity", type: "number" },
    { label: "Product Code", type: "text" },
    { label: "Size", type: "number" },
    { label: "Type", type: "text" },
    { label: "Technical Points", type: "textarea" }
  ],
  "Coupling and Torque Limiter Quotation": [
    { label: "Ringspann Product Quantity", type: "number" },
    { label: "Model", type: "text" },
    { label: "Special Requirements", type: "textarea" },
    { label: "Technical Points", type: "textarea" }
  ],
  "Locking Element for Conveyor Quotation": [
    { label: "Locking element Qty", type: "number" },
    { label: "Product code", type: "text" },
    { label: "Size", type: "text" },
    { label: "Hub inner diameter (Di) mm", type: "number" },
    { label: "Hub outer diameter (Knin) mm", type: "number" },
    { label: "Hub length (Knin) mm", type: "number" },
    { label: "Torque (Mact) Nm", type: "number" },
    { label: "Bending moment (Mb) Nm", type: "number" },
    { label: "Screw Tightening torque (Ms) Nm", type: "number" },
    { label: "Shaft pressure (Pw) N/mm2", type: "number" },
    { label: "Technical points", type: "textarea" }
  ],
  "Over Running Clutch Quotation": [
    { label: "Product code", type: "text" },
    { label: "Size", type: "text" },
    { label: "Technical points", type: "textarea" }
  ]
};

const TechnicalQuoteModal = ({ isOpen, onClose, requirement, existingQuote, onSave }) => {
  const [customerReqs, setCustomerReqs] = useState({});
  const [technicalFields, setTechnicalFields] = useState({});

  useEffect(() => {
    if (requirement) {
      // Load customer requirements
      setCustomerReqs(requirement.fieldValues || {});
      
      // Get technical fields for this part type
      const partType = requirement.partType;
      const fieldDefs = TECHNICAL_FIELDS[partType] || [];
      
      // Load existing technical quote if available
      if (existingQuote && existingQuote.technical_fields) {
        setTechnicalFields(existingQuote.technical_fields);
      } else {
        // Initialize empty fields
        const emptyFields = {};
        fieldDefs.forEach(field => {
          emptyFields[field.label] = '';
        });
        setTechnicalFields(emptyFields);
      }
    }
  }, [requirement, existingQuote]);

  const handleCustomerReqChange = (field, value) => {
    setCustomerReqs(prev => ({ ...prev, [field]: value }));
  };

  const handleTechnicalFieldChange = (field, value) => {
    setTechnicalFields(prev => ({ ...prev, [field]: value }));
  };

  const handleAddRow = () => {
    // TODO: Add row for multi-row technical data
    alert('Add row functionality - to be implemented');
  };

  const handleSave = () => {
    const reqId = requirement.id || requirement.partType;
    const quoteData = {
      customer_requirements: customerReqs,
      technical_fields: technicalFields
    };
    onSave(reqId, quoteData);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <div style={styles.header}>
          <h2 style={styles.title}>{requirement?.partType || 'Technical Quote'} - Technical Quote</h2>
          <button onClick={onClose} style={styles.closeBtn}>×</button>
        </div>

        <div style={styles.content}>
          <div style={styles.columns}>
            {/* Left Column - Customer Requirements */}
            <div style={styles.column}>
              <h3 style={styles.columnTitle}>Customer Requirements</h3>
              <div style={styles.fieldsContainer}>
                {Object.keys(customerReqs).length === 0 ? (
                  <p style={styles.placeholder}>No customer requirements data</p>
                ) : (
                  Object.entries(customerReqs).map(([key, value]) => (
                    <div key={key} style={styles.field}>
                      <label style={styles.label}>{key}:</label>
                      <input
                        type="text"
                        value={value || ''}
                        onChange={(e) => handleCustomerReqChange(key, e.target.value)}
                        style={styles.input}
                      />
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Right Column - Technical Quote */}
            <div style={styles.column}>
              <h3 style={styles.columnTitle}>Technical Quote</h3>
              <h4 style={styles.subTitle}>Technical Quote</h4>
              <div style={styles.fieldsContainer}>
                {(() => {
                  const partType = requirement?.partType;
                  const fieldDefs = TECHNICAL_FIELDS[partType] || [];
                  
                  if (fieldDefs.length === 0) {
                    return (
                      <p style={styles.placeholder}>
                        No technical fields defined for {partType}
                      </p>
                    );
                  }
                  
                  return fieldDefs.map((fieldDef) => (
                    <div key={fieldDef.label} style={styles.field}>
                      <label style={styles.label}>{fieldDef.label}:</label>
                      {fieldDef.type === 'textarea' ? (
                        <textarea
                          value={technicalFields[fieldDef.label] || ''}
                          onChange={(e) => handleTechnicalFieldChange(fieldDef.label, e.target.value)}
                          style={styles.textarea}
                          rows="3"
                        />
                      ) : (
                        <input
                          type={fieldDef.type}
                          value={technicalFields[fieldDef.label] || ''}
                          onChange={(e) => handleTechnicalFieldChange(fieldDef.label, e.target.value)}
                          style={styles.input}
                        />
                      )}
                    </div>
                  ));
                })()}
              </div>
            </div>
          </div>
        </div>

        <div style={styles.footer}>
          <button onClick={handleAddRow} style={styles.addBtn}>Add Row</button>
          <div style={styles.actionBtns}>
            <button onClick={onClose} style={styles.cancelBtn}>Cancel</button>
            <button onClick={handleSave} style={styles.saveBtn}>Save Technical Quote</button>
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
    width: '95vw',
    maxWidth: '1400px',
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
    backgroundColor: '#dc2626'
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
  columns: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '20px',
    height: '100%'
  },
  column: {
    border: '1px solid #d1d5db',
    borderRadius: '4px',
    padding: '20px',
    backgroundColor: '#f9fafb',
    overflowY: 'auto'
  },
  columnTitle: {
    fontSize: '18px',
    fontWeight: 'bold',
    marginBottom: '16px',
    textAlign: 'center',
    color: '#1f2937'
  },
  subTitle: {
    fontSize: '16px',
    fontWeight: '600',
    marginBottom: '12px',
    color: '#374151'
  },
  fieldsContainer: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'
  },
  field: {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px'
  },
  label: {
    fontSize: '13px',
    fontWeight: '500',
    color: '#374151'
  },
  input: {
    padding: '8px',
    border: '1px solid #d1d5db',
    borderRadius: '4px',
    fontSize: '14px'
  },
  textarea: {
    padding: '8px',
    border: '1px solid #d1d5db',
    borderRadius: '4px',
    fontSize: '14px',
    fontFamily: 'Arial, sans-serif',
    resize: 'vertical'
  },
  placeholder: {
    padding: '40px 20px',
    textAlign: 'center',
    color: '#9ca3af',
    fontSize: '14px',
    lineHeight: '1.6'
  },
  footer: {
    padding: '15px 20px',
    borderTop: '1px solid #ddd',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  addBtn: {
    padding: '10px 20px',
    backgroundColor: '#2563eb',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  actionBtns: {
    display: 'flex',
    gap: '10px'
  },
  cancelBtn: {
    padding: '10px 30px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  saveBtn: {
    padding: '10px 30px',
    backgroundColor: '#2563eb',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '15px',
    fontWeight: '600'
  }
};

export default TechnicalQuoteModal;