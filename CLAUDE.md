# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ringspann Desktop is an industrial quotation management system for Ringspann Power Transmission India. It's a 100% offline desktop application built with a Python backend (Eel + SQLAlchemy) and React frontend (Vite + Tailwind), packaged as a standalone executable using PyInstaller.

## Architecture

### Backend Architecture (Python)
- **Framework**: Eel (Python-JavaScript bridge) running a local server
- **Database**: SQLite with SQLAlchemy ORM
- **PDF Generation**: ReportLab for commercial and technical quotations
- **Analytics**: Pandas for data analysis and reporting

The backend follows a layered architecture:
- `backend/app/api/` - Eel-exposed API functions (decorated with `@eel.expose`)
- `backend/app/services/` - Business logic layer
- `backend/app/models/` - SQLAlchemy ORM models
- `backend/app/database/` - Database connection and initialization
- `backend/app/utils/` - Shared utilities (logging, etc.)

**Key Pattern**: All API functions use `@eel.expose` decorator and return dictionaries with `{'success': bool, 'data': dict, 'error': str}` format. The frontend calls these using `window.eel.function_name()`.

**Database Sessions**: Database sessions are created using the `get_db()` context manager from `app/database/connection.py`. This is a generator function that yields a session and ensures proper cleanup with try/finally.

### Frontend Architecture (React)
- **Router**: React Router with HashRouter (required for desktop app). The frontend imports `HashRouter as Router` in App.jsx to maintain compatibility with both desktop and potential web deployments.
- **Styling**: Tailwind CSS with custom components, configured in `frontend/src/index.css`
- **UI Components**: Radix UI primitives (@radix-ui/react-select, @radix-ui/react-tabs) for accessible components
- **Charts**: Recharts library for analytics visualizations
- **State**: React hooks, no global state management
- **Build**: Vite with base path set to './' for desktop compatibility
- **Path aliases**: `@` is aliased to `frontend/src` in vite.config.js

Key modules:
- `frontend/src/pages/` - Main application pages
- `frontend/src/pages/Analytics/` - Analytics dashboard with multiple views:
  - `AnalyticsDashboard.jsx` - Main analytics router (17KB)
  - `CombinedInsights.jsx` - Combined analytics view (38KB)
  - `CustomerAnalytics.jsx` - Customer-specific analytics (56KB)
  - `FinanceAnalytics.jsx` - Financial analytics (43KB)
  - `ProductAnalytics.jsx` - Product analytics (38KB)
  - `components/` - Shared filter panels and components
  - `hooks/` - Custom React hooks for analytics
- `frontend/src/components/` - Reusable UI components
- `frontend/src/components/ui/` - Base UI primitives (button, card, select, tabs)

### Database Models
Core entities with relationships:
- **User** - Authentication and user management
- **Customer** - Customer information
- **Project** - Quotation projects with status (draft/in_progress/completed/archived) and quote_status (Budgetary/Active/Lost/Won)
- **CommercialQuotation** - Commercial quote details linked to projects
- **TechnicalQuotation** - Technical specifications linked to projects

All models use `Base` from `app/models/base.py`. The `TimestampMixin` provides automatic `created_at` and `updated_at` fields.

### PDF Generation
Two specialized generators:
- `backend/app/api/pdf_generator.py` - Commercial quotations (~63KB, complex formatting)
- `backend/app/api/technical_pdf_generator.py` - Technical specifications (~68KB, detailed tables)

Both use ReportLab extensively with custom table styles, page templates, and multi-page support.

## Common Development Commands

**Working Directory Note**: All commands below assume you start from the project root (`ringspann-desktop/`) unless otherwise specified.

