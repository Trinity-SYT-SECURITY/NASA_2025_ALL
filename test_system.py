#!/usr/bin/env python3
"""
Test script for the Exoplanet Discovery Platform
Tests ML models, API endpoints, and data processing
"""

import requests
import json
import sys
import time
from pathlib import Path

# Test configuration
API_BASE_URL = "http://localhost:8000"
TEST_TIMEOUT = 10

def test_ml_models():
    """Test that ML models are properly saved and loadable"""
    print("🔬 Testing ML Models...")
    
    model_files = [
        "ml/exoplanet_model_best.joblib",
        "ml/exoplanet_model_ensemble.joblib",
        "ml/scaler.joblib",
        "ml/label_encoder.joblib"
    ]
    
    for model_file in model_files:
        if Path(model_file).exists():
            print(f"✅ {model_file} exists")
        else:
            print(f"❌ {model_file} missing")
            return False
    
    print("✅ All ML model files present")
    return True

def test_api_health():
    """Test API health endpoint"""
    print("\n🌐 Testing API Health...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['status']}")
            print(f"   Models loaded: {data.get('models_loaded', False)}")
            print(f"   Data loaded: {data.get('data_loaded', False)}")
            return True
        else:
            print(f"❌ API Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API connection failed: {e}")
        return False

def test_api_stats():
    """Test API statistics endpoint"""
    print("\n📊 Testing API Statistics...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/stats", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Statistics retrieved:")
            print(f"   Total exoplanets: {data.get('total_exoplanets', 0)}")
            print(f"   Confirmed: {data.get('confirmed', 0)}")
            print(f"   Candidates: {data.get('candidates', 0)}")
            print(f"   Potentially habitable: {data.get('potentially_habitable', 0)}")
            return True
        else:
            print(f"❌ Statistics API failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Statistics API connection failed: {e}")
        return False

def test_api_exoplanets():
    """Test exoplanets data endpoint"""
    print("\n🪐 Testing Exoplanets Data...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/exoplanets?limit=10", timeout=TEST_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            exoplanets = data.get('exoplanets', [])
            print(f"✅ Retrieved {len(exoplanets)} exoplanets")
            if exoplanets:
                sample = exoplanets[0]
                print(f"   Sample: {sample.get('kepoi_name', 'Unknown')} - {sample.get('disposition', 'Unknown')}")
            return True
        else:
            print(f"❌ Exoplanets API failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Exoplanets API connection failed: {e}")
        return False

def test_api_prediction():
    """Test ML prediction endpoint"""
    print("\n🤖 Testing ML Prediction...")
    
    # Sample exoplanet data for testing
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
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict", 
            json=test_data, 
            timeout=TEST_TIMEOUT
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction successful:")
            print(f"   Prediction: {data.get('prediction', 'Unknown')}")
            print(f"   Confidence: {data.get('confidence', 0):.2%}")
            print(f"   Habitability: {data.get('habitability_score', 0):.1f}")
            print(f"   Planet type: {data.get('planet_type', 'Unknown')}")
            print(f"   Star type: {data.get('star_type', 'Unknown')}")
            return True
        else:
            print(f"❌ Prediction API failed: {response.status_code}")
            if response.text:
                print(f"   Error: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Prediction API connection failed: {e}")
        return False

def test_data_files():
    """Test that required data files exist"""
    print("\n📁 Testing Data Files...")
    
    data_files = [
        "data/cumulative_2025.09.16_22.42.55.csv",
        "data/NASA Exoplanet.csv",
        "data/exoTest.csv"
    ]
    
    for data_file in data_files:
        if Path(data_file).exists():
            file_size = Path(data_file).stat().st_size / (1024 * 1024)  # MB
            print(f"✅ {data_file} exists ({file_size:.1f} MB)")
        else:
            print(f"❌ {data_file} missing")
            return False
    
    print("✅ All data files present")
    return True

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 Starting Exoplanet Discovery Platform Tests")
    print("=" * 60)
    
    tests = [
        ("Data Files", test_data_files),
        ("ML Models", test_ml_models),
        ("API Health", test_api_health),
        ("API Statistics", test_api_stats),
        ("API Exoplanets", test_api_exoplanets),
        ("API Prediction", test_api_prediction),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
        
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! System is ready for deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
