import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import EditTermsModal from '../components/EditTermsModal';
import EditGeneralConditionsModal from '../components/EditGeneralConditionsModal';

const CommercialQuote = () => {
  const { projectId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [project, setProject] = useState(null);
  const [selectedRows, setSelectedRows] = useState(new Set());
  const [isTermsModalOpen, setIsTermsModalOpen] = useState(false);
  const [currentTerms, setCurrentTerms] = useState('');
  const [isGeneralConditionsModalOpen, setIsGeneralConditionsModalOpen] = useState(false);
  const [currentGeneralConditions, setCurrentGeneralConditions] = useState('');
  
  const [formData, setFormData] = useState({
    to: '',
    attn: '',
    email_to: '',
    your_inquiry_ref: '',
    pages: 1,
    your_partner: '',
    mobile_no: '',
    fax_no: '',
    email_partner: '',
    inquiry_date: new Date().toISOString().split('T')[0],
    quotation_date: new Date().toISOString().split('T')[0],
    items: []
  });

  useEffect(() => {
    loadProjectData();
  }, [projectId]);

  const loadProjectData = async () => {
    try {
      const result = await window.eel.get_project_by_id(parseInt(projectId))();
      
      if (result.success) {
        const proj = result.data;
        setProject(proj);
        
        // Get current user
        const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
        
        // Try to load existing commercial quote
        const quoteResult = await window.eel.get_commercial_quote(proj.quotation_number)();
        
        if (quoteResult.success && quoteResult.data) {
          // Load existing quote data
          const quote = quoteResult.data;
          setFormData({
            to: quote.to || '',
            attn: quote.attn || '',
            email_to: quote.email_to || '',
            your_inquiry_ref: quote.your_inquiry_ref || '',
            pages: quote.pages || 1,
            your_partner: quote.your_partner || 'RINGSPANN',
            mobile_no: quote.mobile_no || '',
            fax_no: quote.fax_no || '',
            email_partner: quote.email_partner || currentUser.username || 'parth@ringspann.com',
            inquiry_date: quote.inquiry_date || new Date().toISOString().split('T')[0],
            quotation_date: quote.quotation_date || new Date().toISOString().split('T')[0],
            items: quote.items || []
          });
        } else {
          // New quote - load from requirements
          const requirements = JSON.parse(proj.requirements_data || '[]');
          console.log('Requirements loaded:', requirements);
          
          const items = requirements.map((req, index) => ({
            sr_no: index + 1,
            part_type: req.partType || req.part_type || 'N/A',
            description: `Customer: ${proj.customer_name} - Products: ${req.partType || req.part_type || 'N/A'}`,
            unit_price: 0.0,
            unit: 0,
            total_price: 0.0
          }));
          
          if (items.length === 0) {
            items.push({
              sr_no: 1,
              part_type: '',
              description: '',
              unit_price: 0.0,
              unit: 0,
              total_price: 0.0
            });
            items.push({
              sr_no: 2,
              part_type: '',
              description: '',
              unit_price: 0.0,
              unit: 0,
              total_price: 0.0
            });
          }
          
          setFormData(prev => ({
            ...prev,
            your_partner: 'RINGSPANN',
            email_partner: currentUser.username || 'parth@ringspann.com',
            items
          }));
        }
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error loading project:', error);
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleItemChange = (index, field, value) => {
    const newItems = [...formData.items];
    newItems[index][field] = value;
    
    if (field === 'unit_price' || field === 'unit') {
      const unitPrice = parseFloat(newItems[index].unit_price) || 0;
      const unit = parseFloat(newItems[index].unit) || 0;
      newItems[index].total_price = unitPrice * unit;
    }
    
    setFormData(prev => ({
      ...prev,
      items: newItems
    }));
  };

  const addRow = () => {
    const newItems = [...formData.items];
    newItems.push({
      sr_no: newItems.length + 1,
      part_type: '',
      description: '',
      unit_price: 0.0,
      unit: 0,
      total_price: 0.0
    });
    setFormData(prev => ({
      ...prev,
      items: newItems
    }));
  };

  const deleteSelectedRows = () => {
    if (selectedRows.size === 0) {
      alert('Please select rows to delete');
      return;
    }
    
    const newItems = formData.items
      .filter((_, index) => !selectedRows.has(index))
      .map((item, index) => ({
        ...item,
        sr_no: index + 1
      }));
    
    setFormData(prev => ({
      ...prev,
      items: newItems
    }));
    setSelectedRows(new Set());
  };

  const toggleRowSelection = (index) => {
    const newSelected = new Set(selectedRows);
    if (newSelected.has(index)) {
      newSelected.delete(index);
    } else {
      newSelected.add(index);
    }
    setSelectedRows(newSelected);
  };

  const saveCommercialQuote = async () => {
    try {
      // Check if quote already exists
      const checkResult = await window.eel.get_commercial_quote(project.quotation_number)();
      
      let shouldSave = true;
      if (checkResult.success && checkResult.data) {
        // Quote exists - show confirmation
        shouldSave = window.confirm(
          'This quotation already exists. Updating will permanently change the previous data.\n\n' +
          'Do you want to continue with the update?'
        );
      }
      
      if (!shouldSave) return;
      
      // Save to database
      const saveResult = await window.eel.save_commercial_quote(
        parseInt(projectId),
        project.quotation_number,
        formData
      )();
      
      if (!saveResult.success) {
        alert('Error saving: ' + saveResult.message);
        return;
      }
      
      alert('Commercial quote saved successfully!');
      
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to save commercial quote');
    }
  };

  const generatePDF = async () => {
    try {
      const pdfResult = await window.eel.generate_commercial_pdf(
        project.quotation_number,
        formData
      )();
      
      if (pdfResult.success) {
        alert(`PDF generated successfully!\n\nFile: ${pdfResult.filename}\nLocation: ${pdfResult.filepath}`);
      } else {
        alert('PDF generation failed: ' + pdfResult.message);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to generate PDF');
    }
  };

  const handleOpenTermsModal = async () => {
    try {
      const result = await window.eel.get_quote_terms(project.quotation_number)();
      if (result.success && result.data) {
        setCurrentTerms(result.data);
      }
      setIsTermsModalOpen(true);
    } catch (error) {
      console.error('Error loading terms:', error);
      setIsTermsModalOpen(true);
    }
  };

  const handleSaveTerms = async (termsText) => {
    try {
      const result = await window.eel.save_custom_terms(project.quotation_number, termsText)();
      if (result.success) {
        setCurrentTerms(termsText);
        // Update formData to include saved terms
        setFormData(prev => ({ ...prev, terms: termsText }));
        alert('Terms & Conditions saved successfully!');
      } else {
        alert('Failed to save: ' + result.message);
      }
    } catch (error) {
      console.error('Error saving terms:', error);
      alert('Failed to save terms');
    }
  };

  const handleOpenGeneralConditionsModal = async () => {
    try {
      const result = await window.eel.get_general_conditions(project.quotation_number)();
      if (result.success && result.data) {
        setCurrentGeneralConditions(result.data);
      }
      setIsGeneralConditionsModalOpen(true);
    } catch (error) {
      console.error('Error loading general conditions:', error);
      setIsGeneralConditionsModalOpen(true);
    }
  };

  const handleSaveGeneralConditions = async (conditionsText) => {
    try {
      const result = await window.eel.save_general_conditions(project.quotation_number, conditionsText)();
      if (result.success) {
        setCurrentGeneralConditions(conditionsText);
        alert('General Conditions saved successfully!');
      } else {
        alert('Failed to save: ' + result.message);
      }
    } catch (error) {
      console.error('Error saving general conditions:', error);
      alert('Failed to save general conditions');
    }
  };

  const calculateSubtotal = () => {
    return formData.items.reduce((sum, item) => sum + (item.total_price || 0), 0);
  };

  if (loading) {
    return <div style={styles.loading}>Loading...</div>;
  }

  const subtotal = calculateSubtotal();

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <h1 style={styles.headerTitle}>Ringspann Industrial Suite</h1>
        <div style={styles.headerRight}>
          <span>User: parth@ringspann.com</span>
          <span style={styles.loggedIn}>● Logged In</span>
        </div>
      </div>

      {/* Main Content */}
      <div style={styles.mainContent}>
        <button onClick={() => navigate('/dashboard')} style={styles.backBtn}>
          &lt; Back
        </button>

        <div style={styles.card}>
          {/* Title with Logo */}
          <div style={styles.titleSection}>
            <div>
              <h2 style={styles.companyName}>RINGSPANN Power Transmission India Pvt. Ltd.</h2>
              <h3 style={styles.quotationTitle}>Quotation</h3>
            </div>
            <img 
              src="/assets/ringspann_logo2.png" 
              alt="Ringspann Logo" 
              style={styles.logo}
            />
          </div>

          {/* Form Fields */}
          <div style={styles.formGrid}>
            {/* Left Column */}
            <div style={styles.column}>
              <div style={styles.formRow}>
                <label style={styles.label}>To:</label>
                <input
                  type="text"
                  name="to"
                  value={formData.to}
                  onChange={handleInputChange}
                  style={styles.input}
                />
              </div>
              <div style={styles.formRow}>
                <label style={styles.label}>Attn.:</label>
                <input
                  type="text"
                  name="attn"
                  value={formData.attn}
                  onChange={handleInputChange}
                  style={styles.input}
                />
              </div>
              <div style={styles.formRow}>
                <label style={styles.label}>E-mail (To):</label>
                <input
                  type="email"
                  name="email_to"
                  value={formData.email_to}
                  onChange={handleInputChange}
                  style={styles.input}
                />
              </div>
              <div style={styles.formRow}>
                <label style={styles.label}>Your Inquiry Ref.:</label>
                <input
                  type="text"
                  name="your_inquiry_ref"
                  value={formData.your_inquiry_ref}
                  onChange={handleInputChange}
                  style={styles.input}
                />
              </div>
              <div style={styles.formRow}>
                <label style={styles.label}>Inquiry Date:</label>
                <input
                  type="date"
                  name="inquiry_date"
                  value={formData.inquiry_date}
                  onChange={handleInputChange}
                  style={styles.input}
                />
              </div>
              <div style={styles.formRow}>
                <label style={styles.label}>Quotation No.:</label>
                <input
                  type="text"
                  value={project?.quotation_number || ''}
                  disabled
                  style={styles.inputDisabled}
                />
              </div>
            </div>

            {/* Right Column */}
            <div style={styles.column}>
              <div style={styles.formRow}>
                <label style={styles.label}>Page(s):</label>
                <input
                  type="number"
                  name="pages"
                  value={formData.pages}
                  onChange={handleInputChange}
                  style={styles.input}
                />
              </div>
              <div style={styles.formRow}>
                <label style={styles.label}>Your Partner:</label>
                <input
                  type="text"
                  name="your_partner"
                  value={formData.your_partner}
                  onChange={handleInputChange}
                  style={styles.input}
                />
              </div>
              <div style={styles.formRow}>
                <label style={styles.label}>Mobile No.:</label>
                <input
                  type="text"
                  name="mobile_no"
                  value={formData.mobile_no}
                  onChange={handleInputChange}
                  style={styles.input}
                />
              </div>
              <div style={styles.formRow}>
                <label style={styles.label}>Fax No.:</label>
                <input
                  type="text"
                  name="fax_no"
                  value={formData.fax_no}
                  onChange={handleInputChange}
                  style={styles.input}
                />
              </div>
              <div style={styles.formRow}>
                <label style={styles.label}>E-mail (Partner):</label>
                <input
                  type="email"
                  name="email_partner"
                  value={formData.email_partner}
                  onChange={handleInputChange}
                  style={styles.input}
                />
              </div>
              <div style={styles.formRow}>
                <label style={styles.label}>Date:</label>
                <input
                  type="date"
                  name="quotation_date"
                  value={formData.quotation_date}
                  onChange={handleInputChange}
                  style={styles.input}
                />
              </div>
            </div>
          </div>

          {/* Items Table */}
          <div style={styles.tableContainer}>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>Select</th>
                  <th style={styles.th}>Sr. No</th>
                  <th style={styles.th}>Product / Part Type</th>
                  <th style={styles.th}>Description</th>
                  <th style={styles.th}>Unit Price INR</th>
                  <th style={styles.th}>Unit</th>
                  <th style={styles.th}>Total Price</th>
                </tr>
              </thead>
              <tbody>
                {formData.items.map((item, index) => (
                  <tr key={index}>
                    <td style={styles.td}>
                      <input
                        type="checkbox"
                        checked={selectedRows.has(index)}
                        onChange={() => toggleRowSelection(index)}
                        style={styles.checkbox}
                      />
                    </td>
                    <td style={styles.td}>{item.sr_no}</td>
                    <td style={styles.td}>{item.part_type || 'N/A'}</td>
                    <td style={styles.td}>
                      <input
                        type="text"
                        value={item.description}
                        onChange={(e) => handleItemChange(index, 'description', e.target.value)}
                        style={styles.cellInput}
                      />
                    </td>
                    <td style={styles.td}>
                      <input
                        type="number"
                        step="0.01"
                        value={item.unit_price}
                        onChange={(e) => handleItemChange(index, 'unit_price', e.target.value)}
                        style={styles.cellInputNumber}
                      />
                    </td>
                    <td style={styles.td}>
                      <input
                        type="number"
                        value={item.unit}
                        onChange={(e) => handleItemChange(index, 'unit', e.target.value)}
                        style={styles.cellInputNumber}
                      />
                    </td>
                    <td style={{...styles.td, textAlign: 'right', fontWeight: 'bold'}}>
                      {item.total_price.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Action Buttons */}
          <div style={styles.actionButtons}>
            <button onClick={addRow} style={styles.btn}>Add Row</button>
            <button onClick={deleteSelectedRows} style={styles.btn}>Delete Selected Row</button>
          </div>

          {/* Bottom Buttons */}
          <div style={styles.bottomButtons}>
            <button style={styles.btn} onClick={saveCommercialQuote}>Save Changes</button>
            <button style={styles.btn} onClick={handleOpenTermsModal}>Edit Terms & Conditions</button>
            <button style={styles.btn} onClick={handleOpenGeneralConditionsModal}>Edit General Conditions</button>
            <button onClick={generatePDF} style={styles.btn}>Generate Commercial PDF</button>
          </div>

          {/* Subtotal */}
          <div style={styles.subtotal}>
            <strong>Subtotal: ₹{subtotal.toFixed(2)}</strong>
          </div>
        </div>
      </div>

      {/* Edit Terms Modal */}
      <EditTermsModal 
        isOpen={isTermsModalOpen}
        onClose={() => setIsTermsModalOpen(false)}
        onSave={handleSaveTerms}
        currentTerms={currentTerms}
      />

      {/* Edit General Conditions Modal */}
      <EditGeneralConditionsModal 
        isOpen={isGeneralConditionsModalOpen}
        onClose={() => setIsGeneralConditionsModalOpen(false)}
        onSave={handleSaveGeneralConditions}
        currentConditions={currentGeneralConditions}
      />
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f9fafb',
    fontFamily: 'Arial, sans-serif'
  },
  header: {
    backgroundColor: '#f97316',
    color: 'white',
    padding: '16px 24px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  headerTitle: {
    fontSize: '24px',
    fontWeight: 'bold',
    margin: 0
  },
  headerRight: {
    display: 'flex',
    gap: '16px',
    alignItems: 'center'
  },
  loggedIn: {
    backgroundColor: '#dc2626',
    padding: '4px 12px',
    borderRadius: '4px'
  },
  mainContent: {
    padding: '24px',
    maxWidth: '1600px',
    margin: '0 auto'
  },
  backBtn: {
    backgroundColor: '#2563eb',
    color: 'white',
    padding: '8px 16px',
    borderRadius: '4px',
    border: 'none',
    cursor: 'pointer',
    marginBottom: '16px',
    fontSize: '14px'
  },
  card: {
    backgroundColor: 'white',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    borderRadius: '8px',
    padding: '32px'
  },
  titleSection: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '32px',
    paddingBottom: '16px',
    borderBottom: '2px solid #e5e7eb'
  },
  companyName: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#1f2937',
    margin: '0 0 8px 0'
  },
  quotationTitle: {
    fontSize: '22px',
    color: '#4b5563',
    margin: 0
  },
  logo: {
    height: '64px',
    width: 'auto'
  },
  formGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '32px',
    marginBottom: '32px'
  },
  column: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px'
  },
  formRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px'
  },
  label: {
    width: '160px',
    fontWeight: '600',
    fontSize: '14px',
    color: '#374151'
  },
  input: {
    flex: 1,
    border: '1px solid #9ca3af',
    borderRadius: '4px',
    padding: '8px 12px',
    fontSize: '14px'
  },
  inputDisabled: {
    flex: 1,
    border: '1px solid #9ca3af',
    borderRadius: '4px',
    padding: '8px 12px',
    fontSize: '14px',
    backgroundColor: '#f3f4f6',
    color: '#6b7280'
  },
  tableContainer: {
    border: '2px solid #9ca3af',
    borderRadius: '4px',
    marginBottom: '24px',
    overflow: 'auto'
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse'
  },
  th: {
    backgroundColor: '#e5e7eb',
    border: '1px solid #9ca3af',
    padding: '12px',
    textAlign: 'left',
    fontWeight: 'bold',
    fontSize: '14px'
  },
  td: {
    border: '1px solid #d1d5db',
    padding: '12px',
    fontSize: '14px'
  },
  checkbox: {
    width: '18px',
    height: '18px',
    cursor: 'pointer'
  },
  cellInput: {
    width: '100%',
    border: '1px solid #d1d5db',
    borderRadius: '4px',
    padding: '6px 8px',
    fontSize: '14px'
  },
  cellInputNumber: {
    width: '100%',
    border: '1px solid #d1d5db',
    borderRadius: '4px',
    padding: '6px 8px',
    fontSize: '14px',
    textAlign: 'right'
  },
  actionButtons: {
    display: 'flex',
    gap: '16px',
    marginBottom: '24px'
  },
  bottomButtons: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr 1fr',
    gap: '16px',
    marginTop: '32px'
  },
  btn: {
    backgroundColor: '#2563eb',
    color: 'white',
    padding: '12px 24px',
    borderRadius: '4px',
    border: 'none',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: '600'
  },
  subtotal: {
    marginTop: '24px',
    textAlign: 'right',
    fontSize: '20px',
    color: '#1f2937'
  },
  loading: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    fontSize: '20px'
  }
};

export default CommercialQuote;