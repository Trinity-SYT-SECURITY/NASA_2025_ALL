#!/usr/bin/env python3
"""
Test script to verify improved confidence calculation
"""

import requests
import json

def test_confidence_improvements():
    """Test the improved confidence calculation"""
    print("🔧 Testing Improved Confidence Calculation")
    print("=" * 60)
    
    # Test real planet parameters
    test_cases = [
        {
            "name": "Kepler-62f (Real Planet)",
            "params": {
                "koi_period": 267.3,
                "koi_prad": 1.41,
                "koi_teq": 208,
                "koi_steff": 4925
            },
            "expected_min_confidence": 0.90
        },
        {
            "name": "Kepler-442b (Real Planet)",
            "params": {
                "koi_period": 112.3,
                "koi_prad": 1.34,
                "koi_teq": 233,
                "koi_steff": 4402
            },
            "expected_min_confidence": 0.90
        },
        {
            "name": "Generic Earth-like",
            "params": {
                "koi_period": 300,
                "koi_prad": 1.2,
                "koi_teq": 250,
                "koi_steff": 5000
            },
            "expected_min_confidence": 0.70
        }
    ]
    
    api_url = "https://test-backend-2-ikqg.onrender.com/predict"
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        print(f"Parameters: {test_case['params']}")
        
        try:
            response = requests.post(api_url, json=test_case['params'], timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                confidence = result.get('confidence', 0)
                planet_name = result.get('planet_name', 'Unknown')
                status = result.get('status', 'unknown')
                
                print(f"✅ API Response:")
                print(f"   Planet Name: {planet_name}")
                print(f"   Confidence: {confidence:.1%}")
                print(f"   Status: {status}")
                
                if confidence >= test_case['expected_min_confidence']:
                    print(f"✅ Confidence meets expectation (≥{test_case['expected_min_confidence']:.1%})")
                else:
                    print(f"❌ Confidence too low: {confidence:.1%} < {test_case['expected_min_confidence']:.1%}")
                    
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print("\n" + "=" * 60)
    print("📊 CONFIDENCE TEST RESULTS")
    print("=" * 60)
    print("✅ Real planets should have ≥90% confidence")
    print("✅ Generic predictions should have ≥70% confidence")
    print("✅ System should provide meaningful confidence scores")

if __name__ == "__main__":
    test_confidence_improvements()
