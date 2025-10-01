#!/usr/bin/env python3
"""
Test the API endpoints with real confirmed exoplanet data to verify
that the similarity matching system works correctly and returns
actual planet names instead of generic predictions.
"""

import requests
import json
import time
from typing import Dict, List, Any

# API endpoint
API_BASE_URL = "https://test-backend-2-ikqg.onrender.com"

def test_api_health():
    """Test if the API is accessible."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ API is accessible")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def test_prediction_with_real_planet(planet_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test prediction with real planet data."""
    try:
        # Prepare the input data
        input_data = {
            "koi_period": planet_data["input_parameters"]["koi_period"],
            "koi_duration": planet_data["input_parameters"]["koi_duration"],
            "koi_depth": planet_data["input_parameters"]["koi_depth"],
            "koi_prad": planet_data["input_parameters"]["koi_prad"],
            "koi_teq": planet_data["input_parameters"]["koi_teq"],
            "koi_insol": planet_data["input_parameters"]["koi_insol"],
            "koi_model_snr": planet_data["input_parameters"]["koi_model_snr"],
            "koi_steff": planet_data["input_parameters"]["koi_steff"],
            "koi_slogg": planet_data["input_parameters"]["koi_slogg"],
            "koi_srad": planet_data["input_parameters"]["koi_srad"],
            "koi_kepmag": planet_data["input_parameters"]["koi_kepmag"],
            "ra": planet_data["input_parameters"]["ra"],
            "dec": planet_data["input_parameters"]["dec"]
        }
        
        # Make the prediction request
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=input_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "input_planet": planet_data["planet_name"],
                "predicted_planet": result.get("planet_name", "Unknown"),
                "prediction": result.get("prediction", "Unknown"),
                "confidence": result.get("confidence", 0),
                "similarity_score": result.get("similarity_score", 0),
                "match_status": result.get("match_status", "Unknown"),
                "habitability_score": result.get("habitability_score", 0),
                "planet_type": result.get("planet_type", "Unknown")
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "input_planet": planet_data["planet_name"]
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "input_planet": planet_data["planet_name"]
        }

def load_test_cases() -> List[Dict[str, Any]]:
    """Load test cases from the generated file."""
    try:
        with open("tests/confirmed_planet_test_cases.json", 'r') as f:
            data = json.load(f)
            return data["test_cases"]
    except Exception as e:
        print(f"❌ Failed to load test cases: {e}")
        return []

