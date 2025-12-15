# Installation & Setup Guide

Complete step-by-step instructions for setting up FoodHub locally and deploying to production.

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Database Initialization](#database-initialization)
3. [Running the Application](#running-the-application)
4. [Virtual Environment](#virtual-environment)
5. [Deployment to Render](#deployment-to-render)
6. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites

Before you start, ensure you have:

- **Python 3.8+** installed ([Download here](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** (for cloning the repository)
- A text editor or IDE (VS Code, PyCharm, etc.)

### Verify Installation

```bash
# Check Python version
python --version

# Check pip version
pip --version
```

### Step 1: Clone the Repository

```bash
git clone https://github.com/krushnanarwade/Restaurant-Billing-System.git
cd Restaurant-Billing-System
```

### Step 2: Create a Virtual Environment

A virtual environment isolates project dependencies from your system Python.

#### On Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when activated.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `Flask==3.0.3` - Web framework
- `gunicorn==23.0.0` - Production server

### Step 4: Initialize the Database

The database is automatically created on first run, but you can manually initialize it:

```python
# In Python shell or a script:
from app import app, init_db

with app.app_context():
    init_db()
    print("Database initialized!")
```

Or simply run the app once:
```bash
python app.py
```

This creates `database.db` with all required tables and default admin account.

### Step 5: Run the Application

```bash
python app.py
```

Expected output:
```
WARNING: This is a development server. Do not use it in production.
Running on http://127.0.0.1:5000
```

### Step 6: Access the Application

Open your web browser and go to:
```
http://127.0.0.1:5000
```

You'll be redirected to the login page.

---

## Database Initialization

### Manual Database Reset

To completely reset the database and recreate it:

```bash
# Stop the running app (Ctrl+C)

# Delete the old database
rm database.db  # On macOS/Linux
del database.db  # On Windows PowerShell

# Run the app to recreate
python app.py
```

### Database Tables

The app automatically creates these tables:

| Table | Purpose |
|-------|---------|
| `menu` | Stores food items and prices |
| `orders` | Tracks customer orders |
| `customers` | Stores customer information |
| `admin` | Admin credentials |
| `sales` | Reserved for future analytics |

### Default Admin Account

Created automatically on first setup:
- **Username:** `admin`
- **Password:** `admin`

⚠️ **Change this password immediately in production!**

---

## Running the Application

### Development Mode

```bash
python app.py
```

**Features:**
- Debug mode enabled
- Hot reload on file changes
- Detailed error messages

### Production Mode (Gunicorn)

```bash
gunicorn app:app --bind 0.0.0.0:5000
```

**Features:**
- Production-ready server
- Better error handling
- Suitable for deployment

### Run on Different Port

Edit `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change 5001 to your desired port
```

Then start:
```bash
python app.py
```

---

## Virtual Environment

### Why Use a Virtual Environment?

- Isolates project dependencies
- Prevents conflicts with system packages
- Makes project portable

### Activate Virtual Environment

#### Windows:
```powershell
venv\Scripts\Activate.ps1
```

#### macOS/Linux:
```bash
source venv/bin/activate
```

### Deactivate Virtual Environment

```bash
deactivate
```

### Delete Virtual Environment

```powershell
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### View Installed Packages

```bash
pip list
```

### Update a Package

```bash
pip install --upgrade Flask
```

---

## Deployment to Render

### Option 1: Web UI (Recommended)

1. **Create Render Account**
   - Go to [render.com](https://dashboard.render.com)
   - Sign up with GitHub account

2. **Connect Repository**
   - Click "New" → "Web Service"
   - Select your GitHub repository
   - Click "Connect"

3. **Configure Deployment**
   - **Name:** `restaurant-billing-system`
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free (for testing)

4. **Set Environment Variables** (Optional but recommended)
   - Click "Environment"
   - Add `SECRET_KEY=your-secure-random-string`
   - Add `DEBUG=False`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete
   - Access your app via the provided URL

### Option 2: Using Render CLI

```bash
# Install Render CLI
npm install -g render

# Login to Render
render login

# Deploy from project root
render deploy --service restaurant-billing-system
```

### Post-Deployment

After deploying to Render:

1. **Test the Application**
   - Visit the provided URL
   - Login with admin credentials
   - Test all features

2. **Change Default Credentials**
   - Login with `admin` / `admin`
   - (Security feature to implement in future)

3. **Monitor Logs**
   - Go to Render dashboard
   - View build and runtime logs
   - Check for errors

4. **Set Up Database**
   - Database is ephemeral on Render free plan
   - Data resets on deployment/restart
   - For persistence: Upgrade to PostgreSQL plan

### Connect PostgreSQL Database (Optional)

For persistent data storage:

1. On Render dashboard, create a PostgreSQL database
2. Note the `DATABASE_URL` connection string
3. Add to environment variables
4. Update `app.py` to use PostgreSQL:

```python
import os
import psycopg2
from psycopg2 import sql

# Use PostgreSQL in production
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///database.db')

if DATABASE_URL.startswith('postgresql'):
    # Use PostgreSQL connection
    pass
else:
    # Use SQLite for local development
    pass
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'flask'`

**Solution:** Install requirements in activated virtual environment:
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 Already in Use

**Solution 1:** Kill the process using port 5000

#### Windows:
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

#### macOS/Linux:
```bash
lsof -ti:5000 | xargs kill -9
```

**Solution 2:** Use a different port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### Issue: Database Not Found

**Solution:** The database is created automatically on first run. If missing:

```bash
python app.py
# This will create database.db
```

### Issue: Login Fails

**Solution:** Verify default credentials:
- **Username:** `admin`
- **Password:** `admin`

If still failing, reset database:
```bash
rm database.db
python app.py  # Recreates with default account
```

### Issue: Templates Not Found

**Solution:** Ensure you're running from the project root:

```bash
cd Restaurant-Billing-System
python app.py
```

### Issue: Styles or Favicon Not Loading

**Solution:** Clear browser cache:

#### Chrome/Edge:
- Press `Ctrl + Shift + R` (or Cmd + Shift + R on Mac)

#### Firefox:
- Press `Ctrl + Shift + Delete` (or Cmd + Shift + Delete on Mac)

### Issue: Render Deployment Fails

**Common causes:**

1. **Missing `requirements.txt`** - Ensure file exists in repo root
2. **Syntax error in `app.py`** - Check build logs for Python errors
3. **Port not 8000** - Render expects Gunicorn on port 8000 (automatically handled)
4. **Environment variables** - Check Render dashboard for correct settings

**Debug:**
- View build logs in Render dashboard
- Check for error messages
- Try building locally first: `pip install -r requirements.txt`

### Issue: Render App Crashes After Deploy

**Check logs:**
1. Go to Render dashboard
2. View "Logs" tab
3. Look for error messages
4. Common issues:
   - Database file permissions
   - Missing environment variables
   - Syntax errors in code

---

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `'foodhub123'` | Flask session secret (change in production!) |
| `FLASK_ENV` | `development` | Set to `production` for deployment |
| `DEBUG` | `True` | Set to `False` in production |
| `DATABASE_URL` | SQLite `database.db` | PostgreSQL connection string (optional) |

---

## Next Steps

After setup:

1. **Read [USER_GUIDE.md](./USER_GUIDE.md)** - Learn all features
2. **Review [API_ROUTES.md](./API_ROUTES.md)** - Understand available endpoints
3. **Check [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md)** - Explore database design
4. **Deploy to Render** - Make your app live

---

**Questions?** Check troubleshooting above or create an issue on GitHub.
