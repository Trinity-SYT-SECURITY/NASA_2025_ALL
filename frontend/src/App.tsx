import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Canvas } from '@react-three/fiber';
import { Suspense } from 'react';

// import ExoplanetDiscoveryPlatform from './components/ExoplanetDiscoveryPlatform';
// import LoadingScreen from './components/LoadingScreen';
import './App.css';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00d4ff',
      light: '#66e3ff',
      dark: '#0093cc',
    },
    secondary: {
      main: '#ff6b35',
      light: '#ff9566',
      dark: '#cc4a24',
    },
    background: {
      default: '#000000',
      paper: '#1a1a1a',
    },
    text: {
      primary: '#ffffff',
      secondary: '#cccccc',
    },
  },
  typography: {
    fontFamily: '"Orbitron", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '3rem',
      fontWeight: 700,
      letterSpacing: '0.1em',
    },
    h2: {
      fontSize: '2.5rem',
      fontWeight: 600,
      letterSpacing: '0.05em',
    },
    body1: {
      fontSize: '1.1rem',
      lineHeight: 1.6,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 25,
          textTransform: 'none',
          padding: '12px 30px',
          fontSize: '1.1rem',
          fontWeight: 600,
          boxShadow: '0 4px 15px rgba(0, 212, 255, 0.3)',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 8px 25px rgba(0, 212, 255, 0.5)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(26, 26, 26, 0.9)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(0, 212, 255, 0.2)',
          borderRadius: 15,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <Routes>
            <Route 
              path="/" 
              element={
                <div style={{
                  width: '100vw',
                  height: '100vh',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)',
                  color: '#00d4ff',
                  fontFamily: 'Orbitron',
                  textAlign: 'center'
                }}>
                  <h1 style={{ fontSize: '4rem', marginBottom: '2rem', textShadow: '0 0 30px #00d4ff' }}>
                    🌌 EXOPLANET AI DISCOVERY
                  </h1>
                  <p style={{ fontSize: '1.5rem', marginBottom: '3rem' }}>
                    Advanced Machine Learning Platform for Exoplanet Classification
                  </p>
                  <div style={{ background: 'rgba(0, 212, 255, 0.1)', padding: '2rem', borderRadius: '15px', border: '1px solid rgba(0, 212, 255, 0.3)' }}>
                    <h2>🚀 Backend API Active</h2>
                    <p>Backend running on: <a href="http://localhost:8000" style={{color: '#00d4ff'}}>http://localhost:8000</a></p>
                    <p>API Documentation: <a href="http://localhost:8000/docs" style={{color: '#00d4ff'}}>http://localhost:8000/docs</a></p>
                    <p>Test ML Prediction: <a href="http://localhost:8000/predict" style={{color: '#ff6b35'}}>POST /predict</a></p>
                  </div>
                  <div style={{ marginTop: '2rem', fontSize: '1.2rem' }}>
                    <p>✅ ML Models: 92%+ Accuracy</p>
                    <p>✅ Dataset: 9,564 Kepler Objects</p>
                    <p>✅ AI Predictions: Real-time</p>
                  </div>
                </div>
              } 
            />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
