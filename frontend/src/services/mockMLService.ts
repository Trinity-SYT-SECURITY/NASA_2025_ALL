// Mock ML Service - Simulates real ML predictions based on trained model patterns
export class MockMLService {
  // Simulate ML prediction results based on trained model patterns
  static async predict(params: any) {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 800));

    const { koi_prad, koi_teq, koi_steff, koi_insol } = params;

    // Feature engineering (matching the trained model's preprocessing)
    // Feature engineering removed - using direct parameter analysis instead

    // Simulate ML model prediction based on feature patterns
    // This mimics the behavior of a trained XGBoost model
    let prediction = 'CANDIDATE';
    let confidence = 0.78;

    // Simulate the decision tree logic from the trained model
    if (koi_teq >= 200 && koi_teq <= 300 && koi_prad >= 0.8 && koi_prad <= 1.5) {
      // Earth-like conditions - high confidence CONFIRMED
      prediction = 'CONFIRMED';
      confidence = 0.85 + (Math.random() * 0.1); // 0.85-0.95
    } else if (koi_prad > 2.0 || koi_teq > 1000 || koi_insol < 0.1) {
      // Extreme conditions - likely FALSE POSITIVE
      prediction = 'FALSE POSITIVE';
      confidence = 0.65 + (Math.random() * 0.15); // 0.65-0.80
    } else {
      // Moderate conditions - CANDIDATE
      prediction = 'CANDIDATE';
      confidence = 0.75 + (Math.random() * 0.15); // 0.75-0.90
    }

    // Calculate habitability score based on multiple factors
    let habitabilityScore = 0;
    if (koi_teq >= 200 && koi_teq <= 300) habitabilityScore += 40;
    if (koi_prad >= 0.8 && koi_prad <= 1.5) habitabilityScore += 30;
    if (koi_insol >= 0.25 && koi_insol <= 1.5) habitabilityScore += 30;

    // Add some variability based on other factors
    const variability = (Math.random() - 0.5) * 10; // ±5 points
    habitabilityScore = Math.max(0, Math.min(100, habitabilityScore + variability));

    return {
      prediction,
      confidence,
      habitability_score: habitabilityScore,
      planet_type: this.getPlanetType(koi_prad),
      planet_name: this.getPlanetName(params),
      star_type: this.getStarType(koi_steff),
      probabilities: {
        'CONFIRMED': prediction === 'CONFIRMED' ? confidence : (1 - confidence) * 0.4,
        'CANDIDATE': prediction === 'CANDIDATE' ? confidence : (1 - confidence) * 0.4,
        'FALSE POSITIVE': prediction === 'FALSE POSITIVE' ? confidence : (1 - confidence) * 0.2
      }
    };
  }

  private static getPlanetName(params: any): string {
    const { koi_prad, koi_teq } = params;

    // 基於參數和預測結果生成真實的開普勒行星名稱
    let planetName = "Unknown Exoplanet";

    // 根據特徵組合映射到真實的開普勒行星
    if (koi_teq >= 200 && koi_teq <= 300 && koi_prad >= 0.8 && koi_prad <= 1.5) {
      // 類似地球的行星
      const earthLikePlanets = [
        "Kepler-442 b", "Kepler-186 f", "Kepler-452 b", "Kepler-62 f",
        "Kepler-283 c", "Kepler-296 f", "Kepler-438 b", "Kepler-440 b"
      ];
      planetName = earthLikePlanets[Math.floor(Math.random() * earthLikePlanets.length)];
    } else if (koi_prad > 1.5 && koi_prad <= 3.0) {
      // 超級地球
      const superEarthPlanets = [
        "Kepler-22 b", "Kepler-69 c", "Kepler-62 e", "Kepler-61 b",
        "Kepler-102 e", "Kepler-107 c", "Kepler-108 c", "Kepler-122 e"
      ];
      planetName = superEarthPlanets[Math.floor(Math.random() * superEarthPlanets.length)];
    } else if (koi_prad > 3.0 && koi_prad <= 6.0) {
      // 海王星類
      const neptuneLikePlanets = [
        "Kepler-10 c", "Kepler-18 d", "Kepler-51 d", "Kepler-68 d",
        "Kepler-419 b", "Kepler-420 b", "Kepler-421 b", "Kepler-422 b"
      ];
      planetName = neptuneLikePlanets[Math.floor(Math.random() * neptuneLikePlanets.length)];
    } else if (koi_prad > 6.0) {
      // 氣態巨行星
      const gasGiantPlanets = [
        "Kepler-7 b", "Kepler-8 b", "Kepler-12 b", "Kepler-13 b",
        "Kepler-14 b", "Kepler-15 b", "Kepler-16 b", "Kepler-17 b"
      ];
      planetName = gasGiantPlanets[Math.floor(Math.random() * gasGiantPlanets.length)];
    } else if (koi_teq > 1000) {
      // 熱行星
      const hotPlanets = [
        "Kepler-10 b", "Kepler-78 b", "Kepler-406 b", "Kepler-412 b",
        "Kepler-41 b", "Kepler-43 b", "Kepler-44 b", "Kepler-45 b"
      ];
      planetName = hotPlanets[Math.floor(Math.random() * hotPlanets.length)];
    } else {
      // 其他情況
      const otherPlanets = [
        "Kepler-227 b", "Kepler-227 c", "Kepler-23 b", "Kepler-24 b",
        "Kepler-25 b", "Kepler-26 b", "Kepler-27 b", "Kepler-28 b"
      ];
      planetName = otherPlanets[Math.floor(Math.random() * otherPlanets.length)];
    }

    return planetName;
  }

  private static getPlanetType(radius: number): string {
    if (radius < 0.8) return 'Sub-Earth';
    if (radius <= 1.25) return 'Earth-like';
    if (radius <= 2.0) return 'Super-Earth';
    if (radius <= 3.9) return 'Neptune-like';
    return 'Gas Giant';
  }

  private static getStarType(temp: number): string {
    if (temp >= 7500) return 'A-type (Blue-White)';
    if (temp >= 6000) return 'F-type (White)';
    if (temp >= 5200) return 'G-dwarf (Yellow)';
    if (temp >= 3700) return 'K-dwarf (Orange)';
    return 'M-dwarf (Red)';
  }
}
