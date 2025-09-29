#!/usr/bin/env python3
"""
Exoplanet Discovery Platform Launcher
Starts both backend API and frontend development server
"""

import subprocess
import sys
import time
import threading
import webbrowser
from pathlib import Path

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting Backend API Server...")
    try:
        # Change to backend directory and start uvicorn
        backend_dir = Path("backend")
        if backend_dir.exists():
            subprocess.run([
                sys.executable, "-m", "uvicorn", "main:app", 
                "--host", "0.0.0.0", "--port", "8000", "--reload"
            ], cwd=backend_dir)
        else:
            print("❌ Backend directory not found!")
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Backend server error: {e}")

def start_frontend():
    """Start the React frontend development server"""
    print("🎨 Starting Frontend Development Server...")
    try:
        # Change to frontend directory and start npm
        frontend_dir = Path("frontend")
        if frontend_dir.exists():
            # Check if node_modules exists
            if not (frontend_dir / "node_modules").exists():
                print("📦 Installing frontend dependencies...")
                subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            
            # Start development server
            subprocess.run(["npm", "start"], cwd=frontend_dir)
        else:
            print("❌ Frontend directory not found!")
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Frontend server error: {e}")

def check_requirements():
    """Check if all required files and dependencies are present"""
    print("🔍 Checking System Requirements...")
    
    # Check Python dependencies
    required_packages = [
        "fastapi", "uvicorn", "pandas", "numpy", "scikit-learn", 
        "xgboost", "lightgbm", "joblib"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing Python packages: {', '.join(missing_packages)}")
        print("💡 Install with: pip install " + " ".join(missing_packages))
        return False
    
    # Check ML models
    model_files = [
        "ml/exoplanet_model_best.joblib",
        "ml/scaler.joblib", 
        "ml/label_encoder.joblib"
    ]
    
    missing_models = []
    for model_file in model_files:
        if not Path(model_file).exists():
            missing_models.append(model_file)
    
    if missing_models:
        print(f"❌ Missing ML models: {', '.join(missing_models)}")
        print("💡 Train models with: cd ml && python exoplanet_classifier.py")
        return False
    
    # Check data files
    data_files = [
        "data/cumulative_2025.09.16_22.42.55.csv"
    ]
    
    missing_data = []
    for data_file in data_files:
        if not Path(data_file).exists():
            missing_data.append(data_file)
    
    if missing_data:
        print(f"❌ Missing data files: {', '.join(missing_data)}")
        return False
    
    print("✅ All requirements satisfied!")
    return True

def open_browser():
    """Open web browser after servers start"""
    print("⏳ Waiting for servers to start...")
    time.sleep(8)  # Wait for servers to be ready
    
    try:
        print("🌐 Opening web browser...")
        webbrowser.open("http://localhost:3000")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("🌐 Please open http://localhost:3000 manually")

def main():
    """Main launcher function"""
    print("=" * 80)
    print("🌌 EXOPLANET AI DISCOVERY PLATFORM LAUNCHER 🌌")
    print("=" * 80)
    print()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n🚀 Starting Platform Components...")
    print("   - Backend API: http://localhost:8000")
    print("   - Frontend UI: http://localhost:3000")
    print("   - Press Ctrl+C to stop all servers")
    print()
    
    # Start browser opener in background
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start backend in background thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(3)
    
    try:
        # Start frontend in main thread (so we can catch Ctrl+C)
        start_frontend()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Exoplanet Discovery Platform...")
        print("👋 Thank you for exploring the universe!")
        sys.exit(0)

if __name__ == "__main__":
    main()
