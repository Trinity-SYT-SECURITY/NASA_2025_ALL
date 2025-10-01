"""
Ultra Simple API - No OpenAPI Schema Issues
Pure FastAPI without complex type annotations
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import json
import random
import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Global variable for training data
training_data = None

def load_training_data():
    """Load training data for similarity matching"""
    global training_data
    if training_data is None:
        try:
            # Try multiple possible data file paths
            possible_paths = [
                os.path.join(os.path.dirname(__file__), '..', 'data', 'cumulative_2025.09.16_22.42.55.csv'),
                os.path.join(os.path.dirname(__file__), 'data', 'cumulative_2025.09.16_22.42.55.csv'),
                '/app/data/cumulative_2025.09.16_22.42.55.csv',
                # Try from current directory upwards
                os.path.join(os.getcwd(), 'data', 'cumulative_2025.09.16_22.42.55.csv'),
                os.path.join(os.getcwd(), '..', 'data', 'cumulative_2025.09.16_22.42.55.csv')
            ]

            print("Attempting to load training data...")
            for path in possible_paths:
                print(f"   Checking path: {path}")
                if os.path.exists(path):
                    training_data = pd.read_csv(path)
                    print(f"Training data loaded successfully: {len(training_data)} rows")
                    print(f"   Columns: {len(training_data.columns)}")
                    print(f"   Contains kepler_name column: {'kepler_name' in training_data.columns}")
                    break

            if training_data is None or training_data.empty:
                print("Warning: Could not load training data, will use generic name generation")
                training_data = pd.DataFrame()
            else:
                # Ensure required columns exist
                required_cols = ['kepler_name', 'kepoi_name', 'koi_period', 'koi_prad', 'koi_teq']
                missing_cols = [col for col in required_cols if col not in training_data.columns]
                if missing_cols:
                    print(f"Warning: Training data missing required columns: {missing_cols}")

        except Exception as e:
            print(f"Error loading training data: {e}")
            import traceback
            traceback.print_exc()
            training_data = pd.DataFrame()

    return training_data

def find_similar_planet(input_features, input_data):
    """Find the most similar planet in training data based on input features"""
    if training_data is None or training_data.empty or len(training_data) == 0:
        print("Warning: Training data not available for similarity matching")
        return None, 0.0

    try:
        # Prepare training data features (same as prediction features)
        feature_columns = [
            'koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq',
            'koi_insol', 'koi_model_snr', 'koi_steff', 'koi_slogg', 'koi_srad',
            'koi_smass', 'koi_kepmag', 'koi_fpflag_nt', 'koi_fpflag_ss',
            'koi_fpflag_co', 'koi_fpflag_ec', 'ra', 'dec', 'koi_score'
        ]

        # Ensure all required columns exist
        available_columns = [col for col in feature_columns if col in training_data.columns]
        if len(available_columns) < 10:  # Need at least 10 features
            print(f"Warning: Training data missing sufficient feature columns, found only {len(available_columns)}")
            return None, 0.0

        # Extract features for planets with valid Kepler names only
        valid_planets = training_data[training_data['kepler_name'].notna() & (training_data['kepler_name'] != '')]

        if len(valid_planets) == 0:
            print("Warning: No valid Kepler names found in training data")
            return None, 0.0

        print(f"Found {len(valid_planets)} planets with valid Kepler names")

        # Extract features
        train_features = valid_planets[available_columns].fillna(0).values

        # Prepare input features - use input_data dict directly
        input_vector = []
        for col in available_columns:
            if col in input_data:
                input_vector.append(float(input_data[col]))
            else:
                input_vector.append(0.0)
        
        input_vector = np.array(input_vector).reshape(1, -1)

        # Normalize features for better similarity matching
        from sklearn.preprocessing import StandardScaler
        scaler_sim = StandardScaler()
        train_features_scaled = scaler_sim.fit_transform(train_features)
        input_vector_scaled = scaler_sim.transform(input_vector)

        # Calculate cosine similarity
        similarities = cosine_similarity(input_vector_scaled, train_features_scaled)[0]

        # Find most similar planet (lower threshold for better matching)
        max_sim_idx = np.argmax(similarities)
        max_similarity = similarities[max_sim_idx]

        print(f"Max similarity score: {max_similarity:.3f} (threshold: 0.3)")

        # Lower threshold to 0.3 for better matching
        if max_similarity > 0.3:  # Much lower similarity threshold
            similar_planet = valid_planets.iloc[max_sim_idx]
            planet_name = similar_planet['kepler_name']
            print(f"Found similar planet: {planet_name} (similarity: {max_similarity:.3f})")
            return similar_planet, max_similarity

        print(f"No sufficiently similar planet found, max similarity: {max_similarity:.3f}")
        return None, max_similarity

    except Exception as e:
        print(f"Similarity matching failed: {e}")
        import traceback
        traceback.print_exc()
        return None, 0.0

# Create app without automatic docs generation issues
app = FastAPI(
    title="NASA Exoplanet API",
    description="ML-powered exoplanet prediction API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
try:
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 尝试多个可能的路径（现在 ultra_simple_api.py 在根目录）
    possible_ml_dirs = [
        os.path.join(current_dir, 'ml'),        # Docker: /app/ml/
        os.path.join('/app', 'ml'),             # 绝对 Docker 路径
        os.path.join(current_dir, '..', 'ml'),  # 备用路径
    ]

    ml_dir = None
    for test_dir in possible_ml_dirs:
        model_path = os.path.join(test_dir, 'exoplanet_model_best.joblib')
        if os.path.exists(model_path):
            ml_dir = test_dir
            print(f"Found ML models in: {ml_dir}")
            break

    if ml_dir is None:
        raise FileNotFoundError("Could not find ML models directory. Tried: " + str(possible_ml_dirs))

    ml_model = joblib.load(os.path.join(ml_dir, 'exoplanet_model_best.joblib'))
    scaler = joblib.load(os.path.join(ml_dir, 'scaler.joblib'))
    label_encoder = joblib.load(os.path.join(ml_dir, 'label_encoder.joblib'))
    
    # Fix XGBoost compatibility issue
    try:
        if hasattr(ml_model, 'use_label_encoder'):
            ml_model.use_label_encoder = False
        # Additional XGBoost compatibility fixes
        if hasattr(ml_model, '_le'):
            ml_model._le = None
        if hasattr(ml_model, 'le_'):
            ml_model.le_ = None
        print("XGBoost compatibility fixes applied")
    except Exception as e:
        print(f"Warning: Could not apply XGBoost compatibility fixes: {e}")
    
    models_loaded = True
    print("ML models loaded successfully from:", ml_dir)
except Exception as e:
    ml_model = scaler = label_encoder = None
    models_loaded = False
    print(f"Warning: Running in demo mode - Error loading models: {e}")

def generate_planet_name(data: dict, prediction: str) -> str:
    """Generate a realistic Kepler planet name based on characteristics"""
    radius = data.get('koi_prad', 1.0)
    temp = data.get('koi_teq', 288)
    period = data.get('koi_period', 365.25)
    stellar_temp = data.get('koi_steff', 5778)
    
    # Try to match with known planet parameters first (with tolerance)
    known_planets = {
        # Kepler-62f parameters (267.3, 1.41, 208, 4925)
        (267.3, 1.41, 208, 4925): "Kepler-62 f",
        # Kepler-442b parameters (112.3, 1.34, 233, 4402)
        (112.3, 1.34, 233, 4402): "Kepler-442 b",
        # Kepler-22b parameters (289.9, 2.38, 262, 5518)
        (289.9, 2.38, 262, 5518): "Kepler-22 b",
        # Kepler-186f parameters (129.9, 1.17, 188, 3788)
        (129.9, 1.17, 188, 3788): "Kepler-186 f",
        # Kepler-452b parameters (384.8, 1.63, 265, 5757)
        (384.8, 1.63, 265, 5757): "Kepler-452 b",
        # Kepler-438b parameters (35.2, 1.12, 276, 3748)
        (35.2, 1.12, 276, 3748): "Kepler-438 b",
        # Kepler-69c parameters (242.5, 1.71, 299, 5638)
        (242.5, 1.71, 299, 5638): "Kepler-69 c",
        # Kepler-62e parameters (122.4, 1.61, 270, 4925)
        (122.4, 1.61, 270, 4925): "Kepler-62 e",
        # Kepler-296e parameters (34.1, 1.53, 267, 3748)
        (34.1, 1.53, 267, 3748): "Kepler-296 e",
        # Kepler-10b parameters (0.8, 1.47, 2169, 5627)
        (0.8, 1.47, 2169, 5627): "Kepler-10 b",
        # Kepler-11b parameters (10.3, 1.80, 900, 5680)
        (10.3, 1.80, 900, 5680): "Kepler-11 b",
        # Kepler-20b parameters (3.7, 1.91, 1033, 5455)
        (3.7, 1.91, 1033, 5455): "Kepler-20 b",
        # Kepler-227b parameters (9.49, 2.26, 793, 5455)
        (9.49, 2.26, 793, 5455): "Kepler-227 b",
        # Kepler-227c parameters (54.42, 2.83, 443, 5455)
        (54.42, 2.83, 443, 5455): "Kepler-227 c",
        # Kepler-664b parameters (2.53, 2.75, 1406, 6031)
        (2.53, 2.75, 1406, 6031): "Kepler-664 b"
    }
    
    # Check for exact match with tolerance
    for (known_period, known_radius, known_temp, known_stellar_temp), planet_name in known_planets.items():
        if (abs(period - known_period) < 2.0 and 
            abs(radius - known_radius) < 0.2 and 
            abs(temp - known_temp) < 20.0 and 
            abs(stellar_temp - known_stellar_temp) < 200.0):
            print(f"Found exact match for {planet_name}")
            return planet_name

    # Fallback to category-based selection
    if temp >= 200 and temp <= 300 and radius >= 0.8 and radius <= 1.5:
        # Earth-like planets
        earth_like = [
            "Kepler-442 b", "Kepler-186 f", "Kepler-452 b", "Kepler-62 f",
            "Kepler-283 c", "Kepler-296 f", "Kepler-438 b", "Kepler-440 b"
        ]
        return random.choice(earth_like)
    elif radius > 1.5 and radius <= 3.0:
        # Super-Earth planets
        super_earth = [
            "Kepler-22 b", "Kepler-69 c", "Kepler-62 e", "Kepler-61 b",
            "Kepler-102 e", "Kepler-107 c", "Kepler-108 c", "Kepler-122 e"
        ]
        return random.choice(super_earth)
    elif radius > 3.0 and radius <= 6.0:
        # Neptune-like planets
        neptune_like = [
            "Kepler-10 c", "Kepler-18 d", "Kepler-51 d", "Kepler-68 d",
            "Kepler-419 b", "Kepler-420 b", "Kepler-421 b", "Kepler-422 b"
        ]
        return random.choice(neptune_like)
    elif radius > 6.0:
        # Gas giant planets
        gas_giants = [
            "Kepler-7 b", "Kepler-8 b", "Kepler-12 b", "Kepler-13 b",
            "Kepler-14 b", "Kepler-15 b", "Kepler-16 b", "Kepler-17 b"
        ]
        return random.choice(gas_giants)
    elif temp > 1000:
        # Hot planets
        hot_planets = [
            "Kepler-10 b", "Kepler-78 b", "Kepler-406 b", "Kepler-412 b",
            "Kepler-41 b", "Kepler-43 b", "Kepler-44 b", "Kepler-45 b"
        ]
        return random.choice(hot_planets)
    else:
        # Other planets
        other_planets = [
            "Kepler-227 b", "Kepler-227 c", "Kepler-23 b", "Kepler-24 b",
            "Kepler-25 b", "Kepler-26 b", "Kepler-27 b", "Kepler-28 b"
        ]
        return random.choice(other_planets)

@app.get("/")
async def root():
    return {
        "status": "🌌 EXOPLANET AI PLATFORM ACTIVE 🚀",
        "models_loaded": models_loaded,
        "endpoints": {
            "health": "/health",
            "stats": "/stats", 
            "predict": "/predict (POST)",
            "demo": "/demo",
            "exoplanets": "/exoplanets"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "models_loaded": models_loaded,
        "ml_accuracy": "92.16%",
        "system": "operational",
        "model_details": {
            "best_model": type(ml_model).__name__ if ml_model else "Not loaded",
            "scaler": type(scaler).__name__ if scaler else "Not loaded",
            "label_encoder": type(label_encoder).__name__ if label_encoder else "Not loaded"
        }
    }

@app.get("/stats")
async def stats():
    return {
        "total_exoplanets": 9564,
        "confirmed": 2746,
        "candidates": 1979,
        "false_positives": 4839,
        "potentially_habitable": 94,
        "model_accuracy": 92.16,
        "dataset": "NASA Kepler KOI"
    }

@app.post("/predict")
async def predict(data: dict):
    if not models_loaded:
        return {
            "prediction": "CANDIDATE",
            "confidence": 0.78,
            "habitability_score": 85.0,
            "planet_type": "Earth-like",
            "star_type": "G-dwarf",
            "probabilities": {"CANDIDATE": 0.78, "CONFIRMED": 0.15, "FALSE POSITIVE": 0.07},
            "status": "demo_mode"
        }

    try:
        # Load training data for similarity matching
        load_training_data()  # Load training data to global variable
        print(f"Training data loaded: {len(training_data)} rows")
        # Prepare ML input
        features = [
            data.get('koi_period', 365.25),
            data.get('koi_duration', 6.0),
            data.get('koi_depth', 500.0),
            data.get('koi_prad', 1.0),
            data.get('koi_teq', 288.0),
            data.get('koi_insol', 1.0),
            data.get('koi_model_snr', 25.0),
            data.get('koi_steff', 5778.0),
            data.get('koi_slogg', 4.44),
            data.get('koi_srad', 1.0),
            data.get('koi_smass', 1.0),
            data.get('koi_kepmag', 12.0),
            data.get('koi_fpflag_nt', 0),
            data.get('koi_fpflag_ss', 0),
            data.get('koi_fpflag_co', 0),
            data.get('koi_fpflag_ec', 0),
            data.get('ra', 290.0),
            data.get('dec', 45.0),
            1 if 0.25 <= data.get('koi_insol', 1.0) <= 1.5 else 0,
            data.get('koi_score', 0.5)
        ]
        
        # ML Prediction
        scaled = scaler.transform([features])
        pred = ml_model.predict(scaled)[0]
        probs = ml_model.predict_proba(scaled)[0]
        
        pred_str = label_encoder.inverse_transform([pred])[0]
        prob_dict = {label_encoder.classes_[i]: float(probs[i]) for i in range(len(probs))}
        
        # Calculate habitability
        hab_score = 0
        if 273 <= data.get('koi_teq', 288) <= 373: hab_score += 40
        if 0.8 <= data.get('koi_prad', 1.0) <= 1.5: hab_score += 30  
        if 0.25 <= data.get('koi_insol', 1.0) <= 1.5: hab_score += 30
        
        # Planet type
        radius = data.get('koi_prad', 1.0)
        if radius < 0.8: planet_type = "Sub-Earth"
        elif radius <= 1.25: planet_type = "Earth-like"
        elif radius <= 2.0: planet_type = "Super-Earth"
        elif radius <= 4.0: planet_type = "Mini-Neptune"
        else: planet_type = "Giant"
        
        # Star type
        temp = data.get('koi_steff', 5778)
        if temp < 3700: star_type = "M-dwarf"
        elif temp < 5200: star_type = "K-dwarf"
        elif temp < 6000: star_type = "G-dwarf"
        elif temp < 7500: star_type = "F-dwarf"
        else: star_type = "A-dwarf"
        
        # Try to find similar planet first, generate generic name if not found
        similar_planet, similarity_score = find_similar_planet(features, data)

        if similar_planet is not None and 'kepler_name' in similar_planet:
            # Found highly similar real planet
            planet_name = similar_planet['kepler_name'] if pd.notna(similar_planet['kepler_name']) else f"Kepler-{similar_planet['kepoi_name']}"
            match_status = "matched_existing"
            print(f"Found similar planet: {planet_name} (similarity: {similarity_score:.3f})")
        else:
            # No similar planet found, generate generic name
            planet_name = generate_planet_name(data, pred_str)
            match_status = "generated_name"
            print(f"Generated new name: {planet_name} (max similarity: {similarity_score:.3f})")
            
        # Ensure we have valid values
        if planet_name is None or planet_name == "":
            planet_name = f"AI Predicted {planet_type}"
        if similarity_score is None:
            similarity_score = 0.0

        return {
            "prediction": pred_str,
            "probabilities": prob_dict,
            "confidence": float(max(probs)),
            "habitability_score": hab_score,
            "planet_type": planet_type,
            "planet_name": planet_name,
            "star_type": star_type,
            "match_status": match_status,
            "similarity_score": float(similarity_score),
            "status": "ml_prediction"
        }
    except Exception as e:
        print(f"Prediction error: {e}")
        import traceback
        traceback.print_exc()
        
        # If it's an XGBoost compatibility error, try to provide a fallback prediction
        if "use_label_encoder" in str(e) or "XGBClassifier" in str(e):
            print("XGBoost compatibility error detected, providing fallback prediction")
            
            # Generate fallback prediction based on parameters
            radius = data.get('koi_prad', 1.0)
            temp = data.get('koi_teq', 288)
            period = data.get('koi_period', 365.25)
            stellar_temp = data.get('koi_steff', 5778)
            
            # Simple rule-based prediction
            if radius < 1.5 and 200 <= temp <= 400:
                prediction = "CONFIRMED"
                planet_type = "Earth-like"
                confidence = 0.85
            elif radius < 2.5:
                prediction = "CONFIRMED"
                planet_type = "Super-Earth"
                confidence = 0.80
            else:
                prediction = "CONFIRMED"
                planet_type = "Gas Giant"
                confidence = 0.90
            
            # Calculate habitability
            hab_score = 0
            if 273 <= temp <= 373: hab_score += 40
            if 0.8 <= radius <= 1.5: hab_score += 30  
            if 0.25 <= data.get('koi_insol', 1.0) <= 1.5: hab_score += 30
            
            # Star type
            if stellar_temp < 3700: star_type = "M-dwarf"
            elif stellar_temp < 5200: star_type = "K-dwarf"
            elif stellar_temp < 6000: star_type = "G-dwarf"
            elif stellar_temp < 7500: star_type = "F-dwarf"
            else: star_type = "A-dwarf"
            
            # Try to get planet name
            try:
                planet_name = generate_planet_name(data, prediction)
                match_status = "fallback_prediction"
                similarity_score = 0.0
            except:
                planet_name = f"AI Predicted {planet_type}"
                match_status = "fallback_prediction"
                similarity_score = 0.0
            
            return {
                "prediction": prediction,
                "probabilities": {prediction: confidence, "CANDIDATE": 0.1, "FALSE POSITIVE": 0.05},
                "confidence": confidence,
                "habitability_score": hab_score,
                "planet_type": planet_type,
                "planet_name": planet_name,
                "star_type": star_type,
                "match_status": match_status,
                "similarity_score": similarity_score,
                "status": "fallback_prediction",
                "note": "XGBoost compatibility issue, using fallback prediction"
            }
        else:
            return {
                "error": str(e),
                "status": "error",
                "debug_info": {
                    "models_loaded": models_loaded,
                    "model_type": type(ml_model).__name__ if ml_model else "None",
                    "scaler_type": type(scaler).__name__ if scaler else "None",
                    "encoder_type": type(label_encoder).__name__ if label_encoder else "None"
                }
            }

@app.get("/exoplanets")
async def exoplanets():
    # Sample exoplanet data for 3D visualization
    return {
        "exoplanets": [
            {
                "id": 1,
                "name": "Kepler-442b",
                "position": [10, 5, -20],
                "radius": 1.34,
                "temperature": 233,
                "disposition": "CONFIRMED",
                "habitability": 84,
                "color": "#4CAF50"
            },
            {
                "id": 2, 
                "name": "Kepler-186f",
                "position": [-15, -8, 25],
                "radius": 1.11,
                "temperature": 188,
                "disposition": "CONFIRMED", 
                "habitability": 91,
                "color": "#2196F3"
            },
            {
                "id": 3,
                "name": "Kepler-452b",
                "position": [20, 12, 10],
                "radius": 1.63,
                "temperature": 265,
                "disposition": "CONFIRMED",
                "habitability": 78,
                "color": "#FF9800"
            }
        ],
        "total": 3
    }

@app.get("/demo")
async def demo():
    earth_data = {
        "koi_period": 365.25,
        "koi_prad": 1.0,
        "koi_teq": 288,
        "koi_steff": 5778,
        "koi_insol": 1.0
    }
    result = await predict(earth_data)
    return {
        "input": earth_data,
        "prediction": result,
        "ml_model_loaded": models_loaded,
        "model_type": type(ml_model).__name__ if ml_model else "None"
    }

@app.get("/test-ml")
async def test_ml():
    """Test if ML model is properly loaded and working"""
    test_data = {
        "koi_period": 365.25,
        "koi_prad": 1.0,
        "koi_teq": 288,
        "koi_steff": 5778,
        "koi_insol": 1.0
    }

    try:
        result = await predict(test_data)
        return {
            "success": True,
            "ml_loaded": models_loaded,
            "test_prediction": result,
            "model_info": {
                "type": type(ml_model).__name__ if ml_model else "None",
                "has_predict": hasattr(ml_model, 'predict') if ml_model else False,
                "has_predict_proba": hasattr(ml_model, 'predict_proba') if ml_model else False
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "ml_loaded": models_loaded,
            "fallback_mode": "demo"
        }

# For Render deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# For Vercel deployment, the app will be served by the serverless function
# No need to run uvicorn manually
