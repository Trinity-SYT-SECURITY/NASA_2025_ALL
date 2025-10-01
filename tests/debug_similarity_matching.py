#!/usr/bin/env python3
"""
Debug the similarity matching system by testing with a simple API call
and checking the response details.
"""

import requests
import json

def test_simple_prediction():
    """Test a simple prediction to see what's happening with similarity matching."""
    
    # Simple test data - use exact parameters from a real confirmed planet
    test_data = {
        "koi_period": 9.48803557,  # From Kepler-227 b
        "koi_duration": 2.9575,
        "koi_depth": 0.022344,
        "koi_prad": 2.26,
        "koi_teq": 793,
        "koi_insol": 93.59,
        "koi_model_snr": 35.8,
        "koi_steff": 5455,
        "koi_slogg": 4.467,
        "koi_srad": 0.927,
        "koi_kepmag": 15.347,
        "ra": 291.93423,
        "dec": 48.141651
    }
    
    print("🧪 Testing similarity matching with real planet data...")
    print(f"Input data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            "https://test-backend-2-ikqg.onrender.com/predict",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ API Response:")
            print(json.dumps(result, indent=2))
            
            # Check key fields
            print(f"\n🔍 Analysis:")
            print(f"  Planet Name: {result.get('planet_name', 'Unknown')}")
            print(f"  Match Status: {result.get('match_status', 'Unknown')}")
            print(f"  Similarity Score: {result.get('similarity_score', 0)}")
            print(f"  Prediction: {result.get('prediction', 'Unknown')}")
            print(f"  Confidence: {result.get('confidence', 0)}")
            
            if result.get('match_status') == 'matched_existing':
                print("  ✅ SUCCESS: Found matching real planet!")
            else:
                print("  ⚠️  Generated name instead of real planet")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_health_endpoint():
    """Test the health endpoint to see system status."""
    print("🏥 Testing health endpoint...")
    
    try:
        response = requests.get("https://test-backend-2-ikqg.onrender.com/health", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Health check passed:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Health check failed: {e}")

def test_demo_endpoint():
    """Test the demo endpoint to see if it works."""
    print("\n🎮 Testing demo endpoint...")
    
    try:
        response = requests.get("https://test-backend-2-ikqg.onrender.com/demo", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Demo endpoint works:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Demo endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Demo endpoint failed: {e}")

def main():
    """Main function to run all debug tests."""
    print("🔧 Debugging Similarity Matching System")
    print("=" * 50)
    
    # Test health first
    test_health_endpoint()
    
    # Test demo endpoint
    test_demo_endpoint()
    
    # Test prediction with real data
    test_simple_prediction()
    
    print("\n💡 Debugging completed!")
    print("\nIf similarity matching is still not working, the issue might be:")
    print("1. Training data not loaded on the deployed backend")
    print("2. Feature column mismatch between input and training data")
    print("3. Similarity threshold too high (0.7)")
    print("4. Data preprocessing issues")

if __name__ == "__main__":
    main()
