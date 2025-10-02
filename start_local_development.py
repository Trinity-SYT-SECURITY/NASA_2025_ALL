#!/usr/bin/env python3
"""
Local development startup script
"""

import subprocess
import sys
import os
import time
import requests
import webbrowser
from threading import Thread

def start_backend():
    """Start FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    os.chdir('backend')
    
    try:
        # Try to start with uvicorn first
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'ultra_simple_api:app', 
            '--host', '0.0.0.0', 
            '--port', '8000', 
            '--reload'
        ], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to direct python execution
        print("⚠️ uvicorn not found, trying direct execution...")
        subprocess.run([sys.executable, 'ultra_simple_api.py'], check=True)

def start_frontend():
    """Start React frontend"""
    print("🚀 Starting React frontend...")
    os.chdir('frontend')
    
    # Start npm
    subprocess.run(['npm', 'start'], check=True)

def check_backend_health():
    """Check if backend is healthy"""
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get('http://localhost:8000/health', timeout=2)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Backend is healthy!")
                print(f"   Status: {result.get('status', 'Unknown')}")
                print(f"   Models loaded: {result.get('models_loaded', 'Unknown')}")
                return True
        except:
            pass
        
        print(f"⏳ Waiting for backend... ({i+1}/{max_retries})")
        time.sleep(2)
    
    print("❌ Backend failed to start")
    return False

def test_prediction():
    """Test prediction with sample data"""
    print("\n🧪 Testing prediction...")
    
    test_params = {
        "koi_period": 112.3,
        "koi_prad": 1.34,
        "koi_teq": 233,
        "koi_steff": 4402
    }
    
    try:
        response = requests.post('http://localhost:8000/predict', json=test_params, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction successful!")
            print(f"   Planet Name: {result.get('planet_name', 'Unknown')}")
            print(f"   Confidence: {result.get('confidence', 0) * 100:.1f}%")
            print(f"   Prediction: {result.get('prediction', 'Unknown')}")
            
            # Check if it's a real planet name
            planet_name = result.get('planet_name', '')
            if 'AI Predicted' in planet_name:
                print(f"   ⚠️  Showing AI Predicted result")
            elif 'Kepler-' in planet_name:
                print(f"   🎯 Real planet name returned!")
            
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Prediction test failed: {e}")

def main():
    """Main function"""
    print("🌌 NASA Exoplanet AI Platform - Local Development")
    print("=" * 60)
    
    # Get current directory
    original_dir = os.getcwd()
    
    print("📋 Starting local development environment...")
    print("1. Backend will run on: http://localhost:8000")
    print("2. Frontend will run on: http://localhost:3000")
    print("3. Press Ctrl+C to stop both services")
    
    try:
        # Start backend in a separate thread
        backend_thread = Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # Wait for backend to be ready
        os.chdir(original_dir)
        if check_backend_health():
            test_prediction()
            
            print("\n🎉 Backend is ready!")
            print("📱 Now starting frontend...")
            print("🌐 Browser will open automatically to http://localhost:3000")
            
            # Wait a moment then open browser
            time.sleep(2)
            webbrowser.open('http://localhost:3000')
            
            # Start frontend (this will block)
            start_frontend()
        else:
            print("❌ Backend failed to start, cannot continue")
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down development environment...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    main()
