import React from 'react';
import { SxProps, Theme } from '@mui/material/styles';
import {
  Box,
  Typography,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  Grid,
  Divider,
  IconButton
} from '@mui/material';
import { motion } from 'framer-motion';
import {
  CheckCircle,
  Warning,
  Cancel,
  Close,
  Thermostat,
  Public,
  Star,
  Psychology
} from '@mui/icons-material';

interface PredictionResult {
  prediction: string;
  confidence: number;
  habitability_score: number;
  planet_type: string;
  star_type: string;
  probabilities: Record<string, number>;
  status?: string;
}

interface PredictionDisplayProps {
  result: PredictionResult;
  onClose: () => void;
}

// ---------- Styles ----------
const headerBoxStyle: SxProps<Theme> = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  mb: 3,
};

const headerTitleStyle: SxProps<Theme> = {
  fontWeight: 'bold',
};

const dividerStyle: SxProps<Theme> = {
  my: 3,
  borderColor: 'rgba(0, 212, 255, 0.3)',
};

const flexCenterBox: SxProps<Theme> = {
  display: 'flex',
  alignItems: 'center',
  mb: 2,
};

const flexBetweenBox: SxProps<Theme> = {
  display: 'flex',
  justifyContent: 'space-between',
  mb: 1,
};

const cardTransparent: SxProps<Theme> = {
  background: 'rgba(255, 255, 255, 0.05)',
  p: 2,
};

const cardRecommendation: SxProps<Theme> = {
  background: 'rgba(0, 212, 255, 0.1)',
  p: 2,
  border: '1px solid rgba(0, 212, 255, 0.3)',
};

const probabilityBarStyle = (color: string): SxProps<Theme> => ({
  height: 8,
  borderRadius: 4,
  backgroundColor: 'rgba(255, 255, 255, 0.1)',
  '& .MuiLinearProgress-bar': {
    background: color,
    borderRadius: 4,
  },
});
// ----------------------------

