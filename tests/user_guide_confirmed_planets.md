# 🌟 User Guide: Finding Real Confirmed Exoplanets

## 🎯 Overview

This guide helps you understand what parameter combinations will find **real confirmed exoplanets** from NASA's Kepler mission instead of getting generic "AI Predicted Earth-like" results.

## 📊 Key Statistics

- **Total confirmed exoplanets in dataset**: 2,743
- **Earth-like planets** (0.8-1.5 Earth radii): 612
- **Super-Earths** (1.5-2.0 Earth radii): 537  
- **Gas Giants** (>2.0 Earth radii): 1,594
- **Habitable zone planets** (200-400K): 249

## 🔍 How to Find Real Planets

### Method 1: Use Exact Parameters from Real Planets

The AI system uses **similarity matching** - if your input parameters closely match a real confirmed exoplanet, it will return that planet's actual name instead of generating a generic one.

### Method 2: Parameter Ranges for Different Planet Types

#### 🌍 Earth-like Planets (0.8-1.5 Earth radii)
**Typical ranges:**
- **Orbital Period**: 10-400 days
- **Planet Radius**: 0.8-1.5 Earth radii
- **Equilibrium Temperature**: 200-400K (habitable zone)
- **Stellar Temperature**: 5000-6000K (Sun-like stars)

**Example combinations:**
```
Period: 365 days, Radius: 1.0, Temperature: 300K, Stellar Temp: 5800K
Period: 200 days, Radius: 1.2, Temperature: 280K, Stellar Temp: 5500K
Period: 100 days, Radius: 0.9, Temperature: 350K, Stellar Temp: 6000K
```

#### 🪐 Super-Earths (1.5-2.0 Earth radii)
**Typical ranges:**
- **Orbital Period**: 5-200 days
- **Planet Radius**: 1.5-2.0 Earth radii
- **Equilibrium Temperature**: 300-800K
- **Stellar Temperature**: 5000-6500K

**Example combinations:**
```
Period: 50 days, Radius: 1.8, Temperature: 500K, Stellar Temp: 5800K
Period: 30 days, Radius: 1.6, Temperature: 600K, Stellar Temp: 6000K
Period: 80 days, Radius: 2.0, Temperature: 400K, Stellar Temp: 5500K
```

#### 🪐 Gas Giants (>2.0 Earth radii)
**Typical ranges:**
- **Orbital Period**: 1-1000 days
- **Planet Radius**: 2.0-20+ Earth radii
- **Equilibrium Temperature**: 200-2000K
- **Stellar Temperature**: 4000-7000K

**Example combinations:**
```
Period: 10 days, Radius: 5.0, Temperature: 1000K, Stellar Temp: 6000K
Period: 100 days, Radius: 3.0, Temperature: 400K, Stellar Temp: 5500K
Period: 500 days, Radius: 8.0, Temperature: 200K, Stellar Temp: 5000K
```

## 🎯 Specific Test Cases

### High-Confidence Earth-like Planets
These parameters should find real confirmed Earth-like exoplanets:

| Planet Name | Period (days) | Radius (Earth) | Temperature (K) | Stellar Temp (K) |
|-------------|---------------|----------------|-----------------|------------------|
| Kepler-442b | 112.3 | 1.34 | 233 | 4402 |
| Kepler-62f | 267.3 | 1.41 | 208 | 4925 |
| Kepler-186f | 129.9 | 1.17 | 188 | 3788 |
| Kepler-452b | 384.8 | 1.63 | 265 | 5757 |

### High-Confidence Super-Earths
These parameters should find real confirmed Super-Earths:

| Planet Name | Period (days) | Radius (Earth) | Temperature (K) | Stellar Temp (K) |
|-------------|---------------|----------------|-----------------|------------------|
| Kepler-22b | 289.9 | 2.38 | 262 | 5518 |
| Kepler-69c | 242.5 | 1.71 | 299 | 5638 |
| Kepler-62e | 122.4 | 1.61 | 270 | 4925 |

### High-Confidence Gas Giants
These parameters should find real confirmed gas giants:

| Planet Name | Period (days) | Radius (Earth) | Temperature (K) | Stellar Temp (K) |
|-------------|---------------|----------------|-----------------|------------------|
| Kepler-10b | 0.8 | 1.47 | 2169 | 5627 |
| Kepler-11b | 10.3 | 1.80 | 900 | 5680 |
| Kepler-20b | 3.7 | 1.91 | 1033 | 5455 |

## 🚀 Quick Start Guide

### For First-Time Users:

1. **Start with Earth-like planets** - Use the parameters from the table above
2. **Copy exact values** - The AI will find the most similar real planet
3. **Check the result** - You should see the actual Kepler planet name
4. **Experiment with variations** - Try slightly different values to see how similarity matching works

### Pro Tips:

- **Use realistic combinations** - Don't mix extreme values (e.g., very hot temperature with very long period)
- **Focus on one planet type** - Stick to Earth-like, Super-Earth, or Gas Giant ranges
- **Check habitability** - Planets in the 200-400K temperature range are in the habitable zone
- **Consider stellar type** - Sun-like stars (5000-6000K) are most likely to have habitable planets

## 🔬 Understanding the Results

### What You'll See:

1. **Real Planet Name**: "Kepler-442b" (found similar planet)
2. **Generated Name**: "AI Predicted Earth-like" (no similar planet found)
3. **Similarity Score**: How close your input was to the real planet (0.0-1.0)
4. **Match Status**: "matched_existing" or "generated_name"

### Why You Get "AI Predicted Earth-like":

- Your parameters don't closely match any real confirmed exoplanet
- The similarity score is below 0.7 (70% similarity threshold)
- You're using unrealistic parameter combinations

## 📈 Success Rate Tips

- **Use the exact parameters** from the tables above for guaranteed results
- **Stay within realistic ranges** for each planet type
- **Focus on confirmed planets** - they have the most complete data
- **Try multiple combinations** - some planets are easier to match than others

## 🎮 Interactive Testing

Try these parameter combinations in the application:

### Earth-like Test:
```
Orbital Period: 112.3
Planet Radius: 1.34
Equilibrium Temperature: 233
Stellar Temperature: 4402
```

### Super-Earth Test:
```
Orbital Period: 50.0
Planet Radius: 1.8
Equilibrium Temperature: 500
Stellar Temperature: 5800
```

### Gas Giant Test:
```
Orbital Period: 10.3
Planet Radius: 1.8
Equilibrium Temperature: 900
Stellar Temperature: 5680
```

## 🔍 Advanced Users

For advanced users who want to explore the full dataset:

1. **Download the test cases**: `tests/confirmed_planet_test_cases.json`
2. **Use the analysis script**: `tests/analyze_confirmed_planets.py`
3. **Test API endpoints**: Use the provided test cases to verify the system

## 📚 References

- **NASA Kepler Mission**: https://www.nasa.gov/mission_pages/kepler/main/index.html
- **Kepler Objects of Interest**: https://exoplanetarchive.ipac.caltech.edu/
- **Habitable Zone Calculator**: https://depts.washington.edu/naivpl/content/hz-calculator

---

**Remember**: The AI system is trained on real NASA data, so using realistic parameters from actual exoplanets will give you the most accurate and interesting results!
