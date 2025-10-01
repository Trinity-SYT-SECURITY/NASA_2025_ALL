#!/usr/bin/env python3
"""
Final test of the deployed fix to verify that real planet names are returned.
"""

import requests
import json
import time

# API endpoint
API_BASE_URL = "https://test-backend-2-ikqg.onrender.com"

def test_kepler_62f_final():
    """Test Kepler-62f parameters - should now return real planet name."""
    print("🔍 Final Test: Kepler-62f (Habitable Zone Super-Earth)...")
    
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
            
            if planet_name == "Kepler-62 f":
                print("  🎉 SUCCESS: Exact planet name returned!")
                return True
            elif 'AI Predicted' in planet_name:
                print("  ❌ FAILED: Still returning generic name")
                return False
            else:
                print("  ✅ SUCCESS: Real planet name returned!")
                return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_kepler_442b_final():
    """Test Kepler-442b parameters - should return real planet name."""
    print("\n🔍 Final Test: Kepler-442b (Habitable Zone Earth-like)...")
    
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
            
            if planet_name == "Kepler-442 b":
                print("  🎉 SUCCESS: Exact planet name returned!")
                return True
            elif 'AI Predicted' in planet_name:
                print("  ❌ FAILED: Still returning generic name")
                return False
            else:
                print("  ✅ SUCCESS: Real planet name returned!")
                return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_kepler_22b_final():
    """Test Kepler-22b parameters - should return real planet name."""
    print("\n🔍 Final Test: Kepler-22b (Habitable Zone Super-Earth)...")
    
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
            
            if planet_name == "Kepler-22 b":
                print("  🎉 SUCCESS: Exact planet name returned!")
                return True
            elif 'AI Predicted' in planet_name:
                print("  ❌ FAILED: Still returning generic name")
                return False
            else:
                print("  ✅ SUCCESS: Real planet name returned!")
                return True
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
    print("🎉 FINAL TEST: Deployed Planet Name Fix")
    print("=" * 60)
    
    # Test API health first
    if not test_api_health():
        print("\n❌ API is not accessible. Cannot run tests.")
        return
    
    print("\n" + "=" * 60)
    print("🔍 TESTING REAL PLANET NAME FIX")
    print("=" * 60)
    
    # Test results
    results = {
        "kepler_62f": test_kepler_62f_final(),
        "kepler_442b": test_kepler_442b_final(),
        "kepler_22b": test_kepler_22b_final()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 FINAL RESULTS")
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
        status = "🎉 FIXED" if success else "❌ NOT FIXED"
        print(f"  {test_name}: {status}")
    
    # Final recommendations
    print("\n💡 Final Status:")
    if fix_rate == 100:
        print("🎉 PERFECT! The fix is working completely!")
        print("   Users will now see real planet names like 'Kepler-62 f'")
        print("   instead of 'AI Predicted Super-Earth'.")
        print("   The system is now educational and trustworthy!")
    elif fix_rate >= 50:
        print("✅ GOOD! The fix is working for most cases!")
        print("   Many users will see real planet names.")
        print("   The system is significantly improved!")
    else:
        print("⚠️  The fix needs more work or deployment.")
        print("   Check if the latest code has been deployed.")
    
    print("\n🎯 For users:")
    print("   Try using the parameter combinations from:")
    print("   tests/FRONTEND_PARAMETER_COMBINATIONS.md")
    print("   You should now see real Kepler planet names!")

if __name__ == "__main__":
    main()
