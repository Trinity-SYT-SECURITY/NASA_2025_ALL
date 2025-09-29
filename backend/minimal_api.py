"""
Minimal FastAPI Backend for Exoplanet Discovery Platform
Fixed version without OpenAPI schema issues
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models at startup
try:
    ml_model = joblib.load('../ml/exoplanet_model_best.joblib')
    scaler = joblib.load('../ml/scaler.joblib')
    label_encoder = joblib.load('../ml/label_encoder.joblib')
    models_loaded = True
    print("✅ ML models loaded successfully")
except Exception as e:
    print(f"⚠️ Could not load ML models: {e}")
    ml_model = None
    scaler = None
    label_encoder = None
    models_loaded = False

@app.get("/")
async def root():
    return {
        "message": "🌌 Exoplanet AI Discovery Platform",
        "status": "🚀 OPERATIONAL",
        "models_loaded": models_loaded,
        "endpoints": [
            "GET /health - System health check",
            "GET /stats - Dataset statistics", 
            "POST /predict - AI exoplanet prediction"
        ]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "models_loaded": models_loaded,
        "data_loaded": True,
        "message": "🤖 AI System Ready"
    }

@app.get("/stats")
async def get_stats():
    return {
        "total_exoplanets": 9564,
        "confirmed": 2746,
        "candidates": 1979,
        "false_positives": 4839,
        "potentially_habitable": 94,
        "averages": {
            "radius": 2.1,
            "temperature": 800,
            "period": 50.2
        },
        "ranges": {
            "radius": {"min": 0.1, "max": 84.0},
            "temperature": {"min": 100, "max": 7000},
            "period": {"min": 0.24, "max": 2000}
        }
    }

@app.post("/predict")
async def predict(planet_data: dict):
    """Predict exoplanet classification"""
    
    if not models_loaded:
        # Demo mode response
        return {
            "prediction": "CANDIDATE",
            "probabilities": {
                "CANDIDATE": 0.65,
                "CONFIRMED": 0.25,
                "FALSE POSITIVE": 0.10
            },
            "confidence": 0.65,
            "habitability_score": 75.0,
            "planet_type": "Earth-like" if planet_data.get('koi_prad', 1.0) <= 1.5 else "Super-Earth",
            "star_type": "G-dwarf",
            "status": "demo_mode"
        }
    
    try:
        # Extract required features
        input_data = [
            planet_data.get('koi_period', 365.25),
            planet_data.get('koi_duration', 6.0),
            planet_data.get('koi_depth', 500.0),
            planet_data.get('koi_prad', 1.0),
            planet_data.get('koi_teq', 288.0),
            planet_data.get('koi_insol', 1.0),
            planet_data.get('koi_model_snr', 25.0),
            planet_data.get('koi_steff', 5778.0),
            planet_data.get('koi_slogg', 4.44),
            planet_data.get('koi_srad', 1.0),
            planet_data.get('koi_smass', 1.0),
            planet_data.get('koi_kepmag', 12.0),
            planet_data.get('koi_fpflag_nt', 0),
            planet_data.get('koi_fpflag_ss', 0),
            planet_data.get('koi_fpflag_co', 0),
            planet_data.get('koi_fpflag_ec', 0),
            planet_data.get('ra', 290.0),
            planet_data.get('dec', 45.0),
            1 if 0.25 <= planet_data.get('koi_insol', 1.0) <= 1.5 else 0,  # habitable_zone
            planet_data.get('koi_score', 0.5)
        ]
        
        # Scale and predict
        input_scaled = scaler.transform([input_data])
        prediction = ml_model.predict(input_scaled)[0]
        probabilities = ml_model.predict_proba(input_scaled)[0]
        
        # Convert to readable format
        prediction_str = label_encoder.inverse_transform([prediction])[0]
        prob_dict = {}
        for i, class_name in enumerate(label_encoder.classes_):
            prob_dict[class_name] = float(probabilities[i])
        
        # Calculate habitability score
        habitability = 0.0
        koi_teq = planet_data.get('koi_teq', 288)
        koi_prad = planet_data.get('koi_prad', 1.0)
        koi_insol = planet_data.get('koi_insol', 1.0)
        
        if 273 <= koi_teq <= 373:  # Liquid water temperature
            habitability += 40
        if 0.8 <= koi_prad <= 1.5:  # Earth-like size
            habitability += 30
        if 0.25 <= koi_insol <= 1.5:  # Habitable zone
            habitability += 30
        
        # Planet type classification
        if koi_prad < 0.8:
            planet_type = "Sub-Earth"
        elif koi_prad <= 1.25:
            planet_type = "Earth-like"
        elif koi_prad <= 2.0:
            planet_type = "Super-Earth"
        elif koi_prad <= 4.0:
            planet_type = "Mini-Neptune"
        else:
            planet_type = "Giant"
        
        # Star type classification
        koi_steff = planet_data.get('koi_steff', 5778)
        if koi_steff < 3700:
            star_type = "M-dwarf (Red)"
        elif koi_steff < 5200:
            star_type = "K-dwarf (Orange)"
        elif koi_steff < 6000:
            star_type = "G-dwarf (Yellow)"
        elif koi_steff < 7500:
            star_type = "F-dwarf (White)"
        else:
            star_type = "A-dwarf (Blue-White)"
        
        return {
            "prediction": prediction_str,
            "probabilities": prob_dict,
            "confidence": float(max(probabilities)),
            "habitability_score": habitability,
            "planet_type": planet_type,
            "star_type": star_type,
            "status": "ml_prediction",
            "model_accuracy": "92.16%"
        }
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return {
            "prediction": "CANDIDATE",
            "probabilities": {
                "CANDIDATE": 0.65,
                "CONFIRMED": 0.25,
                "FALSE POSITIVE": 0.10
            },
            "confidence": 0.65,
            "habitability_score": 50.0,
            "planet_type": "Unknown",
            "star_type": "Unknown",
            "status": "error_fallback",
            "error": str(e)
        }

@app.get("/demo")
async def demo_prediction():
    """Demo endpoint with Earth-like planet"""
    earth_like = {
        "koi_period": 365.25,
        "koi_duration": 6.0,
        "koi_depth": 500.0,
        "koi_prad": 1.0,
        "koi_teq": 288.0,
        "koi_insol": 1.0,
        "koi_model_snr": 25.0,
        "koi_steff": 5778.0,
        "koi_slogg": 4.44,
        "koi_srad": 1.0,
        "koi_kepmag": 12.0,
        "ra": 290.0,
        "dec": 45.0
    }
    
    result = await predict(earth_like)
    return {
        "demo_input": earth_like,
        "ai_result": result,
        "description": "🌍 Earth-like exoplanet prediction demo"
    }

if __name__ == "__main__":
    import uvicorn
    print("🌌 Starting Exoplanet AI Discovery Platform...")
    print("🚀 Backend API will be available at: http://localhost:8000")
    print("📚 Endpoints: /health, /stats, /predict, /demo")
    uvicorn.run(app, host="0.0.0.0", port=8000)
