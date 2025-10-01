#!/usr/bin/env python3
"""
測試相似性匹配功能
確認後端現在能正確返回實際行星名稱而不是通用名稱
"""

import requests
import json

def test_similarity_matching():
    """Test similarity matching functionality"""
    base_url = "https://test-backend-2-ikqg.onrender.com"

    print("Testing similarity matching functionality")
    print("=" * 50)

    # Test cases: Use parameters similar to known planets
    test_cases = [
        {
            "name": "Parameters similar to Kepler-442b",
            "data": {
                "koi_period": 112.3,
                "koi_prad": 1.34,
                "koi_teq": 233,
                "koi_steff": 4402,
                "koi_slogg": 4.54,
                "koi_srad": 0.60,
                "koi_smass": 0.61,
                "koi_kepmag": 14.98,
                "koi_score": 1.0,
                "ra": 291.934,
                "dec": 48.142
            }
        },
        {
            "name": "Parameters similar to Kepler-186f",
            "data": {
                "koi_period": 129.9,
                "koi_prad": 1.11,
                "koi_teq": 188,
                "koi_steff": 3755,
                "koi_slogg": 4.69,
                "koi_srad": 0.52,
                "koi_smass": 0.54,
                "koi_kepmag": 15.99,
                "koi_score": 1.0,
                "ra": 292.246,
                "dec": 43.732
            }
        },
        {
            "name": "Completely different parameters (should generate generic name)",
            "data": {
                "koi_period": 50.0,
                "koi_prad": 5.0,
                "koi_teq": 1000,
                "koi_steff": 8000,
                "koi_slogg": 3.0,
                "koi_srad": 2.0,
                "koi_smass": 1.5,
                "koi_kepmag": 10.0,
                "koi_score": 0.1,
                "ra": 100.0,
                "dec": 20.0
            }
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Test: {test_case['name']}")

        try:
            response = requests.post(f"{base_url}/predict", json=test_case['data'], timeout=15)
            print(f"   Status code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"   Prediction result: {data.get('prediction')}")
                print(f"   Planet name: {data.get('planet_name')}")
                print(f"   Match status: {data.get('match_status')}")
                print(f"   Similarity score: {data.get('similarity_score', 0):.3f}")

                if data.get('match_status') == 'matched_existing':
                    print("   Successfully matched existing planet!")
                elif data.get('match_status') == 'generated_name':
                    print("   Generated generic name (normal)")
                else:
                    print("   Unknown match status")
            else:
                print(f"   Request failed: {response.text}")

        except Exception as e:
            print(f"   Test error: {e}")

def test_backend_health():
    """Test backend health status"""
    print("Checking backend health status...")

    base_url = "https://test-backend-2-ikqg.onrender.com"

    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("Backend running normally")
            print(f"   Models loaded: {data.get('models_loaded')}")
            print(f"   ML accuracy: {data.get('ml_accuracy')}")
            return True
        else:
            print(f"Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Backend connection failed: {e}")
        return False

def main():
    print("Similarity Matching Test")
    print("=" * 50)

    # 先檢查後端健康狀態
    if not test_backend_health():
        print("Backend unavailable, cannot perform tests")
        return

    # 測試相似性匹配功能
    test_similarity_matching()

    print("Test completed!")
    print("Backend should now be able to:")
    print("   Match similar real planet names")
    print("   Generate generic names when no similar planets found")
    print("   Provide similarity scores for frontend reference")
if __name__ == "__main__":
    main()
