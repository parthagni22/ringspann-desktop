import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import TechnicalQuoteModal from '../components/TechnicalQuoteModal';

const TechnicalQuote = () => {
  const { projectId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [project, setProject] = useState(null);
  const [requirements, setRequirements] = useState([]);
  const [technicalQuotes, setTechnicalQuotes] = useState({});
  const [selectedRequirement, setSelectedRequirement] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedRows, setSelectedRows] = useState(new Set());
  
  const [pdfMetadata, setPdfMetadata] = useState({
    quote_number: '',
    project_name: '',
    end_user_name: '',
    epc_location: '',
    oem_name: '',
    prepared_by: 'Ringspannn',
    date: new Date().toISOString().split('T')[0]
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
        
        // Parse requirements
        const reqs = JSON.parse(proj.requirements_data || '[]');
        setRequirements(reqs);
        
        // Load existing technical quotes
        const quotesResult = await window.eel.get_technical_quotes(proj.quotation_number)();
        if (quotesResult.success) {
          setTechnicalQuotes(quotesResult.data || {});
        }
        
        // Set PDF metadata
        setPdfMetadata(prev => ({
          ...prev,
          quote_number: proj.quotation_number
        }));
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error loading project:', error);
      setLoading(false);
    }
  };

  const calculateProgress = (requirement) => {
    const reqId = requirement.id || requirement.partType;
    const quote = technicalQuotes[reqId];
    
    if (!quote || !quote.technical_fields) {
      return 0;
    }
    
    // Get technical field definitions for this part type
    const partType = requirement.partType;
    const TECHNICAL_FIELDS = {
      "Brake Quotation": 11,
      "Backstop Quotation": 5,
      "Coupling and Torque Limiter Quotation": 4,
      "Locking Element for Conveyor Quotation": 11,
      "Over Running Clutch Quotation": 3
    };
    
    const totalFields = TECHNICAL_FIELDS[partType] || 0;
    if (totalFields === 0) return 0;
    
    // Count filled fields
    const fields = Object.values(quote.technical_fields);
    const filled = fields.filter(v => v && v.toString().trim() !== '').length;
    
    return Math.round((filled / totalFields) * 100);
  };

  const handleRowDoubleClick = (requirement) => {
    setSelectedRequirement(requirement);
    setIsModalOpen(true);
  };

  const handleSaveTechnicalQuote = async (reqId, quoteData) => {
    try {
      const result = await window.eel.save_technical_quote(
        project.quotation_number,
        reqId,
        quoteData
      )();
      
      if (result.success) {
        setTechnicalQuotes(prev => ({
          ...prev,
          [reqId]: quoteData
        }));
        alert('Technical quote saved successfully!');
      } else {
        alert('Failed to save: ' + result.message);
      }
    } catch (error) {
      console.error('Error saving:', error);
      alert('Failed to save technical quote');
    }
  };

  const handleGeneratePDF = async () => {
    try {
      const result = await window.eel.generate_technical_pdf(
        project.quotation_number,
        pdfMetadata,
        requirements,
        technicalQuotes
      )();
      
      if (result.success) {
        alert(`Technical PDF generated!\n\nFile: ${result.filename}\nLocation: ${result.filepath}`);
      } else {
        alert('PDF generation failed: ' + result.message);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to generate PDF');
    }
  };

  const handleOpenSelectedRow = () => {
    if (selectedRows.size !== 1) {
      alert('Please select exactly one row');
      return;
    }
    
    const index = Array.from(selectedRows)[0];
    handleRowDoubleClick(requirements[index]);
  };

  const handleDeleteSelectedRow = () => {
    if (selectedRows.size === 0) {
      alert('Please select rows to delete');
      return;
    }
    
    if (window.confirm('Delete selected technical quotes?')) {
      const newReqs = requirements.filter((_, idx) => !selectedRows.has(idx));
      setRequirements(newReqs);
      setSelectedRows(new Set());
    }
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

  if (loading) {
    return <div style={styles.loading}>Loading...</div>;
  }

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
          <h2 style={styles.title}>Technical Quotes Summary</h2>

          {/* Add Product Type Dropdown */}
          <div style={styles.addSection}>
            <label style={styles.label}>Add Product Type:</label>
            <select style={styles.select}>
              <option>Choose product type</option>
            </select>
            <button style={styles.addBtn}>+ Add Product Type</button>
          </div>

          {/* Part Type Progress Table */}
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Part Type Progress</h3>
            <p style={styles.subtitle}>Customer Requirements and Technical Quote progress</p>
            
            <div style={styles.tableContainer}>
              <table style={styles.table}>
                <thead>
                  <tr>
                    <th style={styles.th}>Select</th>
                    <th style={styles.th}>SL No.</th>
                    <th style={styles.th}>Part Type</th>
                    <th style={styles.th}>Customer Requirements Progress</th>
                    <th style={styles.th}>Technical Quote Progress</th>
                  </tr>
                </thead>
                <tbody>
                  {requirements.length === 0 ? (
                    <tr>
                      <td colSpan="5" style={styles.noData}>No requirements found</td>
                    </tr>
                  ) : (
                    requirements.map((req, index) => (
                      <tr
                        key={index}
                        onDoubleClick={() => handleRowDoubleClick(req)}
                        style={styles.row}
                      >
                        <td style={styles.td}>
                          <input
                            type="checkbox"
                            checked={selectedRows.has(index)}
                            onChange={() => toggleRowSelection(index)}
                            onClick={(e) => e.stopPropagation()}
                            style={styles.checkbox}
                          />
                        </td>
                        <td style={styles.td}>{index + 1}</td>
                        <td style={styles.td}>{req.partType || 'N/A'}</td>
                        <td style={styles.tdProgress}>
                          <div style={styles.progressBar}>
                            <div style={{...styles.progressFill, width: '100%', backgroundColor: '#28a745'}}>
                              100% Complete
                            </div>
                          </div>
                        </td>
                        <td style={styles.tdProgress}>
                          <div style={styles.progressBar}>
                            <div style={{
                              ...styles.progressFill,
                              width: `${calculateProgress(req)}%`,
                              backgroundColor: calculateProgress(req) === 100 ? '#28a745' : '#007bff'
                            }}>
                              {calculateProgress(req)}% Complete
                            </div>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

            <p style={styles.hint}>
              Technical Quote Summary screen ready. Double-click a row for details.
            </p>
          </div>

          {/* PDF Generation Details */}
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>PDF Generation Details</h3>
            
            <div style={styles.formGrid}>
              <div style={styles.formCol}>
                <div style={styles.formRow}>
                  <label style={styles.label}>Quote number:</label>
                  <input
                    type="text"
                    value={pdfMetadata.quote_number}
                    onChange={(e) => setPdfMetadata({...pdfMetadata, quote_number: e.target.value})}
                    style={styles.input}
                  />
                </div>
                <div style={styles.formRow}>
                  <label style={styles.label}>End-user name / location:</label>
                  <input
                    type="text"
                    value={pdfMetadata.end_user_name}
                    onChange={(e) => setPdfMetadata({...pdfMetadata, end_user_name: e.target.value})}
                    style={styles.input}
                  />
                </div>
                <div style={styles.formRow}>
                  <label style={styles.label}>OEM name / location:</label>
                  <input
                    type="text"
                    value={pdfMetadata.oem_name}
                    onChange={(e) => setPdfMetadata({...pdfMetadata, oem_name: e.target.value})}
                    style={styles.input}
                  />
                </div>
                <div style={styles.formRow}>
                  <label style={styles.label}>Date:</label>
                  <input
                    type="date"
                    value={pdfMetadata.date}
                    onChange={(e) => setPdfMetadata({...pdfMetadata, date: e.target.value})}
                    style={styles.input}
                  />
                </div>
              </div>

              <div style={styles.formCol}>
                <div style={styles.formRow}>
                  <label style={styles.label}>Project name:</label>
                  <input
                    type="text"
                    value={pdfMetadata.project_name}
                    onChange={(e) => setPdfMetadata({...pdfMetadata, project_name: e.target.value})}
                    style={styles.input}
                  />
                </div>
                <div style={styles.formRow}>
                  <label style={styles.label}>EPC / location:</label>
                  <input
                    type="text"
                    value={pdfMetadata.epc_location}
                    onChange={(e) => setPdfMetadata({...pdfMetadata, epc_location: e.target.value})}
                    style={styles.input}
                  />
                </div>
                <div style={styles.formRow}>
                  <label style={styles.label}>Prepared by:</label>
                  <input
                    type="text"
                    value={pdfMetadata.prepared_by}
                    onChange={(e) => setPdfMetadata({...pdfMetadata, prepared_by: e.target.value})}
                    style={styles.input}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div style={styles.buttonGroup}>
            <button style={styles.btn}>Generate Technical Quote</button>
            <button onClick={handleGeneratePDF} style={styles.btn}>Generate Technical PDF</button>
            <button onClick={handleOpenSelectedRow} style={styles.btn}>Open Selected Row</button>
            <button onClick={handleDeleteSelectedRow} style={styles.btnDanger}>Delete Selected Row</button>
          </div>
        </div>
      </div>

      {/* Technical Quote Modal */}
      {isModalOpen && (
        <TechnicalQuoteModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          requirement={selectedRequirement}
          existingQuote={technicalQuotes[selectedRequirement?.id || selectedRequirement?.partType]}
          onSave={handleSaveTechnicalQuote}
        />
      )}

      {/* Footer */}
      <div style={styles.footer}>
        <span>System: Ready</span>
        <span>Real-time Data Stream: Active</span>
        <span>{new Date().toLocaleString()}</span>
      </div>
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
    marginBottom: '16px'
  },
  card: {
    backgroundColor: 'white',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    borderRadius: '8px',
    padding: '32px'
  },
  title: {
    fontSize: '28px',
    fontWeight: 'bold',
    marginBottom: '24px',
    color: '#1f2937'
  },
  addSection: {
    display: 'flex',
    gap: '16px',
    alignItems: 'center',
    marginBottom: '32px',
    padding: '16px',
    backgroundColor: '#f3f4f6',
    borderRadius: '4px'
  },
  label: {
    fontWeight: '600',
    fontSize: '14px'
  },
  select: {
    flex: 1,
    padding: '8px',
    border: '1px solid #d1d5db',
    borderRadius: '4px'
  },
  addBtn: {
    backgroundColor: '#2563eb',
    color: 'white',
    padding: '8px 16px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  section: {
    marginBottom: '32px'
  },
  sectionTitle: {
    fontSize: '20px',
    fontWeight: '600',
    marginBottom: '8px'
  },
  subtitle: {
    color: '#6b7280',
    marginBottom: '16px'
  },
  tableContainer: {
    border: '1px solid #d1d5db',
    borderRadius: '4px',
    overflow: 'auto'
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse'
  },
  th: {
    backgroundColor: '#f3f4f6',
    padding: '12px',
    textAlign: 'left',
    fontWeight: '600',
    borderBottom: '1px solid #d1d5db'
  },
  row: {
    cursor: 'pointer',
    transition: 'background 0.2s'
  },
  td: {
    padding: '12px',
    borderBottom: '1px solid #e5e7eb'
  },
  tdProgress: {
    padding: '12px',
    borderBottom: '1px solid #e5e7eb',
    minWidth: '200px'
  },
  checkbox: {
    width: '18px',
    height: '18px',
    cursor: 'pointer'
  },
  progressBar: {
    width: '100%',
    height: '32px',
    backgroundColor: '#e5e7eb',
    borderRadius: '4px',
    overflow: 'hidden',
    position: 'relative'
  },
  progressFill: {
    height: '100%',
    color: 'white',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: '600',
    fontSize: '13px',
    transition: 'width 0.3s'
  },
  noData: {
    padding: '32px',
    textAlign: 'center',
    color: '#9ca3af'
  },
  hint: {
    marginTop: '12px',
    fontSize: '13px',
    color: '#6b7280',
    fontStyle: 'italic'
  },
  formGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '24px'
  },
  formCol: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px'
  },
  formRow: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px'
  },
  input: {
    padding: '8px',
    border: '1px solid #d1d5db',
    borderRadius: '4px',
    fontSize: '14px'
  },
  buttonGroup: {
    display: 'flex',
    gap: '16px',
    marginTop: '32px'
  },
  btn: {
    flex: 1,
    backgroundColor: '#2563eb',
    color: 'white',
    padding: '12px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600'
  },
  btnDanger: {
    flex: 1,
    backgroundColor: '#dc2626',
    color: 'white',
    padding: '12px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600'
  },
  footer: {
    backgroundColor: '#1f2937',
    color: 'white',
    padding: '12px 24px',
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '13px'
  },
  loading: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh'
  }
};

export default TechnicalQuote;