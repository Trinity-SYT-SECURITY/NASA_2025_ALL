#!/usr/bin/env python3
"""
Test the similarity matching fix locally before deploying.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from ultra_simple_api import find_similar_planet, load_training_data, training_data
import pandas as pd
import numpy as np

def test_similarity_matching():
    """Test the similarity matching function with real planet data."""
    print("🧪 Testing similarity matching fix...")
    
    # Load training data
    load_training_data()
    
    if training_data is None or training_data.empty:
        print("❌ Training data not loaded")
        return False
    
    print(f"✅ Training data loaded: {len(training_data)} rows")
    
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
        "dec": 45.0,
        "koi_smass": 1.0,
        "koi_fpflag_nt": 0,
        "koi_fpflag_ss": 0,
        "koi_fpflag_co": 0,
        "koi_fpflag_ec": 0,
        "koi_score": 0.5
    }
    
    print("\n🔍 Testing with Kepler-62f parameters:")
    print(f"  Period: {test_data['koi_period']} days")
    print(f"  Radius: {test_data['koi_prad']} Earth radii")
    print(f"  Temperature: {test_data['koi_teq']} K")
    print(f"  Stellar Temperature: {test_data['koi_steff']} K")
    
    # Test similarity matching
    features = [test_data[col] for col in [
        'koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq',
        'koi_insol', 'koi_model_snr', 'koi_steff', 'koi_slogg', 'koi_srad',
        'koi_smass', 'koi_kepmag', 'koi_fpflag_nt', 'koi_fpflag_ss',
        'koi_fpflag_co', 'koi_fpflag_ec', 'ra', 'dec', 'koi_score'
    ]]
    
    similar_planet, similarity_score = find_similar_planet(features, test_data)
    
    if similar_planet is not None:
        planet_name = similar_planet['kepler_name']
        print(f"\n✅ SUCCESS: Found similar planet!")
        print(f"  Planet Name: {planet_name}")
        print(f"  Similarity Score: {similarity_score:.3f}")
        print(f"  Match Status: matched_existing")
        return True
    else:
        print(f"\n⚠️  No similar planet found")
        print(f"  Max Similarity Score: {similarity_score:.3f}")
        print(f"  Match Status: generated_name")
        return False

def test_multiple_planets():
    """Test with multiple planet types."""
    print("\n🔍 Testing multiple planet types...")
    
    test_cases = [
        {
            "name": "Kepler-442b (Earth-like)",
            "data": {
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
                "dec": 40.0,
                "koi_smass": 1.0,
                "koi_fpflag_nt": 0,
                "koi_fpflag_ss": 0,
                "koi_fpflag_co": 0,
                "koi_fpflag_ec": 0,
                "koi_score": 0.5
            }
        },
        {
            "name": "Kepler-22b (Super-Earth)",
            "data": {
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
                "dec": 45.0,
                "koi_smass": 1.0,
                "koi_fpflag_nt": 0,
                "koi_fpflag_ss": 0,
                "koi_fpflag_co": 0,
                "koi_fpflag_ec": 0,
                "koi_score": 0.5
            }
        }
    ]
    
    results = []
    for test_case in test_cases:
        print(f"\n  Testing {test_case['name']}...")
        
        features = [test_case['data'][col] for col in [
            'koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq',
            'koi_insol', 'koi_model_snr', 'koi_steff', 'koi_slogg', 'koi_srad',
            'koi_smass', 'koi_kepmag', 'koi_fpflag_nt', 'koi_fpflag_ss',
            'koi_fpflag_co', 'koi_fpflag_ec', 'ra', 'dec', 'koi_score'
        ]]
        
        similar_planet, similarity_score = find_similar_planet(features, test_case['data'])
        
        if similar_planet is not None:
            planet_name = similar_planet['kepler_name']
            print(f"    ✅ Found: {planet_name} (similarity: {similarity_score:.3f})")
            results.append(True)
        else:
            print(f"    ⚠️  No match (max similarity: {similarity_score:.3f})")
            results.append(False)
    
    return results

def main():
    """Main function to run all tests."""
    print("🔧 Testing Similarity Matching Fix")
    print("=" * 50)
    
    # Test basic similarity matching
    success = test_similarity_matching()
    
    # Test multiple planets
    results = test_multiple_planets()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    total_tests = 1 + len(results)
    successful_tests = (1 if success else 0) + sum(results)
    success_rate = (successful_tests / total_tests) * 100
    
    print(f"Total tests: {total_tests}")
    print(f"Successful matches: {successful_tests}")
    print(f"Success rate: {success_rate:.1f}%")
    
    if success_rate > 50:
        print("\n✅ Similarity matching fix is working!")
        print("   Ready to deploy to production.")
    else:
        print("\n⚠️  Similarity matching needs more work.")
        print("   Consider further adjustments before deploying.")
    
    print("\n💡 Next steps:")
    print("1. If tests pass, deploy the fixed backend")
    print("2. Test with the deployed API")
    print("3. Verify frontend integration")

if __name__ == "__main__":
    main()
