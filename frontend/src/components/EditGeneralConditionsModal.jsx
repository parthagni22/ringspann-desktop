import React, { useState, useEffect } from 'react';

const DEFAULT_CONDITIONS = [
  {
    title: "1. Offer and Conclusion of Contract",
    content: "Only our offers and written confirmations will be decisive with respect to the scope and type of products delivered. The contract shall be deemed to have been concluded when we have accepted the order in writing; up to that time our quotation is without obligation. Measures, weights, illustrations and drawings are without obligation for the models, unless expressly confirmed by us in writing. Manufacturing and detail drawings will be supplied by us only if agreed upon before conclusion of the contract and confirmed by us in writing. An appropriate extra charge will be levied for the supply of such drawings. Where special tools and gauges or clamping devices are necessary in order to carry out a special order, these will be invoiced additionally, but shall remain our property after completion of the order."
  },
  {
    title: "2. Terms of Delivery",
    content: "Prices quoted in our offer are EX Works Chakan Basis. All prices are excluding freight and insurance."
  },
  {
    title: "3. Terms of Payment",
    content: "The Terms of Payment as applicable is mentioned in our offer. If the terms of payment laid down in the contract are not complied with, interest will be charged at a rate of 8% above the discount rate. In case of complaints with respect to products received, the customer is requested not suspend payment or make any deductions from the invoiced amount, unless liability is admitted by us."
  },
  {
    title: "4. Retention of Title/Conditional Sale",
    content: "The products shall remain our property until payment has been made in full."
  },
  {
    title: "5. Delivery",
    content: "The Delivery time is mentioned in our offer. The delivery period shall run from the date on which all technical particulars of the models in questions have been clarified and agreement has been reached between the parties with respect to all details of the contract. In case of unforeseeable circumstances which are beyond our control, i.e., force majeure, operating trouble, delayed deliveries by a subcontractor, rejects in our own plant or at a subcontractor's the delivery period shall be reasonably extended. We shall use our best efforts to honour confirmed delivery dates, which are only approximate. However, if in case of confirmed delivery dates there occurs a delay, an appropriate extension of time shall be granted. Claims for damages or penalties are, therefore, excluded unless its discussed in detail during the placement of the order on us."
  },
  {
    title: "6. Packing & Forwarding Charges",
    content: "Packing & Forwarding charge @2% shall be applicable on the Basic price of the contract. In case of NIL P & F, then we shall adopt our standard packing method for the dispatch."
  },
  {
    title: "7. Taxes",
    content: "GST shall be applicable as per the slab of HSN Code."
  },
  {
    title: "8. Liability for Defects",
    content: "Deficiency claims have to be brought forward immediately upon receipt of the shipment. We warrant the quality of our products in such a manner as to replace or repair all components returned to us because they do not meet the specifications or cannot be used because of defects in workmanship. We accept liability only for defects in design or execution which have been caused by us. For defects in material supplied by us we accept liability only insofar as we should have discovered the deficiency in exercising due diligence. If we are responsible for the technical design, we will accept a deficiency claim only in case the customer can prove that our product does not meet the state of art due to our fault. We are not liable for damages due to normal wear and tear or misuse of the products supplied. Any further claims, such as compensation for direct or indirect damages to machinery or cost incurred in dismantling an assembly work, freight charges or penalties for delay etc. are not covered. Where products have been repaired, altered or overhauled without our consent our liability ceases."
  },
  {
    title: "9. Warranty",
    content: "Unless otherwise agreed, we warrant the quality of design and manufacture utilizing good raw material for a period of 12 months from the date of commissioning or 18 months from the date of shipment, whichever is earlier, in such a way that we replace or repair free of charge defective components which have been returned to us."
  },
  {
    title: "10. Cancellation of Contract",
    content: "The customer may cancel the contract only if, upon a reasonable extension of time we have failed to remedy a deficiency or if, in such case, we are, for whatever reason, unable to undertake necessary corrections or to supply a replacement part. In the event that the contract should be cancelled by the customer without our fault, the customer shall reimburse to us, without delay, the invoice value of such contract after deduction of the direct costs saved by us as a result of the cancellation."
  },
  {
    title: "11. Purchasing Conditions of Customer",
    content: "Purchasing conditions of the customer which are not in compliance with these General Conditions of Delivery and Payment, must be accepted by us in writing in order to be binding. The other provisions of these conditions remain in full force and effect."
  },
  {
    title: "12. Test Certificates & Warranty Certificate",
    content: "We shall submit our standard Test & Warranty certificate. Any other additional certificate shall be on a chargeable basis and upon acceptance from our end for the same."
  },
  {
    title: "13. Validity",
    content: "The Validity of this offer is for a period of 30 days from the date of this offer and shall be extended subjected to mutual acceptance."
  }
];

