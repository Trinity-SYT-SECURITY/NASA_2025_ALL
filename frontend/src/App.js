import React, { Suspense, useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars, Text, Html } from '@react-three/drei';
import * as THREE from 'three';
import axios from 'axios';
import './App.css';

// 3D Exoplanet Component
function Exoplanet({ position, radius, color, name, data, onClick }) {
  const meshRef = React.useRef();
  
  React.useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.01;
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime) * 0.5;
    }
  });

  return (
    <group position={position} onClick={() => onClick(data)}>
      <mesh ref={meshRef}>
        <sphereGeometry args={[radius, 32, 32]} />
        <meshStandardMaterial 
          color={color} 
          emissive={color}
          emissiveIntensity={0.2}
        />
      </mesh>
      <Html distanceFactor={10}>
        <div className="planet-label">
          {name}
        </div>
      </Html>
    </group>
  );
}

// 3D Universe Scene
function UniverseScene({ exoplanets, onPlanetClick }) {
  return (
    <>
      <ambientLight intensity={0.1} />
      <pointLight position={[10, 10, 10]} intensity={1} />
      <Stars radius={300} depth={60} count={5000} factor={7} />
      
      {exoplanets.map((planet) => (
        <Exoplanet
          key={planet.id}
          position={planet.position}
          radius={planet.radius}
          color={planet.color}
          name={planet.name}
          data={planet}
          onClick={onPlanetClick}
        />
      ))}
      
      <Text
        position={[0, 15, -10]}
        fontSize={2}
        color="#00d4ff"
        anchorX="center"
        anchorY="middle"
      >
        🌌 EXOPLANET AI DISCOVERY 🌌
      </Text>
    </>
  );
}

