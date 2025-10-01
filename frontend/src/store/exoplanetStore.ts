import { create } from 'zustand';
import axios from 'axios';

// 從環境變數或默認值獲取後端 URL
const getApiBaseUrl = () => {
  // 嘗試從環境變數獲取
  if (typeof process !== 'undefined' && process.env) {
    if (process.env.REACT_APP_API_URL) return process.env.REACT_APP_API_URL;
  }

  // 默認使用 Render 後端
  return 'https://test-backend-2-ikqg.onrender.com';
};

const API_BASE_URL = getApiBaseUrl();

interface ExoplanetData {
  kepoi_name: string;
  kepler_name?: string;
  disposition: string;
  period: number;
  radius: number;
  temperature: number;
  star_temp: number;
  star_radius: number;
  ra: number;
  dec: number;
  habitability_score: number;
}

interface PredictionInput {
  koi_period: number;
  koi_duration: number;
  koi_depth: number;
  koi_prad: number;
  koi_teq: number;
  koi_insol: number;
  koi_model_snr: number;
  koi_steff: number;
  koi_slogg: number;
  koi_srad: number;
  koi_smass?: number;
  koi_kepmag: number;
  koi_fpflag_nt?: number;
  koi_fpflag_ss?: number;
  koi_fpflag_co?: number;
  koi_fpflag_ec?: number;
  ra: number;
  dec: number;
  koi_score?: number;
}

interface PredictionResult {
  prediction: string;
  probabilities: Record<string, number>;
  confidence: number;
  habitability_score: number;
  planet_type: string;
  star_type: string;
}

interface Filters {
  disposition?: string;
  min_habitability?: number;
  min_radius?: number;
  max_radius?: number;
  min_temperature?: number;
  max_temperature?: number;
  limit: number;
}

interface Stats {
  total_exoplanets: number;
  confirmed: number;
  candidates: number;
  potentially_habitable: number;
  averages: {
    radius: number;
    temperature: number;
    period: number;
  };
  habitability_distribution: {
    high: number;
    medium: number;
    low: number;
  };
}

interface ExoplanetStore {
  // State
  exoplanets: ExoplanetData[];
  filteredExoplanets: ExoplanetData[];
  stats: Stats | null;
  filters: Filters;
  loading: boolean;
  error: string | null;

  // Actions
  fetchExoplanets: () => Promise<void>;
  updateFilters: (newFilters: Partial<Filters>) => void;
  predictExoplanet: (input: PredictionInput) => Promise<PredictionResult>;
  fetchStats: () => Promise<void>;
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
}

