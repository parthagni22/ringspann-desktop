import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

const PART_TYPES = [
  'Backstop Quotation',
  'Brake Quotation',
  'Coupling and Torque Limiter Quotation',
  'Locking Element for Conveyor Quotation',
  'Over Running Clutch Quotation'
];

const FIELD_DEFINITIONS = {
  "Brake Quotation": [
    { label: "SL No.", type: "text" },
    { label: "Tag Number", type: "text" },
    { label: "Application", type: "text" },
    { label: "Motor KW", type: "number" },
    { label: "Number of Drive", type: "number" },
    { label: "Stopping Torque (Mn) Min (Nm)", type: "number" },
    { label: "Stopping Torque (Mn) Max (Nm)", type: "number" },
    { label: "Speed at Brake Min (RPM)", type: "number" },
    { label: "Speed at Brake Rated (RPM)", type: "number" },
    { label: "Speed at Brake Max (RPM)", type: "number" },
    { label: "Stopping Time", type: "number" },
    { label: "Number of Braking Per Second", type: "number" },
    { label: "Number of Braking Per Hour", type: "number" },
    { label: "Number of Braking Per Day", type: "number" },
    { label: "Friction coefficient between brake and brake disc", type: "number" },
    { label: "Service Factor", type: "number" }
  ],
  "Backstop Quotation": [
    { label: "SL No.", type: "text" },
    { label: "Tag Number", type: "text" },
    { label: "Application", type: "text" },
    { label: "Shaft Diameter (mm)", type: "number" },
    { label: "Torque (Mn) Min (Nm)", type: "number" },
    { label: "Torque (Mn) Max (Nm)", type: "number" },
    { label: "Speed Min (RPM)", type: "number" },
    { label: "Speed Rated (RPM)", type: "number" },
    { label: "Speed Max (RPM)", type: "number" },
    { label: "Operating Hours (daily)", type: "number" },
    { label: "Service Factor", type: "number" }
  ],
  "Coupling and Torque Limiter Quotation": [
    { label: "SL No.", type: "text" },
    { label: "Tag Number", type: "text" },
    { label: "Application", type: "text" },
    { label: "Motor KW", type: "number" },
    { label: "Number of Drive", type: "number" },
    { label: "Torque (Mn) Min (Nm)", type: "number" },
    { label: "Torque (Mn) Max (Nm)", type: "number" },
    { label: "Speed at Coupling Min (RPM)", type: "number" },
    { label: "Speed at Coupling Rated (RPM)", type: "number" },
    { label: "Speed at Coupling Max (RPM)", type: "number" },
    { label: "Service Factor", type: "number" }
  ],
  "Locking Element for Conveyor Quotation": [
  { label: "SL No.", type: "text" },
  { label: "Pulley type", type: "text" },
  { label: "Tag number", type: "text" },
  { label: "Application", type: "text" },
  { label: "Pulley Qty", type: "number" },
  { label: "Hub material Yield strength (Re) N/mm2", type: "number" },
  { label: "Shaft diameter (d) mm", type: "number" },
  { label: "Outer diameter of pulley (D2) mm", type: "number" },
  
  // Running condition - 4 fields
  { label: "Tension tight side Running condition (T1) KN", type: "number" },
  { label: "Tension slack side Running condition (T2) KN", type: "number" },  
  
  
  // Starting condition - 4 fields
  { label: "Tension tight side Starting condition (T1) KN", type: "number" },
  { label: "Tension slack side Starting condition (T2) KN", type: "number" },
  
  
  { label: "Arm length (L) mm", type: "number" },
  { label: "Wrap angel (β) deg", type: "number" },
  
  { label: "start-up factor Running condition", type: "number" },  
  { label: "start-up factor starting condition", type: "number" },  
  
  { label: "Torque Running condition (M) Nm", type: "number" },
  { label: "Bending moment Running condition (Mb) Nm", type: "number" },
  { label: "Torque Starting condition (M) Nm", type: "number" },
  { label: "Bending moment Starting condition (Mb) Nm", type: "number" }
  ],
  
  "Over Running Clutch Quotation": [
    { label: "SL No.", type: "text" },
    { label: "Tag number", type: "text" },
    { label: "Application", type: "text" },
    { label: "Shaft diameter Main drive - Drive (mm)", type: "number" },
    { label: "Shaft diameter Main drive - Driven (mm)", type: "number" },
    { label: "Shaft diameter Auxiliary drive - Drive (mm)", type: "number" },
    { label: "Shaft diameter Auxiliary drive - Driven (mm)", type: "number" },
    { label: "Torque  Main drive - Min (Nm)", type: "number" },
    { label: "Torque Main drive - Max (Nm)", type: "number" },
    { label: "Torque Auxiliary drive - Min (Nm)", type: "number" },
    { label: "Torque Auxiliary drive - Max (Nm)", type: "number" },
    { label: "Speed Main drive - Min (RPM)", type: "number" },
    { label: "Speed Main drive - Rated (RPM)", type: "number" },
    { label: "Speed Main drive - Max (RPM)", type: "number" },
    { label: "Speed Auxiliary drive - Min (RPM)", type: "number" },
    { label: "Speed Auxiliary drive - Rated (RPM)", type: "number" },
    { label: "Speed Auxiliary drive - Max (RPM)", type: "number" },
    { label: "Operating hours - daily", type: "number" },
    { label: "Direction of rotation from drive side - Main drive", type: "text" },
    { label: "Direction of rotation from drive side - Auxiliary drive", type: "text" }
  ]
};

