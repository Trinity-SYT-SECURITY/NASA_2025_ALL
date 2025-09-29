import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  Divider,
  IconButton,
  LinearProgress
} from '@mui/material';
import { motion } from 'framer-motion';
import {
  Close,
  Public,
  Thermostat,
  AccessTime,
  Star,
  Straighten,
  LocationOn,
  Science
} from '@mui/icons-material';

interface ExoplanetInfoProps {
  exoplanet: any;
  onClose: () => void;
}

const ExoplanetInfo: React.FC<ExoplanetInfoProps> = ({ exoplanet, onClose }) => {
  const getDispositionColor = (disposition: string) => {
    switch (disposition) {
      case 'CONFIRMED':
        return '#4caf50';
      case 'CANDIDATE':
        return '#ff9800';
      case 'FALSE POSITIVE':
        return '#f44336';
      default:
        return '#666666';
    }
  };

  const getHabitabilityColor = (score: number) => {
    if (score >= 70) return '#4caf50';
    if (score >= 40) return '#ff9800';
    return '#f44336';
  };

  const getPlanetType = (radius: number) => {
    if (radius < 0.8) return 'Sub-Earth';
    if (radius <= 1.25) return 'Earth-like';
    if (radius <= 2.0) return 'Super-Earth';
    if (radius <= 4.0) return 'Mini-Neptune';
    return 'Giant';
  };

  const getTemperatureDescription = (temp: number) => {
    if (temp < 200) return 'Frozen';
    if (temp < 273) return 'Very Cold';
    if (temp < 373) return 'Habitable Range';
    if (temp < 600) return 'Hot';
    if (temp < 1000) return 'Very Hot';
    return 'Extreme';
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 100 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="holo-panel">
        <CardContent>
          {/* Header */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h5" className="glow-text">
              EXOPLANET DATA
            </Typography>
            <IconButton onClick={onClose} sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
              <Close />
            </IconButton>
          </Box>

          {/* Planet Name & Status */}
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <Card
              sx={{
                background: `linear-gradient(45deg, ${getDispositionColor(exoplanet.disposition)}, ${getDispositionColor(exoplanet.disposition)}aa)`,
                mb: 3,
                p: 2,
                textAlign: 'center'
              }}
            >
              <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'white', mb: 1 }}>
                {exoplanet.kepler_name || exoplanet.kepoi_name}
              </Typography>
              <Chip
                label={exoplanet.disposition}
                sx={{
                  background: 'rgba(255, 255, 255, 0.2)',
                  color: 'white',
                  fontWeight: 600,
                  fontSize: '1rem',
                  px: 2
                }}
              />
            </Card>
          </motion.div>

          {/* Key Metrics */}
          <Typography variant="h6" sx={{ mb: 2, color: '#00d4ff' }}>
            <Science sx={{ mr: 1, verticalAlign: 'middle' }} />
            Key Properties
          </Typography>

          <Grid container spacing={2} sx={{ mb: 3 }}>
            {/* Habitability Score */}
            <Grid item xs={12} sm={6}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3, duration: 0.5 }}
              >
                <Card sx={{ background: 'rgba(255, 255, 255, 0.05)', p: 2, height: '100%' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Public sx={{ color: getHabitabilityColor(exoplanet.habitability_score), mr: 1 }} />
                    <Typography variant="subtitle1">Habitability</Typography>
                  </Box>
                  <Typography 
                    variant="h3" 
                    sx={{ 
                      color: getHabitabilityColor(exoplanet.habitability_score), 
                      fontWeight: 'bold',
                      mb: 1 
                    }}
                  >
                    {exoplanet.habitability_score.toFixed(0)}
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={exoplanet.habitability_score}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: getHabitabilityColor(exoplanet.habitability_score),
                        borderRadius: 4,
                      }
                    }}
                  />
                </Card>
              </motion.div>
            </Grid>

            {/* Planet Type */}
            <Grid item xs={12} sm={6}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4, duration: 0.5 }}
              >
                <Card sx={{ background: 'rgba(255, 255, 255, 0.05)', p: 2, height: '100%' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Straighten sx={{ color: '#00d4ff', mr: 1 }} />
                    <Typography variant="subtitle1">Planet Type</Typography>
                  </Box>
                  <Typography variant="h4" sx={{ color: '#00d4ff', fontWeight: 'bold', mb: 1 }}>
                    {getPlanetType(exoplanet.radius)}
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.8 }}>
                    {exoplanet.radius.toFixed(2)} Earth radii
                  </Typography>
                </Card>
              </motion.div>
            </Grid>
          </Grid>

          <Divider sx={{ my: 3, borderColor: 'rgba(0, 212, 255, 0.3)' }} />

          {/* Detailed Properties */}
          <Typography variant="h6" sx={{ mb: 2, color: '#00d4ff' }}>
            Physical & Orbital Characteristics
          </Typography>

          <Grid container spacing={2}>
            {/* Temperature */}
            <Grid item xs={12} sm={6}>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5, duration: 0.5 }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Thermostat sx={{ color: '#ff6b35', mr: 2 }} />
                  <Box>
                    <Typography variant="subtitle1">Temperature</Typography>
                    <Typography variant="h6" sx={{ color: '#ff6b35' }}>
                      {exoplanet.temperature.toFixed(0)} K
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.8 }}>
                      {getTemperatureDescription(exoplanet.temperature)}
                    </Typography>
                  </Box>
                </Box>
              </motion.div>
            </Grid>

            {/* Orbital Period */}
            <Grid item xs={12} sm={6}>
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6, duration: 0.5 }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <AccessTime sx={{ color: '#9c27b0', mr: 2 }} />
                  <Box>
                    <Typography variant="subtitle1">Orbital Period</Typography>
                    <Typography variant="h6" sx={{ color: '#9c27b0' }}>
                      {exoplanet.period.toFixed(1)} days
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.8 }}>
                      {(exoplanet.period / 365.25).toFixed(2)} Earth years
                    </Typography>
                  </Box>
                </Box>
              </motion.div>
            </Grid>

            {/* Star Temperature */}
            <Grid item xs={12} sm={6}>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.7, duration: 0.5 }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Star sx={{ color: '#ffaa00', mr: 2 }} />
                  <Box>
                    <Typography variant="subtitle1">Host Star</Typography>
                    <Typography variant="h6" sx={{ color: '#ffaa00' }}>
                      {exoplanet.star_temp.toFixed(0)} K
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.8 }}>
                      {exoplanet.star_radius.toFixed(2)} Solar radii
                    </Typography>
                  </Box>
                </Box>
              </motion.div>
            </Grid>

            {/* Location */}
            <Grid item xs={12} sm={6}>
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.8, duration: 0.5 }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <LocationOn sx={{ color: '#4caf50', mr: 2 }} />
                  <Box>
                    <Typography variant="subtitle1">Sky Position</Typography>
                    <Typography variant="body1" sx={{ color: '#4caf50' }}>
                      RA: {exoplanet.ra.toFixed(2)}°
                    </Typography>
                    <Typography variant="body1" sx={{ color: '#4caf50' }}>
                      Dec: {exoplanet.dec.toFixed(2)}°
                    </Typography>
                  </Box>
                </Box>
              </motion.div>
            </Grid>
          </Grid>

          {/* Discovery Information */}
          <Divider sx={{ my: 3, borderColor: 'rgba(0, 212, 255, 0.3)' }} />
          
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1, duration: 0.5 }}
          >
            <Typography variant="h6" sx={{ mb: 2, color: '#00d4ff' }}>
              Discovery Context
            </Typography>
            
            <Card sx={{ background: 'rgba(0, 212, 255, 0.1)', p: 2, border: '1px solid rgba(0, 212, 255, 0.3)' }}>
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Catalog ID:</strong> {exoplanet.kepoi_name}
              </Typography>
              {exoplanet.kepler_name && (
                <Typography variant="body1" sx={{ mb: 1 }}>
                  <strong>Kepler Name:</strong> {exoplanet.kepler_name}
                </Typography>
              )}
              <Typography variant="body1" sx={{ mb: 1 }}>
                <strong>Status:</strong> {exoplanet.disposition}
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8, mt: 2 }}>
                This object was identified by the Kepler Space Telescope using the transit method, 
                where periodic dimming of starlight indicates a possible planetary companion.
              </Typography>
            </Card>
          </motion.div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default ExoplanetInfo;