export const useExoplanetStore = create<ExoplanetStore>((set, get) => ({
  // Initial state
  exoplanets: [],
  filteredExoplanets: [],
  stats: null,
  filters: {
    limit: 1000,
  },
  loading: false,
  error: null,

  // Actions
  fetchExoplanets: async () => {
    const { filters } = get();
    set({ loading: true, error: null });

    try {
      const params = new URLSearchParams();
      if (filters.disposition) params.append('disposition', filters.disposition);
      if (filters.min_habitability !== undefined) params.append('min_habitability', filters.min_habitability.toString());
      params.append('limit', filters.limit.toString());

      const response = await axios.get(`${API_BASE_URL}/exoplanets?${params}`);
      const exoplanets = response.data.exoplanets;

      // Apply additional client-side filters
      let filtered = exoplanets;
      
      if (filters.min_radius !== undefined) {
        filtered = filtered.filter((p: ExoplanetData) => p.radius >= filters.min_radius!);
      }
      
      if (filters.max_radius !== undefined) {
        filtered = filtered.filter((p: ExoplanetData) => p.radius <= filters.max_radius!);
      }
      
      if (filters.min_temperature !== undefined) {
        filtered = filtered.filter((p: ExoplanetData) => p.temperature >= filters.min_temperature!);
      }
      
      if (filters.max_temperature !== undefined) {
        filtered = filtered.filter((p: ExoplanetData) => p.temperature <= filters.max_temperature!);
      }

      set({ 
        exoplanets,
        filteredExoplanets: filtered,
        loading: false 
      });

      // Also fetch stats
      get().fetchStats();

    } catch (error) {
      console.error('Failed to fetch exoplanets:', error);
      set({ 
        error: 'Failed to load exoplanet data. Using demo data.',
        loading: false,
        exoplanets: generateDemoData(),
        filteredExoplanets: generateDemoData()
      });
    }
  },

  updateFilters: (newFilters) => {
    const currentFilters = get().filters;
    const updatedFilters = { ...currentFilters, ...newFilters };
    set({ filters: updatedFilters });
    
    // Refetch data with new filters
    get().fetchExoplanets();
  },

  predictExoplanet: async (input: PredictionInput): Promise<PredictionResult> => {
    set({ loading: true, error: null });

    try {
      const response = await axios.post(`${API_BASE_URL}/predict`, input);
      set({ loading: false });
      return response.data;
    } catch (error) {
      console.error('Prediction failed:', error);
      set({ 
        error: 'AI prediction service unavailable. Using demo prediction.',
        loading: false 
      });
      
      // Return demo prediction
      return {
        prediction: 'CANDIDATE',
        probabilities: {
          'CANDIDATE': 0.65,
          'CONFIRMED': 0.25,
          'FALSE POSITIVE': 0.10
        },
        confidence: 0.65,
        habitability_score: Math.random() * 100,
        planet_type: input.koi_prad < 1.25 ? 'Earth-like' : 'Super-Earth',
        star_type: input.koi_steff < 5200 ? 'K-dwarf' : 'G-dwarf'
      };
    }
  },

  fetchStats: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/stats`);
      set({ stats: response.data });
    } catch (error) {
      console.error('Failed to fetch stats:', error);
      // Set demo stats
      set({
        stats: {
          total_exoplanets: 5000,
          confirmed: 2500,
          candidates: 2000,
          potentially_habitable: 500,
          averages: {
            radius: 2.1,
            temperature: 800,
            period: 50
          },
          habitability_distribution: {
            high: 100,
            medium: 400,
            low: 4500
          }
        }
      });
    }
  },

  setError: (error) => set({ error }),
  setLoading: (loading) => set({ loading }),
}));

// Demo data generator for offline mode
function generateDemoData(): ExoplanetData[] {
  const demoData: ExoplanetData[] = [];
  
  for (let i = 0; i < 100; i++) {
    const radius = Math.random() * 10 + 0.5;
    const temperature = Math.random() * 2000 + 200;
    const period = Math.random() * 500 + 1;
    const habitability = calculateHabitability(radius, temperature);
    
    demoData.push({
      kepoi_name: `K${String(i + 1000).padStart(5, '0')}.01`,
      kepler_name: Math.random() > 0.5 ? `Kepler-${i + 100} b` : undefined,
      disposition: Math.random() > 0.3 ? (Math.random() > 0.5 ? 'CONFIRMED' : 'CANDIDATE') : 'FALSE POSITIVE',
      period,
      radius,
      temperature,
      star_temp: Math.random() * 3000 + 3000,
      star_radius: Math.random() * 2 + 0.5,
      ra: Math.random() * 360,
      dec: (Math.random() - 0.5) * 180,
      habitability_score: habitability
    });
  }
  
  return demoData;
}

function calculateHabitability(radius: number, temperature: number): number {
  let score = 0;
  
  // Temperature score (0-40)
  if (temperature >= 273 && temperature <= 373) {
    score += 40;
  } else if (temperature >= 200 && temperature <= 400) {
    score += 20;
  }
  
  // Size score (0-30)
  if (radius >= 0.8 && radius <= 1.5) {
    score += 30;
  } else if (radius >= 0.5 && radius <= 2.0) {
    score += 15;
  }
  
  // Random factors (0-30)
  score += Math.random() * 30;
  
  return Math.min(score, 100);
}
