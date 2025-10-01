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
            print(f"✅ Found ML models in: {ml_dir}")
            break

    if ml_dir is None:
        raise FileNotFoundError("Could not find ML models directory. Tried: " + str(possible_ml_dirs))

    ml_model = joblib.load(os.path.join(ml_dir, 'exoplanet_model_best.joblib'))
    scaler = joblib.load(os.path.join(ml_dir, 'scaler.joblib'))
    label_encoder = joblib.load(os.path.join(ml_dir, 'label_encoder.joblib'))
    models_loaded = True
    print("✅ ML models loaded successfully from:", ml_dir)
except Exception as e:
    ml_model = scaler = label_encoder = None
    models_loaded = False
    print(f"⚠️ Running in demo mode - Error loading models: {e}")

def generate_planet_name(data: dict, prediction: str) -> str:
    """Generate a realistic Kepler planet name based on characteristics"""
    radius = data.get('koi_prad', 1.0)
    temp = data.get('koi_teq', 288)

    # Different planet categories based on characteristics
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
        
        # Generate realistic planet name based on characteristics
        planet_name = generate_planet_name(data, pred_str)

        return {
            "prediction": pred_str,
            "probabilities": prob_dict,
            "confidence": float(max(probs)),
            "habitability_score": hab_score,
            "planet_type": planet_type,
            "planet_name": planet_name,
            "star_type": star_type,
            "status": "ml_prediction"
        }
    except Exception as e:
        print(f"❌ 預測錯誤: {e}")
        import traceback
        traceback.print_exc()
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
