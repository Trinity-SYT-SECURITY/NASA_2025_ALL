import React from 'react';
import {
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
  Card,
  CardContent,
  Switch,
  FormControlLabel,
  Divider
} from '@mui/material';
import { motion } from 'framer-motion';
import { Tune, FilterAlt, Visibility } from '@mui/icons-material';

interface ControlPanelProps {
  filters: any;
  onFiltersChange: (filters: any) => void;
}

const ControlPanel: React.FC<ControlPanelProps> = ({ filters, onFiltersChange }) => {
  const handleFilterChange = (field: string) => (event: any) => {
    onFiltersChange({
      [field]: event.target.value
    });
  };

  const handleSliderChange = (field: string) => (event: any, value: number | number[]) => {
    onFiltersChange({
      [field]: value
    });
  };

  return (
    <Card className="holo-panel">
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <Tune sx={{ mr: 2, color: '#00d4ff' }} />
          <Typography variant="h6" className="glow-text">
            VISUALIZATION CONTROLS
          </Typography>
        </Box>

        {/* Disposition Filter */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
        >
          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel 
              sx={{ 
                color: 'rgba(255, 255, 255, 0.7)',
                '&.Mui-focused': { color: '#00d4ff' }
              }}
            >
              Disposition Filter
            </InputLabel>
            <Select
              value={filters.disposition || ''}
              onChange={handleFilterChange('disposition')}
              sx={{
                color: 'white',
                '& .MuiOutlinedInput-notchedOutline': {
                  borderColor: 'rgba(0, 212, 255, 0.3)',
                },
                '&:hover .MuiOutlinedInput-notchedOutline': {
                  borderColor: 'rgba(0, 212, 255, 0.6)',
                },
                '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                  borderColor: '#00d4ff',
                },
                '& .MuiSvgIcon-root': {
                  color: 'rgba(255, 255, 255, 0.7)',
                },
              }}
            >
              <MenuItem value="">All Objects</MenuItem>
              <MenuItem value="CONFIRMED">Confirmed Exoplanets</MenuItem>
              <MenuItem value="CANDIDATE">Candidate Objects</MenuItem>
              <MenuItem value="FALSE POSITIVE">False Positives</MenuItem>
            </Select>
          </FormControl>
        </motion.div>

        {/* Habitability Filter */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
        >
          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle1" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
              <FilterAlt sx={{ mr: 1, color: '#4caf50' }} />
              Minimum Habitability Score: {filters.min_habitability || 0}
            </Typography>
            <Slider
              value={filters.min_habitability || 0}
              onChange={handleSliderChange('min_habitability')}
              min={0}
              max={100}
              step={5}
              marks={[
                { value: 0, label: '0' },
                { value: 40, label: 'Medium' },
                { value: 70, label: 'High' },
                { value: 100, label: '100' },
              ]}
              sx={{
                color: '#4caf50',
                '& .MuiSlider-thumb': {
                  background: 'linear-gradient(45deg, #4caf50, #2e7d32)',
                  boxShadow: '0 0 10px rgba(76, 175, 80, 0.5)',
                },
                '& .MuiSlider-track': {
                  background: 'linear-gradient(90deg, #4caf50, #2e7d32)',
                },
                '& .MuiSlider-rail': {
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                },
                '& .MuiSlider-mark': {
                  backgroundColor: 'rgba(255, 255, 255, 0.3)',
                },
                '& .MuiSlider-markLabel': {
                  color: 'rgba(255, 255, 255, 0.7)',
                  fontSize: '0.75rem',
                },
              }}
            />
          </Box>
        </motion.div>

        <Divider sx={{ my: 2, borderColor: 'rgba(0, 212, 255, 0.3)' }} />

        {/* Size Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
        >
          <Typography variant="subtitle1" sx={{ mb: 2, color: '#00d4ff' }}>
            Planet Size Range (Earth Radii)
          </Typography>
          
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" sx={{ mb: 1 }}>
              Minimum Radius: {filters.min_radius || 0.1}
            </Typography>
            <Slider
              value={filters.min_radius || 0.1}
              onChange={handleSliderChange('min_radius')}
              min={0.1}
              max={20}
              step={0.1}
              sx={{
                color: '#00d4ff',
                '& .MuiSlider-thumb': {
                  background: 'linear-gradient(45deg, #00d4ff, #0093cc)',
                },
                '& .MuiSlider-track': {
                  background: 'linear-gradient(90deg, #00d4ff, #0093cc)',
                },
              }}
            />
          </Box>

          <Box sx={{ mb: 3 }}>
            <Typography variant="body2" sx={{ mb: 1 }}>
              Maximum Radius: {filters.max_radius || 20}
            </Typography>
            <Slider
              value={filters.max_radius || 20}
              onChange={handleSliderChange('max_radius')}
              min={0.1}
              max={20}
              step={0.1}
              sx={{
                color: '#ff6b35',
                '& .MuiSlider-thumb': {
                  background: 'linear-gradient(45deg, #ff6b35, #cc4a24)',
                },
                '& .MuiSlider-track': {
                  background: 'linear-gradient(90deg, #ff6b35, #cc4a24)',
                },
              }}
            />
          </Box>
        </motion.div>

        <Divider sx={{ my: 2, borderColor: 'rgba(0, 212, 255, 0.3)' }} />

        {/* Temperature Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
        >
          <Typography variant="subtitle1" sx={{ mb: 2, color: '#ff6b35' }}>
            Temperature Range (Kelvin)
          </Typography>
          
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" sx={{ mb: 1 }}>
              Minimum Temperature: {filters.min_temperature || 100}K
            </Typography>
            <Slider
              value={filters.min_temperature || 100}
              onChange={handleSliderChange('min_temperature')}
              min={100}
              max={3000}
              step={10}
              marks={[
                { value: 273, label: 'Ice' },
                { value: 373, label: 'Water' },
                { value: 1000, label: 'Hot' },
              ]}
              sx={{
                color: '#2196f3',
                '& .MuiSlider-thumb': {
                  background: 'linear-gradient(45deg, #2196f3, #1565c0)',
                },
                '& .MuiSlider-track': {
                  background: 'linear-gradient(90deg, #2196f3, #1565c0)',
                },
              }}
            />
          </Box>

          <Box sx={{ mb: 3 }}>
            <Typography variant="body2" sx={{ mb: 1 }}>
              Maximum Temperature: {filters.max_temperature || 3000}K
            </Typography>
            <Slider
              value={filters.max_temperature || 3000}
              onChange={handleSliderChange('max_temperature')}
              min={100}
              max={3000}
              step={10}
              sx={{
                color: '#f44336',
                '& .MuiSlider-thumb': {
                  background: 'linear-gradient(45deg, #f44336, #d32f2f)',
                },
                '& .MuiSlider-track': {
                  background: 'linear-gradient(90deg, #f44336, #d32f2f)',
                },
              }}
            />
          </Box>
        </motion.div>

        <Divider sx={{ my: 2, borderColor: 'rgba(0, 212, 255, 0.3)' }} />

        {/* Display Options */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
        >
          <Typography variant="subtitle1" sx={{ mb: 2, color: '#9c27b0', display: 'flex', alignItems: 'center' }}>
            <Visibility sx={{ mr: 1 }} />
            Display Options
          </Typography>

          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" sx={{ mb: 1 }}>
              Maximum Objects: {filters.limit || 1000}
            </Typography>
            <Slider
              value={filters.limit || 1000}
              onChange={handleSliderChange('limit')}
              min={100}
              max={2000}
              step={100}
              marks={[
                { value: 100, label: '100' },
                { value: 500, label: '500' },
                { value: 1000, label: '1K' },
                { value: 2000, label: '2K' },
              ]}
              sx={{
                color: '#9c27b0',
                '& .MuiSlider-thumb': {
                  background: 'linear-gradient(45deg, #9c27b0, #7b1fa2)',
                },
                '& .MuiSlider-track': {
                  background: 'linear-gradient(90deg, #9c27b0, #7b1fa2)',
                },
              }}
            />
          </Box>
        </motion.div>

        {/* Performance Note */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.5 }}
        >
          <Card sx={{ background: 'rgba(255, 193, 7, 0.1)', p: 2, border: '1px solid rgba(255, 193, 7, 0.3)' }}>
            <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
              💡 <strong>Tip:</strong> Lower object limits improve 3D performance. 
              Use filters to focus on specific types of exoplanets for better visualization.
            </Typography>
          </Card>
        </motion.div>
      </CardContent>
    </Card>
  );
};

export default ControlPanel;