const CustomerRequirements = () => {
  const navigate = useNavigate();
  const { projectId } = useParams();
  const [user, setUser] = useState(null);
  const [customerName, setCustomerName] = useState('');
  const [quotationNumber, setQuotationNumber] = useState('');
  const [requirements, setRequirements] = useState([
    { id: 1, partType: '', fieldValues: {} }
  ]);

  useEffect(() => {
    const currentUser = localStorage.getItem('currentUser');
    if (!currentUser) {
      navigate('/login');
      return;
    }
    setUser(JSON.parse(currentUser));
    loadProjectData();
  }, [navigate, projectId]);

  const loadProjectData = async () => {
    try {
      const response = await window.eel.get_project_by_id(parseInt(projectId))();
      if (response.success) {
        setCustomerName(response.data.customer);
        setQuotationNumber(response.data.quotationNo);
        
        // Load existing requirements if available
        if (response.data.requirements_data) {
          const existingReqs = JSON.parse(response.data.requirements_data);
          if (existingReqs && existingReqs.length > 0) {
            setRequirements(existingReqs.map((req, idx) => ({
              id: idx + 1,
              partType: req.partType || req.part_type || '',
              fieldValues: req.fieldValues || {}
            })));
          }
        }
      }
    } catch (error) {
      console.error('Failed to load project:', error);
    }
  };

  const addRequirement = () => {
    const newId = Math.max(...requirements.map(r => r.id), 0) + 1;
    setRequirements([...requirements, { id: newId, partType: '', fieldValues: {} }]);
  };

  const deleteRequirement = (id) => {
    if (requirements.length === 1) {
      alert('At least one requirement is needed');
      return;
    }
    setRequirements(requirements.filter(r => r.id !== id));
  };

  const updateRequirement = (id, field, value) => {
    setRequirements(requirements.map(r => 
      r.id === id ? { ...r, [field]: value, ...(field === 'partType' ? { fieldValues: {} } : {}) } : r
    ));
  };

  const updateFieldValue = (reqId, fieldLabel, value) => {
    setRequirements(requirements.map(r => 
      r.id === reqId ? { ...r, fieldValues: { ...r.fieldValues, [fieldLabel]: value } } : r
    ));
  };

  const saveRequirements = async () => {
    try {
      const response = await window.eel.save_requirements(parseInt(projectId), requirements)();
      if (response.success) {
        alert('Requirements saved successfully');
      }
    } catch (error) {
      alert('Failed to save requirements');
    }
  };

  const validateRequirements = () => {
    for (const req of requirements) {
      if (!req.partType) {
        alert('Please select a part type for all requirements');
        return false;
      }
    }
    return true;
  };

  const handleProceedCommercial = async () => {
    if (!validateRequirements()) return;
    await saveRequirements();
    navigate(`/quotation/commercial/${projectId}`);
  };

  const handleProceedTechnical = async () => {
    if (!validateRequirements()) return;
    await saveRequirements();
    navigate(`/quotation/technical/${projectId}`);
  };

  const handleAnalytics = () => {
    navigate('/analytics');
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

      {/* Sub Header */}
      <div style={styles.subHeader}>
        <button onClick={() => navigate('/dashboard')} style={styles.backBtn}>
          &lt; Back
        </button>
        <span style={styles.projectStatus}>New Project (Current)</span>
        <span style={styles.projectTitle}>
          Customer Requirements - {quotationNumber}
        </span>
        <span style={styles.savedStatus}>Open Saved (Current)</span>
      </div>

      {/* Main Content */}
      <div style={styles.mainContent}>
        {/* Customer Details */}
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>Customer Details</h3>
          <div style={styles.formGroup}>
            <label style={styles.label}>Customer Name:</label>
            <input
              type="text"
              value={customerName}
              onChange={(e) => setCustomerName(e.target.value)}
              style={styles.input}
            />
          </div>
          <button onClick={addRequirement} style={styles.addBtn}>
            + Add Customer Requirement
          </button>
        </div>

        {/* Requirements */}
        <div style={styles.requirementsContainer}>
          {requirements.map((req, index) => (
            <div key={req.id} style={styles.requirementCard}>
              <div style={styles.requirementHeader}>
                <h4 style={styles.requirementTitle}>
                  Customer Requirement {index + 1}
                </h4>
                {requirements.length > 1 && (
                  <button
                    onClick={() => deleteRequirement(req.id)}
                    style={styles.deleteBtn}
                  >
                    🗑️
                  </button>
                )}
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Select Part Type:</label>
                <select
                  value={req.partType}
                  onChange={(e) => updateRequirement(req.id, 'partType', e.target.value)}
                  style={styles.select}
                >
                  <option value="">Choose part type</option>
                  {PART_TYPES.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              {/* Dynamic Fields based on part type */}
              {req.partType && FIELD_DEFINITIONS[req.partType] && (
                <div style={styles.dynamicFields}>
                  <div style={styles.fieldsGrid}>
                    {FIELD_DEFINITIONS[req.partType].map((field, idx) => (
                      <div key={idx} style={styles.fieldGroup}>
                        <label style={styles.fieldLabel}>{field.label}</label>
                        <input
                          type={field.type}
                          value={req.fieldValues[field.label] || ''}
                          onChange={(e) => updateFieldValue(req.id, field.label, e.target.value)}
                          style={styles.fieldInput}
                          placeholder={`Enter ${field.label.toLowerCase()}`}
                        />
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Proceed Buttons */}
        <div style={styles.proceedSection}>
          <h4 style={styles.proceedTitle}>Proceed to Quote:</h4>
          <div style={styles.proceedButtons}>
            <button onClick={handleProceedCommercial} style={styles.proceedBtn}>
              Commercial Quote
            </button>
            <button onClick={handleProceedTechnical} style={styles.proceedBtn}>
              Technical Quote
            </button>
            <button onClick={handleAnalytics} style={styles.analyticsBtn}>
              Analytics
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: { minHeight: '100vh', display: 'flex', flexDirection: 'column', background: '#f5f5f5' },
  header: { background: '#e85d04', padding: '16px 0' },
  headerContent: { maxWidth: '1400px', margin: '0 auto', padding: '0 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  headerTitle: { color: 'white', fontSize: '28px', fontWeight: 'bold', margin: 0 },
  headerRight: { display: 'flex', gap: '15px' },
  userBadge: { background: 'white', color: '#333', padding: '6px 16px', borderRadius: '4px', fontSize: '14px' },
  statusBadge: { background: 'white', color: '#28a745', padding: '6px 16px', borderRadius: '4px', fontSize: '14px' },
  subHeader: { background: '#f8f9fa', padding: '12px 20px', display: 'flex', gap: '15px', alignItems: 'center', borderBottom: '1px solid #dee2e6' },
  backBtn: { background: '#007bff', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', fontSize: '14px' },
  projectStatus: { background: '#007bff', color: 'white', padding: '6px 16px', borderRadius: '4px', fontSize: '13px' },
  projectTitle: { flex: 1, fontSize: '16px', fontWeight: 600, color: '#333' },
  savedStatus: { background: '#007bff', color: 'white', padding: '6px 16px', borderRadius: '4px', fontSize: '13px' },
  mainContent: { flex: 1, maxWidth: '1400px', margin: '0 auto', padding: '30px 20px', width: '100%' },
  section: { background: 'white', borderRadius: '8px', padding: '30px', marginBottom: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  sectionTitle: { fontSize: '24px', fontWeight: 600, color: '#333', marginBottom: '20px' },
  formGroup: { marginBottom: '20px' },
  label: { display: 'block', fontSize: '14px', fontWeight: 500, color: '#333', marginBottom: '8px' },
  input: { width: '100%', padding: '12px', fontSize: '14px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box' },
  select: { width: '100%', padding: '12px', fontSize: '14px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box', background: 'white' },
  addBtn: { background: '#007bff', color: 'white', border: 'none', padding: '12px 24px', borderRadius: '4px', cursor: 'pointer', fontSize: '14px', fontWeight: 600 },
  requirementsContainer: { marginBottom: '30px' },
  requirementCard: { background: 'white', borderRadius: '8px', padding: '30px', marginBottom: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', border: '1px solid #dee2e6' },
  requirementHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', paddingBottom: '15px', borderBottom: '2px solid #e9ecef' },
  requirementTitle: { fontSize: '18px', fontWeight: 600, color: '#333', margin: 0 },
  deleteBtn: { background: '#dc3545', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', fontSize: '16px' },
  dynamicFields: { marginTop: '20px', padding: '20px', background: '#f8f9fa', borderRadius: '4px' },
  fieldsGrid: { display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' },
  fieldGroup: { display: 'flex', flexDirection: 'column' },
  fieldLabel: { fontSize: '13px', fontWeight: 500, color: '#555', marginBottom: '6px' },
  fieldInput: { padding: '10px', fontSize: '14px', border: '1px solid #ccc', borderRadius: '4px' },
  infoText: { color: '#666', fontSize: '14px', margin: 0, fontStyle: 'italic' },
  proceedSection: { background: 'white', borderRadius: '8px', padding: '30px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
  proceedTitle: { fontSize: '18px', fontWeight: 600, color: '#333', marginBottom: '20px', textAlign: 'center' },
  proceedButtons: { display: 'flex', gap: '15px', justifyContent: 'center' },
  proceedBtn: { background: '#007bff', color: 'white', border: 'none', padding: '14px 32px', fontSize: '16px', fontWeight: 600, borderRadius: '4px', cursor: 'pointer' },
  analyticsBtn: { background: '#007bff', color: 'white', border: 'none', padding: '14px 32px', fontSize: '16px', fontWeight: 600, borderRadius: '4px', cursor: 'pointer', flex: 1, maxWidth: '800px' },
  loading: { display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', fontSize: '18px' },
};

export default CustomerRequirements;