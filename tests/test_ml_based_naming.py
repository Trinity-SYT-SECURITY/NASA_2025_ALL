#!/usr/bin/env python3
"""
Test script to verify ML-based planet naming system
"""

import requests
import json

def test_ml_based_naming():
    """Test the ML-based planet naming system"""
    print("🔧 Testing ML-Based Planet Naming System")
    print("=" * 60)
    
    # Test cases with real planet parameters
    test_cases = [
        {
            "name": "Kepler-442b Parameters",
            "params": {
                "koi_period": 112.3,
                "koi_prad": 1.34,
                "koi_teq": 233,
                "koi_steff": 4402,
                "koi_duration": 6.0,
                "koi_depth": 500.0,
                "koi_insol": 1.0,
                "koi_model_snr": 25.0,
                "koi_slogg": 4.44,
                "koi_srad": 1.0,
                "koi_smass": 1.0,
                "koi_kepmag": 12.0,
                "ra": 290.0,
                "dec": 45.0,
                "koi_score": 0.5
            },
            "expected_type": "Real planet name from training data"
        },
        {
            "name": "Generic Earth-like",
            "params": {
                "koi_period": 300,
                "koi_prad": 1.2,
                "koi_teq": 250,
                "koi_steff": 5000
            },
            "expected_type": "AI Predicted or similar planet from training data"
        },
        {
            "name": "Large Gas Giant",
            "params": {
                "koi_period": 100,
                "koi_prad": 8.0,
                "koi_teq": 800,
                "koi_steff": 6000
            },
            "expected_type": "AI Predicted Giant or similar from training data"
        }
    ]
    
    api_url = "https://test-backend-2-ikqg.onrender.com/predict"
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        print(f"Expected: {test_case['expected_type']}")
        
        try:
            response = requests.post(api_url, json=test_case['params'], timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                planet_name = result.get('planet_name', 'Unknown')
                confidence = result.get('confidence', 0)
                status = result.get('status', 'unknown')
                match_status = result.get('match_status', 'unknown')
                similarity_score = result.get('similarity_score', 0)
                
                print(f"✅ API Response:")
                print(f"   Planet Name: {planet_name}")
                print(f"   Confidence: {confidence:.1%}")
                print(f"   Status: {status}")
                print(f"   Match Status: {match_status}")
                print(f"   Similarity Score: {similarity_score:.3f}")
                
                # Analyze the result
                if "AI Predicted" in planet_name:
                    print(f"📊 Result: ML-based prediction (no similar planet found)")
                elif "Kepler-" in planet_name:
                    print(f"🎯 Result: Real planet from training data!")
                    if similarity_score > 0.3:
                        print(f"   High similarity match (score: {similarity_score:.3f})")
                    else:
                        print(f"   Moderate similarity match (score: {similarity_score:.3f})")
                else:
                    print(f"❓ Result: Unexpected naming pattern")
                    
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print("\n" + "=" * 60)
    print("📊 ML-BASED NAMING TEST RESULTS")
    print("=" * 60)
    print("✅ System should use ML training data for planet naming")
    print("✅ High similarity matches should return real planet names")
    print("✅ Low similarity should return 'AI Predicted' names")
    print("✅ No hardcoded planet data should be used")

if __name__ == "__main__":
    test_ml_based_naming()
