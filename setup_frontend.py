"""
Complete Frontend Setup Script
Automatically creates all necessary files for React + Vite + Tailwind
"""
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / "frontend"

# File contents
FILES = {
    "package.json": """{
  "name": "ringspann-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "vite": "^5.0.8"
  }
}""",

    "vite.config.js": """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    emptyOutDir: true,
  },
  server: {
    port: 3000,
  }
})
""",

    "tailwind.config.js": """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
""",

    "postcss.config.js": """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""",

    "index.html": """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Ringspann Desktop</title>
    <script type="text/javascript" src="/eel.js"></script>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""",

    ".gitignore": """# Logs
logs
*.log
npm-debug.log*

# Dependencies
node_modules/

# Production
dist/
build/

# Misc
.DS_Store
*.env.local
*.env.development.local
*.env.test.local
*.env.production.local
""",

    "src/main.jsx": """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""",

    "src/index.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
""",

    "src/App.jsx": """import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/auth/Login';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
""",

    "src/pages/auth/Login.jsx": """import React, { useState } from 'react';
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
    userPrefix: '',
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

    if (!registerData.name.trim()) {
      setError('Name is required');
      return;
    }

    if (!registerData.userPrefix.trim()) {
      setError('User ID prefix is required');
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
      const username = registerData.userPrefix + '@ringspann.com';
      
      const response = await window.eel.register_user(
        registerData.name,
        username,
        registerData.region,
        registerData.password
      )();

      if (response.success) {
        alert('Registration successful! Please login.');
        setIsLogin(true);
        setRegisterData({
          name: '',
          userPrefix: '',
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
      <div style={styles.maxWidth}>
        <div style={styles.header}>
          <div style={styles.logo}>R</div>
          <h1 style={styles.title}>Ringspann Desktop</h1>
          <p style={styles.subtitle}>Quotation Management System</p>
        </div>

        <div style={styles.card}>
          <div style={styles.toggleContainer}>
            <button
              onClick={() => setIsLogin(true)}
              style={{...styles.toggleBtn, ...(isLogin ? styles.toggleBtnActive : {})}}
            >
              Login
            </button>
            <button
              onClick={() => setIsLogin(false)}
              style={{...styles.toggleBtn, ...(!isLogin ? styles.toggleBtnActive : {})}}
            >
              Register
            </button>
          </div>

          {error && (
            <div style={styles.error}>{error}</div>
          )}

          {isLogin ? (
            <form onSubmit={handleLogin}>
              <div style={styles.formGroup}>
                <label style={styles.label}>User ID</label>
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
                <label style={styles.label}>Password</label>
                <input
                  type="password"
                  value={loginData.password}
                  onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
                  placeholder="Enter password"
                  style={styles.input}
                  required
                />
              </div>

              <button type="submit" disabled={loading} style={styles.submitBtn}>
                {loading ? 'Logging in...' : 'Login'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleRegister}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Name</label>
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
                <label style={styles.label}>User ID</label>
                <div style={styles.inputGroup}>
                  <input
                    type="text"
                    value={registerData.userPrefix}
                    onChange={(e) => setRegisterData({ ...registerData, userPrefix: e.target.value.toLowerCase().replace(/\\s/g, '') })}
                    placeholder="username"
                    style={styles.inputGroupInput}
                    required
                  />
                  <span style={styles.inputGroupText}>@ringspann.com</span>
                </div>
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Region</label>
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
                <label style={styles.label}>Password</label>
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
                <label style={styles.label}>Confirm Password</label>
                <input
                  type="password"
                  value={registerData.confirmPassword}
                  onChange={(e) => setRegisterData({ ...registerData, confirmPassword: e.target.value })}
                  placeholder="Re-enter password"
                  style={styles.input}
                  required
                />
              </div>

              <button type="submit" disabled={loading} style={styles.submitBtn}>
                {loading ? 'Registering...' : 'Register'}
              </button>
            </form>
          )}

          <div style={styles.footer}>
            {isLogin ? (
              <p>Default: <strong>admin@ringspann.com</strong> / <strong>admin123</strong></p>
            ) : (
              <p>User ID will be: {registerData.userPrefix || 'username'}@ringspann.com</p>
            )}
          </div>
        </div>

        <div style={styles.version}>
          Version 1.0.0 • Ringspann Power Transmission India
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '20px',
  },
  maxWidth: {
    maxWidth: '450px',
    width: '100%',
  },
  header: {
    textAlign: 'center',
    marginBottom: '30px',
  },
  logo: {
    width: '80px',
    height: '80px',
    background: 'white',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    margin: '0 auto 20px',
    fontSize: '36px',
    fontWeight: 'bold',
    color: '#667eea',
    boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
  },
  title: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: 'white',
    marginBottom: '8px',
  },
  subtitle: {
    color: 'rgba(255,255,255,0.9)',
    fontSize: '16px',
  },
  card: {
    background: 'white',
    borderRadius: '16px',
    boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
    padding: '40px',
  },
  toggleContainer: {
    display: 'flex',
    background: '#f3f4f6',
    borderRadius: '8px',
    padding: '4px',
    marginBottom: '24px',
  },
  toggleBtn: {
    flex: 1,
    padding: '10px',
    border: 'none',
    background: 'transparent',
    borderRadius: '6px',
    fontWeight: 500,
    cursor: 'pointer',
    transition: 'all 0.3s',
    color: '#6b7280',
  },
  toggleBtnActive: {
    background: 'white',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    color: '#667eea',
  },
  error: {
    background: '#fee',
    border: '1px solid #fcc',
    color: '#c33',
    padding: '12px',
    borderRadius: '8px',
    marginBottom: '16px',
    fontSize: '14px',
  },
  formGroup: {
    marginBottom: '16px',
  },
  label: {
    display: 'block',
    fontSize: '14px',
    fontWeight: 500,
    color: '#374151',
    marginBottom: '6px',
  },
  input: {
    width: '100%',
    padding: '12px 16px',
    border: '1px solid #d1d5db',
    borderRadius: '8px',
    fontSize: '14px',
    boxSizing: 'border-box',
  },
  inputGroup: {
    display: 'flex',
  },
  inputGroupInput: {
    flex: 1,
    padding: '12px 16px',
    border: '1px solid #d1d5db',
    borderRight: 'none',
    borderRadius: '8px 0 0 8px',
    fontSize: '14px',
  },
  inputGroupText: {
    background: '#f3f4f6',
    padding: '12px 16px',
    border: '1px solid #d1d5db',
    borderRadius: '0 8px 8px 0',
    color: '#6b7280',
    whiteSpace: 'nowrap',
  },
  submitBtn: {
    width: '100%',
    background: '#667eea',
    color: 'white',
    padding: '14px',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: 600,
    cursor: 'pointer',
    marginTop: '8px',
  },
  footer: {
    marginTop: '20px',
    textAlign: 'center',
    fontSize: '13px',
    color: '#6b7280',
  },
  version: {
    textAlign: 'center',
    marginTop: '24px',
    fontSize: '13px',
    color: 'rgba(255,255,255,0.9)',
  },
};

export default Login;
""",

    "src/pages/Dashboard.jsx": """import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const currentUser = localStorage.getItem('currentUser');
    if (!currentUser) {
      navigate('/login');
      return;
    }
    setUser(JSON.parse(currentUser));
  }, [navigate]);

  const handleLogout = async () => {
    await window.eel.logout()();
    localStorage.removeItem('currentUser');
    navigate('/login');
  };

  if (!user) {
    return <div style={styles.loading}>Loading...</div>;
  }

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <div style={styles.headerContent}>
          <div>
            <h1 style={styles.headerTitle}>Ringspann Desktop</h1>
            <p style={styles.headerSubtitle}>Quotation Management System</p>
          </div>
          <div style={styles.userInfo}>
            <div style={styles.userDetails}>
              <p style={styles.userName}>{user.name}</p>
              <p style={styles.userRegion}>{user.region} Region</p>
            </div>
            <button onClick={handleLogout} style={styles.logoutBtn}>
              Logout
            </button>
          </div>
        </div>
      </header>

      <main style={styles.main}>
        <div style={styles.grid}>
          <div style={styles.card}>
            <div style={styles.cardIcon}>👥</div>
            <h3 style={styles.cardTitle}>Customer Management</h3>
            <p style={styles.cardText}>Manage customer information and details</p>
          </div>

          <div style={styles.card}>
            <div style={styles.cardIcon}>📄</div>
            <h3 style={styles.cardTitle}>Quotations</h3>
            <p style={styles.cardText}>Create and manage quotations</p>
          </div>

          <div style={styles.card}>
            <div style={styles.cardIcon}>📊</div>
            <h3 style={styles.cardTitle}>Analytics</h3>
            <p style={styles.cardText}>View business insights and reports</p>
          </div>
        </div>

        <div style={styles.welcomeCard}>
          <h2 style={styles.welcomeTitle}>Welcome, {user.name}! 👋</h2>
          <p style={styles.welcomeText}>
            You are logged in as <strong>{user.username}</strong> from the{' '}
            <strong>{user.region}</strong> region.
          </p>
          <p style={styles.welcomeText}>
            Select a module above to get started with managing quotations.
          </p>
        </div>
      </main>
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    background: '#f3f4f6',
  },
  header: {
    background: 'white',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    padding: '16px 0',
  },
  headerContent: {
    maxWidth: '1280px',
    margin: '0 auto',
    padding: '0 24px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#111',
    margin: 0,
  },
  headerSubtitle: {
    fontSize: '14px',
    color: '#6b7280',
    margin: '4px 0 0 0',
  },
  userInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
  },
  userDetails: {
    textAlign: 'right',
  },
  userName: {
    fontSize: '14px',
    fontWeight: 500,
    color: '#111',
    margin: 0,
  },
  userRegion: {
    fontSize: '12px',
    color: '#6b7280',
    margin: '4px 0 0 0',
  },
  logoutBtn: {
    background: '#ef4444',
    color: 'white',
    padding: '8px 16px',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: 500,
  },
  main: {
    maxWidth: '1280px',
    margin: '0 auto',
    padding: '32px 24px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '24px',
    marginBottom: '32px',
  },
  card: {
    background: 'white',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    padding: '24px',
    cursor: 'pointer',
    transition: 'box-shadow 0.3s',
  },
  cardIcon: {
    fontSize: '48px',
    marginBottom: '16px',
  },
  cardTitle: {
    fontSize: '18px',
    fontWeight: 600,
    color: '#111',
    margin: '0 0 8px 0',
  },
  cardText: {
    fontSize: '14px',
    color: '#6b7280',
    margin: 0,
  },
  welcomeCard: {
    background: 'white',
    borderRadius: '12px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    padding: '24px',
  },
  welcomeTitle: {
    fontSize: '20px',
    fontWeight: 600,
    color: '#111',
    margin: '0 0 16px 0',
  },
  welcomeText: {
    fontSize: '14px',
    color: '#6b7280',
    margin: '8px 0',
  },
  loading: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    fontSize: '18px',
  },
};

export default Dashboard;
""",
}

def create_file(filepath, content):
    """Create file with content"""
    full_path = FRONTEND_DIR / filepath
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created: {filepath}")

def main():
    print("="*70)
    print("  FRONTEND SETUP - AUTOMATED")
    print("="*70)
    print()
    
    # Create frontend directory if doesn't exist
    FRONTEND_DIR.mkdir(exist_ok=True)
    
    # Create all files
    for filepath, content in FILES.items():
        create_file(filepath, content)
    
    print()
    print("="*70)
    print("  ✅ FRONTEND FILES CREATED!")
    print("="*70)
    print()
    print("Next steps:")
    print("1. cd frontend")
    print("2. npm install")
    print("3. npm run build")
    print("4. cd ../backend")
    print("5. python app/main.py")
    print()
    print("="*70)

if __name__ == '__main__':
    main()