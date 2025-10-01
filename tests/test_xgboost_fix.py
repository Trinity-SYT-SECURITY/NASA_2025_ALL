#!/usr/bin/env python3
"""
Test the XGBoost compatibility fix and fallback prediction system.
"""

import requests
import json
import time

# API endpoint
API_BASE_URL = "https://test-backend-2-ikqg.onrender.com"

def test_xgboost_fallback():
    """Test if the XGBoost fallback system works."""
    print("🔍 Testing XGBoost Fallback System...")
    
    # Test with Kepler-62f parameters
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
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            # Check if we got a proper response
            if "error" in result:
                print("❌ Still getting error response")
                return False
            elif result.get("status") == "fallback_prediction":
                print("✅ Fallback prediction system is working!")
                print(f"  Planet Name: {result.get('planet_name', 'Unknown')}")
                print(f"  Prediction: {result.get('prediction', 'Unknown')}")
                print(f"  Planet Type: {result.get('planet_type', 'Unknown')}")
                print(f"  Confidence: {result.get('confidence', 0)}")
                return True
            elif result.get("status") == "ml_prediction":
                print("✅ ML prediction system is working!")
                print(f"  Planet Name: {result.get('planet_name', 'Unknown')}")
                print(f"  Prediction: {result.get('prediction', 'Unknown')}")
                print(f"  Planet Type: {result.get('planet_type', 'Unknown')}")
                print(f"  Confidence: {result.get('confidence', 0)}")
                return True
            else:
                print("⚠️  Unexpected response format")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_multiple_planet_types():
    """Test different planet types to ensure fallback works for all."""
    print("\n🔍 Testing Multiple Planet Types...")
    
    test_cases = [
        {
            "name": "Earth-like",
            "data": {
                "koi_period": 365.25,
                "koi_prad": 1.0,
                "koi_teq": 288,
                "koi_steff": 5778,
                "koi_duration": 12.0,
                "koi_depth": 0.01,
                "koi_insol": 1.0,
                "koi_model_snr": 15.0,
                "koi_slogg": 4.4,
                "koi_srad": 1.0,
                "koi_kepmag": 12.0,
                "ra": 180.0,
                "dec": 0.0
            }
        },
        {
            "name": "Super-Earth",
            "data": {
                "koi_period": 200.0,
                "koi_prad": 1.8,
                "koi_teq": 300,
                "koi_steff": 5500,
                "koi_duration": 14.0,
                "koi_depth": 0.03,
                "koi_insol": 0.8,
                "koi_model_snr": 20.0,
                "koi_slogg": 4.4,
                "koi_srad": 0.9,
                "koi_kepmag": 13.0,
                "ra": 200.0,
                "dec": 20.0
            }
        },
        {
            "name": "Gas Giant",
            "data": {
                "koi_period": 10.0,
                "koi_prad": 5.0,
                "koi_teq": 1000,
                "koi_steff": 6000,
                "koi_duration": 4.0,
                "koi_depth": 0.05,
                "koi_insol": 20.0,
                "koi_model_snr": 30.0,
                "koi_slogg": 4.3,
                "koi_srad": 1.0,
                "koi_kepmag": 12.0,
                "ra": 250.0,
                "dec": 40.0
            }
        }
    ]
    
    results = []
    for test_case in test_cases:
        print(f"\n  Testing {test_case['name']}...")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/predict",
                json=test_case['data'],
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if "error" not in result:
                    planet_name = result.get('planet_name', 'Unknown')
                    planet_type = result.get('planet_type', 'Unknown')
                    prediction = result.get('prediction', 'Unknown')
                    confidence = result.get('confidence', 0)
                    
                    print(f"    Planet Name: {planet_name}")
                    print(f"    Planet Type: {planet_type}")
                    print(f"    Prediction: {prediction}")
                    print(f"    Confidence: {confidence}")
                    
                    if planet_name and planet_name != "Unknown":
                        print("    ✅ Got planet name")
                        results.append(True)
                    else:
                        print("    ❌ No planet name")
                        results.append(False)
                else:
                    print(f"    ❌ Error: {result.get('error', 'Unknown error')}")
                    results.append(False)
            else:
                print(f"    ❌ API Error: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"    ❌ Request failed: {e}")
            results.append(False)
    
    return results

def main():
    """Main function to run all tests."""
    print("🔧 Testing XGBoost Compatibility Fix")
    print("=" * 60)
    
    # Test fallback system
    fallback_ok = test_xgboost_fallback()
    
    # Test multiple planet types
    type_results = test_multiple_planet_types()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 XGBOOST FIX TEST RESULTS")
    print("=" * 60)
    
    total_tests = len(type_results)
    successful_tests = sum(type_results)
    success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"Fallback System: {'✅ WORKING' if fallback_ok else '❌ NOT WORKING'}")
    print(f"Planet Type Tests: {successful_tests}/{total_tests} ({success_rate:.1f}%)")
    
    # Analysis
    print("\n💡 Analysis:")
    if fallback_ok and success_rate > 50:
        print("✅ XGBoost fix is working!")
        print("   The fallback system provides reasonable predictions.")
        print("   Users will get planet names and predictions.")
    elif fallback_ok:
        print("⚠️  Fallback system works but needs improvement.")
        print("   Some planet types work, others don't.")
    else:
        print("❌ XGBoost fix is not working.")
        print("   The deployed version doesn't have the fix.")
        print("   Need to redeploy the updated code.")
    
    print("\n🎯 Recommendations:")
    if not fallback_ok:
        print("1. Deploy the updated backend code to Render")
        print("2. Check deployment logs for any errors")
        print("3. Verify the XGBoost compatibility fixes are included")
        print("4. Test locally before deploying")
    else:
        print("1. System is working with fallback predictions")
        print("2. Users will get reasonable results")
        print("3. Consider fixing the XGBoost issue for better accuracy")

if __name__ == "__main__":
    main()
