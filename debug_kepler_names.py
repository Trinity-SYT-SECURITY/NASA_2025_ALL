#!/usr/bin/env python3
"""
調試腳本：檢查數據中實際有哪些行星有開普勒名稱
"""

import pandas as pd
import os

def analyze_kepler_names():
    """Analyze Kepler name distribution in data"""
    print("Analyzing Kepler name distribution...")

    # Load data
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'cumulative_2025.09.16_22.42.55.csv')

    if not os.path.exists(data_path):
        print(f"Data file does not exist: {data_path}")
        return

    try:
        df = pd.read_csv(data_path)
        print(f"Data loaded successfully: {len(df)} rows")

        # Check kepler_name column
        if 'kepler_name' not in df.columns:
            print("kepler_name column not found in data")
            return

        # Analyze kepler_name distribution
        kepler_names = df['kepler_name'].dropna()
        unique_names = kepler_names.unique()

        print("Kepler name statistics:")
        print(f"   Planets with Kepler names: {len(kepler_names)}")
        print(f"   Unique Kepler names: {len(unique_names)}")
        print(f"   Total planets: {len(df)}")
        print(f"   Percentage with names: {len(kepler_names)/len(df)*100:.1f}%")

        # Show first 20 Kepler names as examples
        print("First 20 Kepler name examples:")
        for i, name in enumerate(unique_names[:20]):
            count = (df['kepler_name'] == name).sum()
            print(f"   {i+1}. {name} ({count} samples)")

        # Check distribution by classification
        print("Distribution by classification:")
        for disposition in df['koi_disposition'].unique():
            subset = df[df['koi_disposition'] == disposition]
            named_subset = subset[subset['kepler_name'].notna()]
            print(f"   {disposition}: {len(named_subset)}/{len(subset)} have names")

        return df

    except Exception as e:
        print(f"Data analysis failed: {e}")
        return None

def test_similarity_with_real_data():
    """Test similarity matching with real data"""
    print("\nTesting similarity matching with real data...")

    df = analyze_kepler_names()
    if df is None:
        return

    # Select a planet with Kepler name for testing
    named_planets = df[df['kepler_name'].notna() & (df['kepler_name'] != '')]

    if len(named_planets) == 0:
        print("No planets with Kepler names found")
        return

    # Select first planet with Kepler name
    test_planet = named_planets.iloc[0]
    print(f"Selected test planet: {test_planet['kepler_name']}")

    # Prepare test features (same order as backend)
    feature_columns = [
        'koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq',
        'koi_insol', 'koi_model_snr', 'koi_steff', 'koi_slogg', 'koi_srad',
        'koi_smass', 'koi_kepmag', 'koi_fpflag_nt', 'koi_fpflag_ss',
        'koi_fpflag_co', 'koi_fpflag_ec', 'ra', 'dec', 'koi_score'
    ]

    # Extract test features
    test_features = []
    for col in feature_columns:
        value = test_planet.get(col, 0)
        test_features.append(float(value) if pd.notna(value) else 0.0)

    print(f"Test features prepared: {len(test_features)} features")

    # Test similarity matching (simulate backend logic)
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    # Prepare training data features (exclude test planet itself)
    train_subset = named_planets[named_planets.index != test_planet.name]

    if len(train_subset) > 0:
        train_features = train_subset[feature_columns].fillna(0).values
        input_vector = np.array(test_features).reshape(1, -1)

        similarities = cosine_similarity(input_vector, train_features)[0]
        max_sim_idx = np.argmax(similarities)
        max_similarity = similarities[max_sim_idx]

        print(f"Similarity test result: {max_similarity:.3f}")

        if max_similarity > 0.7:
            similar_planet = train_subset.iloc[max_sim_idx]
            print(f"Found similar planet: {similar_planet['kepler_name']} (similarity: {max_similarity:.3f})")
        else:
            print(f"No sufficiently similar planet found, max similarity: {max_similarity:.3f}")

def main():
    print("Kepler Name Analysis and Similarity Testing")
    print("=" * 60)

    # Analyze Kepler name distribution
    analyze_kepler_names()

    # Test similarity matching
    test_similarity_with_real_data()

    print("Analysis completed!")
    print("Now we know:")
    print("   - Number and distribution of planets with Kepler names")
    print("   - Can use this data for similarity matching tests")
    print("   - Backend should now correctly match real planet names")

if __name__ == "__main__":
    main()
