// Mock ML Service - 替代方案：使用雲端ML API
export class MockMLService {
  // 模擬ML預測結果
  static async predict(params: any) {
    // 模擬延遲
    await new Promise(resolve => setTimeout(resolve, 1000));

    // 基於輸入參數生成預測結果
    const { koi_period, koi_prad, koi_teq, koi_steff, koi_insol } = params;

    // 簡單的規則-based預測（實際應該使用真實ML模型）
    let prediction = 'CANDIDATE';
    let confidence = 0.78;

    // 基於參數的特徵工程
    const features = [
      koi_period / 1000,  // 標準化軌道周期
      koi_prad,           // 行星半徑
      koi_teq / 300,      // 標準化溫度
      koi_steff / 6000,   // 恆星溫度標準化
      koi_insol,          // 絕緣值
      1,                  // 恆星表面重力（默認）
      1,                  // 恆星半徑（默認）
      1,                  // 恆星質量（默認）
      12,                 // 視星等（默認）
      0, 0, 0, 0,         // 標誌位（默認）
      290, 45,            // 坐標（默認）
      1,                  // 適居帶（默認）
      0.5                 // 得分（默認）
    ];

    // 簡單的啟發式規則
    if (koi_teq >= 200 && koi_teq <= 300 && koi_prad >= 0.8 && koi_prad <= 1.5) {
      prediction = 'CONFIRMED';
      confidence = 0.85;
    } else if (koi_prad > 2.0 || koi_teq > 1000) {
      prediction = 'FALSE POSITIVE';
      confidence = 0.65;
    }

    // 計算適居性分數
    let habitabilityScore = 0;
    if (koi_teq >= 200 && koi_teq <= 300) habitabilityScore += 40;
    if (koi_prad >= 0.8 && koi_prad <= 1.5) habitabilityScore += 30;
    if (koi_insol >= 0.25 && koi_insol <= 1.5) habitabilityScore += 30;

    return {
      prediction,
      confidence,
      habitability_score: habitabilityScore,
      planet_type: this.getPlanetType(koi_prad),
      star_type: this.getStarType(koi_steff),
      probabilities: {
        'CONFIRMED': prediction === 'CONFIRMED' ? confidence : (1 - confidence) / 2,
        'CANDIDATE': prediction === 'CANDIDATE' ? confidence : (1 - confidence) / 2,
        'FALSE POSITIVE': prediction === 'FALSE POSITIVE' ? confidence : (1 - confidence) / 2
      },
      status: 'mock_prediction'
    };
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
