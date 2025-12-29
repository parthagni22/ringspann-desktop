"""
COMPLETE PROJECT FIX SCRIPT
Run this from project root: python fix_project.py
"""
import os
from pathlib import Path

BASE_DIR = Path.cwd()

# ============================================
# FIX 1: Database Setup Script
# ============================================
print("=" * 70)
print("FIX 1: Creating correct setup_database.py")
print("=" * 70)

setup_db_content = '''"""
Database Setup Script
"""
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.database.connection import init_database

if __name__ == '__main__':
    print("Initializing database...")
    init_database()
    print("Database initialized successfully!")
'''

scripts_dir = BASE_DIR / "scripts"
scripts_dir.mkdir(exist_ok=True)

with open(scripts_dir / "setup_database.py", 'w', encoding='utf-8') as f:
    f.write(setup_db_content)

print("[OK] Fixed scripts/setup_database.py")

# ============================================
# FIX 2: Frontend Package.json (NO TAILWIND)
# ============================================
print("\n" + "=" * 70)
print("FIX 2: Creating package.json WITHOUT Tailwind")
print("=" * 70)

package_json = '''{
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
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8"
  }
}
'''

frontend_dir = BASE_DIR / "frontend"
with open(frontend_dir / "package.json", 'w', encoding='utf-8') as f:
    f.write(package_json)

print("[OK] Fixed frontend/package.json")

# ============================================
# FIX 3: Frontend index.css (NO TAILWIND)
# ============================================
print("\n" + "=" * 70)
print("FIX 3: Creating index.css WITHOUT Tailwind")
print("=" * 70)

index_css = '''* {
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
'''

src_dir = frontend_dir / "src"
src_dir.mkdir(exist_ok=True)

with open(src_dir / "index.css", 'w', encoding='utf-8') as f:
    f.write(index_css)

print("[OK] Fixed frontend/src/index.css")

# ============================================
# DELETE TAILWIND CONFIG FILES
# ============================================
print("\n" + "=" * 70)
print("FIX 4: Removing Tailwind config files")
print("=" * 70)

tailwind_files = [
    frontend_dir / "tailwind.config.js",
    frontend_dir / "postcss.config.js"
]

for file in tailwind_files:
    if file.exists():
        file.unlink()
        print(f"[OK] Deleted {file.name}")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 70)
print("ALL FIXES APPLIED SUCCESSFULLY!")
print("=" * 70)
print("\nNow run these commands:")
print("\n1. Initialize database:")
print("   python scripts\\setup_database.py")
print("\n2. Install frontend:")
print("   cd frontend")
print("   npm install")
print("   npm run build")
print("\n3. Run application:")
print("   cd ..\\backend")
print("   python app\\main.py")
print("\n" + "=" * 70)