#!/usr/bin/env python3
"""
Streamlit Backend Launcher for Exoplanet Discovery Platform
Launches Streamlit in API-only mode for production use
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def main():
    print("🚀 Starting Streamlit Backend for Exoplanet Discovery Platform...")

    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    # Check if required files exist
    required_files = [
        'streamlit_api.py',
        '../ml/exoplanet_model_best.joblib',
        '../ml/scaler.joblib',
        '../ml/label_encoder.joblib',
        '../data/cumulative_2025.09.16_22.42.55.csv'
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure all ML models are trained and data files are available.")
        sys.exit(1)

    # Check if streamlit is installed
    try:
        import streamlit
        print(f"✅ Streamlit version: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit not installed. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'streamlit'])
        print("✅ Streamlit installed successfully")

    # Launch Streamlit in headless mode (API-only)
    print("🌐 Starting Streamlit API server...")
    print("📍 Server will be available at: http://localhost:8501")
    print("🔗 API endpoints:")
    print("   • GET /?endpoint=health")
    print("   • GET /?endpoint=stats")
    print("   • GET /?endpoint=predict&data={json}")
    print("   • GET /?endpoint=exoplanets")
    print("   • GET /?endpoint=test-ml")
    print("")
    print("Press Ctrl+C to stop the server")

    try:
        # Run streamlit with specific configuration for API-only mode
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run',
            'streamlit_api.py',
            '--server.port', '8501',
            '--server.address', '0.0.0.0',
            '--server.headless', 'true',
            '--theme.base', 'light'
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
