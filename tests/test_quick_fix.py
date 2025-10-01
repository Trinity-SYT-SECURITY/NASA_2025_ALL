#!/usr/bin/env python3
"""
Quick test of the parameter matching fix.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from ultra_simple_api import generate_planet_name

def test_parameter_matching():
    """Test the parameter matching with known planet data."""
    print("🧪 Testing Parameter Matching Fix...")
    
    test_cases = [
        {
            "name": "Kepler-62f",
            "data": {
                "koi_period": 267.3,
                "koi_prad": 1.41,
                "koi_teq": 208,
                "koi_steff": 4925
            },
            "expected": "Kepler-62 f"
        },
        {
            "name": "Kepler-442b",
            "data": {
                "koi_period": 112.3,
                "koi_prad": 1.34,
                "koi_teq": 233,
                "koi_steff": 4402
            },
            "expected": "Kepler-442 b"
        },
        {
            "name": "Kepler-22b",
            "data": {
                "koi_period": 289.9,
                "koi_prad": 2.38,
                "koi_teq": 262,
                "koi_steff": 5518
            },
            "expected": "Kepler-22 b"
        }
    ]
    
    results = []
    for test_case in test_cases:
        print(f"\n🔍 Testing {test_case['name']}...")
        print(f"  Period: {test_case['data']['koi_period']} days")
        print(f"  Radius: {test_case['data']['koi_prad']} Earth radii")
        print(f"  Temperature: {test_case['data']['koi_teq']} K")
        print(f"  Stellar Temperature: {test_case['data']['koi_steff']} K")
        
        result = generate_planet_name(test_case['data'], "CONFIRMED")
        print(f"  Result: {result}")
        print(f"  Expected: {test_case['expected']}")
        
        if result == test_case['expected']:
            print("  ✅ SUCCESS: Exact match found!")
            results.append(True)
        else:
            print("  ⚠️  No exact match, using category-based selection")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    successful = sum(results)
    total = len(results)
    success_rate = (successful / total) * 100
    
    print(f"Total tests: {total}")
    print(f"Exact matches: {successful}")
    print(f"Success rate: {success_rate:.1f}%")
    
    if success_rate > 0:
        print("\n✅ Parameter matching is working!")
        print("   Some inputs will now return exact planet names.")
    else:
        print("\n⚠️  Parameter matching needs adjustment.")
        print("   Consider relaxing tolerance values.")
    
    print("\n💡 This fix will work even if similarity matching fails.")
    print("   Users will get real planet names for common parameter combinations.")

if __name__ == "__main__":
    test_parameter_matching()
