#!/usr/bin/env python3
"""
Analyze confirmed exoplanets from training data to create test cases
for the AI prediction system. This script extracts real planet parameters
to help users understand what input combinations will find actual planets.
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, List, Any

def load_and_analyze_data():
    """Load the training dataset and analyze confirmed exoplanets."""
    try:
        # Load the dataset
        df = pd.read_csv('data/cumulative_2025.09.16_22.42.55.csv')
        
        print(f"Total dataset size: {len(df)}")
        print(f"Columns available: {list(df.columns)}")
        
        # Filter for confirmed exoplanets with kepler_name
        confirmed = df[
            (df['koi_disposition'] == 'CONFIRMED') & 
            (df['kepler_name'].notna()) & 
            (df['kepler_name'] != '')
        ].copy()
        
        print(f"Confirmed exoplanets with names: {len(confirmed)}")
        
        # Select key parameters that users can input
        key_params = [
            'kepler_name', 'koi_period', 'koi_prad', 'koi_teq', 'koi_steff',
            'koi_duration', 'koi_depth', 'koi_insol', 'koi_model_snr', 
            'koi_slogg', 'koi_srad', 'koi_kepmag', 'ra', 'dec'
        ]
        
        # Get examples with all required parameters
        examples = confirmed[key_params].dropna()
        
        print(f"Confirmed exoplanets with complete data: {len(examples)}")
        
        return examples
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def create_test_cases(examples: pd.DataFrame) -> List[Dict[str, Any]]:
    """Create test cases from confirmed exoplanets."""
    test_cases = []
    
    for idx, row in examples.iterrows():
        # Create test case with user-input parameters
        test_case = {
            "planet_name": row['kepler_name'],
            "description": f"Real confirmed exoplanet: {row['kepler_name']}",
            "input_parameters": {
                "koi_period": float(row['koi_period']),
                "koi_duration": float(row['koi_duration']),
                "koi_depth": float(row['koi_depth']),
                "koi_prad": float(row['koi_prad']),
                "koi_teq": float(row['koi_teq']),
                "koi_insol": float(row['koi_insol']),
                "koi_model_snr": float(row['koi_model_snr']),
                "koi_steff": float(row['koi_steff']),
                "koi_slogg": float(row['koi_slogg']),
                "koi_srad": float(row['koi_srad']),
                "koi_kepmag": float(row['koi_kepmag']),
                "ra": float(row['ra']),
                "dec": float(row['dec'])
            },
            "expected_result": "CONFIRMED",
            "habitability_zone": "Habitable" if 200 <= row['koi_teq'] <= 400 else "Non-habitable",
            "planet_type": "Earth-like" if 0.8 <= row['koi_prad'] <= 1.5 else "Super-Earth" if row['koi_prad'] <= 2.0 else "Gas Giant"
        }
        
        test_cases.append(test_case)
    
    return test_cases

def categorize_planets(test_cases: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize planets by type and habitability."""
    categories = {
        "earth_like": [],
        "super_earth": [],
        "gas_giant": [],
        "habitable_zone": [],
        "hot_planets": [],
        "cold_planets": []
    }
    
    for case in test_cases:
        params = case["input_parameters"]
        period = params["koi_period"]
        radius = params["koi_prad"]
        temp = params["koi_teq"]
        
        # Categorize by size
        if 0.8 <= radius <= 1.5:
            categories["earth_like"].append(case)
        elif 1.5 < radius <= 2.0:
            categories["super_earth"].append(case)
        else:
            categories["gas_giant"].append(case)
        
        # Categorize by temperature
        if 200 <= temp <= 400:
            categories["habitable_zone"].append(case)
        elif temp > 400:
            categories["hot_planets"].append(case)
        else:
            categories["cold_planets"].append(case)
    
    return categories

def main():
    """Main function to analyze data and create test cases."""
    print("🔍 Analyzing confirmed exoplanets from training data...")
    
    # Load and analyze data
    examples = load_and_analyze_data()
    if examples is None:
        return
    
    # Create test cases
    test_cases = create_test_cases(examples)
    print(f"Created {len(test_cases)} test cases")
    
    # Categorize planets
    categories = categorize_planets(test_cases)
    
    # Print summary
    print("\n📊 Planet Categories:")
    for category, planets in categories.items():
        print(f"  {category}: {len(planets)} planets")
    
    # Save test cases to file
    output_file = "tests/confirmed_planet_test_cases.json"
    with open(output_file, 'w') as f:
        json.dump({
            "test_cases": test_cases,
            "categories": categories,
            "summary": {
                "total_confirmed_planets": len(test_cases),
                "earth_like": len(categories["earth_like"]),
                "super_earth": len(categories["super_earth"]),
                "gas_giant": len(categories["gas_giant"]),
                "habitable_zone": len(categories["habitable_zone"])
            }
        }, f, indent=2)
    
    print(f"\n💾 Test cases saved to: {output_file}")
    
    # Print some examples
    print("\n🌟 Example confirmed planets:")
    for i, case in enumerate(test_cases[:5]):
        print(f"\n{i+1}. {case['planet_name']}")
        print(f"   Period: {case['input_parameters']['koi_period']:.2f} days")
        print(f"   Radius: {case['input_parameters']['koi_prad']:.2f} Earth radii")
        print(f"   Temperature: {case['input_parameters']['koi_teq']:.0f} K")
        print(f"   Type: {case['planet_type']}")
        print(f"   Habitability: {case['habitability_zone']}")

if __name__ == "__main__":
    main()
