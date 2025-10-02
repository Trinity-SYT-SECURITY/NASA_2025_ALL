#!/usr/bin/env python3
"""
Test script to verify frontend-backend communication
"""

import requests
import json

def test_api_response_format():
    """Test the API response format that frontend expects"""
    print("🔧 Testing Frontend-Backend Communication")
    print("=" * 60)
    
    # Test with Kepler-442b parameters
    test_params = {
        "koi_period": 112.3,
        "koi_prad": 1.34,
        "koi_teq": 233,
        "koi_steff": 4402
    }
    
    api_url = "https://test-backend-2-ikqg.onrender.com/predict"
    
    print(f"🔍 Testing with parameters:")
    print(f"  Period: {test_params['koi_period']}")
    print(f"  Radius: {test_params['koi_prad']}")
    print(f"  Temperature: {test_params['koi_teq']}")
    print(f"  Stellar Temperature: {test_params['koi_steff']}")
    
    try:
        response = requests.post(api_url, json=test_params, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ API Response (Status: {response.status_code}):")
            print(f"Raw Response: {json.dumps(result, indent=2)}")
            
            # Check all fields that frontend expects
            expected_fields = [
                'planet_name', 'prediction', 'confidence', 'habitability_score',
                'planet_type', 'star_type', 'probabilities'
            ]
            
            print(f"\n📊 Field Analysis:")
            for field in expected_fields:
                value = result.get(field, 'MISSING')
                print(f"  {field}: {value}")
            
            # Specific checks for frontend display
            planet_name = result.get('planet_name', 'Unknown')
            confidence = result.get('confidence', 0)
            
            print(f"\n🎯 Frontend Display Values:")
            print(f"  Planet Name: '{planet_name}'")
            print(f"  Confidence: {confidence} ({confidence * 100:.1f}%)")
            print(f"  Is AI Predicted: {'Yes' if 'AI Predicted' in planet_name else 'No'}")
            print(f"  Is Real Planet: {'Yes' if 'Kepler-' in planet_name and 'AI Predicted' not in planet_name else 'No'}")
            
            # Check if this matches what user is seeing
            if 'AI Predicted' in planet_name and confidence < 0.9:
                print(f"\n❌ PROBLEM IDENTIFIED:")
                print(f"   API returns: {planet_name} with {confidence * 100:.1f}% confidence")
                print(f"   This matches what user is seeing in frontend!")
                print(f"   The issue is that the API is still returning old results.")
            else:
                print(f"\n✅ API Response looks correct!")
                print(f"   If frontend still shows old results, it might be caching.")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    print("\n" + "=" * 60)
    print("📋 TROUBLESHOOTING STEPS")
    print("=" * 60)
    print("1. Check if API returns correct planet names")
    print("2. Verify frontend cache is cleared")
    print("3. Check browser developer tools for API calls")
    print("4. Ensure frontend is calling the correct API endpoint")

if __name__ == "__main__":
    test_api_response_format()
