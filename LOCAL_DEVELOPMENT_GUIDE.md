# 🚀 Local Development Guide

## Quick Start for Testing Frontend and Backend

This guide helps you run and test both the frontend and backend locally for development and testing purposes.

## 📋 Prerequisites

- **Node.js**: 16.0+ (for frontend)
- **Python**: 3.9+ (for backend)
- **Git**: Latest version

## 🛠️ Setup Instructions

### 1. Clone and Setup Repository

```bash
git clone <repository-url>
cd test_nasa
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in new terminal)
cd frontend

# Install dependencies
npm install
```

## 🚀 Running the Application

### Option 1: Manual Start (Recommended for Development)

#### Terminal 1 - Backend
```bash
cd backend
# Ensure virtual environment is activated
uvicorn ultra_simple_api:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm start
```

### Option 2: Automated Start (Windows)

```bash
# Run the batch file
start_local.bat
```

### Option 3: Python Script

```bash
# Run the Python startup script
python tests/start_local_development.py
```

## 🌐 Access Points

Once both services are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## 🧪 Testing the Application

### 1. Verify Backend Status

Check the **Backend Status** indicator in the bottom-left corner of the frontend:
- 🟢 **Connected**: Backend is working properly
- 🔴 **Disconnected**: Backend is not responding

### 2. Test AI Prediction

1. **Open Frontend**: Navigate to http://localhost:3000
2. **Expand AI Panel**: Click on "🤖 AI PREDICTOR" in the top-left
3. **Input Parameters**: Try these test values:
   - Orbital Period: 112.3
   - Planet Radius: 1.34
   - Equilibrium Temperature: 233
   - Stellar Temperature: 4402
4. **Click Predict**: Press "PREDICT & MATERIALIZE"
5. **Check Results**: Should show specific planet name (not generic "AI Predicted")

### 3. Use Parameter Guide

Refer to `PLANET_PARAMETER_GUIDE.md` for specific parameter combinations that should return confirmed planets.

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check for missing models
ls ml/  # Should contain .joblib files
```

**Problem**: "Models not found" error
```bash
# Train models if missing
cd ml
python exoplanet_classifier.py
```

### Frontend Issues

**Problem**: Frontend won't start
```bash
# Check Node.js version
node --version  # Should be 16.0+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem**: "API not connected"
- Ensure backend is running on port 8000
- Check firewall settings
- Verify no other service is using port 8000

### Common Issues

**Problem**: Always getting "AI Predicted" results
- Check backend logs for XGBoost compatibility issues
- Verify training data is loaded properly
- Ensure similarity matching is working

**Problem**: UI elements overlapping
- Try collapsing panels (click on headers)
- Refresh the page
- Check browser zoom level

## 📊 Development Features

### Debug Information

Open browser developer tools (F12) to see:
- API request/response logs
- Prediction data structure
- Backend connection status
- Error messages

### Hot Reload

Both frontend and backend support hot reload:
- **Frontend**: Changes to React components auto-refresh
- **Backend**: Changes to Python files auto-restart (with `--reload` flag)

## 🎯 Testing Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:3000
- [ ] Backend status shows "Connected"
- [ ] AI panel can be expanded/collapsed
- [ ] Prediction returns specific planet names
- [ ] 3D visualization works smoothly
- [ ] Planet details panel shows correct information

## 📁 Project Structure

```
test_nasa/
├── backend/
│   ├── ultra_simple_api.py     # Main FastAPI application
│   ├── requirements.txt        # Python dependencies
│   └── ml/                     # ML models and training
├── frontend/
│   ├── src/
│   │   ├── EpicApp.js         # Main React application
│   │   └── SimpleApp.css      # Styling
│   ├── package.json           # Node.js dependencies
│   └── public/                # Static assets
├── data/                      # Training datasets
├── ml_training_results/       # ML visualization charts
├── tests/                     # Test scripts and utilities
└── PLANET_PARAMETER_GUIDE.md  # Parameter combinations guide
```

## 🆘 Getting Help

If you encounter issues:

1. **Check Logs**: Look at terminal output for error messages
2. **Verify Ports**: Ensure 3000 and 8000 are available
3. **Test API Directly**: Visit http://localhost:8000/docs
4. **Run Test Scripts**: Use scripts in `tests/` directory
5. **Check Dependencies**: Ensure all requirements are installed

## 🎉 Success Indicators

You'll know everything is working when:
- Backend status indicator shows green
- Predictions return real planet names (e.g., "Kepler-452 b")
- Confidence scores are > 85%
- 3D planets appear and can be clicked
- Parameter guide examples work as expected

---

*Happy planet hunting! 🪐✨*
