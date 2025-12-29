import os
import shutil
from pathlib import Path

BASE = Path('D:/Irizpro/ringspann-desktop')

# Delete empty/unused directories
DELETE_DIRS = [
    'frontend/src/components',
    'frontend/src/hooks', 
    'frontend/src/utils',
    'frontend/src/pages/analytics',
    'frontend/src/pages/customers',
    'frontend/src/pages/quotations',
    'frontend/src/pages/settings',
    'backend/app/analytics',
    'backend/app/repositories',
    'backend/app/schemas',
    'backend/app/pdf/templates'
]

# Delete empty/unused files
DELETE_FILES = [
    'frontend/src/index.js',
    'frontend/src/routes.js',
    'frontend/src/pages/auth/UserManagement.jsx',
    'backend/app/pdf/base_generator.py',
    'backend/app/pdf/commercial_pdf.py',
    'backend/app/pdf/technical_pdf.py',
    'scripts/backup_database.py',
    'scripts/build.py',
    'scripts/seed_data.py',
    'create_backend_structure.py',
    'setup_frontend.py',
    'fix_project.py'
]

for d in DELETE_DIRS:
    path = BASE / d
    if path.exists():
        shutil.rmtree(path)
        print(f'✓ Deleted {d}')

for f in DELETE_FILES:
    path = BASE / f
    if path.exists():
        path.unlink()
        print(f'✓ Deleted {f}')

print('\n✅ Cleanup complete!')