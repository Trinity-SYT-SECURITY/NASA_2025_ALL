#!/usr/bin/env python3
"""
Create Comprehensive ML Training Charts with Multiple Models and Detailed Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, learning_curve
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
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

def train_multiple_models(X, y):
    """Train multiple ML models with cross-validation"""
    print("🤖 Training multiple ML models...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)
    
    # Define models
    models = {
        'Random Forest': RandomForestClassifier(
            n_estimators=200, max_depth=15, min_samples_split=5, 
            min_samples_leaf=2, random_state=42, n_jobs=-1
        ),
        'XGBoost': xgb.XGBClassifier(
            n_estimators=200, max_depth=8, learning_rate=0.1,
            subsample=0.8, colsample_bytree=0.8, random_state=42
        ),
        'Logistic Regression': LogisticRegression(
            max_iter=1000, random_state=42, multi_class='ovr'
        ),
        'SVM': SVC(
            kernel='rbf', C=1.0, gamma='scale', random_state=42, probability=True
        )
    }
    
    # Train and evaluate models
    results = {}
    cv_scores = {}
    
    for name, model in models.items():
        print(f"\n🔄 Training {name}...")
        
        # Train model
        if name == 'XGBoost':
            model.fit(X_train_scaled, y_train_encoded)
            y_pred_encoded = model.predict(X_test_scaled)
            y_pred = label_encoder.inverse_transform(y_pred_encoded)
            accuracy = (y_pred == y_test).mean()
            
            # Cross-validation
            cv = cross_val_score(model, X_train_scaled, y_train_encoded, cv=5, scoring='accuracy')
        else:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            accuracy = (y_pred == y_test).mean()
            
            # Cross-validation
            cv = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'predictions': y_pred
        }
        
        cv_scores[name] = {
            'mean': cv.mean(),
            'std': cv.std()
        }
        
        print(f"✅ {name} - Test Accuracy: {accuracy:.4f}")
        print(f"✅ {name} - CV Accuracy: {cv.mean():.4f} ± {cv.std():.4f}")
    
    return results, cv_scores, X_test, y_test, scaler, label_encoder

def create_comprehensive_model_comparison(results, cv_scores, output_dir):
    """Create comprehensive model performance comparison"""
    print("📊 Creating comprehensive model performance comparison...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Test accuracy comparison
    models = list(results.keys())
    test_accuracies = [results[model]['accuracy'] for model in models]
    cv_means = [cv_scores[model]['mean'] for model in models]
    cv_stds = [cv_scores[model]['std'] for model in models]
    
    colors = ['#4CAF50', '#FF6B35', '#2196F3', '#9C27B0']
    
    # Test accuracy bar chart
    bars1 = ax1.bar(models, test_accuracies, color=colors)
    ax1.set_title('Real Model Performance Comparison (Test Set)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Accuracy Score')
    ax1.set_ylim(0, 1)
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bar, acc in zip(bars1, test_accuracies):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                f'{acc:.4f}', ha='center', va='bottom', fontweight='bold')
    
    # Cross-validation comparison
    x_pos = np.arange(len(models))
    bars2 = ax2.bar(x_pos, cv_means, yerr=cv_stds, color=colors, capsize=5)
    ax2.set_title('Cross-Validation Performance (5-Fold)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('CV Accuracy Score')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(models, rotation=45)
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3, axis='y')
    
    for i, (mean, std) in enumerate(zip(cv_means, cv_stds)):
        ax2.text(i, mean + std + 0.01, f'{mean:.3f}±{std:.3f}', 
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/comprehensive_model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_detailed_feature_importance(results, feature_names, output_dir):
    """Create detailed feature importance analysis"""
    print("📊 Creating detailed feature importance analysis...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Real Feature Importance Analysis Across Models', fontsize=16, fontweight='bold')
    
    # Get models that support feature importance
    importance_models = {
        'Random Forest': results['Random Forest']['model'],
        'XGBoost': results['XGBoost']['model']
    }
    
    for i, (name, model) in enumerate(importance_models.items()):
        row, col = i // 2, i % 2
        ax = axes[row, col]
        
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
            feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': importance
            }).sort_values('importance', ascending=True)
            
            # Plot top 15 features
            top_features = feature_importance.tail(15)
            
            bars = ax.barh(range(len(top_features)), top_features['importance'])
            ax.set_yticks(range(len(top_features)))
            ax.set_yticklabels(top_features['feature'])
            ax.set_title(f'{name} Feature Importance', fontweight='bold')
            ax.set_xlabel('Importance Score')
            ax.grid(True, alpha=0.3, axis='x')
            
            # Add value labels
            for j, (bar, imp) in enumerate(zip(bars, top_features['importance'])):
                ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
                       f'{imp:.3f}', ha='left', va='center', fontsize=9)
    
    # Key features comparison
    key_features = ['koi_prad', 'koi_teq', 'koi_steff', 'koi_period']
    available_key_features = [f for f in key_features if f in feature_names]
    
    if len(available_key_features) > 0:
        ax = axes[1, 1]
        
        # Get importance for key features from Random Forest
        rf_model = results['Random Forest']['model']
        if hasattr(rf_model, 'feature_importances_'):
            importance = rf_model.feature_importances_
            feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': importance
            })
            
            key_importance = feature_importance[feature_importance['feature'].isin(available_key_features)]
            key_importance = key_importance.sort_values('importance', ascending=True)
            
            colors = ['#FF6B35', '#F7931E', '#4CAF50', '#2196F3']
            bars = ax.barh(range(len(key_importance)), key_importance['importance'], 
                          color=colors[:len(key_importance)])
            ax.set_yticks(range(len(key_importance)))
            ax.set_yticklabels(key_importance['feature'])
            ax.set_title('Key Features Importance (Random Forest)', fontweight='bold')
            ax.set_xlabel('Importance Score')
            ax.grid(True, alpha=0.3, axis='x')
            
            # Add value labels
            for j, (bar, imp) in enumerate(zip(bars, key_importance['importance'])):
                ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
                       f'{imp:.3f}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/detailed_feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()

def analyze_overfitting_underfitting(X, y, output_dir):
    """Analyze overfitting and underfitting with learning curves"""
    print("📊 Analyzing overfitting/underfitting with learning curves...")
    
    # Use XGBoost for analysis
    model = xgb.XGBClassifier(n_estimators=200, max_depth=8, learning_rate=0.1, random_state=42)
    
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
        random_state=42, scoring='accuracy'
    )
    
    # Calculate means and stds
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)
    
    # Create comprehensive analysis
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Real Overfitting/Underfitting Analysis', fontsize=16, fontweight='bold')
    
    # Learning curves
    ax1.plot(train_sizes, train_mean, 'o-', label='Training Score', 
             linewidth=2, color='#4CAF50', markersize=6)
    ax1.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, 
                     alpha=0.1, color='#4CAF50')
    
    ax1.plot(train_sizes, val_mean, 'o-', label='Validation Score', 
             linewidth=2, color='#FF6B35', markersize=6)
    ax1.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, 
                     alpha=0.1, color='#FF6B35')
    
    ax1.set_title('Learning Curves - XGBoost', fontweight='bold')
    ax1.set_xlabel('Training Set Size')
    ax1.set_ylabel('Accuracy Score')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0.7, 1.0)
    
    # Gap analysis (overfitting indicator)
    gap = train_mean - val_mean
    ax2.plot(train_sizes, gap, 'o-', color='#F44336', linewidth=2, markersize=6)
    ax2.set_title('Training-Validation Gap (Overfitting Indicator)', fontweight='bold')
    ax2.set_xlabel('Training Set Size')
    ax2.set_ylabel('Accuracy Gap')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0.05, color='orange', linestyle='--', alpha=0.7, label='Warning Threshold')
    ax2.axhline(y=0.1, color='red', linestyle='--', alpha=0.7, label='Overfitting Threshold')
    ax2.legend()
    
    # Cross-validation stability
    cv_scores = []
    for i in range(5):  # 5 different random states
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_encoded, test_size=0.2, random_state=i*42, stratify=y_encoded
        )
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        cv_scores.append(score)
    
    ax3.hist(cv_scores, bins=5, alpha=0.7, color='#4CAF50', edgecolor='black')
    ax3.set_title('Cross-Validation Score Distribution', fontweight='bold')
    ax3.set_xlabel('Accuracy Score')
    ax3.set_ylabel('Frequency')
    ax3.grid(True, alpha=0.3)
    ax3.axvline(np.mean(cv_scores), color='red', linestyle='--', 
                label=f'Mean: {np.mean(cv_scores):.4f}')
    ax3.legend()
    
    # Model complexity analysis
    depths = [3, 6, 9, 12, 15]
    train_scores_complexity = []
    val_scores_complexity = []
    
    for depth in depths:
        model_complex = xgb.XGBClassifier(n_estimators=100, max_depth=depth, random_state=42)
        model_complex.fit(X_scaled, y_encoded)
        
        train_score = model_complex.score(X_scaled, y_encoded)
        val_score = np.mean(cross_val_score(model_complex, X_scaled, y_encoded, cv=5))
        
        train_scores_complexity.append(train_score)
        val_scores_complexity.append(val_score)
    
    ax4.plot(depths, train_scores_complexity, 'o-', label='Training Score', 
             linewidth=2, color='#4CAF50', markersize=6)
    ax4.plot(depths, val_scores_complexity, 'o-', label='Validation Score', 
             linewidth=2, color='#FF6B35', markersize=6)
    ax4.set_title('Model Complexity Analysis', fontweight='bold')
    ax4.set_xlabel('Max Depth')
    ax4.set_ylabel('Accuracy Score')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/overfitting_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Print analysis results
    print("\n🔍 Overfitting/Underfitting Analysis:")
    print(f"📊 Training-Validation Gap: {gap[-1]:.4f} (Last training size)")
    print(f"📊 Cross-validation Stability: {np.std(cv_scores):.4f} (Lower is better)")
    print(f"📊 Model Complexity Optimal Depth: {depths[np.argmax(val_scores_complexity)]}")
    
    if gap[-1] < 0.05:
        print("✅ No significant overfitting detected")
    elif gap[-1] < 0.1:
        print("⚠️  Mild overfitting detected")
    else:
        print("❌ Significant overfitting detected")
    
    if np.std(cv_scores) < 0.01:
        print("✅ Model is very stable")
    elif np.std(cv_scores) < 0.02:
        print("✅ Model is stable")
    else:
        print("⚠️  Model shows some instability")

def main():
    """Main function to create comprehensive ML analysis"""
    print("🚀 Creating Comprehensive ML Training Analysis")
    print("=" * 60)
    
    # Create output directory
    output_dir = "../ml_training_results"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Load and preprocess data
        X, y, feature_names, valid_data = load_and_preprocess_data()
        
        # Train multiple models
        results, cv_scores, X_test, y_test, scaler, label_encoder = train_multiple_models(X, y)
        
        # Create comprehensive charts
        create_comprehensive_model_comparison(results, cv_scores, output_dir)
        create_detailed_feature_importance(results, feature_names, output_dir)
        analyze_overfitting_underfitting(X, y, output_dir)
        
        print("\n" + "=" * 60)
        print("🎉 Comprehensive ML Analysis Completed!")
        print("📊 Generated charts:")
        print("  - comprehensive_model_comparison.png")
        print("  - detailed_feature_importance.png") 
        print("  - overfitting_analysis.png")
        print(f"📁 Charts saved to: {output_dir}/")
        
        # Training summary
        print("\n📈 Training Summary:")
        print(f"🔄 Models trained: {len(results)}")
        print(f"📊 Cross-validation: 5-fold")
        print(f"🎯 Best model: {max(results.keys(), key=lambda x: results[x]['accuracy'])}")
        print(f"🏆 Best accuracy: {max(results[model]['accuracy'] for model in results):.4f}")
        
    except Exception as e:
        print(f"❌ Error in comprehensive analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
