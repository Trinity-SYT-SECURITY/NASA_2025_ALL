#!/usr/bin/env python3
"""
Test the local backend to verify the XGBoost compatibility fix works.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from ultra_simple_api import app, load_training_data, find_similar_planet
import uvicorn
import requests
import json

def test_local_backend():
    """Test the local backend with the fixed XGBoost model."""
    print("🧪 Testing local backend with XGBoost fix...")
    
    # Test data - use exact parameters from a real confirmed planet
    test_data = {
        "koi_period": 9.48803557,  # From Kepler-227 b
        "koi_duration": 2.9575,
        "koi_depth": 0.022344,
        "koi_prad": 2.26,
        "koi_teq": 793,
        "koi_insol": 93.59,
        "koi_model_snr": 35.8,
        "koi_steff": 5455,
        "koi_slogg": 4.467,
        "koi_srad": 0.927,
        "koi_kepmag": 15.347,
        "ra": 291.93423,
        "dec": 48.141651
    }
    
    try:
        # Test the prediction function directly
        from ultra_simple_api import ml_model, scaler, label_encoder, training_data
        
        if ml_model is None:
            print("❌ ML model not loaded")
            return
        
        print("✅ ML model loaded successfully")
        
        # Test similarity matching
        if training_data is not None and not training_data.empty:
            print("✅ Training data loaded successfully")
            
            # Test find_similar_planet function
            features = [test_data[col] for col in [
                'koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq',
                'koi_insol', 'koi_model_snr', 'koi_steff', 'koi_slogg', 'koi_srad',
                'koi_smass', 'koi_kepmag', 'koi_fpflag_nt', 'koi_fpflag_ss',
                'koi_fpflag_co', 'koi_fpflag_ec', 'ra', 'dec', 'koi_score'
            ]]
            
            similar_planet, similarity_score = find_similar_planet(features, test_data)
            
            if similar_planet is not None:
                print(f"✅ Found similar planet: {similar_planet['kepler_name']} (similarity: {similarity_score:.3f})")
            else:
                print(f"⚠️  No similar planet found (max similarity: {similarity_score:.3f})")
        else:
            print("❌ Training data not loaded")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function to run the test."""
    print("🔧 Testing Local Backend with XGBoost Fix")
    print("=" * 50)
    
    test_local_backend()
    
    print("\n💡 If the test passes, the fix is working!")
    print("Next step: Deploy the fixed backend to Render.")

if __name__ == "__main__":
    main()
