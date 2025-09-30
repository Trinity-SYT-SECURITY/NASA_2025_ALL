"""
FastAPI Backend for Exoplanet Discovery Platform
Serves ML predictions and exoplanet data for 3D visualization
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import joblib
import numpy as np
import pandas as pd
import json
from pathlib import Path

app = FastAPI(
    title="Exoplanet Discovery API",
    description="AI-powered exoplanet classification and visualization API",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models and data
ml_model = None
scaler = None
label_encoder = None
feature_names = []
exoplanet_data = None

class PlanetInput(BaseModel):
    """Input model for exoplanet prediction"""
    koi_period: float
    koi_duration: float
    koi_depth: float
    koi_prad: float
    koi_teq: float
    koi_insol: float
    koi_model_snr: float
    koi_steff: float
    koi_slogg: float
    koi_srad: float
    koi_smass: Optional[float] = None
    koi_kepmag: float
    koi_fpflag_nt: int = 0
    koi_fpflag_ss: int = 0
    koi_fpflag_co: int = 0
    koi_fpflag_ec: int = 0
    ra: float
    dec: float
    koi_score: Optional[float] = 0.5

class PredictionResponse(BaseModel):
    """Response model for predictions"""
    prediction: str
    probabilities: Dict[str, float]
    confidence: float
    habitability_score: float
    planet_type: str
    star_type: str

class ExoplanetData(BaseModel):
    """Model for exoplanet visualization data"""
    kepoi_name: str
    kepler_name: Optional[str]
    disposition: str
    period: float
    radius: float
    temperature: float
    star_temp: float
    star_radius: float
    ra: float
    dec: float
    habitability_score: float

try:
    # Load ML models at startup
    ml_model = joblib.load('../ml/exoplanet_model_best.joblib')
    scaler = joblib.load('../ml/scaler.joblib')
    label_encoder = joblib.load('../ml/label_encoder.joblib')
        
        # Load feature names
        feature_names = [
            'koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq', 
            'koi_insol', 'koi_model_snr', 'koi_steff', 'koi_slogg', 'koi_srad', 
            'koi_smass', 'koi_kepmag', 'koi_fpflag_nt', 'koi_fpflag_ss', 
            'koi_fpflag_co', 'koi_fpflag_ec', 'ra', 'dec', 'habitable_zone', 'koi_score'
        ]
        
        # Load exoplanet data for visualization
        df = pd.read_csv('../data/cumulative_2025.09.16_22.42.55.csv')
        exoplanet_data = prepare_visualization_data(df)
        
        print("Models and data loaded successfully")
        
    except Exception as e:
        print(f"Error loading models: {e}")
        # For development, continue without models
        pass

def prepare_visualization_data(df):
    """Prepare exoplanet data for 3D visualization"""
    # Filter confirmed and candidate exoplanets
    viz_data = df[df['koi_disposition'].isin(['CONFIRMED', 'CANDIDATE'])].copy()
    
    # Clean and prepare data
    viz_data = viz_data.dropna(subset=['koi_period', 'koi_prad', 'koi_teq', 'koi_steff'])
    
    # Calculate habitability score
    def calculate_habitability(row):
        score = 0.0
        
        # Temperature habitability (0-40 points)
        if 273 <= row['koi_teq'] <= 373:  # Liquid water range
            score += 40
        elif 200 <= row['koi_teq'] <= 400:  # Extended range
            score += 20
        
        # Size habitability (0-30 points)
        if 0.8 <= row['koi_prad'] <= 1.5:  # Earth-like
            score += 30
        elif 0.5 <= row['koi_prad'] <= 2.0:  # Extended range
            score += 15
        
        # Insolation habitability (0-30 points)
        if 0.25 <= row['koi_insol'] <= 1.5:  # Habitable zone
            score += 30
        elif 0.1 <= row['koi_insol'] <= 4.0:  # Extended range
            score += 10
        
        return min(score, 100)
    
    viz_data['habitability_score'] = viz_data.apply(calculate_habitability, axis=1)
    
    # Convert to list of dictionaries
    exoplanets = []
    for _, row in viz_data.iterrows():
        exoplanet = {
            'kepoi_name': row['kepoi_name'],
            'kepler_name': row['kepler_name'] if pd.notna(row['kepler_name']) else None,
            'disposition': row['koi_disposition'],
            'period': float(row['koi_period']),
            'radius': float(row['koi_prad']),
            'temperature': float(row['koi_teq']),
            'star_temp': float(row['koi_steff']) if pd.notna(row['koi_steff']) else 5778,
            'star_radius': float(row['koi_srad']) if pd.notna(row['koi_srad']) else 1.0,
            'ra': float(row['ra']),
            'dec': float(row['dec']),
            'habitability_score': row['habitability_score']
        }
        exoplanets.append(exoplanet)
    
    return exoplanets

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Exoplanet Discovery API",
        "status": "active",
        "models_loaded": ml_model is not None
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_exoplanet(planet_data: PlanetInput):
    """Predict exoplanet classification"""
    if ml_model is None:
        raise HTTPException(status_code=503, detail="ML model not loaded")
    
    try:
        # Prepare input data
        input_data = [
            planet_data.koi_period,
            planet_data.koi_duration,
            planet_data.koi_depth,
            planet_data.koi_prad,
            planet_data.koi_teq,
            planet_data.koi_insol,
            planet_data.koi_model_snr,
            planet_data.koi_steff,
            planet_data.koi_slogg,
            planet_data.koi_srad,
            planet_data.koi_smass or 1.0,
            planet_data.koi_kepmag,
            planet_data.koi_fpflag_nt,
            planet_data.koi_fpflag_ss,
            planet_data.koi_fpflag_co,
            planet_data.koi_fpflag_ec,
            planet_data.ra,
            planet_data.dec,
            1 if 0.25 <= planet_data.koi_insol <= 1.5 else 0,  # habitable_zone
            planet_data.koi_score or 0.5
        ]
        
        # Scale input data
        input_scaled = scaler.transform([input_data])
        
        # Make prediction
        prediction = ml_model.predict(input_scaled)[0]
        probabilities = ml_model.predict_proba(input_scaled)[0]
        
        # Convert prediction to string
        prediction_str = label_encoder.inverse_transform([prediction])[0]
        
        # Create probability dictionary
        prob_dict = {}
        for i, class_name in enumerate(label_encoder.classes_):
            prob_dict[class_name] = float(probabilities[i])
        
        # Calculate confidence (highest probability)
        confidence = float(max(probabilities))
        
        # Calculate habitability score
        habitability_score = 0.0
        if 273 <= planet_data.koi_teq <= 373:
            habitability_score += 40
        if 0.8 <= planet_data.koi_prad <= 1.5:
            habitability_score += 30
        if 0.25 <= planet_data.koi_insol <= 1.5:
            habitability_score += 30
        
        # Determine planet type
        if planet_data.koi_prad < 0.8:
            planet_type = "Sub-Earth"
        elif planet_data.koi_prad <= 1.25:
            planet_type = "Earth-like"
        elif planet_data.koi_prad <= 2.0:
            planet_type = "Super-Earth"
        elif planet_data.koi_prad <= 4.0:
            planet_type = "Mini-Neptune"
        else:
            planet_type = "Giant"
        
        # Determine star type
        if planet_data.koi_steff < 3700:
            star_type = "M-dwarf"
        elif planet_data.koi_steff < 5200:
            star_type = "K-dwarf"
        elif planet_data.koi_steff < 6000:
            star_type = "G-dwarf"
        elif planet_data.koi_steff < 7500:
            star_type = "F-dwarf"
        else:
            star_type = "A-dwarf"
        
        return PredictionResponse(
            prediction=prediction_str,
            probabilities=prob_dict,
            confidence=confidence,
            habitability_score=habitability_score,
            planet_type=planet_type,
            star_type=star_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/exoplanets")
async def get_exoplanets(
    limit: int = 1000,
    disposition: Optional[str] = None,
    min_habitability: Optional[float] = None
):
    """Get exoplanet data for visualization"""
    if exoplanet_data is None:
        raise HTTPException(status_code=503, detail="Exoplanet data not loaded")
    
    filtered_data = exoplanet_data.copy()
    
    # Filter by disposition
    if disposition:
        filtered_data = [p for p in filtered_data if p['disposition'] == disposition]
    
    # Filter by minimum habitability score
    if min_habitability is not None:
        filtered_data = [p for p in filtered_data if p['habitability_score'] >= min_habitability]
    
    # Limit results
    filtered_data = filtered_data[:limit]
    
    return {
        "exoplanets": filtered_data,
        "total": len(filtered_data),
        "filters": {
            "disposition": disposition,
            "min_habitability": min_habitability,
            "limit": limit
        }
    }

@app.get("/stats")
async def get_statistics():
    """Get dataset statistics"""
    if exoplanet_data is None:
        raise HTTPException(status_code=503, detail="Exoplanet data not loaded")
    
    total = len(exoplanet_data)
    confirmed = len([p for p in exoplanet_data if p['disposition'] == 'CONFIRMED'])
    candidates = len([p for p in exoplanet_data if p['disposition'] == 'CANDIDATE'])
    habitable = len([p for p in exoplanet_data if p['habitability_score'] >= 70])
    
    # Calculate average values
    avg_radius = np.mean([p['radius'] for p in exoplanet_data])
    avg_temp = np.mean([p['temperature'] for p in exoplanet_data])
    avg_period = np.mean([p['period'] for p in exoplanet_data])
    
    return {
        "total_exoplanets": total,
        "confirmed": confirmed,
        "candidates": candidates,
        "potentially_habitable": habitable,
        "averages": {
            "radius": float(avg_radius),
            "temperature": float(avg_temp),
            "period": float(avg_period)
        },
        "habitability_distribution": {
            "high": len([p for p in exoplanet_data if p['habitability_score'] >= 70]),
            "medium": len([p for p in exoplanet_data if 40 <= p['habitability_score'] < 70]),
            "low": len([p for p in exoplanet_data if p['habitability_score'] < 40])
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": ml_model is not None,
        "data_loaded": exoplanet_data is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