// ML Prediction Panel
function PredictionPanel({ onPredict, prediction, loading }) {
  const [formData, setFormData] = useState({
    koi_period: 365.25,
    koi_prad: 1.0,
    koi_teq: 288,
    koi_steff: 5778,
    koi_insol: 1.0
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onPredict(formData);
  };

  return (
    <div className="prediction-panel">
      <h2>🤖 AI EXOPLANET PREDICTOR</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label>Orbital Period (days):</label>
          <input
            type="number"
            value={formData.koi_period}
            onChange={(e) => setFormData({...formData, koi_period: parseFloat(e.target.value)})}
            step="0.1"
          />
        </div>
        
        <div className="input-group">
          <label>Planet Radius (Earth radii):</label>
          <input
            type="number"
            value={formData.koi_prad}
            onChange={(e) => setFormData({...formData, koi_prad: parseFloat(e.target.value)})}
            step="0.1"
          />
        </div>
        
        <div className="input-group">
          <label>Equilibrium Temperature (K):</label>
          <input
            type="number"
            value={formData.koi_teq}
            onChange={(e) => setFormData({...formData, koi_teq: parseFloat(e.target.value)})}
          />
        </div>
        
        <div className="input-group">
          <label>Stellar Temperature (K):</label>
          <input
            type="number"
            value={formData.koi_steff}
            onChange={(e) => setFormData({...formData, koi_steff: parseFloat(e.target.value)})}
          />
        </div>
        
        <button type="submit" disabled={loading} className="predict-btn">
          {loading ? '🔄 ANALYZING...' : '🚀 PREDICT EXOPLANET'}
        </button>
      </form>
      
      {prediction && (
        <div className="prediction-result">
          <h3>🎯 AI PREDICTION RESULT</h3>
          <div className="result-item">
            <strong>Classification:</strong> {prediction.prediction}
          </div>
          <div className="result-item">
            <strong>Confidence:</strong> {(prediction.confidence * 100).toFixed(1)}%
          </div>
          <div className="result-item">
            <strong>Habitability Score:</strong> {prediction.habitability_score}/100
          </div>
          <div className="result-item">
            <strong>Planet Type:</strong> {prediction.planet_type}
          </div>
          <div className="result-item">
            <strong>Star Type:</strong> {prediction.star_type}
          </div>
        </div>
      )}
    </div>
  );
}

// Planet Info Panel
function PlanetInfoPanel({ planet, onClose }) {
  if (!planet) return null;
  
  return (
    <div className="planet-info-panel">
      <button className="close-btn" onClick={onClose}>✕</button>
      <h2>🪐 {planet.name}</h2>
      <div className="info-item">
        <strong>Status:</strong> {planet.disposition}
      </div>
      <div className="info-item">
        <strong>Radius:</strong> {planet.radius} Earth radii
      </div>
      <div className="info-item">
        <strong>Temperature:</strong> {planet.temperature} K
      </div>
      <div className="info-item">
        <strong>Habitability:</strong> {planet.habitability}/100
      </div>
      <div className="habitability-bar">
        <div 
          className="habitability-fill" 
          style={{ width: `${planet.habitability}%` }}
        ></div>
      </div>
    </div>
  );
}

// Main App Component
function App() {
  const [exoplanets, setExoplanets] = useState([]);
  const [selectedPlanet, setSelectedPlanet] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);

  // Load exoplanet data
  useEffect(() => {
    const loadData = async () => {
      try {
        const [exoResponse, statsResponse] = await Promise.all([
          axios.get('http://localhost:8000/exoplanets'),
          axios.get('http://localhost:8000/stats')
        ]);
        
        setExoplanets(exoResponse.data.exoplanets);
        setStats(statsResponse.data);
      } catch (error) {
        console.error('Failed to load data:', error);
        // Fallback data
        setExoplanets([
          {
            id: 1,
            name: "Kepler-442b",
            position: [10, 5, -20],
            radius: 1.34,
            temperature: 233,
            disposition: "CONFIRMED",
            habitability: 84,
            color: "#4CAF50"
          }
        ]);
        setStats({ total_exoplanets: 9564, confirmed: 2746 });
      }
    };
    
    loadData();
  }, []);

  // Handle ML prediction
  const handlePredict = async (formData) => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/predict', formData);
      setPrediction(response.data);
      
      // Add predicted planet to scene
      const newPlanet = {
        id: Date.now(),
        name: `Predicted Planet`,
        position: [Math.random() * 40 - 20, Math.random() * 20 - 10, Math.random() * 40 - 20],
        radius: formData.koi_prad,
        temperature: formData.koi_teq,
        disposition: response.data.prediction,
        habitability: response.data.habitability_score,
        color: response.data.prediction === 'CONFIRMED' ? '#4CAF50' : 
               response.data.prediction === 'CANDIDATE' ? '#FF9800' : '#F44336'
      };
      
      setExoplanets(prev => [...prev, newPlanet]);
    } catch (error) {
      console.error('Prediction failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePlanetClick = (planet) => {
    setSelectedPlanet(planet);
  };

  return (
    <div className="App">
      {/* 3D Universe Canvas */}
      <Canvas camera={{ position: [0, 0, 30], fov: 75 }}>
        <Suspense fallback={null}>
          <UniverseScene 
            exoplanets={exoplanets} 
            onPlanetClick={handlePlanetClick}
          />
          <OrbitControls enableZoom={true} enablePan={true} enableRotate={true} />
        </Suspense>
      </Canvas>

      {/* UI Overlays */}
      <PredictionPanel 
        onPredict={handlePredict} 
        prediction={prediction}
        loading={loading}
      />
      
      <PlanetInfoPanel 
        planet={selectedPlanet}
        onClose={() => setSelectedPlanet(null)}
      />
      
      {/* Stats Panel */}
      <div className="stats-panel">
        <h3>📊 DATASET STATS</h3>
        {stats && (
          <>
            <div>Total Exoplanets: {stats.total_exoplanets}</div>
            <div>Confirmed: {stats.confirmed}</div>
            <div>ML Accuracy: 92.16%</div>
          </>
        )}
      </div>
      
      {/* Loading Indicator */}
      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
          <div>🤖 AI ANALYZING EXOPLANET...</div>
        </div>
      )}
    </div>
  );
}

export default App;
