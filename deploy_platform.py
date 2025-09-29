#!/usr/bin/env python3
"""
Complete Deployment Script for Exoplanet Discovery Platform
Handles all setup, training, and deployment steps
"""

import subprocess
import sys
import time
import threading
import webbrowser
import os
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a command and return the result"""
    try:
        print(f"🔧 Running: {command}")
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, cwd=cwd, check=check, 
                                  capture_output=True, text=True)
        else:
            result = subprocess.run(command, cwd=cwd, check=check, 
                                  capture_output=True, text=True)
        
        if result.stdout:
            print(f"✅ Output: {result.stdout.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        if e.stdout:
            print(f"   stdout: {e.stdout}")
        if e.stderr:
            print(f"   stderr: {e.stderr}")
        if check:
            raise
        return e

def install_python_dependencies():
    """Install Python dependencies for ML and backend"""
    print("\n📦 Installing Python Dependencies...")
    
    packages = [
        "pandas", "numpy", "scikit-learn", "xgboost", "lightgbm", 
        "matplotlib", "seaborn", "joblib", "fastapi", "uvicorn", 
        "python-multipart", "requests"
    ]
    
    for package in packages:
        try:
            run_command([sys.executable, "-m", "pip", "install", package])
        except:
            print(f"⚠️  Failed to install {package}, continuing...")

def train_ml_models():
    """Train the ML models"""
    print("\n🤖 Training ML Models...")
    
    try:
        result = run_command([sys.executable, "exoplanet_classifier.py"], cwd="ml")
        print("✅ ML models trained successfully!")
        return True
    except Exception as e:
        print(f"❌ ML training failed: {e}")
        return False

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("\n🎨 Installing Frontend Dependencies...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    try:
        # Check if npm is available
        run_command(["npm", "--version"])
        
        # Install dependencies
        run_command(["npm", "install"], cwd=frontend_dir)
        print("✅ Frontend dependencies installed!")
        return True
    except Exception as e:
        print(f"❌ Frontend installation failed: {e}")
        print("💡 Please install Node.js and npm first")
        return False

def start_backend_server():
    """Start the backend server"""
    print("\n🚀 Starting Backend Server...")
    
    try:
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], cwd="backend")
        
        # Wait for server to start
        time.sleep(5)
        
        # Test if server is running
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server started successfully!")
            return backend_process
        else:
            print("❌ Backend server health check failed")
            return None
    except Exception as e:
        print(f"❌ Failed to start backend server: {e}")
        return None

def start_frontend_server():
    """Start the frontend development server"""
    print("\n🎨 Starting Frontend Server...")
    
    try:
        frontend_process = subprocess.Popen([
            "npm", "start"
        ], cwd="frontend")
        
        # Wait for server to start
        time.sleep(10)
        
        print("✅ Frontend server started successfully!")
        return frontend_process
    except Exception as e:
        print(f"❌ Failed to start frontend server: {e}")
        return None

def open_browser():
    """Open the web browser"""
    print("\n🌐 Opening Web Browser...")
    time.sleep(3)
    
    try:
        webbrowser.open("http://localhost:3000")
        print("✅ Browser opened successfully!")
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")
        print("🌐 Please open http://localhost:3000 manually")

def check_system_requirements():
    """Check system requirements"""
    print("🔍 Checking System Requirements...")
    
    # Check Python
    try:
        python_version = sys.version_info
        if python_version.major < 3 or python_version.minor < 8:
            print("❌ Python 3.8+ required")
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}")
    except:
        print("❌ Python not found")
        return False
    
    # Check Node.js
    try:
        result = run_command(["node", "--version"], check=False)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()}")
        else:
            print("❌ Node.js not found - please install Node.js")
            return False
    except:
        print("❌ Node.js not found - please install Node.js")
        return False
    
    # Check npm
    try:
        result = run_command(["npm", "--version"], check=False)
        if result.returncode == 0:
            print(f"✅ npm {result.stdout.strip()}")
        else:
            print("❌ npm not found")
            return False
    except:
        print("❌ npm not found")
        return False
    
    return True

def run_system_test():
    """Run system tests"""
    print("\n🧪 Running System Tests...")
    
    try:
        result = run_command([sys.executable, "test_system.py"])
        if result.returncode == 0:
            print("✅ All system tests passed!")
            return True
        else:
            print("❌ Some system tests failed")
            return False
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("=" * 80)
    print("🌌 EXOPLANET AI DISCOVERY PLATFORM - COMPLETE DEPLOYMENT 🌌")
    print("=" * 80)
    print()
    
    # Step 1: Check requirements
    print("STEP 1: System Requirements Check")
    print("-" * 40)
    if not check_system_requirements():
        print("\n❌ System requirements not met. Please install required software.")
        sys.exit(1)
    
    # Step 2: Install Python dependencies
    print("\nSTEP 2: Python Dependencies")
    print("-" * 40)
    install_python_dependencies()
    
    # Step 3: Train ML models
    print("\nSTEP 3: Machine Learning Training")
    print("-" * 40)
    if not train_ml_models():
        print("⚠️  ML training failed, but continuing with demo mode...")
    
    # Step 4: Install frontend dependencies
    print("\nSTEP 4: Frontend Dependencies")
    print("-" * 40)
    if not install_frontend_dependencies():
        print("❌ Frontend setup failed. Please check Node.js installation.")
        sys.exit(1)
    
    # Step 5: Run system tests
    print("\nSTEP 5: System Testing")
    print("-" * 40)
    run_system_test()
    
    # Step 6: Start servers
    print("\nSTEP 6: Server Deployment")
    print("-" * 40)
    
    # Start backend
    backend_process = start_backend_server()
    if not backend_process:
        print("❌ Backend deployment failed")
        sys.exit(1)
    
    # Start frontend in a separate thread
    def start_frontend_thread():
        frontend_process = start_frontend_server()
        return frontend_process
    
    frontend_thread = threading.Thread(target=start_frontend_thread, daemon=True)
    frontend_thread.start()
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Final status
    print("\n" + "=" * 80)
    print("🎉 DEPLOYMENT COMPLETE!")
    print("=" * 80)
    print()
    print("🌐 Platform URLs:")
    print("   • Frontend:  http://localhost:3000")
    print("   • Backend:   http://localhost:8000")
    print("   • API Docs:  http://localhost:8000/docs")
    print()
    print("🎮 Usage:")
    print("   • Explore 3D universe by clicking and dragging")
    print("   • Click planets to view detailed information")
    print("   • Use AI panel (left) to predict new exoplanets")
    print("   • Apply filters to focus on specific types")
    print()
    print("🛑 Press Ctrl+C to stop all servers")
    print()
    
    try:
        # Keep the main process running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Exoplanet Discovery Platform...")
        
        # Cleanup processes
        if backend_process:
            backend_process.terminate()
        
        print("👋 Thank you for exploring the universe!")
        sys.exit(0)

if __name__ == "__main__":
    main()
