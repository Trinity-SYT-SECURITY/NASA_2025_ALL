import React, { Suspense, useState, useEffect, useRef, useMemo } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Stars, Text, Html } from '@react-three/drei';
import * as THREE from 'three';
import axios from 'axios';
import { MockMLService } from './services/mockMLService';
import './SimpleApp.css';

// 在文件頂部添加類型斷言輔助函數
// const sx = (styles) => styles; // Removed unused function

// Backend detection and URL management
const detectBackendType = async () => {
  // Priority: Render > ngrok > Local FastAPI > Vercel > Mock
  const backends = [
    { name: 'local_fastapi', url: 'http://localhost:8000', testUrl: '/health' },
    { name: 'render', url: 'https://test-backend-2-ikqg.onrender.com', testUrl: '/health' },
  ];

  // Try to get from environment variables first
  if (typeof process !== 'undefined' && process.env) {
    const envUrl = process.env.REACT_APP_API_URL || process.env.VITE_API_URL;
    if (envUrl) {
      console.log(`🔧 Using API URL from environment: ${envUrl}`);
      return envUrl;
    }
  }

  if (typeof process !== 'undefined' && process.env) {
    const envUrl = process.env.REACT_APP_API_URL || process.env.VITE_API_URL;
    if (envUrl) {
      console.log(`🔧 Using API URL from environment: ${envUrl}`);
      return envUrl;
    }
  }

  for (const backend of backends) {
    try {
      const response = await axios.get(`${backend.url}${backend.testUrl}`, {
        timeout: 3000,
        headers: { 'Accept': 'application/json' }
      });

      if (response.status === 200 && response.data) {
        // Check if it's a real backend (not just a web server)
        const isValidBackend = response.data.status ||
                              response.data.models_loaded !== undefined ||
                              response.data.backend_type ||
                              response.data.total_exoplanets;

        if (isValidBackend) {
          console.log(`✅ Backend detected: ${backend.name} at ${backend.url}`);
          console.log(`   Backend info:`, response.data);
          return backend.url;
        }
      }
    } catch (error) {
      console.log(`❌ ${backend.name} backend not available:`, error.message);
    }
  }

  console.log('⚠️ No backends available, using mock service');
  return null;
};

const getApiBaseUrl = () => {
  // For local development, try local backend first
  console.log('🔧 Local development: Trying local backend first');
  return 'http://localhost:8000';
};

const API_BASE_URL = getApiBaseUrl();

console.log('API Base URL:', API_BASE_URL);

// Test backend connectivity and ML model loading
const testBackend = async () => {
  try {
    // First detect which backend is available
    const backendUrl = await detectBackendType();
    if (!backendUrl) {
      console.log('⚠️ No backend detected, using mock service');
      return { success: false, fallback_mode: 'mock', backend_url: null };
    }

    // Test the detected backend
    const response = await axios.get(`${backendUrl}/test-ml`, { timeout: 3000 });
    console.log('🔬 Backend Test Result:', response.data);

    // Check if it's a real ML backend or demo mode
    const isMLBackend = response.data.models_loaded !== false && response.data.status !== 'streamlit_unavailable';

    return {
      success: true,
      backend_url: backendUrl,
      ml_available: isMLBackend,
      backend_info: response.data
    };
  } catch (error) {
    console.log('⚠️ Backend Test Failed:', error.message);
    return { success: false, fallback_mode: 'mock', backend_url: null };
  }
};

// Initialize backend detection
let currentBackendUrl = null;
let mlAvailable = false;

testBackend().then(result => {
  currentBackendUrl = result.backend_url;
  mlAvailable = result.ml_available;
  console.log('🚀 Backend initialization complete:', result);
});

// 安全的 material 屬性設置函數
const setMaterialProperty = (material, property, value) => {
  if (!material) return;
  
  if (Array.isArray(material)) {
    material.forEach(mat => {
      if (mat && mat[property] !== undefined) {
        mat[property] = value;
      }
    });
  } else {
    if (material && material[property] !== undefined) {
      material[property] = value;
    }
  }
};

// Camera Controller for smooth transitions
function CameraController({ targetPosition, targetLookAt, isTransitioning, onTransitionEnd }) {
  const { camera } = useThree();
  const controlsRef = useRef();
  const startPosition = useRef(new THREE.Vector3());
  const startTarget = useRef(new THREE.Vector3());
  const progress = useRef(0);
  
  useEffect(() => {
    if (isTransitioning && targetPosition) {
      startPosition.current.copy(camera.position);
      if (controlsRef.current) {
        startTarget.current.copy(controlsRef.current.target);
      }
      progress.current = 0;
    }
  }, [isTransitioning, targetPosition, camera]);
  
  useFrame((state, delta) => {
    if (isTransitioning && targetPosition && controlsRef.current) {
      progress.current += delta * 2; // Transition speed
      
      if (progress.current >= 1) {
        progress.current = 1;
        camera.position.copy(targetPosition);
        if (targetLookAt) {
          controlsRef.current.target.copy(targetLookAt);
        }
        controlsRef.current.update();
        if (onTransitionEnd) onTransitionEnd();
      } else {
        // Smooth interpolation
        const easedProgress = 1 - Math.pow(1 - progress.current, 3); // Ease out cubic
        
        camera.position.lerpVectors(startPosition.current, targetPosition, easedProgress);
        if (targetLookAt) {
          controlsRef.current.target.lerpVectors(startTarget.current, targetLookAt, easedProgress);
        }
        controlsRef.current.update();
      }
    }
  });
  
  return (
    <OrbitControls
      ref={controlsRef}
      enableZoom={true}
      enablePan={true}
      enableRotate={!isTransitioning}
      minDistance={5}
      maxDistance={100}
      enableDamping={true}
      dampingFactor={0.05}
    />
  );
}

