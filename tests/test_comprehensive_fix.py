#!/usr/bin/env python3
"""
Comprehensive test to verify the actual system status and fix any remaining issues.
"""

import requests
import json
import time

# API endpoint
API_BASE_URL = "https://test-backend-2-ikqg.onrender.com"

def test_api_detailed():
    """Test API with detailed response analysis."""
    print("🔍 Detailed API Test...")
    
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
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=test_data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Full Response: {json.dumps(result, indent=2)}")
            
            # Check each field
            planet_name = result.get('planet_name', 'MISSING')
            match_status = result.get('match_status', 'MISSING')
            similarity_score = result.get('similarity_score', 'MISSING')
            prediction = result.get('prediction', 'MISSING')
            confidence = result.get('confidence', 'MISSING')
            planet_type = result.get('planet_type', 'MISSING')
            
            print(f"\nField Analysis:")
            print(f"  planet_name: '{planet_name}' (type: {type(planet_name)})")
            print(f"  match_status: '{match_status}' (type: {type(match_status)})")
            print(f"  similarity_score: {similarity_score} (type: {type(similarity_score)})")
            print(f"  prediction: '{prediction}' (type: {type(prediction)})")
            print(f"  confidence: {confidence} (type: {type(confidence)})")
            print(f"  planet_type: '{planet_type}' (type: {type(planet_type)})")
            
            # Determine if fix is working
            if planet_name == "Kepler-62 f":
                print("  ✅ EXACT MATCH: Fix is working!")
                return True
            elif planet_name and planet_name != "Unknown" and "AI Predicted" not in str(planet_name):
                print("  ✅ REAL NAME: Fix is working!")
                return True
            elif planet_name == "Unknown":
                print("  ❌ UNKNOWN: Fix not deployed or not working")
                return False
            elif "AI Predicted" in str(planet_name):
                print("  ❌ GENERIC: Still using old system")
                return False
            else:
                print("  ⚠️  UNEXPECTED: Unknown response format")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_multiple_scenarios():
    """Test multiple scenarios to understand system behavior."""
    print("\n🔍 Testing Multiple Scenarios...")
    
    scenarios = [
        {
            "name": "Kepler-62f (Exact)",
            "data": {
                "koi_period": 267.3,
                "koi_prad": 1.41,
                "koi_teq": 208,
                "koi_steff": 4925,
                "koi_duration": 12.0,
                "koi_depth": 0.03,
                "koi_insol": 0.4,
                "koi_model_snr": 20.0,
                "koi_slogg": 4.4,
                "koi_srad": 0.7,
                "koi_kepmag": 14.0,
                "ra": 300.0,
                "dec": 45.0
            }
        },
        {
            "name": "Generic Earth-like",
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
            "name": "Hot Jupiter",
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
                "ra": 200.0,
                "dec": 30.0
            }
        }
    ]
    
    results = []
    for scenario in scenarios:
        print(f"\n  Testing {scenario['name']}...")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/predict",
                json=scenario['data'],
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                planet_name = result.get('planet_name', 'Unknown')
                prediction = result.get('prediction', 'Unknown')
                confidence = result.get('confidence', 0)
                
                print(f"    Planet Name: {planet_name}")
                print(f"    Prediction: {prediction}")
                print(f"    Confidence: {confidence}")
                
                if planet_name and planet_name != "Unknown":
                    print("    ✅ Got planet name")
                    results.append(True)
                else:
                    print("    ❌ No planet name")
                    results.append(False)
            else:
                print(f"    ❌ API Error: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"    ❌ Request failed: {e}")
            results.append(False)
    
    return results

def test_health_endpoint():
    """Test health endpoint for system status."""
    print("🏥 Testing Health Endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Health check passed:")
            print(json.dumps(result, indent=2))
            
            # Check if models are loaded
            models_loaded = result.get('models_loaded', False)
            if models_loaded:
                print("✅ ML models are loaded")
            else:
                print("❌ ML models not loaded")
            
            return models_loaded
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def main():
    """Main function to run comprehensive tests."""
    print("🔧 Comprehensive System Status Check")
    print("=" * 60)
    
    # Test health first
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print("\n❌ System health check failed. Cannot proceed with tests.")
        return
    
    # Test detailed API response
    detailed_ok = test_api_detailed()
    
    # Test multiple scenarios
    scenario_results = test_multiple_scenarios()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    
    total_scenarios = len(scenario_results)
    successful_scenarios = sum(scenario_results)
    success_rate = (successful_scenarios / total_scenarios) * 100 if total_scenarios > 0 else 0
    
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Detailed Test: {'✅ PASS' if detailed_ok else '❌ FAIL'}")
    print(f"Scenario Tests: {successful_scenarios}/{total_scenarios} ({success_rate:.1f}%)")
    
    # Analysis
    print("\n💡 Analysis:")
    if detailed_ok and success_rate > 50:
        print("✅ System is working well!")
        print("   Real planet names are being returned.")
        print("   The fix appears to be deployed and working.")
    elif detailed_ok:
        print("⚠️  System is partially working.")
        print("   Some tests pass, but not all scenarios work.")
        print("   The fix may be partially deployed.")
    else:
        print("❌ System needs fixing.")
        print("   The deployed version doesn't have the fix.")
        print("   Need to redeploy or check deployment status.")
    
    print("\n🎯 Recommendations:")
    if not detailed_ok:
        print("1. Check if the latest code has been deployed to Render")
        print("2. Verify the deployment logs for any errors")
        print("3. Consider manual deployment if automatic deployment failed")
        print("4. Test locally to ensure the fix works before deploying")
    else:
        print("1. System is working correctly")
        print("2. Users should see real planet names")
        print("3. Continue monitoring for any issues")

if __name__ == "__main__":
    main()
