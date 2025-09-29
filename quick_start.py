#!/usr/bin/env python3
"""
Quick Start Script for Exoplanet Discovery Platform
Starts backend and provides demo functionality
"""

import subprocess
import sys
import time
import webbrowser
import requests
from pathlib import Path

def test_ml_models():
    """Test ML models are working"""
    print("🤖 Testing ML Models...")
    
    try:
        # Test prediction with sample data
        test_data = {
            "koi_period": 365.25,
            "koi_duration": 6.0,
            "koi_depth": 500.0,
            "koi_prad": 1.0,
            "koi_teq": 288.0,
            "koi_insol": 1.0,
            "koi_model_snr": 25.0,
            "koi_steff": 5778.0,
            "koi_slogg": 4.44,
            "koi_srad": 1.0,
            "koi_smass": 1.0,
            "koi_kepmag": 12.0,
            "ra": 290.0,
            "dec": 45.0
        }
        
        response = requests.post("http://localhost:8000/predict", json=test_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ML Prediction: {result['prediction']} ({result['confidence']:.1%} confidence)")
            print(f"   Planet Type: {result['planet_type']}")
            print(f"   Habitability: {result['habitability_score']:.1f}/100")
            return True
        else:
            print(f"❌ ML prediction failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ML test failed: {e}")
        return False

def test_data_api():
    """Test data API endpoints"""
    print("📊 Testing Data APIs...")
    
    try:
        # Test stats
        response = requests.get("http://localhost:8000/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Dataset Stats:")
            print(f"   Total Exoplanets: {stats['total_exoplanets']}")
            print(f"   Confirmed: {stats['confirmed']}")
            print(f"   Candidates: {stats['candidates']}")
            print(f"   Potentially Habitable: {stats['potentially_habitable']}")
        
        # Test exoplanet data
        response = requests.get("http://localhost:8000/exoplanets?limit=5", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {len(data['exoplanets'])} sample exoplanets")
        
        return True
    except Exception as e:
        print(f"❌ Data API test failed: {e}")
        return False

def start_backend():
    """Start backend server"""
    print("🚀 Starting Backend Server...")
    
    try:
        # Start backend process
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], cwd="backend")
        
        # Wait for server to start
        print("⏳ Waiting for backend to initialize...")
        time.sleep(8)
        
        # Test health
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print("✅ Backend server is healthy!")
            print(f"   Models loaded: {health.get('models_loaded', False)}")
            print(f"   Data loaded: {health.get('data_loaded', False)}")
            return backend_process
        else:
            print("❌ Backend health check failed")
            return None
            
    except Exception as e:
        print(f"❌ Backend startup failed: {e}")
        return None

def run_comprehensive_demo():
    """Run comprehensive platform demo"""
    print("\n🎮 Running Platform Demo...")
    print("-" * 50)
    
    # Test ML functionality
    if test_ml_models():
        print("✅ ML System: OPERATIONAL")
    else:
        print("❌ ML System: FAILED")
    
    # Test data APIs
    if test_data_api():
        print("✅ Data System: OPERATIONAL")
    else:
        print("❌ Data System: FAILED")
    
    print("-" * 50)
    print("🎯 Platform Demo Complete!")

def show_api_documentation():
    """Show API endpoints and usage"""
    print("\n📚 API DOCUMENTATION")
    print("=" * 60)
    print()
    print("🔗 Base URL: http://localhost:8000")
    print()
    print("📍 Endpoints:")
    print("   GET  /health          - System health check")
    print("   GET  /stats           - Dataset statistics")
    print("   GET  /exoplanets      - Get exoplanet data")
    print("   POST /predict         - ML exoplanet prediction")
    print("   GET  /docs            - Interactive API documentation")
    print()
    print("💡 Usage Examples:")
    print("   curl http://localhost:8000/health")
    print("   curl http://localhost:8000/stats")
    print("   curl http://localhost:8000/exoplanets?limit=10")
    print()
    print("🌐 Interactive Docs: http://localhost:8000/docs")

def main():
    """Main function"""
    print("=" * 80)
    print("🌌 EXOPLANET AI DISCOVERY PLATFORM - QUICK START 🌌")
    print("=" * 80)
    print()
    
    # Check if models exist
    model_files = [
        "ml/exoplanet_model_best.joblib",
        "ml/scaler.joblib",
        "ml/label_encoder.joblib"
    ]
    
    missing_models = [f for f in model_files if not Path(f).exists()]
    if missing_models:
        print("⚠️  Some ML models are missing. Training now...")
        try:
            subprocess.run([sys.executable, "exoplanet_classifier.py"], cwd="ml", check=True)
            print("✅ ML models trained successfully!")
        except:
            print("❌ ML training failed, continuing with demo mode...")
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Cannot start platform without backend")
        sys.exit(1)
    
    # Run demo
    run_comprehensive_demo()
    
    # Show documentation
    show_api_documentation()
    
    # Open browser to API docs
    print("\n🌐 Opening API Documentation...")
    try:
        webbrowser.open("http://localhost:8000/docs")
    except:
        print("⚠️  Please open http://localhost:8000/docs manually")
    
    print("\n" + "=" * 80)
    print("🎉 PLATFORM IS RUNNING!")
    print("=" * 80)
    print()
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs:    http://localhost:8000/docs")
    print()
    print("🎮 Try these commands:")
    print("   python test_system.py              # Run full system test")
    print("   curl http://localhost:8000/stats   # Get dataset statistics")
    print()
    print("🛑 Press Ctrl+C to stop the platform")
    print()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down platform...")
        if backend_process:
            backend_process.terminate()
        print("👋 Thank you for exploring the universe!")

if __name__ == "__main__":
    main()