// Realistic 3D Planet inspired by planetarium
function RealisticPlanet({ position, radius, color, name, data = {}, onClick, isAnimating, isPredicted }) {
  const meshRef = useRef();
  const groupRef = useRef();
  const ringRef = useRef();
  const atmosphereRef = useRef();
  const glowRef = useRef();
  
  // Realistic rotation speeds based on planet type
  const rotationSpeed = useMemo(() => {
    if (radius > 4) return 0.005; // Gas giants rotate faster
    if (radius > 2) return 0.01;  // Super Earths
    return 0.02; // Earth-like planets
  }, [radius]);
  
  useFrame((state) => {
    if (meshRef.current) {
      // Realistic planet rotation
      meshRef.current.rotation.y += rotationSpeed;
      
      if (isAnimating) {
        // Epic entrance animation for predicted planets
        const time = state.clock.elapsedTime;
        if (groupRef.current) {
          groupRef.current.position.y = position[1] + Math.sin(time * 2) * 0.8;
          groupRef.current.scale.setScalar(1 + Math.sin(time * 3) * 0.15);
        }
        
        // Pulsing atmosphere
        if (atmosphereRef.current) {
          const opacity = 0.3 + Math.sin(time * 4) * 0.2;
          setMaterialProperty(atmosphereRef.current.material, 'opacity', opacity);
        }
        
        // Pulsing glow effect
        if (glowRef.current) {
          const glowPulse = Math.sin(time * 1.5) * 0.3 + 0.7;
          setMaterialProperty(glowRef.current.material, 'opacity', glowPulse * 0.3);
        }
      } else {
        // Subtle orbital motion
        if (groupRef.current) {
          groupRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 0.3) * 0.2;
        }
      }
      
      // Ring rotation for gas giants
      if (ringRef.current) {
        ringRef.current.rotation.z += 0.003;
      }
    }
  });

  // Planet surface details based on type
  const surfaceProps = useMemo(() => {
    if (data.habitability > 70) {
      return { roughness: 0.8, metalness: 0.1 }; // Earth-like
    } else if (radius > 3) {
      return { roughness: 0.3, metalness: 0.7 }; // Gas giant
    } else if (data.temperature > 1000) {
      return { roughness: 0.2, metalness: 0.9 }; // Hot planet
    }
    return { roughness: 0.9, metalness: 0.1 }; // Rocky planet
  }, [data.habitability, radius, data.temperature]);

  return (
    <group ref={groupRef} position={position}>
      {/* Main Planet with realistic materials */}
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
        <sphereGeometry args={[radius, 32, 32]} />
        <meshStandardMaterial 
          color={color} 
          emissive={color}
          emissiveIntensity={isAnimating ? 0.6 : 0.2}
          roughness={surfaceProps.roughness}
          metalness={surfaceProps.metalness}
        />
      </mesh>
      
      {/* Realistic Atmosphere for habitable planets */}
      {data.habitability > 40 && (
        <mesh ref={atmosphereRef}>
          <sphereGeometry args={[radius * 1.05, 16, 16]} />
          <meshBasicMaterial 
            color={data.habitability > 70 ? "#4a9eff" : "#ffaa44"} 
            transparent 
            opacity={isAnimating ? 0.4 : 0.15}
            side={THREE.BackSide}
          />
        </mesh>
      )}
      
      {/* Realistic Ring system for large planets */}
      {radius > 2.5 && (
        <mesh ref={ringRef} rotation={[Math.PI / 2 + 0.1, 0, 0]}>
          <ringGeometry args={[radius * 1.3, radius * 1.7, 64]} />
          <meshBasicMaterial 
            color={new THREE.Color(color).multiplyScalar(0.7)} 
            transparent 
            opacity={0.6} 
            side={THREE.DoubleSide}
          />
        </mesh>
      )}
      
      {/* Selection glow when clicked */}
      {data.selected && (
        <mesh ref={glowRef}>
          <sphereGeometry args={[radius * 1.2, 16, 16]} />
          <meshBasicMaterial 
            color="#ffffff" 
            transparent 
            opacity={0.3}
            side={THREE.BackSide}
          />
        </mesh>
      )}
      
      {/* Planet Information Label */}
      <Html distanceFactor={12} position={[0, radius + 1.8, 0]}>
        <div className={`planet-label ${isAnimating ? 'pulsing' : ''} ${isPredicted ? 'predicted' : ''}`}>
          <div className="planet-name">{name}</div>
          <div className="planet-info">
            <span className={`status ${data.disposition ? data.disposition.toLowerCase() : 'unknown'}`}>
              {data.disposition || 'Unknown'}
            </span>
            <span className="habitability">
              {data.habitability || 0}% habitable
            </span>
          </div>
          {isPredicted && (
            <div className="predicted-badge">🤖 AI PREDICTED</div>
          )}
        </div>
      </Html>
    </group>
  );
}

