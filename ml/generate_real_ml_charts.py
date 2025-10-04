#!/usr/bin/env python3
"""
Generate Real ML Training Charts Based on Actual Training Results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data():
    """Load and preprocess real NASA data"""
    print("📊 Loading real NASA Kepler data...")
    
    # Load the actual NASA data
    df = pd.read_csv('../data/cumulative_2025.09.16_22.42.55.csv')
    print(f"✅ Loaded {len(df)} samples with {len(df.columns)} columns")
    
    # Select features
    feature_columns = [
        'koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq',
        'koi_insol', 'koi_model_snr', 'koi_steff', 'koi_slogg', 'koi_srad',
        'koi_smass', 'koi_kepmag', 'koi_fpflag_nt', 'koi_fpflag_ss',
        'koi_fpflag_co', 'koi_fpflag_ec', 'ra', 'dec', 'koi_score'
    ]
    
    # Filter valid data
    valid_data = df[df['koi_disposition'].isin(['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE'])]
    X = valid_data[feature_columns].fillna(0)
    y = valid_data['koi_disposition']
    
    print(f"✅ Valid samples: {len(valid_data)}")
    print("📊 Class distribution:")
    print(y.value_counts())
    
    return X, y, feature_columns, valid_data

def create_dataset_overview(valid_data, output_dir):
    """Create dataset overview chart based on real data"""
    print("📊 1. Creating dataset overview from real data...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Real Exoplanet Dataset Feature Distributions', fontsize=16, fontweight='bold')
    
    # Real data distributions
    features_to_plot = [
        ('koi_period', 'Orbital Period (days)'),
        ('koi_prad', 'Planet Radius (Earth radii)'),
        ('koi_teq', 'Equilibrium Temperature (K)'),
        ('koi_steff', 'Stellar Temperature (K)')
    ]
    
    colors = ['#FF6B35', '#F7931E', '#4CAF50', '#2196F3']
    
    for i, (col, title) in enumerate(features_to_plot):
        row, col_idx = i // 2, i % 2
        
        # Get real data, remove outliers for better visualization
        data = valid_data[col].dropna()
        if len(data) > 0:
            # Remove extreme outliers (top 1% and bottom 1%)
            q1, q99 = data.quantile([0.01, 0.99])
            data = data[(data >= q1) & (data <= q99)]
            
            axes[row, col_idx].hist(data, bins=50, alpha=0.7, color=colors[i])
            axes[row, col_idx].set_title(title, fontweight='bold')
            axes[row, col_idx].set_xlabel(title.split('(')[0].strip())
            axes[row, col_idx].set_ylabel('Frequency')
            axes[row, col_idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_dataset_overview.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_classification_distribution(y, output_dir):
    """Create classification distribution chart from real data"""
    print("📊 2. Creating classification distribution from real data...")
    
    plt.figure(figsize=(10, 6))
    
    # Real class distribution
    class_counts = y.value_counts()
    colors = ['#4CAF50', '#FF9800', '#F44336']  # Green, Orange, Red
    
    bars = plt.bar(class_counts.index, class_counts.values, color=colors)
    plt.title('Real Exoplanet Classification Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Classification Type')
    plt.ylabel('Number of Samples')
    
    # Add value labels
    for bar, count in zip(bars, class_counts.values):
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
                f'{count}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_classification_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_feature_correlations(X, output_dir):
    """Create feature correlation matrix from real data"""
    print("📊 3. Creating feature correlations from real data...")
    
    plt.figure(figsize=(12, 10))
    
    # Select key features for correlation
    key_features = ['koi_period', 'koi_prad', 'koi_teq', 'koi_steff', 'koi_insol', 'koi_model_snr']
    available_features = [f for f in key_features if f in X.columns]
    
    if len(available_features) > 1:
        corr_matrix = X[available_features].corr()
        
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f', cbar_kws={'label': 'Correlation Coefficient'})
        plt.title('Real Feature Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/02_feature_correlations.png', dpi=300, bbox_inches='tight')
        plt.close()

def create_habitable_zone_analysis(valid_data, output_dir):
    """Create habitable zone analysis from real data"""
    print("📊 4. Creating habitable zone analysis from real data...")
    
    plt.figure(figsize=(12, 8))
    
    # Use real data for habitable zone analysis
    if 'koi_insol' in valid_data.columns and 'koi_teq' in valid_data.columns:
        # Filter valid data
        hz_data = valid_data[['koi_insol', 'koi_teq', 'koi_prad', 'koi_disposition']].dropna()
        
        if len(hz_data) > 0:
            # Create scatter plot
            colors = {'CONFIRMED': '#4CAF50', 'CANDIDATE': '#FF9800', 'FALSE POSITIVE': '#F44336'}
            
            for disposition in hz_data['koi_disposition'].unique():
                data = hz_data[hz_data['koi_disposition'] == disposition]
                plt.scatter(data['koi_insol'], data['koi_teq'], 
                           c=colors[disposition], label=disposition, alpha=0.6, s=30)
            
            plt.xlabel('Stellar Insolation (Earth = 1.0)')
            plt.ylabel('Equilibrium Temperature (K)')
            plt.title('Real Habitable Zone Analysis', fontsize=16, fontweight='bold')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/03_habitable_zone_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()

def create_model_performance_comparison(X, y, output_dir):
    """Create model performance comparison from real training"""
    print("📊 5. Creating model performance comparison from real training...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        'XGBoost': xgb.XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
    }
    
    # Encode labels for XGBoost
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)
    
    accuracies = []
    model_names = []
    
    for name, model in models.items():
        if name == 'XGBoost':
            model.fit(X_train_scaled, y_train_encoded)
            y_pred_encoded = model.predict(X_test_scaled)
            y_pred = label_encoder.inverse_transform(y_pred_encoded)
            accuracy = (y_pred == y_test).mean()
        else:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            accuracy = (y_pred == y_test).mean()
        
        accuracies.append(accuracy)
        model_names.append(name)
    
    # Create chart
    plt.figure(figsize=(10, 6))
    colors = ['#4CAF50', '#FF6B35']
    bars = plt.bar(model_names, accuracies, color=colors)
    
    plt.title('Real Model Performance Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('ML Models')
    plt.ylabel('Accuracy Score')
    plt.ylim(0, 1)
    
    for bar, acc in zip(bars, accuracies):
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                f'{acc:.4f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/03_model_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return models, X_test, y_test, scaler, label_encoder

def create_confusion_matrix(models, X_test, y_test, scaler, label_encoder, output_dir):
    """Create confusion matrix from real predictions"""
    print("📊 6. Creating confusion matrix from real predictions...")
    
    # Get best model (XGBoost)
    xgb_model = models['XGBoost']
    X_test_scaled = scaler.transform(X_test)
    
    # Get predictions
    y_test_encoded = label_encoder.transform(y_test)
    y_pred_encoded = xgb_model.predict(X_test_scaled)
    y_pred = label_encoder.inverse_transform(y_pred_encoded)
    
    # Create confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
               xticklabels=['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE'],
               yticklabels=['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE'],
               cbar_kws={'label': 'Number of Predictions'})
    plt.title('Real Confusion Matrix - XGBoost', fontsize=14, fontweight='bold')
    plt.xlabel('Predicted Classification')
    plt.ylabel('True Classification')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/04_confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_feature_importance(models, feature_names, output_dir):
    """Create feature importance chart from real model"""
    print("📊 7. Creating feature importance from real model...")
    
    # Get XGBoost model
    xgb_model = models['XGBoost']
    
    if hasattr(xgb_model, 'feature_importances_'):
        plt.figure(figsize=(12, 8))
        
        # Get feature importance
        importance = xgb_model.feature_importances_
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=True)
        
        # Plot top 15 features
        top_features = feature_importance.tail(15)
        
        plt.barh(range(len(top_features)), top_features['importance'])
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.title('Real Feature Importance - XGBoost', fontsize=14, fontweight='bold')
        plt.xlabel('Importance Score')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/05_feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()

def create_learning_curves(X, y, output_dir):
    """Create learning curves from real data"""
    print("📊 8. Creating learning curves from real data...")
    
    # Use XGBoost for learning curves
    model = xgb.XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Generate learning curves
    train_sizes, train_scores, val_scores = learning_curve(
        model, X_scaled, y_encoded, cv=5, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10),
        random_state=42
    )
    
    # Calculate means and stds
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, 'o-', label='Training Score', 
             linewidth=2, color='#4CAF50', markersize=6)
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, 
                     alpha=0.1, color='#4CAF50')
    
    plt.plot(train_sizes, val_mean, 'o-', label='Validation Score', 
             linewidth=2, color='#FF6B35', markersize=6)
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, 
                     alpha=0.1, color='#FF6B35')
    
    plt.title('Real Learning Curves - XGBoost', fontsize=14, fontweight='bold')
    plt.xlabel('Training Set Size')
    plt.ylabel('Accuracy Score')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.ylim(0.7, 1.0)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/06_learning_curves.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_roc_curves(models, X_test, y_test, scaler, label_encoder, output_dir):
    """Create ROC curves from real predictions"""
    print("📊 9. Creating ROC curves from real predictions...")
    
    plt.figure(figsize=(10, 8))
    
    # Get XGBoost model
    xgb_model = models['XGBoost']
    X_test_scaled = scaler.transform(X_test)
    
    # Get prediction probabilities
    y_test_encoded = label_encoder.transform(y_test)
    y_proba = xgb_model.predict_proba(X_test_scaled)
    
    # Create ROC curves for each class
    classes = label_encoder.classes_
    colors = ['#4CAF50', '#FF9800', '#F44336']
    
    for i, (class_name, color) in enumerate(zip(classes, colors)):
        # Binary classification for each class
        y_binary = (y_test_encoded == i).astype(int)
        fpr, tpr, _ = roc_curve(y_binary, y_proba[:, i])
        roc_auc = auc(fpr, tpr)
        
        plt.plot(fpr, tpr, color=color, linewidth=2,
                label=f'{class_name} (AUC = {roc_auc:.3f})')
    
    plt.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Random Classifier')
    plt.title('Real ROC Curves - Multi-class Classification', fontsize=14, fontweight='bold')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/07_roc_curves.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_training_progress(X, y, output_dir):
    """Create training progress chart from real training"""
    print("📊 10. Creating training progress from real training...")
    
    # Simulate training progress with real data
    model = xgb.XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)
    
    # Train with early stopping to get training progress
    model.fit(X_train, y_train, 
              eval_set=[(X_test, y_test)], 
              early_stopping_rounds=10, 
              verbose=False)
    
    # Get training history
    results = model.evals_result()
    epochs = range(1, len(results['validation_0']['mlogloss']) + 1)
    train_loss = results['validation_0']['mlogloss']
    
    plt.figure(figsize=(12, 6))
    plt.plot(epochs, train_loss, label='Training Loss', color='#4CAF50', linewidth=2)
    plt.title('Real Model Training Progress', fontsize=14, fontweight='bold')
    plt.xlabel('Training Epochs')
    plt.ylabel('Loss Value')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/08_training_progress.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Main function to generate all real ML charts"""
    print("🚀 Generating Real ML Training Charts")
    print("=" * 60)
    
    # Create output directory
    output_dir = "../ml_training_results"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Load and preprocess data
        X, y, feature_names, valid_data = load_and_preprocess_data()
        
        # Create all charts based on real data
        create_dataset_overview(valid_data, output_dir)
        create_classification_distribution(y, output_dir)
        create_feature_correlations(X, output_dir)
        create_habitable_zone_analysis(valid_data, output_dir)
        
        # Train models and create performance charts
        models, X_test, y_test, scaler, label_encoder = create_model_performance_comparison(X, y, output_dir)
        create_confusion_matrix(models, X_test, y_test, scaler, label_encoder, output_dir)
        create_feature_importance(models, feature_names, output_dir)
        create_learning_curves(X, y, output_dir)
        create_roc_curves(models, X_test, y_test, scaler, label_encoder, output_dir)
        create_training_progress(X, y, output_dir)
        
        print("\n" + "=" * 60)
        print("🎉 All Real ML Charts Generated Successfully!")
        print(f"📁 Charts saved to: {output_dir}/")
        print("✅ All charts are based on real NASA Kepler data training results")
        
    except Exception as e:
        print(f"❌ Error generating charts: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
