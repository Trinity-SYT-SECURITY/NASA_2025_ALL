import React, { Suspense, useState, useEffect, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Text, Html } from '@react-three/drei';
import axios from 'axios';
import './SimpleApp.css';

// Simple 3D Planet Component
function Planet({ position, radius, color, name, data, onClick, isAnimating }) {
  const meshRef = useRef();
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.01;
      if (isAnimating) {
        meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 2) * 0.8;
        meshRef.current.scale.setScalar(1 + Math.sin(state.clock.elapsedTime * 3) * 0.1);
      } else {
        meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime) * 0.2;
      }
    }
  });

  return (
    <group position={position}>
      <mesh 
        ref={meshRef} 
        onClick={() => onClick && onClick(data)}
        onPointerOver={(e) => {
          e.stopPropagation();
          document.body.style.cursor = 'pointer';
        }}
        onPointerOut={() => {
          document.body.style.cursor = 'default';
        }}
      >
        <sphereGeometry args={[radius, 16, 16]} />
        <meshStandardMaterial 
          color={color} 
          emissive={color}
          emissiveIntensity={isAnimating ? 0.5 : 0.2}
          roughness={0.3}
          metalness={0.1}
        />
      </mesh>
      
      {/* Planet Ring for some planets */}
      {radius > 1.5 && (
        <mesh rotation={[Math.PI / 2, 0, 0]}>
          <ringGeometry args={[radius * 1.2, radius * 1.4, 32]} />
          <meshBasicMaterial color={color} transparent opacity={0.3} side={2} />
        </mesh>
      )}
      
      <Html distanceFactor={8} position={[0, radius + 1, 0]}>
        <div className="planet-label">
          <div style={{ fontWeight: 'bold' }}>{name}</div>
          <div style={{ fontSize: '10px', opacity: 0.8 }}>
            {data.disposition} • {data.habitability}% habitable
          </div>
        </div>
      </Html>
    </group>
  );
}

// Cosmic Background with Stars
function CosmicBackground() {
  return (
    <>
      <Stars radius={200} depth={50} count={3000} factor={4} saturation={0} fade speed={1} />
      <ambientLight intensity={0.2} />
      <pointLight position={[10, 10, 10]} intensity={1} color="#ffffff" />
      <pointLight position={[-10, -10, -10]} intensity={0.5} color="#4a9eff" />
      <directionalLight position={[0, 0, 5]} intensity={0.5} />
    </>
  );
}

// Main 3D Scene
function ExoplanetUniverse({ exoplanets, onPlanetClick, animatingPlanetId }) {
  return (
    <>
      <CosmicBackground />
      
      {/* Title */}
       <Text
         position={[0, 12, -8]}
         fontSize={1.8}
         color="#00d4ff"
         anchorX="center"
         anchorY="middle"
         letterSpacing={0.1}
       >
         🌌 EXOPLANET AI DISCOVERY 🌌
       </Text>
      
      <Text
        position={[0, 10, -8]}
        fontSize={0.8}
        color="#ffffff"
        anchorX="center"
        anchorY="middle"
        opacity={0.8}
      >
        Click planets to explore • Use mouse to navigate
      </Text>
      
      {/* Planets */}
      {exoplanets.map((planet) => (
        <Planet
          key={planet.id}
          position={planet.position}
          radius={planet.radius}
          color={planet.color}
          name={planet.name}
          data={planet}
          onClick={onPlanetClick}
          isAnimating={planet.id === animatingPlanetId}
        />
      ))}
    </>
  );
}