const EditGeneralConditionsModal = ({ isOpen, onClose, onSave, currentConditions }) => {
  const [conditions, setConditions] = useState(DEFAULT_CONDITIONS);

  useEffect(() => {
    if (currentConditions) {
      parseConditions(currentConditions);
    }
  }, [currentConditions]);

  const parseConditions = (conditionsText) => {
    if (!conditionsText) return;
    
    const parsed = [];
    const lines = conditionsText.split('\n');
    let currentCondition = null;
    
    lines.forEach(line => {
      const titleMatch = line.match(/^(\d+\.\s+.+?):/);
      if (titleMatch) {
        if (currentCondition) {
          parsed.push(currentCondition);
        }
        currentCondition = {
          title: titleMatch[1],
          content: line.substring(titleMatch[0].length).trim()
        };
      } else if (currentCondition && line.trim()) {
        currentCondition.content += ' ' + line.trim();
      }
    });
    
    if (currentCondition) {
      parsed.push(currentCondition);
    }
    
    if (parsed.length > 0) {
      setConditions(parsed);
    }
  };

  const handleConditionChange = (index, field, value) => {
    const newConditions = [...conditions];
    newConditions[index][field] = value;
    setConditions(newConditions);
  };

  const handleAddCondition = () => {
    setConditions([...conditions, {
      title: `${conditions.length + 1}. New Condition`,
      content: ''
    }]);
  };

  const handleRemoveCondition = (index) => {
    if (conditions.length === 1) {
      alert('At least one condition is required');
      return;
    }
    setConditions(conditions.filter((_, i) => i !== index));
  };

  const handleSave = async () => {
    const formattedConditions = conditions.map(c => 
      `${c.title}: ${c.content}`
    ).join('\n\n');
    
    await onSave(formattedConditions);
    onClose();
  };

  const handleResetDefaults = () => {
    setConditions(DEFAULT_CONDITIONS);
  };

  if (!isOpen) return null;

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <div style={styles.header}>
          <h2 style={styles.title}>Edit General Conditions</h2>
          <button onClick={onClose} style={styles.closeBtn}>×</button>
        </div>

        <div style={styles.content}>
          {conditions.map((condition, index) => (
            <div key={index} style={styles.conditionBlock}>
              <div style={styles.conditionHeader}>
                <input
                  type="text"
                  value={condition.title}
                  onChange={(e) => handleConditionChange(index, 'title', e.target.value)}
                  style={styles.titleInput}
                />
                {conditions.length > 1 && (
                  <button
                    onClick={() => handleRemoveCondition(index)}
                    style={styles.removeBtn}
                  >
                    Remove
                  </button>
                )}
              </div>
              <textarea
                value={condition.content}
                onChange={(e) => handleConditionChange(index, 'content', e.target.value)}
                style={styles.textarea}
                rows="5"
                placeholder="Enter condition details..."
              />
            </div>
          ))}

          <button onClick={handleAddCondition} style={styles.addBtn}>
            + Add New Condition
          </button>
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
    width: '900px',
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
  conditionBlock: {
    marginBottom: '25px',
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    backgroundColor: '#f9f9f9'
  },
  conditionHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px'
  },
  titleInput: {
    flex: 1,
    padding: '10px',
    fontSize: '15px',
    fontWeight: 'bold',
    border: '1px solid #ccc',
    borderRadius: '4px',
    marginRight: '10px'
  },
  textarea: {
    width: '100%',
    padding: '12px',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontFamily: 'Arial, sans-serif',
    resize: 'vertical',
    lineHeight: '1.5'
  },
  removeBtn: {
    padding: '8px 15px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px'
  },
  addBtn: {
    padding: '12px 24px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '15px',
    fontWeight: '600',
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

export default EditGeneralConditionsModal;