// Epic Cosmic Background with Enhanced Effects
function EpicCosmicBackground() {
  const starsRef = useRef();
  
  useFrame((state) => {
    if (starsRef.current) {
      starsRef.current.rotation.y += 0.0002;
    }
  });

  return (
    <>
      {/* Multiple star layers for depth */}
      <Stars 
        ref={starsRef}
        radius={300} 
        depth={80} 
        count={5000} 
        factor={6} 
        saturation={0.2} 
        fade 
        speed={0.5} 
      />
      <Stars 
        radius={150} 
        depth={40} 
        count={2000} 
        factor={4} 
        saturation={0.5} 
        fade 
        speed={1} 
      />
      
      {/* Advanced Lighting Setup */}
      <ambientLight intensity={0.3} color="#4a4a6a" />
      <pointLight position={[20, 20, 20]} intensity={1.5} color="#ffffff" />
      <pointLight position={[-20, -20, -20]} intensity={0.8} color="#4a9eff" />
      <spotLight 
        position={[0, 50, 0]} 
        intensity={1} 
        angle={Math.PI / 4} 
        penumbra={0.5} 
        color="#00d4ff" 
      />
      <directionalLight position={[10, 10, 5]} intensity={0.7} color="#ffaa00" />
    </>
  );
}

// Particle System for Enhanced Visual Effects
function ParticleField() {
  const particlesRef = useRef();
  
  useFrame((state) => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y += 0.001;
      particlesRef.current.rotation.x += 0.0005;
    }
  });

  const particleCount = 1000;
  const positions = new Float32Array(particleCount * 3);
  
  for (let i = 0; i < particleCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 200;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 200;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 200;
  }

  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          array={positions}
          count={particleCount}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.5} color="#00d4ff" transparent opacity={0.6} />
    </points>
  );
}

// Main 3D Universe Scene
function EpicExoplanetUniverse({ exoplanets, onPlanetClick, animatingPlanetId, predictedPlanetIds }) {
  return (
    <>
      <EpicCosmicBackground />
      <ParticleField />
      
      {/* Epic Title with Glow Effect */}
      <Text
        position={[0, 15, -10]}
        fontSize={2.5}
        color="#00d4ff"
        anchorX="center"
        anchorY="middle"
        letterSpacing={0.15}
      >
        🌌 EXOPLANET AI DISCOVERY 🌌
      </Text>
      
      <Text
        position={[0, 12, -10]}
        fontSize={1}
        color="#ffffff"
        anchorX="center"
        anchorY="middle"
        opacity={0.9}
      >
        Advanced Machine Learning • NASA Data • Interactive 3D Universe
      </Text>
      
      <Text
        position={[0, 10, -10]}
        fontSize={0.7}
        color="#4a9eff"
        anchorX="center"
        anchorY="middle"
        opacity={0.8}
      >
        Click planets to explore • Use AI predictor • Navigate with mouse
      </Text>
      
      {/* Render all planets */}
      {exoplanets.map((planet) => (
        <RealisticPlanet
          key={planet.id}
          position={planet.position}
          radius={planet.radius}
          color={planet.color}
          name={planet.name}
          data={planet}
          onClick={onPlanetClick}
          isAnimating={planet.id === animatingPlanetId}
          isPredicted={predictedPlanetIds.includes(planet.id)}
        />
      ))}
    </>
  );
}

