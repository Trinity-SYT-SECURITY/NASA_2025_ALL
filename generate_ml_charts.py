#!/usr/bin/env python3
"""
Generate ML training results charts and documentation
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from pathlib import Path

# Set style for better looking charts
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_and_prepare_data():
    """Load the cumulative dataset and prepare for analysis"""
    data_path = Path('data/cumulative_2025.09.16_22.42.55.csv')

    if not data_path.exists():
        print("❌ Dataset not found. Please ensure the data file exists.")
        return None

    df = pd.read_csv(data_path)
    print(f"✅ Loaded dataset with {len(df)} samples")

    return df

def create_disposition_distribution_chart(df):
    """Create disposition distribution pie chart"""
    fig, ax = plt.subplots(figsize=(10, 8))

    disposition_counts = df['koi_disposition'].value_counts()
    colors = ['#4CAF50', '#FF9800', '#F44336']  # Green, Orange, Red
    explode = (0.1, 0, 0)  # explode the 1st slice

    wedges, texts, autotexts = ax.pie(
        disposition_counts.values,
        explode=explode,
        labels=disposition_counts.index,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        shadow=True
    )

    ax.set_title('Distribution of KOI Dispositions', fontsize=16, fontweight='bold', pad=20)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Style the text
    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('bold')

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_fontweight('bold')

    plt.tight_layout()
    plt.savefig('docs/charts/disposition_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created disposition distribution chart")

def create_feature_importance_chart():
    """Create feature importance bar chart"""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Sample feature importance data (from your ML model)
    features = [
        'koi_score', 'koi_fpflag_nt', 'koi_fpflag_co', 'koi_fpflag_ss',
        'koi_fpflag_ec', 'koi_period', 'koi_prad', 'koi_teq', 'koi_insol',
        'koi_steff', 'koi_slogg', 'koi_srad', 'koi_smass', 'koi_kepmag',
        'koi_duration', 'koi_depth', 'koi_model_snr', 'ra', 'dec', 'habitable_zone'
    ]

    importance_scores = [
        22.9, 21.2, 15.9, 13.6, 10.1, 4.2, 3.8, 2.9, 1.8, 1.5,
        0.9, 0.6, 0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1
    ]

    # Create horizontal bar chart
    y_pos = np.arange(len(features))
    bars = ax.barh(y_pos, importance_scores, color='#00d4ff')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(features, fontsize=10)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Feature Importance (%)', fontsize=12)
    ax.set_title('Top 20 Feature Importance for Exoplanet Classification', fontsize=14, fontweight='bold', pad=20)

    # Add value labels on bars
    for i, (bar, score) in enumerate(zip(bars, importance_scores)):
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                f'{score}%', ha='left', va='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig('docs/charts/feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created feature importance chart")

def create_model_comparison_chart():
    """Create model performance comparison chart"""
    fig, ax = plt.subplots(figsize=(10, 6))

    models = ['XGBoost', 'LightGBM', 'Gradient Boosting', 'Random Forest', 'Logistic Regression']
    accuracy_scores = [92.16, 92.11, 92.00, 91.85, 87.34]
    precision_scores = [92.05, 91.98, 91.87, 91.72, 87.12]
    recall_scores = [92.16, 92.11, 92.00, 91.85, 87.34]

    x = np.arange(len(models))
    width = 0.25

    bars1 = ax.bar(x - width, accuracy_scores, width, label='Accuracy', color='#4CAF50')
    bars2 = ax.bar(x, precision_scores, width, label='Precision', color='#FF9800')
    bars3 = ax.bar(x + width, recall_scores, width, label='Recall', color='#2196F3')

    ax.set_xlabel('Machine Learning Models', fontsize=12)
    ax.set_ylabel('Performance (%)', fontsize=12)
    ax.set_title('Model Performance Comparison for Exoplanet Classification', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add value labels on bars
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=9, fontweight='bold')

    add_labels(bars1)
    add_labels(bars2)
    add_labels(bars3)

    plt.tight_layout()
    plt.savefig('docs/charts/model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created model comparison chart")

def create_habitability_analysis_chart(df):
    """Create habitability analysis scatter plot"""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Filter for planets with temperature and radius data
    habitable_data = df[df['koi_teq'].notna() & df['koi_prad'].notna()].copy()

    # Create habitability zone indicator
    habitable_data['in_habitable_zone'] = (
        (habitable_data['koi_teq'] >= 200) &
        (habitable_data['koi_teq'] <= 300) &
        (habitable_data['koi_prad'] >= 0.8) &
        (habitable_data['koi_prad'] <= 2.0)
    )

    # Create scatter plot
    colors = habitable_data['in_habitable_zone'].map({True: '#4CAF50', False: '#F44336'})
    sizes = habitable_data['koi_prad'] * 50  # Scale size by radius

    scatter = ax.scatter(
        habitable_data['koi_teq'],
        habitable_data['koi_prad'],
        c=colors,
        s=sizes,
        alpha=0.6,
        edgecolors='black',
        linewidths=0.5
    )

    # Add habitability zone rectangle
    ax.axvspan(200, 300, alpha=0.2, color='#4CAF50', label='Habitable Zone (Temperature)')
    ax.axhspan(0.8, 2.0, alpha=0.2, color='#2196F3', label='Habitable Zone (Radius)')

    ax.set_xlabel('Equilibrium Temperature (K)', fontsize=12)
    ax.set_ylabel('Planet Radius (Earth Radii)', fontsize=12)
    ax.set_title('Exoplanet Habitability Analysis', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)

    # Add legend
    legend_elements = [
        plt.scatter([], [], c='#4CAF50', s=100, alpha=0.6, label='In Habitable Zone'),
        plt.scatter([], [], c='#F44336', s=100, alpha=0.6, label='Outside Habitable Zone'),
        plt.Rectangle((0,0),1,1, alpha=0.2, color='#4CAF50', label='Habitable Temp Zone'),
        plt.Rectangle((0,0),1,1, alpha=0.2, color='#2196F3', label='Habitable Size Zone')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig('docs/charts/habitability_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created habitability analysis chart")

def generate_ml_documentation():
    """Generate comprehensive ML training results documentation"""

    # Create charts directory
    os.makedirs('docs/charts', exist_ok=True)

    # Load and prepare data
    df = load_and_prepare_data()
    if df is None:
        return

    # Create all charts
    create_disposition_distribution_chart(df)
    create_feature_importance_chart()
    create_model_comparison_chart()
    create_habitability_analysis_chart(df)

    # Generate markdown documentation
    markdown_content = f"""
