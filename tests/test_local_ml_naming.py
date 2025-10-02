#!/usr/bin/env python3
"""
Local test to verify ML-based planet naming logic
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_local_ml_naming():
    """Test the ML-based planet naming logic locally"""
    print("🔧 Testing ML-Based Planet Naming Logic Locally")
    print("=" * 60)
    
    # Import the function
    try:
        from ultra_simple_api import generate_planet_name, find_similar_planet
        print("✅ Successfully imported functions")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return
    
    # Test data for Kepler-442b
    test_data = {
        'koi_period': 112.3,
        'koi_prad': 1.34,
        'koi_teq': 233,
        'koi_steff': 4402,
        'koi_duration': 6.0,
        'koi_depth': 500.0,
        'koi_insol': 1.0,
        'koi_model_snr': 25.0,
        'koi_slogg': 4.44,
        'koi_srad': 1.0,
        'koi_smass': 1.0,
        'koi_kepmag': 12.0,
        'koi_fpflag_nt': 0,
        'koi_fpflag_ss': 0,
        'koi_fpflag_co': 0,
        'koi_fpflag_ec': 0,
        'ra': 290.0,
        'dec': 45.0,
        'koi_score': 0.5
    }
    
    print(f"Input parameters:")
    print(f"  Period: {test_data['koi_period']}")
    print(f"  Radius: {test_data['koi_prad']}")
    print(f"  Temperature: {test_data['koi_teq']}")
    print(f"  Stellar Temperature: {test_data['koi_steff']}")
    
    # Test the generate_planet_name function
    try:
        planet_name = generate_planet_name(test_data, "CONFIRMED")
        print(f"\n📊 Results:")
        print(f"  Generated Planet Name: {planet_name}")
        
        if "AI Predicted" in planet_name:
            print("✅ Correctly using ML-based naming (no hardcoded data)")
        elif "Kepler-" in planet_name:
            print("✅ Found similar planet from training data")
        else:
            print("❓ Unexpected naming pattern")
            
    except Exception as e:
        print(f"❌ generate_planet_name failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test similarity matching directly
    try:
        features = [
            test_data.get('koi_period', 365.25),
            test_data.get('koi_duration', 6.0),
            test_data.get('koi_depth', 500.0),
            test_data.get('koi_prad', 1.0),
            test_data.get('koi_teq', 288.0),
            test_data.get('koi_insol', 1.0),
            test_data.get('koi_model_snr', 25.0),
            test_data.get('koi_steff', 5778.0),
            test_data.get('koi_slogg', 4.44),
            test_data.get('koi_srad', 1.0),
            test_data.get('koi_smass', 1.0),
            test_data.get('koi_kepmag', 12.0),
            test_data.get('koi_fpflag_nt', 0),
            test_data.get('koi_fpflag_ss', 0),
            test_data.get('koi_fpflag_co', 0),
            test_data.get('koi_fpflag_ec', 0),
            test_data.get('ra', 290.0),
            test_data.get('dec', 45.0),
            1 if 0.25 <= test_data.get('koi_insol', 1.0) <= 1.5 else 0,
            test_data.get('koi_score', 0.5)
        ]
        
        similar_planet, similarity_score = find_similar_planet(features, test_data)
        
        print(f"\n🔍 Similarity Matching:")
        print(f"  Similar Planet: {similar_planet}")
        print(f"  Similarity Score: {similarity_score}")
        
        if similar_planet is not None:
            kepler_name = similar_planet.get('kepler_name', 'No name')
            print(f"  Kepler Name: {kepler_name}")
        
    except Exception as e:
        print(f"❌ Similarity matching failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_local_ml_naming()
