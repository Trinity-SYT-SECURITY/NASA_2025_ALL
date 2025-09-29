import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Slider,
  FormControlLabel,
  Switch,
  Divider,
  Chip
} from '@mui/material';
import { motion } from 'framer-motion';
import { Psychology, Rocket, Science } from '@mui/icons-material';

interface ExoplanetInputPanelProps {
  onPredict: (data: any) => void;
  isLoading: boolean;
}

const ExoplanetInputPanel: React.FC<ExoplanetInputPanelProps> = ({
  onPredict,
  isLoading
}) => {
  const [inputData, setInputData] = useState({
    koi_period: 10.0,
    koi_duration: 3.0,
    koi_depth: 1000,
    koi_prad: 1.5,
    koi_teq: 300,
    koi_insol: 1.0,
    koi_model_snr: 20,
    koi_steff: 5500,
    koi_slogg: 4.5,
    koi_srad: 1.0,
    koi_smass: 1.0,
    koi_kepmag: 14.0,
    ra: 290.0,
    dec: 45.0,
    koi_fpflag_nt: 0,
    koi_fpflag_ss: 0,
    koi_fpflag_co: 0,
    koi_fpflag_ec: 0,
    koi_score: 0.8,
  });

  const [useAdvanced, setUseAdvanced] = useState(false);

  const handleInputChange = (field: string) => (event: any) => {
    const value = event.target.value;
    setInputData(prev => ({
      ...prev,
      [field]: parseFloat(value) || 0
    }));
  };

  const handleSliderChange = (field: string) => (event: any, value: number | number[]) => {
    setInputData(prev => ({
      ...prev,
      [field]: value as number
    }));
  };

  const handlePredict = () => {
    onPredict(inputData);
  };

  const loadPreset = (preset: string) => {
    const presets: Record<string, any> = {
      'earth-like': {
        ...inputData,
        koi_period: 365,
        koi_prad: 1.0,
        koi_teq: 288,
        koi_insol: 1.0,
        koi_steff: 5778,
        koi_srad: 1.0,
      },
      'hot-jupiter': {
        ...inputData,
        koi_period: 3.5,
        koi_prad: 11.2,
        koi_teq: 1200,
        koi_insol: 100,
        koi_steff: 6000,
        koi_srad: 1.2,
      },
      'super-earth': {
        ...inputData,
        koi_period: 20,
        koi_prad: 1.8,
        koi_teq: 400,
        koi_insol: 2.5,
        koi_steff: 4500,
        koi_srad: 0.8,
      }
    };
    setInputData(presets[preset]);
  };

  return (
    <Card className="holo-panel">
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <Psychology sx={{ mr: 2, color: '#00d4ff' }} />
          <Typography variant="h6" className="glow-text">
            AI EXOPLANET ANALYZER
          </Typography>
        </Box>

        {/* Preset Buttons */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" sx={{ mb: 1, opacity: 0.8 }}>
            Quick Presets:
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Chip
              label="Earth-like"
              onClick={() => loadPreset('earth-like')}
              sx={{ background: 'linear-gradient(45deg, #4caf50, #2e7d32)' }}
            />
            <Chip
              label="Hot Jupiter"
              onClick={() => loadPreset('hot-jupiter')}
              sx={{ background: 'linear-gradient(45deg, #ff5722, #d84315)' }}
            />
            <Chip
              label="Super Earth"
              onClick={() => loadPreset('super-earth')}
              sx={{ background: 'linear-gradient(45deg, #2196f3, #1565c0)' }}
            />
          </Box>
        </Box>

        <Divider sx={{ my: 2, borderColor: 'rgba(0, 212, 255, 0.3)' }} />

        {/* Basic Parameters */}
        <Typography variant="subtitle1" sx={{ mb: 2, color: '#00d4ff' }}>
          <Science sx={{ mr: 1, verticalAlign: 'middle' }} />
          Planetary Parameters
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Orbital Period (days)"
              type="number"
              value={inputData.koi_period}
              onChange={handleInputChange('koi_period')}
              variant="outlined"
              InputProps={{
                style: { color: 'white' }
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: 'rgba(0, 212, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(0, 212, 255, 0.6)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#00d4ff',
                  },
                },
                '& .MuiInputLabel-root': {
                  color: 'rgba(255, 255, 255, 0.7)',
                },
              }}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Planet Radius (Earth radii)"
              type="number"
              value={inputData.koi_prad}
              onChange={handleInputChange('koi_prad')}
              variant="outlined"
              InputProps={{
                style: { color: 'white' }
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: 'rgba(0, 212, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(0, 212, 255, 0.6)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#00d4ff',
                  },
                },
                '& .MuiInputLabel-root': {
                  color: 'rgba(255, 255, 255, 0.7)',
                },
              }}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Equilibrium Temperature (K)"
              type="number"
              value={inputData.koi_teq}
              onChange={handleInputChange('koi_teq')}
              variant="outlined"
              InputProps={{
                style: { color: 'white' }
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: 'rgba(0, 212, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(0, 212, 255, 0.6)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#00d4ff',
                  },
                },
                '& .MuiInputLabel-root': {
                  color: 'rgba(255, 255, 255, 0.7)',
                },
              }}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Stellar Temperature (K)"
              type="number"
              value={inputData.koi_steff}
              onChange={handleInputChange('koi_steff')}
              variant="outlined"
              InputProps={{
                style: { color: 'white' }
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: 'rgba(0, 212, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(0, 212, 255, 0.6)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#00d4ff',
                  },
                },
                '& .MuiInputLabel-root': {
                  color: 'rgba(255, 255, 255, 0.7)',
                },
              }}
            />
          </Grid>
        </Grid>

        {/* Sliders for intuitive input */}
        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle2" sx={{ mb: 2 }}>
            Insolation Flux (Earth = 1.0):
          </Typography>
          <Slider
            value={inputData.koi_insol}
            onChange={handleSliderChange('koi_insol')}
            min={0.1}
            max={10}
            step={0.1}
            marks={[
              { value: 0.25, label: 'Cold' },
              { value: 1.0, label: 'Earth' },
              { value: 1.5, label: 'Hot' },
            ]}
            sx={{
              color: '#00d4ff',
              '& .MuiSlider-thumb': {
                background: 'linear-gradient(45deg, #00d4ff, #ff6b35)',
              },
              '& .MuiSlider-track': {
                background: 'linear-gradient(90deg, #00d4ff, #ff6b35)',
              },
            }}
          />
        </Box>

        {/* Advanced Options */}
        <FormControlLabel
          control={
            <Switch
              checked={useAdvanced}
              onChange={(e) => setUseAdvanced(e.target.checked)}
              sx={{
                '& .MuiSwitch-switchBase.Mui-checked': {
                  color: '#00d4ff',
                },
                '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
                  backgroundColor: '#00d4ff',
                },
              }}
            />
          }
          label="Advanced Parameters"
          sx={{ mt: 2, color: 'rgba(255, 255, 255, 0.8)' }}
        />

        {useAdvanced && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Transit Duration (hrs)"
                  type="number"
                  value={inputData.koi_duration}
                  onChange={handleInputChange('koi_duration')}
                  variant="outlined"
                  size="small"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Transit Depth (ppm)"
                  type="number"
                  value={inputData.koi_depth}
                  onChange={handleInputChange('koi_depth')}
                  variant="outlined"
                  size="small"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Signal-to-Noise Ratio"
                  type="number"
                  value={inputData.koi_model_snr}
                  onChange={handleInputChange('koi_model_snr')}
                  variant="outlined"
                  size="small"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Kepler Magnitude"
                  type="number"
                  value={inputData.koi_kepmag}
                  onChange={handleInputChange('koi_kepmag')}
                  variant="outlined"
                  size="small"
                />
              </Grid>
            </Grid>
          </motion.div>
        )}

        {/* Predict Button */}
        <Button
          fullWidth
          variant="contained"
          size="large"
          onClick={handlePredict}
          disabled={isLoading}
          startIcon={<Rocket />}
          className="cosmic-button"
          sx={{
            mt: 3,
            py: 2,
            background: 'linear-gradient(45deg, #00d4ff, #ff6b35)',
            '&:hover': {
              background: 'linear-gradient(45deg, #66e3ff, #ff9566)',
              transform: 'translateY(-2px)',
            },
            '&:disabled': {
              background: 'rgba(255, 255, 255, 0.1)',
            },
          }}
        >
          {isLoading ? 'ANALYZING...' : 'DISCOVER EXOPLANET'}
        </Button>
      </CardContent>
    </Card>
  );
};

export default ExoplanetInputPanel;