// AI Prediction Panel
function AIPanel({ onPredict, prediction, loading }) {
  const [params, setParams] = useState({
    koi_period: 365.25,
    koi_prad: 1.0,
    koi_teq: 288,
    koi_steff: 5778,
    koi_insol: 1.0
  });

  const presets = {
    earth: { koi_period: 365.25, koi_prad: 1.0, koi_teq: 288, koi_steff: 5778, koi_insol: 1.0 },
    hotJupiter: { koi_period: 3.5, koi_prad: 11.0, koi_teq: 1200, koi_steff: 6000, koi_insol: 100 },
    superEarth: { koi_period: 20, koi_prad: 1.8, koi_teq: 350, koi_steff: 4500, koi_insol: 2.5 }
  };

  const handlePreset = (preset) => {
    setParams(presets[preset]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onPredict(params);
  };

  return (
    <div className="ai-panel">
      <h2>🤖 AI EXOPLANET PREDICTOR</h2>
      
      {/* Quick Presets */}
      <div className="presets">
        <button onClick={() => handlePreset('earth')} className="preset-btn earth">🌍 Earth-like</button>
        <button onClick={() => handlePreset('hotJupiter')} className="preset-btn jupiter">🔥 Hot Jupiter</button>
        <button onClick={() => handlePreset('superEarth')} className="preset-btn super">🌎 Super Earth</button>
      </div>
      
      <form onSubmit={handleSubmit}>
        <div className="param-grid">
          <div className="param-item">
            <label>Period (days)</label>
            <input
              type="number"
              value={params.koi_period}
              onChange={(e) => setParams({...params, koi_period: parseFloat(e.target.value)})}
              step="0.1"
            />
          </div>
          
          <div className="param-item">
            <label>Radius (Earth = 1)</label>
            <input
              type="number"
              value={params.koi_prad}
              onChange={(e) => setParams({...params, koi_prad: parseFloat(e.target.value)})}
              step="0.1"
            />
          </div>
          
          <div className="param-item">
            <label>Temperature (K)</label>
            <input
              type="number"
              value={params.koi_teq}
              onChange={(e) => setParams({...params, koi_teq: parseFloat(e.target.value)})}
            />
          </div>
          
          <div className="param-item">
            <label>Star Temp (K)</label>
            <input
              type="number"
              value={params.koi_steff}
              onChange={(e) => setParams({...params, koi_steff: parseFloat(e.target.value)})}
            />
          </div>
        </div>
        
        <button type="submit" disabled={loading} className="predict-button">
          {loading ? '🔄 ANALYZING...' : '🚀 PREDICT & VISUALIZE'}
        </button>
      </form>
      
      {prediction && (
        <div className="prediction-results">
          <h3>🎯 AI RESULT</h3>
          <div className="result-grid">
            <div className="result-card">
              <div className="result-label">Classification</div>
              <div className="result-value">{prediction.prediction}</div>
            </div>
            <div className="result-card">
              <div className="result-label">Confidence</div>
              <div className="result-value">{(prediction.confidence * 100).toFixed(1)}%</div>
            </div>
            <div className="result-card">
              <div className="result-label">Habitability</div>
              <div className="result-value">{prediction.habitability_score}/100</div>
            </div>
            <div className="result-card">
              <div className="result-label">Type</div>
              <div className="result-value">{prediction.planet_type}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Planet Details Panel
function PlanetDetails({ planet, onClose }) {
  if (!planet) return null;
  
  return (
    <div className="planet-details">
      <button className="close-button" onClick={onClose}>✕</button>
      <h2>🪐 {planet.name}</h2>
      
      <div className="detail-grid">
        <div className="detail-item">
          <span className="detail-label">Status:</span>
          <span className={`detail-value status-${planet.disposition.toLowerCase()}`}>
            {planet.disposition}
          </span>
        </div>
        
        <div className="detail-item">
          <span className="detail-label">Radius:</span>
          <span className="detail-value">{planet.radius}× Earth</span>
        </div>
        
        <div className="detail-item">
          <span className="detail-label">Temperature:</span>
          <span className="detail-value">{planet.temperature} K</span>
        </div>
        
        <div className="detail-item">
          <span className="detail-label">Habitability:</span>
          <span className="detail-value">{planet.habitability}%</span>
        </div>
      </div>
      
      <div className="habitability-meter">
        <div className="meter-label">Life Potential</div>
        <div className="meter-bar">
          <div 
            className="meter-fill" 
            style={{ 
              width: `${planet.habitability}%`,
              background: planet.habitability > 70 ? '#4CAF50' : 
                         planet.habitability > 40 ? '#FF9800' : '#F44336'
            }}
          ></div>
        </div>
        <div className="meter-text">{planet.habitability}% Habitable</div>
      </div>
    </div>
  );
}

// Stats Dashboard
function StatsDashboard({ stats }) {
  if (!stats) return null;
  
  return (
    <div className="stats-dashboard">
      <h3>📊 MISSION STATS</h3>
      <div className="stats-grid">
        <div className="stat-item">
          <div className="stat-number">{stats.total_exoplanets?.toLocaleString()}</div>
          <div className="stat-label">Total Exoplanets</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">{stats.confirmed?.toLocaleString()}</div>
          <div className="stat-label">Confirmed</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">92.16%</div>
          <div className="stat-label">AI Accuracy</div>
        </div>
      </div>
    </div>
  );
}

// Main App
function App() {
  const [exoplanets, setExoplanets] = useState([]);
  const [selectedPlanet, setSelectedPlanet] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [animatingPlanetId, setAnimatingPlanetId] = useState(null);

  // Load initial data
  useEffect(() => {
    const loadData = async () => {
      try {
        const [planetsRes, statsRes] = await Promise.all([
          axios.get('http://localhost:8000/exoplanets'),
          axios.get('http://localhost:8000/stats')
        ]);
        
        setExoplanets(planetsRes.data.exoplanets);
        setStats(statsRes.data);
      } catch (error) {
        console.error('Failed to load data:', error);
        // Fallback data for demo
        setExoplanets([
          {
            id: 1, name: "Kepler-442b", position: [8, 3, -15], radius: 1.34, 
            temperature: 233, disposition: "CONFIRMED", habitability: 84, color: "#4CAF50"
          },
          {
            id: 2, name: "Kepler-186f", position: [-12, -5, 20], radius: 1.11,
            temperature: 188, disposition: "CONFIRMED", habitability: 91, color: "#2196F3" 
          },
          {
            id: 3, name: "Kepler-452b", position: [15, 8, 8], radius: 1.63,
            temperature: 265, disposition: "CONFIRMED", habitability: 78, color: "#FF9800"
          }
        ]);
        setStats({ total_exoplanets: 9564, confirmed: 2746 });
      }
    };
    
    loadData();
  }, []);

  // Handle AI prediction
  const handlePredict = async (params) => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/predict', params);
      setPrediction(response.data);
      
      // Create new planet in 3D space
      const newPlanet = {
        id: Date.now(),
        name: "AI Predicted Planet",
        position: [
          (Math.random() - 0.5) * 30,
          (Math.random() - 0.5) * 20, 
          (Math.random() - 0.5) * 30
        ],
        radius: params.koi_prad,
        temperature: params.koi_teq,
        disposition: response.data.prediction,
        habitability: response.data.habitability_score,
        color: response.data.prediction === 'CONFIRMED' ? '#4CAF50' : 
               response.data.prediction === 'CANDIDATE' ? '#FF9800' : '#F44336'
      };
      
      setExoplanets(prev => [...prev, newPlanet]);
      setAnimatingPlanetId(newPlanet.id);
      
      // Stop animation after 5 seconds
      setTimeout(() => setAnimatingPlanetId(null), 5000);
      
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
      {/* 3D Universe */}
      <Canvas 
        camera={{ position: [0, 5, 25], fov: 60 }}
        style={{ background: 'radial-gradient(circle, #001122 0%, #000000 100%)' }}
      >
        <Suspense fallback={null}>
          <ExoplanetUniverse 
            exoplanets={exoplanets}
            onPlanetClick={handlePlanetClick}
            animatingPlanetId={animatingPlanetId}
          />
          <OrbitControls 
            enableZoom={true} 
            enablePan={true} 
            enableRotate={true}
            minDistance={10}
            maxDistance={50}
          />
        </Suspense>
      </Canvas>

      {/* UI Overlays */}
      <AIPanel 
        onPredict={handlePredict}
        prediction={prediction}
        loading={loading}
      />
      
      <PlanetDetails 
        planet={selectedPlanet}
        onClose={() => setSelectedPlanet(null)}
      />
      
      <StatsDashboard stats={stats} />
      
      {/* Loading Screen */}
      {loading && (
        <div className="loading-screen">
          <div className="loading-content">
            <div className="loading-spinner"></div>
            <div className="loading-text">
              🤖 AI ANALYZING EXOPLANET DATA...
            </div>
            <div className="loading-subtext">
              Training neural networks on NASA Kepler data
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