def run_comprehensive_test():
    """Run comprehensive test with real planet data."""
    print("🚀 Starting comprehensive API test with real planet data...")
    
    # Check API health
    if not test_api_health():
        return
    
    # Load test cases
    test_cases = load_test_cases()
    if not test_cases:
        return
    
    print(f"📊 Loaded {len(test_cases)} test cases")
    
    # Test different categories
    categories = {
        "earth_like": [case for case in test_cases if case["planet_type"] == "Earth-like"],
        "super_earth": [case for case in test_cases if case["planet_type"] == "Super-Earth"],
        "gas_giant": [case for case in test_cases if case["planet_type"] == "Gas Giant"],
        "habitable_zone": [case for case in test_cases if case["habitability_zone"] == "Habitable"]
    }
    
    results = {
        "total_tests": 0,
        "successful_matches": 0,
        "failed_matches": 0,
        "category_results": {}
    }
    
    # Test each category
    for category_name, category_cases in categories.items():
        if not category_cases:
            continue
            
        print(f"\n🔍 Testing {category_name} planets ({len(category_cases)} cases)...")
        
        category_results = {
            "total": 0,
            "matched": 0,
            "generated": 0,
            "failed": 0,
            "examples": []
        }
        
        # Test first 10 cases from each category
        test_sample = category_cases[:10]
        
        for i, test_case in enumerate(test_sample):
            print(f"  Testing {i+1}/10: {test_case['planet_name']}")
            
            result = test_prediction_with_real_planet(test_case)
            category_results["total"] += 1
            results["total_tests"] += 1
            
            if result["success"]:
                if result["match_status"] == "matched_existing":
                    category_results["matched"] += 1
                    results["successful_matches"] += 1
                    print(f"    ✅ Matched: {result['predicted_planet']} (similarity: {result['similarity_score']:.3f})")
                else:
                    category_results["generated"] += 1
                    results["failed_matches"] += 1
                    print(f"    ⚠️  Generated: {result['predicted_planet']} (similarity: {result['similarity_score']:.3f})")
                
                # Store example results
                if len(category_results["examples"]) < 3:
                    category_results["examples"].append(result)
            else:
                category_results["failed"] += 1
                print(f"    ❌ Failed: {result['error']}")
            
            # Add delay to avoid overwhelming the API
            time.sleep(1)
        
        results["category_results"][category_name] = category_results
        
        # Print category summary
        match_rate = (category_results["matched"] / category_results["total"]) * 100 if category_results["total"] > 0 else 0
        print(f"  📈 {category_name} match rate: {match_rate:.1f}% ({category_results['matched']}/{category_results['total']})")
    
    # Print overall results
    print("\n" + "="*60)
    print("📊 COMPREHENSIVE TEST RESULTS")
    print("="*60)
    
    overall_match_rate = (results["successful_matches"] / results["total_tests"]) * 100 if results["total_tests"] > 0 else 0
    
    print(f"Total tests: {results['total_tests']}")
    print(f"Successful matches: {results['successful_matches']}")
    print(f"Failed matches: {results['failed_matches']}")
    print(f"Overall match rate: {overall_match_rate:.1f}%")
    
    print("\n📋 Category Breakdown:")
    for category, cat_results in results["category_results"].items():
        match_rate = (cat_results["matched"] / cat_results["total"]) * 100 if cat_results["total"] > 0 else 0
        print(f"  {category}: {match_rate:.1f}% ({cat_results['matched']}/{cat_results['total']})")
    
    # Save detailed results
    with open("tests/api_test_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: tests/api_test_results.json")
    
    # Print recommendations
    print("\n💡 Recommendations:")
    if overall_match_rate > 70:
        print("✅ Excellent! The similarity matching system is working well.")
    elif overall_match_rate > 50:
        print("⚠️  Good performance, but there's room for improvement.")
    else:
        print("❌ The similarity matching system needs improvement.")
    
    print("\n🎯 For best results, use the parameter combinations from:")
    print("   tests/user_guide_confirmed_planets.md")

def test_specific_planets():
    """Test specific well-known planets."""
    print("\n🌟 Testing specific well-known planets...")
    
    # Well-known confirmed exoplanets
    famous_planets = [
        {
            "name": "Kepler-442b",
            "params": {
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
                "dec": 40.0
            }
        },
        {
            "name": "Kepler-22b",
            "params": {
                "koi_period": 289.9,
                "koi_duration": 12.0,
                "koi_depth": 0.05,
                "koi_prad": 2.38,
                "koi_teq": 262,
                "koi_insol": 1.1,
                "koi_model_snr": 20.0,
                "koi_steff": 5518,
                "koi_slogg": 4.4,
                "koi_srad": 0.9,
                "koi_kepmag": 12.0,
                "ra": 300.0,
                "dec": 45.0
            }
        }
    ]
    
    for planet in famous_planets:
        print(f"\n🔍 Testing {planet['name']}...")
        
        result = test_prediction_with_real_planet({
            "planet_name": planet["name"],
            "input_parameters": planet["params"]
        })
        
        if result["success"]:
            print(f"  Input: {planet['name']}")
            print(f"  Output: {result['predicted_planet']}")
            print(f"  Match Status: {result['match_status']}")
            print(f"  Similarity Score: {result['similarity_score']:.3f}")
            print(f"  Confidence: {result['confidence']:.3f}")
            
            if result["match_status"] == "matched_existing":
                print("  ✅ SUCCESS: Found matching real planet!")
            else:
                print("  ⚠️  Generated name instead of real planet")
        else:
            print(f"  ❌ FAILED: {result['error']}")

def main():
    """Main function to run all tests."""
    print("🧪 API Testing with Real Planet Data")
    print("="*50)
    
    # Test specific famous planets first
    test_specific_planets()
    
    # Run comprehensive test
    run_comprehensive_test()
    
    print("\n🎉 Testing completed!")
    print("\n📚 Next steps:")
    print("1. Check the results in tests/api_test_results.json")
    print("2. Use the user guide: tests/user_guide_confirmed_planets.md")
    print("3. Try the parameter combinations in the application")

if __name__ == "__main__":
    main()
