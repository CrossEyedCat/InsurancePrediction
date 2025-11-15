"""
Utility functions for prediction
Preprocesses patient data without requiring insurance_cost
"""
import pandas as pd
import numpy as np
from datetime import datetime


def preprocess_patient_features(patient_data: dict):
    """
    Preprocess patient data for prediction
    Returns features array matching the model input format
    """
    # Create DataFrame
    df = pd.DataFrame([patient_data])
    
    # Calculate age from date_of_birth if provided
    if 'date_of_birth' in df.columns:
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
        df['age'] = (datetime.now() - df['date_of_birth']).dt.days / 365.25
    elif 'age' not in df.columns:
        raise ValueError("Either 'age' or 'date_of_birth' must be provided")
    
    # Encode categorical features
    df['sex_encoded'] = df['sex'].map({'male': 1.0, 'female': 0.0})
    df['sex_encoded'] = df['sex_encoded'].fillna(0.0)
    
    # Smoking status
    df['smoker_encoded'] = df['smoking_status'].map({'current': 1.0, 'never': 0.0, 'former': 0.5})
    df['smoker_encoded'] = df['smoker_encoded'].fillna(0.0)
    
    # One-hot encode region
    region_dummies = pd.get_dummies(df['region'], prefix='region')
    df = pd.concat([df, region_dummies], axis=1)
    
    # Fill missing values with default/median values
    defaults = {
        'bmi': 25.0,
        'number_of_dependents': 0,
        'height_cm': 170.0,
        'weight_kg': 70.0,
        'systolic_bp': 120,
        'diastolic_bp': 80,
        'resting_heart_rate': 70,
        'total_cholesterol': 200.0,
        'glucose': 90.0,
        'hba1c': 5.0,
    }
    
    for col, default_val in defaults.items():
        if col in df.columns:
            df[col] = df[col].fillna(default_val)
        else:
            df[col] = default_val
    
    # Normalize features (same as in training)
    df['age_norm'] = (df['age'] - 18) / (64 - 18)  # Normalize to 0-1
    df['bmi_norm'] = (df['bmi'] - 15) / (50 - 15)  # Normalize to 0-1
    df['children_norm'] = df['number_of_dependents'] / 5.0  # Max 5 children
    df['height_norm'] = (df['height_cm'] - 140) / (210 - 140)
    df['weight_norm'] = (df['weight_kg'] - 40) / (200 - 40)
    df['bp_systolic_norm'] = (df['systolic_bp'] - 90) / (180 - 90)
    df['bp_diastolic_norm'] = (df['diastolic_bp'] - 60) / (120 - 60)
    df['heart_rate_norm'] = (df['resting_heart_rate'] - 50) / (100 - 50)
    df['cholesterol_norm'] = (df['total_cholesterol'] - 100) / (300 - 100)
    df['glucose_norm'] = (df['glucose'] - 70) / (120 - 70)
    
    # Activity level encoding
    activity_map = {'sedentary': 0.0, 'light': 0.25, 'moderate': 0.5, 'active': 0.75, 'very_active': 1.0}
    df['activity_encoded'] = df['physical_activity_level'].map(activity_map).fillna(0.5)
    
    # Ensure all region columns exist
    all_regions = ['region_northeast', 'region_northwest', 'region_southeast', 'region_southwest']
    for region in all_regions:
        if region not in df.columns:
            df[region] = 0.0
    
    # Select features in correct order
    feature_cols = [
        'age_norm', 'sex_encoded', 'bmi_norm', 'children_norm', 'smoker_encoded',
        'height_norm', 'weight_norm', 'bp_systolic_norm', 'bp_diastolic_norm',
        'heart_rate_norm', 'cholesterol_norm', 'glucose_norm', 'activity_encoded'
    ] + all_regions
    
    # Build feature matrix
    features_list = []
    for col in feature_cols:
        if col in df.columns:
            features_list.append(df[col].values[0])
        else:
            features_list.append(0.0)
    
    features = np.array(features_list)
    
    # Ensure exactly 17 features
    if len(features) != 17:
        raise ValueError(f"Expected 17 features, got {len(features)}")
    
    return features

