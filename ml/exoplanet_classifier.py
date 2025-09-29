"""
Advanced Exoplanet Classification Models
Multiple algorithms for robust KOI disposition prediction
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
from sklearn.model_selection import cross_val_score, GridSearchCV
import xgboost as xgb
import lightgbm as lgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from data_preprocessing import KOIDataProcessor
import warnings
warnings.filterwarnings('ignore')

class ExoplanetClassifier:
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.feature_importance = None
        
    def create_models(self):
        """Create multiple classification models"""
        
        # Random Forest
        self.models['rf'] = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        # XGBoost
        self.models['xgb'] = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric='mlogloss'
        )
        
        # LightGBM
        self.models['lgb'] = lgb.LGBMClassifier(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            verbose=-1
        )
        
        # Gradient Boosting
        self.models['gb'] = GradientBoostingClassifier(
            n_estimators=150,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42
        )
        
        # Logistic Regression
        self.models['lr'] = LogisticRegression(
            max_iter=1000,
            random_state=42,
            multi_class='ovr'
        )
        
        print(f"Created {len(self.models)} models: {list(self.models.keys())}")
    
    def train_models(self, X_train, y_train):
        """Train all models"""
        print("Training models...")
        
        self.trained_models = {}
        self.cv_scores = {}
        
        for name, model in self.models.items():
            print(f"\nTraining {name}...")
            
            # Train model
            model.fit(X_train, y_train)
            self.trained_models[name] = model
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            self.cv_scores[name] = {
                'mean': cv_scores.mean(),
                'std': cv_scores.std()
            }
            
            print(f"{name} CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    def evaluate_models(self, X_test, y_test, class_names):
        """Evaluate all trained models"""
        print("\nEvaluating models...")
        
        self.test_scores = {}
        
        for name, model in self.trained_models.items():
            print(f"\n=== {name.upper()} ===")
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)
            
            # Accuracy
            accuracy = accuracy_score(y_test, y_pred)
            self.test_scores[name] = accuracy
            
            print(f"Test Accuracy: {accuracy:.4f}")
            
            # Classification report
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred, target_names=class_names))
            
            # ROC AUC for multiclass
            try:
                auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr')
                print(f"ROC AUC (OvR): {auc:.4f}")
            except:
                print("ROC AUC calculation failed")
    
    def select_best_model(self):
        """Select the best performing model"""
        best_score = max(self.test_scores.values())
        best_name = max(self.test_scores, key=self.test_scores.get)
        
        self.best_model = self.trained_models[best_name]
        self.best_model_name = best_name
        
        print(f"\nBest model: {best_name} with accuracy: {best_score:.4f}")
        return self.best_model
    
    def get_feature_importance(self, feature_names):
        """Get feature importance from the best model"""
        if hasattr(self.best_model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': self.best_model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            self.feature_importance = importance_df
            return importance_df
        else:
            print("Best model doesn't support feature importance")
            return None
    
    def plot_feature_importance(self, top_n=15):
        """Plot feature importance"""
        if self.feature_importance is not None:
            plt.figure(figsize=(10, 8))
            top_features = self.feature_importance.head(top_n)
            
            sns.barplot(data=top_features, x='importance', y='feature')
            plt.title(f'Top {top_n} Feature Importance - {self.best_model_name.upper()}')
            plt.xlabel('Importance')
            plt.tight_layout()
            plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def create_ensemble(self, X_train, y_train):
        """Create ensemble model with best performers"""
        print("\nCreating ensemble model...")
        
        # Select top 3 models based on test scores
        sorted_models = sorted(self.test_scores.items(), key=lambda x: x[1], reverse=True)
        top_models = sorted_models[:3]
        
        ensemble_models = []
        for name, score in top_models:
            ensemble_models.append((name, self.trained_models[name]))
            print(f"Including {name} (accuracy: {score:.4f}) in ensemble")
        
        # Create voting classifier
        self.ensemble_model = VotingClassifier(
            estimators=ensemble_models,
            voting='soft'
        )
        
        self.ensemble_model.fit(X_train, y_train)
        print("Ensemble model trained")
        
        return self.ensemble_model
    
    def predict(self, X, use_ensemble=True):
        """Make predictions"""
        if use_ensemble and hasattr(self, 'ensemble_model'):
            return self.ensemble_model.predict(X)
        else:
            return self.best_model.predict(X)
    
    def predict_proba(self, X, use_ensemble=True):
        """Get prediction probabilities"""
        if use_ensemble and hasattr(self, 'ensemble_model'):
            return self.ensemble_model.predict_proba(X)
        else:
            return self.best_model.predict_proba(X)
    
    def save_models(self, filepath_prefix='exoplanet_model'):
        """Save trained models"""
        # Save best model
        joblib.dump(self.best_model, f'{filepath_prefix}_best.joblib')
        
        # Save ensemble if exists
        if hasattr(self, 'ensemble_model'):
            joblib.dump(self.ensemble_model, f'{filepath_prefix}_ensemble.joblib')
        
        # Save feature importance
        if self.feature_importance is not None:
            self.feature_importance.to_csv(f'{filepath_prefix}_feature_importance.csv', index=False)
        
        print(f"Models saved with prefix: {filepath_prefix}")
    
    def load_model(self, filepath):
        """Load a saved model"""
        self.best_model = joblib.load(filepath)
        print(f"Model loaded from: {filepath}")

def main():
    """Main training pipeline"""
    print("=== Exoplanet Classification Training Pipeline ===")
    
    # Load and preprocess data
    processor = KOIDataProcessor('../data/cumulative_2025.09.16_22.42.55.csv')
    X_train, X_test, y_train, y_test = processor.process_all()
    
    feature_names = processor.get_feature_names()
    class_names = processor.get_class_names()
    
    # Initialize classifier
    classifier = ExoplanetClassifier()
    
    # Create and train models
    classifier.create_models()
    classifier.train_models(X_train, y_train)
    
    # Evaluate models
    classifier.evaluate_models(X_test, y_test, class_names)
    
    # Select best model
    best_model = classifier.select_best_model()
    
    # Feature importance
    importance_df = classifier.get_feature_importance(feature_names)
    if importance_df is not None:
        print("\nTop 10 Most Important Features:")
        print(importance_df.head(10))
        classifier.plot_feature_importance()
    
    # Create ensemble
    ensemble_model = classifier.create_ensemble(X_train, y_train)
    
    # Test ensemble
    ensemble_pred = ensemble_model.predict(X_test)
    ensemble_accuracy = accuracy_score(y_test, ensemble_pred)
    print(f"\nEnsemble accuracy: {ensemble_accuracy:.4f}")
    
    # Save models
    classifier.save_models()
    
    # Save preprocessing objects
    joblib.dump(processor.scaler, 'scaler.joblib')
    joblib.dump(processor.label_encoder, 'label_encoder.joblib')
    
    print("\nTraining completed successfully!")
    print(f"Best single model: {classifier.best_model_name}")
    print(f"Ensemble model created with top 3 models")

if __name__ == "__main__":
    main()