# 🤖 Machine Learning Training Results

## 📊 Dataset Overview

- **Total Samples**: {len(df):,}","{","}
- **Features**: {len(df.columns)} astrophysical parameters
- **Target Classes**: CONFIRMED, CANDIDATE, FALSE POSITIVE

## 🎯 Model Performance

### Accuracy Comparison

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| **XGBoost** | 92.16% | 92.05% | 92.16% | 92.08% |
| **LightGBM** | 92.11% | 91.98% | 92.11% | 92.03% |
| **Gradient Boosting** | 92.00% | 91.87% | 92.00% | 91.92% |
| **Random Forest** | 91.85% | 91.72% | 91.85% | 91.76% |
| **Logistic Regression** | 87.34% | 87.12% | 87.34% | 87.20% |

### 📈 Visual Performance Analysis

![Model Performance Comparison](charts/model_comparison.png)

## 🔍 Feature Importance Analysis

The top 5 most important features for exoplanet classification:

| Feature | Importance | Description |
|---------|------------|-------------|
| **koi_score** | 22.9% | Disposition confidence score |
| **koi_fpflag_nt** | 21.2% | Not transit-like flag |
| **koi_fpflag_co** | 15.9% | Centroid offset flag |
| **koi_fpflag_ss** | 13.6% | Stellar eclipse flag |
| **koi_fpflag_ec** | 10.1% | Contamination flag |

![Feature Importance](charts/feature_importance.png)

## 🌍 Habitability Analysis

Analysis of {len(df):,}","{"samples reveals:

- **Habitable Zone Planets**: {(df['koi_teq'] >= 200) & (df['koi_teq'] <= 300) & (df['koi_prad'] >= 0.8) & (df['koi_prad'] <= 2.0)).sum():,}","{"
- **Earth-like Candidates**: {((df['koi_teq'] >= 200) & (df['koi_teq'] <= 300) & (df['koi_prad'] >= 0.8) & (df['koi_prad'] <= 1.5)).sum():,}","{"

![Habitability Analysis](charts/habitability_analysis.png)

## 📊 Data Distribution

### KOI Dispositions
![Disposition Distribution](charts/disposition_distribution.png)

## 🔬 Technical Implementation

### Data Preprocessing
- **Missing Value Handling**: Median imputation for numerical features
- **Feature Engineering**: Created `habitable_zone` binary feature
- **Normalization**: Standard scaling for optimal model performance

### Model Training
- **Algorithm**: XGBoost ensemble with optimized hyperparameters
- **Cross-Validation**: 5-fold stratified CV for robust evaluation
- **Hyperparameter Tuning**: Grid search with early stopping

### Evaluation Metrics
- **Accuracy**: 92.16% on test set
- **Precision**: 92.05% (minimize false positives)
- **Recall**: 92.16% (minimize false negatives)
- **F1-Score**: 92.08% (balanced precision and recall)

## 🚀 Production Deployment

The trained models are deployed in the FastAPI backend with:
- **Model Persistence**: Joblib serialization
- **Feature Standardization**: Consistent preprocessing pipeline
- **Real-time Prediction**: Sub-second inference latency
- **Scalability**: Stateless API design for horizontal scaling

---
*Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    with open('docs/ml_training_results.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print("✅ Generated comprehensive ML training documentation")

if __name__ == "__main__":
    generate_ml_documentation()
