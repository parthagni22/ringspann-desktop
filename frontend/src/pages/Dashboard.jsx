import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deleteModal, setDeleteModal] = useState({ show: false, project: null });

  useEffect(() => {
    const currentUser = localStorage.getItem('currentUser');
    if (!currentUser) {
      navigate('/login');
      return;
    }
    setUser(JSON.parse(currentUser));
    loadRecentProjects();
  }, [navigate]);

  const loadRecentProjects = async () => {
    try {
      const response = await window.eel.get_recent_projects(10)();
      if (response.success) {
        setProjects(response.data);
      }
    } catch (error) {
      console.error('Failed to load projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await window.eel.logout()();
    localStorage.removeItem('currentUser');
    navigate('/login');
  };

  const handleNewProject = () => {
    // Navigate to new quotation form
    navigate('/quotation/new');
  };

  

  const handleAnalytics = () => {
    // Navigate to analytics
    navigate('/analytics');
  };

  const handleProjectClick = (project) => {
    // Navigate to customer requirements page with project ID
    navigate(`/quotation/requirements/${project.id}`);
  };

  const confirmDelete = (project, e) => {
    e.stopPropagation();
    setDeleteModal({ show: true, project });
  };

  const handleDelete = async () => {
    if (!deleteModal.project) return;

    try {
      const response = await window.eel.delete_project(deleteModal.project.id)();
      
      if (response.success) {
        setProjects(projects.filter(p => p.id !== deleteModal.project.id));
        setDeleteModal({ show: false, project: null });
        alert('Project deleted successfully');
      } else {
        alert('Failed to delete project: ' + response.error);
      }
    } catch (error) {
      alert('Failed to delete project');
    }
  };

  if (!user) {
    return <div style={styles.loading}>Loading...</div>;
  }

  return (
    <div style={styles.container}>
      {/* Orange Header */}
      <div style={styles.header}>
        <div style={styles.headerContent}>
          <h1 style={styles.headerTitle}>Ringspann Industrial Suite</h1>
          <button onClick={handleLogout} style={styles.logoutBtn}>
            Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div style={styles.mainContent}>
        {/* Project Actions */}
        <div style={styles.actionsSection}>
          <h2 style={styles.sectionTitle}>Select Project Action</h2>
          <div style={styles.actionButtons}>
            <button onClick={handleNewProject} style={styles.actionBtn}>
              New
            </button>
            <button onClick={handleAnalytics} style={styles.actionBtn}>
              Analytics
            </button>
          </div>
        </div>

        {/* Recent Projects */}
        <div style={styles.projectsSection}>
          <h3 style={styles.projectsTitle}>Recent Projects</h3>
          <div style={styles.tableContainer}>
            <table style={styles.table}>
              <thead>
                <tr style={styles.tableHeader}>
                  <th style={styles.th}>Project Name</th>
                  <th style={styles.th}>Quotation No.</th>
                  <th style={styles.th}>Customer</th>
                  <th style={styles.th}>Last Modified</th>
                  <th style={styles.th}>Status</th>
                  <th style={styles.th}>Date Created</th>
                  <th style={styles.th}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan="7" style={styles.noData}>Loading...</td>
                  </tr>
                ) : projects.length === 0 ? (
                  <tr>
                    <td colSpan="7" style={styles.noData}>No projects found</td>
                  </tr>
                ) : (
                  projects.map((project) => (
                    <tr
                      key={project.id}
                      onClick={() => handleProjectClick(project)}
                      style={styles.tableRow}
                    >
                      <td style={styles.td}>{project.name}</td>
                      <td style={styles.td}>{project.quotationNo}</td>
                      <td style={styles.td}>{project.customer}</td>
                      <td style={styles.td}>{project.lastModified}</td>
                      <td style={styles.td}>{project.status}</td>
                      <td style={styles.td}>{project.dateCreated}</td>
                      <td style={styles.td}>
                        <button
                          onClick={(e) => confirmDelete(project, e)}
                          style={styles.deleteBtn}
                        >
                          🗑️
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {deleteModal.show && (
        <div style={styles.modalOverlay}>
          <div style={styles.modal}>
            <h3 style={styles.modalTitle}>Confirm Delete</h3>
            <p style={styles.modalText}>
              This quotation will be permanently deleted. Are you sure?
            </p>
            <div style={styles.modalButtons}>
              <button
                onClick={() => setDeleteModal({ show: false, project: null })}
                style={styles.cancelBtn}
              >
                Cancel
              </button>
              <button onClick={handleDelete} style={styles.confirmDeleteBtn}>
                Delete
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <div style={styles.footer}>
        <span>Analytics dashboard opened.</span>
      </div>
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    background: '#f5f5f5',
  },
  header: {
    background: '#e85d04',
    padding: '16px 0',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  headerContent: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: '0 20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerTitle: {
    color: 'white',
    fontSize: '28px',
    fontWeight: 'bold',
    margin: 0,
  },
  logoutBtn: {
    background: '#2c3e50',
    color: 'white',
    border: 'none',
    padding: '10px 24px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: 600,
  },
  mainContent: {
    flex: 1,
    maxWidth: '1400px',
    margin: '0 auto',
    padding: '40px 20px',
    width: '100%',
  },
  actionsSection: {
    background: 'white',
    borderRadius: '8px',
    padding: '40px',
    marginBottom: '30px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    textAlign: 'center',
  },
  sectionTitle: {
    fontSize: '32px',
    fontWeight: 600,
    color: '#333',
    marginBottom: '30px',
  },
  actionButtons: {
    display: 'flex',
    justifyContent: 'center',
    gap: '20px',
  },
  actionBtn: {
    background: '#e85d04',
    color: 'white',
    border: 'none',
    padding: '16px 40px',
    fontSize: '18px',
    fontWeight: 600,
    borderRadius: '4px',
    cursor: 'pointer',
    minWidth: '120px',
  },
  projectsSection: {
    background: 'white',
    borderRadius: '8px',
    padding: '30px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  projectsTitle: {
    fontSize: '20px',
    fontWeight: 600,
    color: '#333',
    marginBottom: '20px',
    paddingBottom: '10px',
    borderBottom: '2px solid #e0e0e0',
  },
  tableContainer: {
    overflowX: 'auto',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  tableHeader: {
    background: '#f8f9fa',
  },
  th: {
    padding: '12px',
    textAlign: 'left',
    fontWeight: 600,
    color: '#555',
    borderBottom: '2px solid #dee2e6',
  },
  tableRow: {
    cursor: 'pointer',
    transition: 'background 0.2s',
  },
  td: {
    padding: '12px',
    borderBottom: '1px solid #dee2e6',
    color: '#333',
  },
  deleteBtn: {
    background: 'transparent',
    border: 'none',
    cursor: 'pointer',
    fontSize: '18px',
    padding: '4px 8px',
  },
  noData: {
    padding: '40px',
    textAlign: 'center',
    color: '#999',
  },
  loading: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    fontSize: '18px',
  },
  footer: {
    background: '#2c3e50',
    color: 'white',
    padding: '12px 20px',
    fontSize: '13px',
  },
  modalOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
  },
  modal: {
    background: 'white',
    borderRadius: '8px',
    padding: '30px',
    maxWidth: '400px',
    width: '90%',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
  modalTitle: {
    fontSize: '20px',
    fontWeight: 600,
    color: '#333',
    marginBottom: '15px',
  },
  modalText: {
    fontSize: '14px',
    color: '#666',
    marginBottom: '25px',
  },
  modalButtons: {
    display: 'flex',
    gap: '10px',
    justifyContent: 'flex-end',
  },
  cancelBtn: {
    background: '#6c757d',
    color: 'white',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  confirmDeleteBtn: {
    background: '#dc3545',
    color: 'white',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
};

export default Dashboard;