// Enhanced AI Prediction Panel
function EnhancedAIPanel({ onPredict, prediction, loading, predictedPlanetIds, expanded, setExpanded }) {
  const [params, setParams] = useState({
    koi_period: 365.25,
    koi_prad: 1.0,
    koi_teq: 288,
    koi_steff: 5778,
    koi_insol: 1.0
  });

  const presets = {
    earth: { 
      name: "Earth-like", 
      params: { koi_period: 365.25, koi_prad: 1.0, koi_teq: 288, koi_steff: 5778, koi_insol: 1.0 }
    },
    hotJupiter: { 
      name: "Hot Jupiter", 
      params: { koi_period: 3.5, koi_prad: 11.0, koi_teq: 1200, koi_steff: 6000, koi_insol: 100 }
    },
    superEarth: { 
      name: "Super Earth", 
      params: { koi_period: 20, koi_prad: 1.8, koi_teq: 350, koi_steff: 4500, koi_insol: 2.5 }
    },
    frozen: {
      name: "Frozen World",
      params: { koi_period: 500, koi_prad: 0.8, koi_teq: 150, koi_steff: 3500, koi_insol: 0.1 }
    }
  };

  const handlePreset = (presetKey) => {
    setParams(presets[presetKey].params);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onPredict(params);
  };

  return (
    <div className={`ai-panel epic-panel ${expanded ? 'expanded' : 'collapsed'}`}>
      {/* Collapsible header - always visible */}
      <div className="ai-compact-header" onClick={() => setExpanded(!expanded)}>
        <span className="ai-icon">🤖</span>
        <span className="ai-compact-title">AI PREDICTOR</span>
        <span className="expand-icon">
          {expanded ? '◀' : '▶'}
        </span>
      </div>
      
      {/* Expandable content */}
      <div className={`ai-panel-content ${expanded ? 'visible' : 'hidden'}`}>
        <div className="panel-header">
          <h2>🤖 AI EXOPLANET PREDICTOR</h2>
          <div className="ai-status">Neural Networks Active • 92.16% Accuracy</div>
        </div>
      
      {/* Enhanced Presets */}
      <div className="presets-grid">
        {Object.entries(presets).map(([key, preset]) => (
          <button 
            key={key}
            onClick={() => handlePreset(key)} 
            className={`preset-btn ${key}`}
          >
            <div className="preset-icon">
              {key === 'earth' && '🌍'}
              {key === 'hotJupiter' && '🔥'}
              {key === 'superEarth' && '🌎'}
              {key === 'frozen' && '❄️'}
            </div>
            <div className="preset-name">{preset.name}</div>
          </button>
        ))}
      </div>
      
      <form onSubmit={handleSubmit}>
        <div className="param-grid enhanced">
          <div className="param-item">
            <label>Orbital Period</label>
            <input
              type="number"
              value={params.koi_period}
              onChange={(e) => setParams({...params, koi_period: parseFloat(e.target.value)})}
              step="0.1"
            />
            <span className="param-unit">days</span>
          </div>
          
          <div className="param-item">
            <label>Planet Radius</label>
            <input
              type="number"
              value={params.koi_prad}
              onChange={(e) => setParams({...params, koi_prad: parseFloat(e.target.value)})}
              step="0.1"
            />
            <span className="param-unit">Earth radii</span>
          </div>
          
          <div className="param-item">
            <label>Equilibrium Temperature</label>
            <input
              type="number"
              value={params.koi_teq}
              onChange={(e) => setParams({...params, koi_teq: parseFloat(e.target.value)})}
            />
            <span className="param-unit">Kelvin</span>
          </div>
          
          <div className="param-item">
            <label>Stellar Temperature</label>
            <input
              type="number"
              value={params.koi_steff}
              onChange={(e) => setParams({...params, koi_steff: parseFloat(e.target.value)})}
            />
            <span className="param-unit">Kelvin</span>
          </div>
        </div>
        
        <button type="submit" disabled={loading} className="predict-button epic">
          <span className="btn-icon">{loading ? '🔄' : '🚀'}</span>
          <span className="btn-text">
            {loading ? 'AI ANALYZING...' : 'PREDICT & MATERIALIZE'}
          </span>
        </button>
      </form>
      
      {prediction && (
        <div className="prediction-results epic">
          <h3>🎯 AI PREDICTION RESULT</h3>
          <div className="result-grid enhanced">
            <div className="result-card primary">
              <div className="result-icon">🏷️</div>
              <div className="result-content">
                <div className="result-label">Classification</div>
                <div className="result-value">{prediction.prediction}</div>
              </div>
            </div>
            
            <div className="result-card">
              <div className="result-icon">📊</div>
              <div className="result-content">
                <div className="result-label">Confidence</div>
                <div className="result-value">
                  {prediction.confidence ? (prediction.confidence * 100).toFixed(1) : '0.0'}%
                </div>
              </div>
            </div>
            
            <div className="result-card">
              <div className="result-icon">🌍</div>
              <div className="result-content">
                <div className="result-label">Habitability</div>
                <div className="result-value">{prediction.habitability_score || 0}/100</div>
              </div>
            </div>
            
            <div className="result-card">
              <div className="result-icon">🪐</div>
              <div className="result-content">
                <div className="result-label">Planet Type</div>
                <div className="result-value">{prediction.planet_type || 'Unknown'}</div>
              </div>
            </div>
          </div>
          
          {/* Probability Breakdown */}
          <div className="probability-breakdown">
            <h4>Classification Probabilities</h4>
            {prediction.probabilities && Object.entries(prediction.probabilities).map(([category, prob]) => (
              <div key={category} className="prob-item">
                <span className="prob-label">{category}</span>
                <div className="prob-bar">
                  <div 
                    className="prob-fill" 
                    style={{ width: `${prob * 100}%` }}
                  ></div>
                </div>
                <span className="prob-value">{(prob * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
      </div>
    </div>
  );
}

// Main Epic App
function App() {
  const [exoplanets, setExoplanets] = useState([]);
  const [selectedPlanet, setSelectedPlanet] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [animatingPlanetId, setAnimatingPlanetId] = useState(null);
  const [predictedPlanetIds, setPredictedPlanetIds] = useState([]);
  // const [hasPredictedPlanet, setHasPredictedPlanet] = useState(false); // Removed unused state
  
  // Backend connection status
  const [backendStatus, setBackendStatus] = useState({
    connected: false,
    url: '',
    lastCheck: null,
    modelsLoaded: false,
    error: null
  });
  
  // Status indicator collapse/expand state
  const [statusExpanded, setStatusExpanded] = useState(false);
  
  // AI panel collapse/expand state
  const [aiPanelExpanded, setAiPanelExpanded] = useState(true);

  // Camera control states
  const [cameraTarget, setCameraTarget] = useState(null);
  const [cameraLookAt, setCameraLookAt] = useState(null);
  const [isTransitioning, setIsTransitioning] = useState(false);

  // Check backend status function
  const checkBackendStatus = async () => {
    const currentTime = new Date().toLocaleTimeString();
    
    try {
      console.log('🔍 Checking backend status...');
      
      // Test local backend first
      const testUrl = 'http://localhost:8000';
      const response = await axios.get(`${testUrl}/health`, { 
        timeout: 3000,
        headers: { 'Accept': 'application/json' }
      });
      
      if (response.status === 200 && response.data) {
        setBackendStatus({
          connected: true,
          url: testUrl,
          lastCheck: currentTime,
          modelsLoaded: response.data.models_loaded || false,
          error: null
        });
        console.log('✅ Local backend connected:', response.data);
        return testUrl;
      }
    } catch (localError) {
      console.log('❌ Local backend failed:', localError.message);
      
      // Try Render backend as fallback
      try {
        const renderUrl = 'https://test-backend-2-ikqg.onrender.com';
        const response = await axios.get(`${renderUrl}/health`, { 
          timeout: 5000,
          headers: { 'Accept': 'application/json' }
        });
        
        if (response.status === 200 && response.data) {
          setBackendStatus({
            connected: true,
            url: renderUrl,
            lastCheck: currentTime,
            modelsLoaded: response.data.models_loaded || false,
            error: null
          });
          console.log('✅ Render backend connected:', response.data);
          return renderUrl;
        }
      } catch (renderError) {
        console.log('❌ Render backend failed:', renderError.message);
        
        setBackendStatus({
          connected: false,
          url: '',
          lastCheck: currentTime,
          modelsLoaded: false,
          error: `Local: ${localError.message.substring(0, 30)}...`
        });
      }
    }
    
    return null;
  };

  // Check backend status on component mount and periodically
  useEffect(() => {
    // Initial check
    checkBackendStatus();
    
    // Check every 30 seconds
    const interval = setInterval(checkBackendStatus, 30000);
    
    return () => clearInterval(interval);
  }, []);

  // Initialize with some default planets for immediate visual impact
  useEffect(() => {
    const defaultPlanets = [
      {
        id: "kepler-442b", 
        name: "Kepler-442b", 
        position: [12, 4, -18], 
        radius: 1.34, 
        temperature: 233, 
        disposition: "CONFIRMED", 
        habitability: 84, 
        color: "#4CAF50"
      },
      {
        id: "kepler-186f", 
        name: "Kepler-186f", 
        position: [-18, -6, 25], 
        radius: 1.11,
        temperature: 188, 
        disposition: "CONFIRMED", 
        habitability: 91, 
        color: "#2196F3" 
      },
      {
        id: "kepler-452b", 
        name: "Kepler-452b", 
        position: [22, 10, 12], 
        radius: 1.63,
        temperature: 265, 
        disposition: "CONFIRMED", 
        habitability: 78, 
        color: "#FF9800"
      },
      {
        id: "hd-40307g",
        name: "HD 40307g",
        position: [-25, 15, -30],
        radius: 2.1,
        temperature: 320,
        disposition: "CANDIDATE",
        habitability: 65,
        color: "#9C27B0"
      },
      {
        id: "gliese-667cc",
        name: "Gliese 667Cc",
        position: [10, -12, 35],
        radius: 1.5,
        temperature: 277,
        disposition: "CONFIRMED",
        habitability: 88,
        color: "#00BCD4"
      }
    ];
    
    setExoplanets(defaultPlanets);
    
    // Load real data from API
    const loadData = async () => {
      try {
        const [planetsRes, statsRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/exoplanets`),
          axios.get(`${API_BASE_URL}/stats`)
        ]);
        
        if (planetsRes.data.exoplanets) {
          // Add unique IDs to API planets to avoid key conflicts
          const apiPlanets = planetsRes.data.exoplanets.map(planet => ({
            ...planet,
            id: `api-${planet.id || (planet.name ? planet.name.replace(/\s+/g, '-').toLowerCase() : 'unknown')}`
          }));
          setExoplanets(prev => [...prev, ...apiPlanets]);
        }
        setStats(statsRes.data);
      } catch (error) {
        console.error('API not available, using default data:', error);
        setStats({ total_exoplanets: 9564, confirmed: 2746 });
      }
    };
    
    loadData();
  }, []);

  // Handle AI prediction with epic animation
  const handlePredict = async (params) => {
    setLoading(true);
    try {
      let response;
      let usedBackend = null;

      // Check backend status before prediction
      const availableBackend = await checkBackendStatus();
      
      if (availableBackend) {
        try {
          console.log(`🚀 Making prediction request to: ${availableBackend}`);
          response = await axios.post(`${availableBackend}/predict`, params, { timeout: 10000 });
          usedBackend = availableBackend;
          console.log(`✅ Prediction successful from backend: ${availableBackend}`);
          console.log('📊 API Response:', response.data);
          
          // Debug: Check response data structure
          console.log('🔍 Response structure check:');
          console.log('  - prediction:', response.data.prediction);
          console.log('  - confidence:', response.data.confidence);
          console.log('  - habitability_score:', response.data.habitability_score);
          console.log('  - planet_type:', response.data.planet_type);
          console.log('  - planet_name:', response.data.planet_name);
          
          // Update backend status with successful call
          setBackendStatus(prev => ({
            ...prev,
            lastCheck: new Date().toLocaleTimeString(),
            error: null
          }));
          
        } catch (apiError) {
          console.log(`⚠️ Backend prediction failed, using mock ML service: ${apiError.message}`);
          
          // Update backend status with error
          setBackendStatus(prev => ({
            ...prev,
            error: `Prediction failed: ${apiError.message.substring(0, 50)}...`,
            lastCheck: new Date().toLocaleTimeString()
          }));
          
          response = await MockMLService.predict(params);
        }
      } else {
        console.log('ℹ️ No backend available, using mock ML service');
        response = await MockMLService.predict(params);
      }

      // Use response.data if it's an axios response, otherwise use response directly
      const predictionData = response.data || response;
      setPrediction(predictionData);
      
      console.log('🎯 Setting prediction data:', predictionData);
      
      // Use a fixed predicted planet that gets updated
      const fixedPlanetId = 'predicted-main';
      const existingPredictedIndex = exoplanets.findIndex(planet =>
        planet.id === fixedPlanetId
      );

      let targetPlanet;
      let planetId = fixedPlanetId;

      if (existingPredictedIndex !== -1) {
        // Update existing predicted planet
        const updatedPlanet = {
          ...exoplanets[existingPredictedIndex],
          name: predictionData.planet_name || `Kepler-${Math.floor(Math.random() * 999) + 1} ${String.fromCharCode(97 + Math.floor(Math.random() * 26))}`,
          radius: params.koi_prad || 1.0,
          temperature: params.koi_teq || 288,
          disposition: predictionData.prediction || 'UNKNOWN',
          habitability: predictionData.habitability_score || 0,
          color: predictionData.prediction === 'CONFIRMED' ? '#4CAF50' :
                 predictionData.prediction === 'CANDIDATE' ? '#FF9800' : '#F44336'
        };

        setExoplanets(prev => prev.map((planet, index) =>
          index === existingPredictedIndex ? updatedPlanet : planet
        ));
        targetPlanet = updatedPlanet;
        setAnimatingPlanetId(planetId);
        // setHasPredictedPlanet(true); // Removed unused state setter
      } else {
        // Create the main predicted planet (only once)
        const newPlanet = {
          id: planetId,
          name: predictionData.planet_name || `Kepler-${Math.floor(Math.random() * 999) + 1} ${String.fromCharCode(97 + Math.floor(Math.random() * 26))}`,
          position: [15, 5, -10], // Fixed position for the predicted planet
          radius: params.koi_prad || 1.0,
          temperature: params.koi_teq || 288,
          disposition: predictionData.prediction || 'UNKNOWN',
          habitability: predictionData.habitability_score || 0,
          color: predictionData.prediction === 'CONFIRMED' ? '#4CAF50' :
                 predictionData.prediction === 'CANDIDATE' ? '#FF9800' : '#F44336'
        };

        setExoplanets(prev => [...prev, newPlanet]);
        targetPlanet = newPlanet;
        setAnimatingPlanetId(planetId);
        setPredictedPlanetIds(prev => [...prev, planetId]);
        // setHasPredictedPlanet(true); // Removed unused state setter
      }

      // Jump camera to predicted planet
      const planetPos = new THREE.Vector3(...targetPlanet.position);
      const distance = Math.max(targetPlanet.radius * 5, 10);
      const cameraPos = planetPos.clone().add(new THREE.Vector3(distance, distance * 0.7, distance));
      
      setCameraTarget(cameraPos);
      setCameraLookAt(planetPos);
      setIsTransitioning(true);
      setSelectedPlanet(targetPlanet);
      
      // Stop animation after 8 seconds
      setTimeout(() => setAnimatingPlanetId(null), 8000);
      
    } catch (error) {
      console.error('Prediction failed:', error);
      // Show demo prediction even if API fails
      const demoPrediction = {
        prediction: "CANDIDATE",
        confidence: 0.78,
        habitability_score: 85,
        planet_type: "Earth-like",
        star_type: "G-dwarf",
        probabilities: {
          "CANDIDATE": 0.78,
          "CONFIRMED": 0.15,
          "FALSE POSITIVE": 0.07
        }
      };
      setPrediction(demoPrediction);
      
      // Use fixed demo planet instead of creating new ones
      const demoPlanetId = 'demo-main';
      const existingDemoIndex = exoplanets.findIndex(planet =>
        planet.id === demoPlanetId
      );

      if (existingDemoIndex !== -1) {
        // Update existing demo planet
        const updatedPlanet = {
          ...exoplanets[existingDemoIndex],
          name: `Kepler-${Math.floor(Math.random() * 999) + 1} ${String.fromCharCode(97 + Math.floor(Math.random() * 26))}`,
          radius: params.koi_prad,
          temperature: params.koi_teq,
          disposition: "CANDIDATE",
          habitability: 85,
          color: '#FF9800'
        };

        setExoplanets(prev => prev.map((planet, index) =>
          index === existingDemoIndex ? updatedPlanet : planet
        ));
        setAnimatingPlanetId(updatedPlanet.id);
      } else {
        // Create demo planet (only once)
        const newPlanet = {
          id: demoPlanetId,
          name: `Kepler-${Math.floor(Math.random() * 999) + 1} ${String.fromCharCode(97 + Math.floor(Math.random() * 26))}`,
          position: [10, 3, -15], // Fixed position for demo planet
          radius: params.koi_prad,
          temperature: params.koi_teq,
          disposition: "CANDIDATE",
          habitability: 85,
          color: '#FF9800'
        };

        setExoplanets(prev => [...prev, newPlanet]);
        setAnimatingPlanetId(newPlanet.id);
        setPredictedPlanetIds(prev => [...prev, newPlanet.id]);
      }
      setTimeout(() => setAnimatingPlanetId(null), 8000);
    } finally {
      setLoading(false);
    }
  };

  // Handle planet selection with camera transition
  const handlePlanetClick = (planet) => {
    setSelectedPlanet(planet);
    
    // Calculate camera position for close-up view
    const planetPos = new THREE.Vector3(...planet.position);
    const distance = Math.max(planet.radius * 4, 8); // Minimum distance based on planet size
    const cameraPos = planetPos.clone().add(new THREE.Vector3(distance, distance * 0.5, distance));
    
    // Start camera transition
    setCameraTarget(cameraPos);
    setCameraLookAt(planetPos);
    setIsTransitioning(true);
  };
  
  // Handle camera transition completion
  const handleTransitionEnd = () => {
    setIsTransitioning(false);
  };
  
  // Return to overview
  const returnToOverview = () => {
    setCameraTarget(new THREE.Vector3(0, 15, 30));
    setCameraLookAt(new THREE.Vector3(0, 0, 0));
    setIsTransitioning(true);
    setSelectedPlanet(null);
  };

  return (
    <div className="App epic-app">
      {/* Epic 3D Universe */}
      <Canvas
        className="universe-canvas"
        camera={{ position: [0, 8, 35], fov: 65 }}
        style={{
          background: 'radial-gradient(ellipse at center, #001122 0%, #000000 70%, #000000 100%)',
          zIndex: 1
        }}
      >
        <Suspense fallback={null}>
          <EpicExoplanetUniverse 
            exoplanets={exoplanets}
            onPlanetClick={handlePlanetClick}
            animatingPlanetId={animatingPlanetId}
            predictedPlanetIds={predictedPlanetIds}
          />
          <CameraController
            targetPosition={cameraTarget}
            targetLookAt={cameraLookAt}
            isTransitioning={isTransitioning}
            onTransitionEnd={handleTransitionEnd}
          />
        </Suspense>
      </Canvas>

      {/* Enhanced UI Overlays */}
      <EnhancedAIPanel
        onPredict={handlePredict}
        prediction={prediction}
        loading={loading}
        predictedPlanetIds={predictedPlanetIds}
        expanded={aiPanelExpanded}
        setExpanded={setAiPanelExpanded}
      />
      
      {/* Stats remain the same but enhanced */}
      {stats && (
        <div className="stats-dashboard epic">
          <h3>📊 MISSION CONTROL</h3>
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
      )}
      
      {/* Enhanced Planet Details Panel */}
      {selectedPlanet && (
        <div className="planet-details epic-panel enhanced">
          <div className="panel-header">
            <button className="close-button" onClick={() => setSelectedPlanet(null)}>✕</button>
            <button className="overview-button" onClick={returnToOverview}>🌌 Return to Overview</button>
          </div>
          
          <h2>🪐 {selectedPlanet.name}</h2>
          
          <div className="planet-preview">
            <div className="preview-sphere" style={{
              background: `radial-gradient(circle at 30% 30%, ${selectedPlanet.color}, ${selectedPlanet.color}88)`,
              width: '80px',
              height: '80px',
              borderRadius: '50%',
              margin: '0 auto 20px',
              boxShadow: `0 0 30px ${selectedPlanet.color}66`
            }}></div>
          </div>

          <div className="detail-grid enhanced">
            <div className="detail-item">
              <span className="detail-icon">🎯</span>
              <div className="detail-content">
                <span className="detail-label">Status:</span>
                <span className={`detail-value status-${selectedPlanet.disposition ? selectedPlanet.disposition.toLowerCase() : 'unknown'}`}>
                  {selectedPlanet.disposition || 'Unknown'}
                </span>
              </div>
            </div>

            <div className="detail-item">
              <span className="detail-icon">📏</span>
              <div className="detail-content">
                <span className="detail-label">Radius:</span>
                <span className="detail-value">{selectedPlanet.radius}× Earth</span>
              </div>
            </div>

            <div className="detail-item">
              <span className="detail-icon">🌡️</span>
              <div className="detail-content">
                <span className="detail-label">Temperature:</span>
                <span className="detail-value">{selectedPlanet.temperature} K</span>
              </div>
            </div>

            <div className="detail-item">
              <span className="detail-icon">🌍</span>
              <div className="detail-content">
                <span className="detail-label">Habitability:</span>
                <span className="detail-value">{selectedPlanet.habitability}%</span>
              </div>
            </div>
          </div>

          <div className="habitability-meter enhanced">
            <div className="meter-label">Life Potential Assessment</div>
            <div className="meter-bar">
              <div
                className="meter-fill"
                style={{
                  width: `${selectedPlanet.habitability}%`,
                  background: selectedPlanet.habitability > 70 ? 'linear-gradient(90deg, #4CAF50, #8BC34A)' :
                             selectedPlanet.habitability > 40 ? 'linear-gradient(90deg, #FF9800, #FFC107)' : 
                             'linear-gradient(90deg, #F44336, #FF5722)'
                }}
              ></div>
            </div>
            <div className="meter-text">{selectedPlanet.habitability}% Habitable</div>
          </div>
          
          {predictedPlanetIds.includes(selectedPlanet.id) && (
            <div className="ai-prediction-info">
              <h4>🤖 AI Prediction Results</h4>
              <div className="prediction-confidence">
                Confidence: {prediction && prediction.confidence ? (prediction.confidence * 100).toFixed(1) : 'N/A'}%
              </div>
            </div>
          )}
        </div>
      )}
      
      {/* Collapsible Backend Status Indicator - Left Bottom Corner */}
      <div className={`backend-status-indicator ${statusExpanded ? 'expanded' : 'collapsed'}`}>
        {/* Always visible compact header */}
        <div className="status-compact-header" onClick={() => setStatusExpanded(!statusExpanded)}>
          <span className="status-icon">
            {backendStatus.connected ? '🟢' : '🔴'}
          </span>
          <span className="status-compact-title">
            {backendStatus.connected ? 'API Connected' : 'API Disconnected'}
          </span>
          <span className="expand-icon">
            {statusExpanded ? '▼' : '▲'}
          </span>
        </div>
        
        {/* Expandable details */}
        <div className={`status-details ${statusExpanded ? 'visible' : 'hidden'}`}>
          <div className="status-header">
            <span className="status-title">Backend Status</span>
            <button 
              className="refresh-btn"
              onClick={checkBackendStatus}
              title="Refresh backend status"
            >
              🔄
            </button>
          </div>
          
          <div className="status-rows">
            <div className="status-row">
              <span className="label">Connection:</span>
              <span className={`value ${backendStatus.connected ? 'connected' : 'disconnected'}`}>
                {backendStatus.connected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
            
            {backendStatus.connected && (
              <>
                <div className="status-row">
                  <span className="label">URL:</span>
                  <span className="value url" title={backendStatus.url}>
                    {backendStatus.url.includes('localhost') ? 'Local' : 'Render'}
                  </span>
                </div>
                
                <div className="status-row">
                  <span className="label">ML Models:</span>
                  <span className={`value ${backendStatus.modelsLoaded ? 'loaded' : 'not-loaded'}`}>
                    {backendStatus.modelsLoaded ? 'Loaded ✅' : 'Not Loaded ❌'}
                  </span>
                </div>
              </>
            )}
            
            <div className="status-row">
              <span className="label">Last Check:</span>
              <span className="value time">
                {backendStatus.lastCheck || 'Never'}
              </span>
            </div>
            
            {backendStatus.error && (
              <div className="status-row error">
                <span className="label">Error:</span>
                <span className="value error-msg" title={backendStatus.error}>
                  {backendStatus.error}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Epic Loading Screen */}
      {loading && (
        <div className="loading-screen epic">
          <div className="loading-content">
            <div className="loading-spinner epic"></div>
            <div className="loading-text">
              🤖 AI NEURAL NETWORKS ANALYZING...
            </div>
            <div className="loading-subtext">
              Processing NASA Kepler data • Training deep learning models
            </div>
            <div className="loading-progress">
              <div className="progress-bar"></div>
            </div>
          </div>
        </div>
      )}
      
    </div>
  );
}

export default App;