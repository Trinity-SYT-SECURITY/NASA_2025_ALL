
# Test script to verify different parameter combinations
import requests
import json

def test_parameter_combinations():
    """Test various parameter combinations"""
    backend_url = "https://test-backend-2-ikqg.onrender.com"
    
    test_cases = [
        {
            "name": "Earth-like Planet",
            "params": {"koi_period": 365.25, "koi_prad": 1.0, "koi_teq": 288, "koi_steff": 5778}
        },
        {
            "name": "Super-Earth",
            "params": {"koi_period": 112.3, "koi_prad": 1.34, "koi_teq": 233, "koi_steff": 4402}
        },
        {
            "name": "Hot Jupiter",
            "params": {"koi_period": 3.5, "koi_prad": 11.2, "koi_teq": 1200, "koi_steff": 6000}
        },
        {
            "name": "Kepler-452 b Parameters",
            "params": {"koi_period": 384.8, "koi_prad": 1.09, "koi_teq": 220, "koi_steff": 5579}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        try:
            response = requests.post(f"{backend_url}/predict", json=test_case['params'])
            result = response.json()
            
            print(f"  Planet Name: {result.get('planet_name', 'N/A')}")
            print(f"  Confidence: {result.get('confidence', 0)*100:.1f}%")
            print(f"  Status: {result.get('status', 'N/A')}")
            print(f"  Similarity Score: {result.get('similarity_score', 0):.3f}")
            
            if result.get('planet_name') == 'Kepler-1386 b':
                print("  ⚠️  Still returning Kepler-1386 b!")
            else:
                print("  ✅ Different planet returned")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    test_parameter_combinations()
