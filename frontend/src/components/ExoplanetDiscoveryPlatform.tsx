import React, { useState, useEffect, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { Box, Typography, Fab, Drawer, Card, CardContent, Slider, TextField, Button, Chip, Grid } from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Settings, Info, Explore, PsychologyAlt } from '@mui/icons-material';

import CosmicScene from './3D/CosmicScene';
import ExoplanetInputPanel from './UI/ExoplanetInputPanel';
import PredictionDisplay from './UI/PredictionDisplay';
import ExoplanetInfo from './UI/ExoplanetInfo';
import ControlPanel from './UI/ControlPanel';
import { useExoplanetStore } from '../store/exoplanetStore';

const ExoplanetDiscoveryPlatform: React.FC = () => {
  const [leftDrawerOpen, setLeftDrawerOpen] = useState(false);
  const [rightDrawerOpen, setRightDrawerOpen] = useState(false);
  const [selectedExoplanet, setSelectedExoplanet] = useState<any>(null);
  const [predictionResult, setPredictionResult] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  
  const { 
    exoplanets, 
    filters, 
    stats,
    fetchExoplanets, 
    updateFilters,
    predictExoplanet 
  } = useExoplanetStore();

  useEffect(() => {
    fetchExoplanets();
  }, [fetchExoplanets]);

  const handlePlanetClick = (planet: any) => {
    setSelectedExoplanet(planet);
    setRightDrawerOpen(true);
  };

  const handlePrediction = async (inputData: any) => {
    setIsAnalyzing(true);
    try {
      const result = await predictExoplanet(inputData);
      setPredictionResult(result);
      setRightDrawerOpen(true);
    } catch (error) {
      console.error('Prediction failed:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <Box sx={{ width: '100vw', height: '100vh', position: 'relative', overflow: 'hidden' }}>
      {/* Main 3D Canvas */}
      <Canvas
        camera={{ position: [50, 30, 50], fov: 60 }}
        style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}
        gl={{ 
          antialias: true, 
          alpha: true,
          powerPreference: "high-performance"
        }}
      >
        <CosmicScene 
          exoplanets={exoplanets}
          onPlanetClick={handlePlanetClick}
          selectedPlanet={selectedExoplanet}
          filters={filters}
        />
      </Canvas>

      {/* UI Overlay */}
      <Box className="ui-overlay">
        {/* Top Header */}
        <motion.div
          initial={{ y: -100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
        >
          <Box
            sx={{
              position: 'absolute',
              top: 20,
              left: '50%',
              transform: 'translateX(-50%)',
              zIndex: 100,
            }}
          >
            <Card className="holo-panel" sx={{ px: 4, py: 2 }}>
              <Typography
                variant="h4"
                className="glow-text pulse-glow"
                sx={{
                  textAlign: 'center',
                  fontWeight: 900,
                  background: 'linear-gradient(45deg, #00d4ff, #ff6b35)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                EXOPLANET AI DISCOVERY
              </Typography>
              <Typography
                variant="subtitle1"
                sx={{
                  textAlign: 'center',
                  color: 'rgba(255, 255, 255, 0.8)',
                  mt: 1,
                  letterSpacing: '0.1em',
                }}
              >
                Explore {stats?.total_exoplanets || 0} Celestial Objects
              </Typography>
            </Card>
          </Box>
        </motion.div>

        {/* Left Control Panel FAB */}
        <motion.div
          initial={{ x: -100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 1 }}
        >
          <Fab
            color="primary"
            sx={{
              position: 'absolute',
              top: 120,
              left: 20,
              background: 'linear-gradient(45deg, #00d4ff, #0093cc)',
              '&:hover': {
                background: 'linear-gradient(45deg, #66e3ff, #00d4ff)',
                transform: 'scale(1.1)',
              },
            }}
            onClick={() => setLeftDrawerOpen(true)}
          >
            <Settings />
          </Fab>
        </motion.div>

        {/* AI Prediction FAB */}
        <motion.div
          initial={{ x: -100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 1.2 }}
        >
          <Fab
            color="secondary"
            sx={{
              position: 'absolute',
              top: 200,
              left: 20,
              background: 'linear-gradient(45deg, #ff6b35, #cc4a24)',
              '&:hover': {
                background: 'linear-gradient(45deg, #ff9566, #ff6b35)',
                transform: 'scale(1.1)',
              },
            }}
            onClick={() => setLeftDrawerOpen(true)}
          >
            <PsychologyAlt />
          </Fab>
        </motion.div>

        {/* Info FAB */}
        <motion.div
          initial={{ x: 100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 1 }}
        >
          <Fab
            sx={{
              position: 'absolute',
              top: 120,
              right: 20,
              background: 'linear-gradient(45deg, rgba(0, 212, 255, 0.8), rgba(255, 107, 53, 0.8))',
              '&:hover': {
                background: 'linear-gradient(45deg, #00d4ff, #ff6b35)',
                transform: 'scale(1.1)',
              },
            }}
            onClick={() => setRightDrawerOpen(true)}
          >
            <Info />
          </Fab>
        </motion.div>

        {/* Stats Display */}
        <motion.div
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 1.5 }}
        >
          <Box
            sx={{
              position: 'absolute',
              bottom: 20,
              left: 20,
              display: 'flex',
              gap: 2,
              flexWrap: 'wrap',
            }}
          >
            {stats && (
              <>
                <Chip
                  label={`Confirmed: ${stats.confirmed}`}
                  sx={{
                    background: 'linear-gradient(45deg, #4caf50, #2e7d32)',
                    color: 'white',
                    fontWeight: 600,
                    fontSize: '0.9rem',
                  }}
                />
                <Chip
                  label={`Candidates: ${stats.candidates}`}
                  sx={{
                    background: 'linear-gradient(45deg, #ff9800, #f57c00)',
                    color: 'white',
                    fontWeight: 600,
                    fontSize: '0.9rem',
                  }}
                />
                <Chip
                  label={`Habitable: ${stats.potentially_habitable}`}
                  sx={{
                    background: 'linear-gradient(45deg, #00d4ff, #0093cc)',
                    color: 'white',
                    fontWeight: 600,
                    fontSize: '0.9rem',
                  }}
                />
              </>
            )}
          </Box>
        </motion.div>

        {/* Analysis Status */}
        <AnimatePresence>
          {isAnalyzing && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                zIndex: 1000,
              }}
            >
              <Card className="holo-panel" sx={{ p: 4, textAlign: 'center' }}>
                <Box className="loading-spinner" sx={{ mx: 'auto', mb: 2 }} />
                <Typography variant="h6" className="glow-text">
                  AI ANALYZING EXOPLANET...
                </Typography>
                <Typography variant="body2" sx={{ mt: 1, opacity: 0.8 }}>
                  Processing celestial data with machine learning
                </Typography>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
      </Box>

      {/* Left Drawer - Controls and Input */}
      <Drawer
        anchor="left"
        open={leftDrawerOpen}
        onClose={() => setLeftDrawerOpen(false)}
        PaperProps={{
          sx: {
            width: { xs: '90vw', sm: 400 },
            background: 'linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(16, 33, 62, 0.95))',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(0, 212, 255, 0.3)',
          },
        }}
      >
        <Box sx={{ p: 3, height: '100%', overflow: 'auto' }}>
          <Typography variant="h5" className="glow-text" sx={{ mb: 3, textAlign: 'center' }}>
            AI DISCOVERY CENTER
          </Typography>
          
          <ExoplanetInputPanel 
            onPredict={handlePrediction}
            isLoading={isAnalyzing}
          />
          
          <Box sx={{ mt: 4 }}>
            <ControlPanel 
              filters={filters}
              onFiltersChange={updateFilters}
            />
          </Box>
        </Box>
      </Drawer>

      {/* Right Drawer - Information Display */}
      <Drawer
        anchor="right"
        open={rightDrawerOpen}
        onClose={() => setRightDrawerOpen(false)}
        PaperProps={{
          sx: {
            width: { xs: '90vw', sm: 400 },
            background: 'linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(16, 33, 62, 0.95))',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(0, 212, 255, 0.3)',
          },
        }}
      >
        <Box sx={{ p: 3, height: '100%', overflow: 'auto' }}>
          {predictionResult ? (
            <PredictionDisplay 
              result={predictionResult}
              onClose={() => {
                setPredictionResult(null);
                setRightDrawerOpen(false);
              }}
            />
          ) : selectedExoplanet ? (
            <ExoplanetInfo 
              exoplanet={selectedExoplanet}
              onClose={() => {
                setSelectedExoplanet(null);
                setRightDrawerOpen(false);
              }}
            />
          ) : (
            <Box sx={{ textAlign: 'center', mt: 10 }}>
              <Explore sx={{ fontSize: 80, color: 'rgba(0, 212, 255, 0.5)', mb: 2 }} />
              <Typography variant="h6" className="glow-text">
                SELECT AN EXOPLANET
              </Typography>
              <Typography variant="body2" sx={{ mt: 1, opacity: 0.8 }}>
                Click on any celestial object in the 3D view to explore its properties
              </Typography>
            </Box>
          )}
        </Box>
      </Drawer>
    </Box>
  );
};

export default ExoplanetDiscoveryPlatform;
