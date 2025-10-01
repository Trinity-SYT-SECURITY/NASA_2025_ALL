#!/usr/bin/env python3
"""
Test the deployed similarity matching fix to verify that real planet names
are now being returned instead of generic "AI Predicted" names.
"""

import requests
import json
import time
from typing import Dict, List, Any

# API endpoint
API_BASE_URL = "https://test-backend-2-ikqg.onrender.com"

def test_kepler_62f_fix():
    """Test Kepler-62f parameters - should now return real planet name."""
    print("🔍 Testing Kepler-62f Fix (Habitable Zone Super-Earth)...")
    
    # Exact parameters from Kepler-62f
    test_data = {
        "koi_period": 267.3,
        "koi_duration": 12.0,
        "koi_depth": 0.03,
        "koi_prad": 1.41,
        "koi_teq": 208,
        "koi_insol": 0.4,
        "koi_model_snr": 20.0,
        "koi_steff": 4925,
        "koi_slogg": 4.4,
        "koi_srad": 0.7,
        "koi_kepmag": 14.0,
        "ra": 300.0,
        "dec": 45.0
    }
    
    print(f"Input parameters:")
    print(f"  Orbital Period: {test_data['koi_period']} days")
    print(f"  Planet Radius: {test_data['koi_prad']} Earth radii")
    print(f"  Equilibrium Temperature: {test_data['koi_teq']} K")
    print(f"  Stellar Temperature: {test_data['koi_steff']} K")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ API Response:")
            print(f"  Planet Name: {result.get('planet_name', 'Unknown')}")
            print(f"  Match Status: {result.get('match_status', 'Unknown')}")
            print(f"  Similarity Score: {result.get('similarity_score', 0)}")
            print(f"  Prediction: {result.get('prediction', 'Unknown')}")
            print(f"  Confidence: {result.get('confidence', 0)}")
            print(f"  Planet Type: {result.get('planet_type', 'Unknown')}")
            print(f"  Habitability Score: {result.get('habitability_score', 0)}")
            
            # Check if fix is working
            planet_name = result.get('planet_name', '')
            match_status = result.get('match_status', '')
            similarity_score = result.get('similarity_score', 0)
            
            if match_status == 'matched_existing' and similarity_score > 0.3:
                print("  ✅ SUCCESS: Fix is working! Found real planet name!")
                return True
            elif 'AI Predicted' in planet_name:
                print("  ❌ FAILED: Still returning generic name")
                return False
            else:
                print("  ⚠️  PARTIAL: Got planet name but low similarity")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_kepler_442b_fix():
    """Test Kepler-442b parameters - should return real planet name."""
    print("\n🔍 Testing Kepler-442b Fix (Habitable Zone Earth-like)...")
    
    # Exact parameters from Kepler-442b
    test_data = {
        "koi_period": 112.3,
        "koi_duration": 8.0,
        "koi_depth": 0.02,
        "koi_prad": 1.34,
        "koi_teq": 233,
        "koi_insol": 0.7,
        "koi_model_snr": 15.0,
        "koi_steff": 4402,
        "koi_slogg": 4.6,
        "koi_srad": 0.6,
        "koi_kepmag": 15.0,
        "ra": 290.0,
        "dec": 40.0
    }
    
    print(f"Input parameters:")
    print(f"  Orbital Period: {test_data['koi_period']} days")
    print(f"  Planet Radius: {test_data['koi_prad']} Earth radii")
    print(f"  Equilibrium Temperature: {test_data['koi_teq']} K")
    print(f"  Stellar Temperature: {test_data['koi_steff']} K")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ API Response:")
            print(f"  Planet Name: {result.get('planet_name', 'Unknown')}")
            print(f"  Match Status: {result.get('match_status', 'Unknown')}")
            print(f"  Similarity Score: {result.get('similarity_score', 0)}")
            print(f"  Prediction: {result.get('prediction', 'Unknown')}")
            print(f"  Confidence: {result.get('confidence', 0)}")
            print(f"  Planet Type: {result.get('planet_type', 'Unknown')}")
            print(f"  Habitability Score: {result.get('habitability_score', 0)}")
            
            # Check if fix is working
            planet_name = result.get('planet_name', '')
            match_status = result.get('match_status', '')
            similarity_score = result.get('similarity_score', 0)
            
            if match_status == 'matched_existing' and similarity_score > 0.3:
                print("  ✅ SUCCESS: Fix is working! Found real planet name!")
                return True
            elif 'AI Predicted' in planet_name:
                print("  ❌ FAILED: Still returning generic name")
                return False
            else:
                print("  ⚠️  PARTIAL: Got planet name but low similarity")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_kepler_22b_fix():
    """Test Kepler-22b parameters - should return real planet name."""
    print("\n🔍 Testing Kepler-22b Fix (Habitable Zone Super-Earth)...")
    
    # Exact parameters from Kepler-22b
    test_data = {
        "koi_period": 289.9,
        "koi_duration": 18.0,
        "koi_depth": 0.05,
        "koi_prad": 2.38,
        "koi_teq": 262,
        "koi_insol": 1.1,
        "koi_model_snr": 30.0,
        "koi_steff": 5518,
        "koi_slogg": 4.4,
        "koi_srad": 0.9,
        "koi_kepmag": 12.0,
        "ra": 300.0,
        "dec": 45.0
    }
    
    print(f"Input parameters:")
    print(f"  Orbital Period: {test_data['koi_period']} days")
    print(f"  Planet Radius: {test_data['koi_prad']} Earth radii")
    print(f"  Equilibrium Temperature: {test_data['koi_teq']} K")
    print(f"  Stellar Temperature: {test_data['koi_steff']} K")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ API Response:")
            print(f"  Planet Name: {result.get('planet_name', 'Unknown')}")
            print(f"  Match Status: {result.get('match_status', 'Unknown')}")
            print(f"  Similarity Score: {result.get('similarity_score', 0)}")
            print(f"  Prediction: {result.get('prediction', 'Unknown')}")
            print(f"  Confidence: {result.get('confidence', 0)}")
            print(f"  Planet Type: {result.get('planet_type', 'Unknown')}")
            print(f"  Habitability Score: {result.get('habitability_score', 0)}")
            
            # Check if fix is working
            planet_name = result.get('planet_name', '')
            match_status = result.get('match_status', '')
            similarity_score = result.get('similarity_score', 0)
            
            if match_status == 'matched_existing' and similarity_score > 0.3:
                print("  ✅ SUCCESS: Fix is working! Found real planet name!")
                return True
            elif 'AI Predicted' in planet_name:
                print("  ❌ FAILED: Still returning generic name")
                return False
            else:
                print("  ⚠️  PARTIAL: Got planet name but low similarity")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_api_health():
    """Test if the API is accessible."""
    print("🏥 Testing API health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ API is accessible")
            print(f"  Status: {result.get('status', 'Unknown')}")
            print(f"  Models loaded: {result.get('models_loaded', False)}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def main():
    """Main function to run all tests."""
    print("🧪 Testing Deployed Similarity Matching Fix")
    print("=" * 60)
    
    # Test API health first
    if not test_api_health():
        print("\n❌ API is not accessible. Cannot run tests.")
        return
    
    print("\n" + "=" * 60)
    print("🔍 TESTING SIMILARITY MATCHING FIX")
    print("=" * 60)
    
    # Test results
    results = {
        "kepler_62f": test_kepler_62f_fix(),
        "kepler_442b": test_kepler_442b_fix(),
        "kepler_22b": test_kepler_22b_fix()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FIX VERIFICATION RESULTS")
    print("=" * 60)
    
    total_tests = len(results)
    successful_fixes = sum(results.values())
    fix_rate = (successful_fixes / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"Total tests: {total_tests}")
    print(f"Successful fixes: {successful_fixes}")
    print(f"Failed fixes: {total_tests - successful_fixes}")
    print(f"Fix success rate: {fix_rate:.1f}%")
    
    print("\nDetailed results:")
    for test_name, success in results.items():
        status = "✅ FIXED" if success else "❌ NOT FIXED"
        print(f"  {test_name}: {status}")
    
    # Recommendations
    print("\n💡 Recommendations:")
    if fix_rate == 100:
        print("🎉 EXCELLENT! The similarity matching fix is working perfectly!")
        print("   Users will now see real planet names instead of generic ones.")
        print("   The system is ready for production use.")
    elif fix_rate >= 50:
        print("✅ GOOD! The similarity matching fix is partially working.")
        print("   Some tests are finding real planets, which is an improvement.")
        print("   Consider further tuning for better results.")
    else:
        print("❌ The similarity matching fix needs more work.")
        print("   Most tests are still returning generic names.")
        print("   Check deployment logs and consider additional fixes.")
    
    print("\n🎯 For users:")
    if fix_rate >= 50:
        print("   You should now see real planet names like 'Kepler-62 f'")
        print("   instead of 'AI Predicted Super-Earth' for many inputs.")
        print("   The system is more educational and trustworthy now!")
    else:
        print("   The fix is still being deployed or needs more work.")
        print("   You may still see generic names for now.")

if __name__ == "__main__":
    main()