### Backend Development
```bash
# Setup Python environment
cd backend
python -m venv venv
venv\Scripts\activate          # Windows CMD
# venv\Scripts\Activate.ps1    # Windows PowerShell
# source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt

# Run application in development mode (requires frontend to be built first)
python app/main.py             # from backend/ directory
# OR from project root:
python backend/app/main.py

# Important: There are two main.py files:
# - main.py (root) - Production entry point used by PyInstaller for .exe builds
#   Looks for frontend in '_internal/web' when frozen
# - backend/app/main.py - Development entry point (ALWAYS use this for development)
#   Looks for frontend in 'frontend/dist'

# Run tests (from backend/ directory with venv activated)
pytest
pytest -v                      # verbose
pytest --cov                   # with coverage
pytest tests/test_specific.py  # single test file

# Code formatting (from backend/ directory)
black app/                     # format code
flake8 app/                    # lint
mypy app/                      # type checking
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Development server (for UI development only)
npm run dev                    # runs on port 3000

# Note: npm run dev runs a standalone development server without the Python backend.
# Backend API calls (window.eel.*) will fail. For full-stack development, build the
# frontend and run the Python backend instead.

# Production build (required before running app)
npm run build                  # outputs to frontend/dist/

# Preview production build
npm run preview
```

### Desktop App Packaging
```bash
# Build frontend first
cd frontend && npm run build && cd ..

# Create executable
pyinstaller build.spec

# Output location: dist/QuotationSystem/QuotationSystem.exe
```

The `build.spec` file configures PyInstaller to:
- Bundle the Python backend with all dependencies
- Copy frontend/dist to '_internal/web' in the packaged app
- Copy eel.js from venv to the web directory
- Create a Windows executable with custom icon (icon.ico)
- Output to `dist/QuotationSystem/QuotationSystem.exe`
- Console mode enabled in spec for debugging (set to False for production)

## Data Storage Structure

The application creates the following directory structure in `data/`:
```
data/
├── database/
│   └── ringspann.db          # SQLite database
├── pdfs/
│   ├── commercial/           # Generated commercial quotations
│   └── technical/            # Generated technical quotations
├── exports/                  # Analytics exports (xlsx, csv, pdf)
├── backups/                  # Database backups
└── logs/
    └── app.log              # Application logs
```

Paths are configured in `backend/app/config.py` and created automatically on startup.

## Key Configuration

- **Database URL**: `sqlite:///data/database/ringspann.db` (configured in `app/config.py`)
- **Frontend served from**: `frontend/dist/` (set in `app/main.py`)
- **Eel port**: 8080 (localhost only)
- **Eel mode**: Chrome app mode (opens in Chrome/Chromium window without browser UI)
- **Default admin user**: Created automatically on first run via `app/database/seed.py`
- **Date formats**: Configured in `app/config.py` (DATE_FORMAT, DATETIME_FORMAT, DISPLAY_DATE_FORMAT)

## Testing Notes

Test dependencies are in `requirements.txt`:
- pytest - test runner
- pytest-cov - coverage reporting
- faker - test data generation

No test directory currently exists in the codebase - tests should be created in `backend/tests/` following pytest conventions.

## API Structure and Response Format

All backend API functions follow a consistent pattern:
- Decorated with `@eel.expose` to make them callable from frontend
- Return a standardized dictionary: `{'success': bool, 'data': dict, 'error': str}`
- Use `get_db()` context manager for database sessions
- Wrap operations in try/except blocks with proper error handling

Example pattern:
```python
@eel.expose
def api_function_name(params):
    try:
        db = next(get_db())
        # Business logic here
        return {'success': True, 'data': result, 'error': None}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {'success': False, 'data': None, 'error': str(e)}
```

## Important Development Notes

1. **Frontend builds are required**: The app serves the built frontend from `frontend/dist/`, not the source. Always run `npm run build` after frontend changes.

2. **HashRouter requirement**: The app uses HashRouter (not BrowserRouter) because it's served locally via Eel, not a traditional web server.

3. **Eel API pattern**: Backend functions decorated with `@eel.expose` are called from frontend as `await window.eel.function_name(args)()`. Always handle the promise/async nature. The double parentheses are required: first call returns a promise, second executes it.

4. **Analytics data flow**: Analytics use a service-heavy approach with complex Pandas operations in `analytics_service.py` (44KB) and `product_analytics_service.py` (27KB).

5. **PDF generation is blocking**: PDF generation in ReportLab is synchronous and can be slow for large quotations. Consider this when calling from the frontend.

6. **Database migrations**: Alembic is installed but migrations directory exists without configuration. Schema changes currently handled via SQLAlchemy's `create_all()`.

7. **Logging**: Uses Loguru logging library. Logger setup in `app/utils/logger.py`. Logs go to both console and `data/logs/app.log`.
