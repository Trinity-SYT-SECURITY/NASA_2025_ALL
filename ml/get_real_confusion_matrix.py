#!/usr/bin/env python3
"""
Get real confusion matrix from trained model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix
import xgboost as xgb

def get_real_confusion_matrix():
    # Load data
    df = pd.read_csv('../data/cumulative_2025.09.16_22.42.55.csv')
    feature_columns = ['koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq', 'koi_insol', 'koi_model_snr', 'koi_steff', 'koi_slogg', 'koi_srad', 'koi_smass', 'koi_kepmag', 'koi_fpflag_nt', 'koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec', 'ra', 'dec', 'koi_score']
    valid_data = df[df['koi_disposition'].isin(['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE'])]
    X = valid_data[feature_columns].fillna(0)
    y = valid_data['koi_disposition']

    # Split and scale
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train XGBoost
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    model = xgb.XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
    model.fit(X_train_scaled, y_train_encoded)

    # Get predictions
    y_pred_encoded = model.predict(X_test_scaled)
    y_pred = label_encoder.inverse_transform(y_pred_encoded)

    # Calculate confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print('Real Confusion Matrix:')
    print(cm)
    print(f'Total samples: {cm.sum()}')
    print(f'Correct predictions: {np.trace(cm)}')
    print(f'Accuracy: {np.trace(cm) / cm.sum():.4f}')
    
    return cm

if __name__ == "__main__":
    get_real_confusion_matrix()
