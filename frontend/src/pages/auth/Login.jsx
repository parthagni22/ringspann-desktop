import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [loginData, setLoginData] = useState({
    username: '',
    password: ''
  });
  
  const [registerData, setRegisterData] = useState({
    name: '',
    username: '',  // Full email address
    region: 'EAST',
    password: '',
    confirmPassword: ''
  });

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await window.eel.login(
        loginData.username,
        loginData.password
      )();

      if (response.success) {
        localStorage.setItem('currentUser', JSON.stringify(response.data));
        navigate('/dashboard');
      } else {
        setError(response.error || 'Login failed');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!registerData.name.trim()) {
      setError('Name is required');
      return;
    }

    if (!registerData.username.trim()) {
      setError('Email ID is required');
      return;
    }

    // VALIDATE: Must end with @ringspann.com
    if (!registerData.username.endsWith('@ringspann.com')) {
      setError('Email ID must end with @ringspann.com');
      return;
    }

    if (registerData.password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    if (registerData.password !== registerData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      const response = await window.eel.register_user(
        registerData.name,
        registerData.username,  // Send complete email as-is
        registerData.region,
        registerData.password
      )();

      if (response.success) {
        alert('Registration successful! Please login.');
        setIsLogin(true);
        setRegisterData({
          name: '',
          username: '',
          region: 'EAST',
          password: '',
          confirmPassword: ''
        });
      } else {
        setError(response.error || 'Registration failed');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      {/* Orange Header */}
      <div style={styles.header}>
        <div style={styles.headerContent}>
          <h1 style={styles.headerTitle}>Ringspann Industrial Suite</h1>
          <div style={styles.headerRight}>
            <span style={styles.userBadge}>User: Guest</span>
            <span style={styles.statusBadge}>● Ready</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div style={styles.mainContent}>
        <div style={styles.authCard}>
          <h2 style={styles.authTitle}>Ringspann App Authentication</h2>

          {/* Error Message */}
          {error && (
            <div style={styles.error}>{error}</div>
          )}

          {isLogin ? (
            /* Login Form */
            <form onSubmit={handleLogin} style={styles.form}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Email ID:</label>
                <input
                  type="text"
                  value={loginData.username}
                  onChange={(e) => setLoginData({ ...loginData, username: e.target.value })}
                  placeholder="username@ringspann.com"
                  style={styles.input}
                  required
                />
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Password:</label>
                <input
                  type="password"
                  value={loginData.password}
                  onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
                  placeholder="Enter password"
                  style={styles.input}
                  required
                />
              </div>

              <button type="submit" disabled={loading} style={styles.loginButton}>
                {loading ? 'Logging in...' : 'Login'}
              </button>

              <div style={styles.switchLink}>
                Don't have an account?{' '}
                <span onClick={() => setIsLogin(false)} style={styles.link}>
                  Register here
                </span>
              </div>
            </form>
          ) : (
            /* Registration Form */
            <form onSubmit={handleRegister} style={styles.form}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Name:</label>
                <input
                  type="text"
                  value={registerData.name}
                  onChange={(e) => setRegisterData({ ...registerData, name: e.target.value })}
                  placeholder="Enter your full name"
                  style={styles.input}
                  required
                />
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Email ID:</label>
                <input
                  type="text"
                  value={registerData.username}
                  onChange={(e) => setRegisterData({ ...registerData, username: e.target.value })}
                  placeholder="username@ringspann.com"
                  style={styles.input}
                  required
                />
                <small style={styles.helpText}>Must end with @ringspann.com</small>
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Region:</label>
                <select
                  value={registerData.region}
                  onChange={(e) => setRegisterData({ ...registerData, region: e.target.value })}
                  style={styles.input}
                >
                  <option value="EAST">East</option>
                  <option value="WEST">West</option>
                  <option value="NORTH">North</option>
                  <option value="SOUTH">South</option>
                </select>
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Password:</label>
                <input
                  type="password"
                  value={registerData.password}
                  onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })}
                  placeholder="Minimum 6 characters"
                  style={styles.input}
                  required
                />
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Confirm Password:</label>
                <input
                  type="password"
                  value={registerData.confirmPassword}
                  onChange={(e) => setRegisterData({ ...registerData, confirmPassword: e.target.value })}
                  placeholder="Re-enter password"
                  style={styles.input}
                  required
                />
              </div>

              <button type="submit" disabled={loading} style={styles.loginButton}>
                {loading ? 'Registering...' : 'Register'}
              </button>

              <div style={styles.switchLink}>
                Already have an account?{' '}
                <span onClick={() => setIsLogin(true)} style={styles.link}>
                  Login here
                </span>
              </div>
            </form>
          )}
        </div>
      </div>

      {/* Footer */}
      <div style={styles.footer}>
        <span style={styles.footerText}>Ready</span>
        <span style={styles.footerCenter}>System: Ready</span>
        <span style={styles.footerCenter}>Real-time Data Stream: Active</span>
        <span style={styles.footerRight}>{new Date().toLocaleString()}</span>
      </div>
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    background: '#f0f0f0',
  },
  header: {
    background: '#e85d04',
    padding: '12px 0',
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
  headerRight: {
    display: 'flex',
    gap: '20px',
    alignItems: 'center',
  },
  userBadge: {
    background: 'white',
    color: '#333',
    padding: '6px 16px',
    borderRadius: '4px',
    fontSize: '14px',
    fontWeight: 500,
  },
  statusBadge: {
    background: 'white',
    color: '#28a745',
    padding: '6px 16px',
    borderRadius: '4px',
    fontSize: '14px',
    fontWeight: 500,
  },
  mainContent: {
    flex: 1,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '40px 20px',
  },
  authCard: {
    background: 'white',
    borderRadius: '8px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    padding: '40px',
    width: '100%',
    maxWidth: '500px',
  },
  authTitle: {
    fontSize: '28px',
    fontWeight: 600,
    color: '#333',
    marginBottom: '30px',
    textAlign: 'center',
  },
  error: {
    background: '#f8d7da',
    border: '1px solid #f5c6cb',
    color: '#721c24',
    padding: '12px',
    borderRadius: '4px',
    marginBottom: '20px',
    fontSize: '14px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
  },
  label: {
    fontSize: '14px',
    fontWeight: 500,
    color: '#333',
    marginBottom: '8px',
  },
  input: {
    padding: '12px',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    outline: 'none',
  },
  helpText: {
    fontSize: '12px',
    color: '#666',
    marginTop: '4px',
  },
  loginButton: {
    background: '#007bff',
    color: 'white',
    padding: '14px',
    fontSize: '16px',
    fontWeight: 600,
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    marginTop: '10px',
  },
  switchLink: {
    textAlign: 'center',
    fontSize: '14px',
    color: '#666',
    marginTop: '10px',
  },
  link: {
    color: '#007bff',
    cursor: 'pointer',
    textDecoration: 'underline',
  },
  footer: {
    background: '#2c3e50',
    color: 'white',
    padding: '12px 20px',
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '13px',
  },
  footerText: {
    flex: 1,
  },
  footerCenter: {
    flex: 1,
    textAlign: 'center',
  },
  footerRight: {
    flex: 1,
    textAlign: 'right',
  },
};

export default Login;