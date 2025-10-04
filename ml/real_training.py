#!/usr/bin/env python3
"""
Real ML Training Script for Exoplanet Classification
Based on actual NASA Kepler data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import xgboost as xgb
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

def load_real_data():
    """Load real NASA Kepler data"""
    print("📊 Loading real NASA Kepler data...")
    
    # Load the actual NASA data
    data_path = '../data/cumulative_2025.09.16_22.42.55.csv'
    if not os.path.exists(data_path):
        print(f"❌ Data file not found: {data_path}")
        return None
    
    df = pd.read_csv(data_path)
    print(f"✅ Loaded {len(df)} samples with {len(df.columns)} columns")
    
    # Check data quality
    print(f"📈 Data shape: {df.shape}")
    print(f"📊 Missing values: {df.isnull().sum().sum()}")
    
    return df

def preprocess_data(df):
    """Preprocess the real data"""
    print("🔧 Preprocessing data...")
    
    # Select features (based on actual data columns)
    feature_columns = [
        'koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq',
        'koi_insol', 'koi_model_snr', 'koi_steff', 'koi_slogg', 'koi_srad',
        'koi_smass', 'koi_kepmag', 'koi_fpflag_nt', 'koi_fpflag_ss',
        'koi_fpflag_co', 'koi_fpflag_ec', 'ra', 'dec', 'koi_score'
    ]
    
    # Check which features exist
    available_features = [col for col in feature_columns if col in df.columns]
    print(f"✅ Available features: {len(available_features)}/{len(feature_columns)}")
    
    # Filter data with valid disposition
    valid_data = df[df['koi_disposition'].isin(['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE'])]
    print(f"✅ Valid samples: {len(valid_data)}")
    
    # Prepare features and labels
    X = valid_data[available_features].fillna(0)
    y = valid_data['koi_disposition']
    
    # Check class distribution
    print("📊 Class distribution:")
    print(y.value_counts())
    
    return X, y, available_features

def train_real_models(X, y, feature_names):
    """Train models on real data"""
    print("🤖 Training models on real data...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    print("🌳 Training Random Forest...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_scaled, y_train)
    
    # Encode labels for XGBoost
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)
    
    # Train XGBoost
    print("🚀 Training XGBoost...")
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42
    )
    xgb_model.fit(X_train_scaled, y_train_encoded)
    
    # Evaluate models
    models = {'Random Forest': rf_model, 'XGBoost': xgb_model}
    results = {}
    
    for name, model in models.items():
        print(f"\n📊 Evaluating {name}...")
        
        # Predictions
        if name == 'XGBoost':
            y_pred_encoded = model.predict(X_test_scaled)
            y_pred = label_encoder.inverse_transform(y_pred_encoded)
            accuracy = accuracy_score(y_test, y_pred)
        else:
            y_pred = model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        if name == 'XGBoost':
            cv_scores = cross_val_score(model, X_train_scaled, y_train_encoded, cv=5)
        else:
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'predictions': y_pred
        }
        
        print(f"✅ {name} - Test Accuracy: {accuracy:.4f}")
        print(f"✅ {name} - CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    
    return results, X_test, y_test, scaler, feature_names

def create_real_charts(results, X_test, y_test, feature_names):
    """Create charts based on real training results"""
    print("📊 Creating charts from real training results...")
    
    # Create output directory
    output_dir = "../ml_training_results"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Model Performance Comparison
    plt.figure(figsize=(10, 6))
    models = list(results.keys())
    accuracies = [results[model]['accuracy'] for model in models]
    
    bars = plt.bar(models, accuracies, color=['#4CAF50', '#FF6B35'])
    plt.title('Real Model Performance Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('ML Models')
    plt.ylabel('Accuracy Score')
    plt.ylim(0, 1)
    
    for bar, acc in zip(bars, accuracies):
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                f'{acc:.4f}', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/real_model_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Confusion Matrix for best model
    best_model_name = max(results.keys(), key=lambda x: results[x]['accuracy'])
    best_model = results[best_model_name]['model']
    y_pred = results[best_model_name]['predictions']
    
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
               xticklabels=['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE'],
               yticklabels=['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE'])
    plt.title(f'Real Confusion Matrix - {best_model_name}', fontsize=14, fontweight='bold')
    plt.xlabel('Predicted Classification')
    plt.ylabel('True Classification')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/real_confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Feature Importance (if available)
    if hasattr(best_model, 'feature_importances_'):
        plt.figure(figsize=(12, 8))
        importance = best_model.feature_importances_
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=True)
        
        plt.barh(range(len(feature_importance)), feature_importance['importance'])
        plt.yticks(range(len(feature_importance)), feature_importance['feature'])
        plt.title(f'Real Feature Importance - {best_model_name}', fontsize=14, fontweight='bold')
        plt.xlabel('Importance Score')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/real_feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    print(f"✅ Real charts saved to: {output_dir}/")
    return best_model_name, results[best_model_name]['accuracy']

def save_real_models(best_model, scaler, feature_names):
    """Save the real trained models"""
    print("💾 Saving real trained models...")
    
    # Save model
    joblib.dump(best_model, 'exoplanet_model_real.joblib')
    joblib.dump(scaler, 'scaler_real.joblib')
    
    # Save feature names
    with open('feature_names_real.txt', 'w') as f:
        for name in feature_names:
            f.write(f"{name}\n")
    
    print("✅ Real models saved successfully!")

def main():
    """Main training pipeline with real data"""
    print("🚀 Starting REAL ML Training Pipeline")
    print("=" * 60)
    
    try:
        # Load real data
        df = load_real_data()
        if df is None:
            print("❌ Cannot proceed without real data")
            return
        
        # Preprocess data
        X, y, feature_names = preprocess_data(df)
        
        # Train models
        results, X_test, y_test, scaler, feature_names = train_real_models(X, y, feature_names)
        
        # Create real charts
        best_model_name, best_accuracy = create_real_charts(results, X_test, y_test, feature_names)
        
        # Save models
        best_model = results[best_model_name]['model']
        save_real_models(best_model, scaler, feature_names)
        
        print("\n" + "=" * 60)
        print("🎉 REAL ML Training Completed Successfully!")
        print(f"🏆 Best Model: {best_model_name}")
        print(f"📊 Best Accuracy: {best_accuracy:.4f}")
        print("📁 Real results saved to ml_training_results/")
        
    except Exception as e:
        print(f"❌ Error during real training: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