const PredictionDisplay: React.FC<PredictionDisplayProps> = ({ result, onClose }) => {
  const getPredictionIcon = (prediction: string) => {
    switch (prediction) {
      case 'CONFIRMED':
        return <CheckCircle sx={{ color: '#4caf50' }} />;
      case 'CANDIDATE':
        return <Warning sx={{ color: '#ff9800' }} />;
      case 'FALSE POSITIVE':
        return <Cancel sx={{ color: '#f44336' }} />;
      default:
        return <Psychology sx={{ color: '#00d4ff' }} />;
    }
  };

  const getPredictionColor = (prediction: string) => {
    switch (prediction) {
      case 'CONFIRMED':
        return 'linear-gradient(45deg, #4caf50, #2e7d32)';
      case 'CANDIDATE':
        return 'linear-gradient(45deg, #ff9800, #f57c00)';
      case 'FALSE POSITIVE':
        return 'linear-gradient(45deg, #f44336, #d32f2f)';
      default:
        return 'linear-gradient(45deg, #00d4ff, #0093cc)';
    }
  };

  const getHabitabilityLevel = (score: number): { level: string; color: string } => {
    if (score >= 70) return { level: 'High', color: '#4caf50' };
    if (score >= 40) return { level: 'Medium', color: '#ff9800' };
    return { level: 'Low', color: '#f44336' };
  };

  const habitability = getHabitabilityLevel(result.habitability_score);

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
          <Box sx={headerBoxStyle}>
            <Typography variant="h5" className="glow-text" sx={headerTitleStyle}>
              AI PREDICTION RESULT
            </Typography>
            <IconButton onClick={onClose} sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
              <Close />
            </IconButton>
          </Box>

          {/* Main Prediction */}
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.6 }}
          >
            <Card
              sx={{
                background: getPredictionColor(result.prediction),
                mb: 3,
                p: 2,
                textAlign: 'center',
              }}
            >
              <Box sx={flexCenterBox}>
                {getPredictionIcon(result.prediction)}
                <Typography variant="h4" sx={{ ml: 2, fontWeight: 'bold', color: 'white' }}>
                  {result.prediction}
                </Typography>
              </Box>
              <Typography variant="h6" sx={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                Confidence: {(result.confidence * 100).toFixed(1)}%
              </Typography>
            </Card>
          </motion.div>

          {/* Probability Breakdown */}
          <Typography variant="h6" sx={{ mb: 2, color: '#00d4ff' }}>
            Classification Probabilities
          </Typography>

          {(Object.entries(result.probabilities) as [string, number][]).map(([category, probability], index) => (
            <motion.div
              key={category}
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 + index * 0.1, duration: 0.5 }}
            >
              <Box sx={{ mb: 2 }}>
                <Box sx={flexBetweenBox}>
                  <Typography variant="body1">{category}</Typography>
                  <Typography variant="body1">{(Number(probability) * 100).toFixed(1)}%</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={Number(probability) * 100}
                  sx={probabilityBarStyle(getPredictionColor(category))}
                />
              </Box>
            </motion.div>
          ))}

          <Divider sx={dividerStyle} />

          {/* Detailed Analysis */}
          <Typography variant="h6" sx={{ mb: 2, color: '#00d4ff' }}>
            Detailed Analysis
          </Typography>

          <Grid container spacing={2}>
            {/* Habitability */}
            <Grid item xs={12} sm={6}>
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6, duration: 0.5 }}>
                <Card sx={cardTransparent}>
                  <Box sx={flexCenterBox}>
                    <Public sx={{ color: habitability.color, mr: 1 }} />
                    <Typography variant="subtitle1">Habitability</Typography>
                  </Box>
                  <Typography variant="h4" sx={{ color: habitability.color, mb: 1 }}>
                    {result.habitability_score.toFixed(1)}
                  </Typography>
                  <Chip
                    label={`${habitability.level} Potential`}
                    sx={{
                      background: `linear-gradient(45deg, ${habitability.color}, ${habitability.color}aa)`,
                      color: 'white',
                      fontWeight: 600,
                    }}
                  />
                </Card>
              </motion.div>
            </Grid>

            {/* Planet Type */}
            <Grid item xs={12} sm={6}>
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.7, duration: 0.5 }}>
                <Card sx={cardTransparent}>
                  <Box sx={flexCenterBox}>
                    <Thermostat sx={{ color: '#ff6b35', mr: 1 }} />
                    <Typography variant="subtitle1">Planet Type</Typography>
                  </Box>
                  <Typography variant="h5" sx={{ color: '#ff6b35', mb: 1 }}>
                    {result.planet_type}
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.8 }}>
                    Classification based on radius
                  </Typography>
                </Card>
              </motion.div>
            </Grid>

            {/* Star Type */}
            <Grid item xs={12}>
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.8, duration: 0.5 }}>
                <Card sx={cardTransparent}>
                  <Box sx={flexCenterBox}>
                    <Star sx={{ color: '#ffaa00', mr: 1 }} />
                    <Typography variant="subtitle1">Host Star Classification</Typography>
                  </Box>
                  <Typography variant="h5" sx={{ color: '#ffaa00', mb: 1 }}>
                    {result.star_type}
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.8 }}>
                    Based on stellar effective temperature
                  </Typography>
                </Card>
              </motion.div>
            </Grid>
          </Grid>

          {/* Recommendations */}
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, color: '#00d4ff' }}>
              AI Recommendations
            </Typography>

            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1, duration: 0.5 }}>
              <Card sx={cardRecommendation}>
                <Typography variant="body1" sx={{ mb: 1 }}>
                  {result.prediction === 'CONFIRMED' &&
                    '🎉 This object shows strong evidence of being a genuine exoplanet! Consider it for follow-up observations.'}
                  {result.prediction === 'CANDIDATE' &&
                    '🔍 This object requires additional verification. Consider spectroscopic follow-up or extended monitoring.'}
                  {result.prediction === 'FALSE POSITIVE' &&
                    '⚠️ This signal is likely caused by stellar variability or instrumental effects rather than a planetary transit.'}
                </Typography>

                {result.habitability_score > 70 && (
                  <Typography variant="body2" sx={{ color: '#4caf50', mt: 1 }}>
                    ⭐ High habitability potential detected! This could be a prime target for atmospheric characterization.
                  </Typography>
                )}
              </Card>
            </motion.div>
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default PredictionDisplay;
