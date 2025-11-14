"""
Data loading and preprocessing for Flower client
Loads data from CSV files in output directory
"""
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import os
from typing import Tuple
from pathlib import Path
from datetime import datetime


class PatientDataset(Dataset):
    """Dataset class for patient data"""
    
    def __init__(self, features: np.ndarray, targets: np.ndarray):
        self.features = torch.FloatTensor(features)
        self.targets = torch.FloatTensor(targets)
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return self.features[idx], self.targets[idx]


class DataLoaderClient:
    """Data loader for Flower client - loads from CSV files"""
    
    def __init__(self, client_id: int, data_dir: str = "output", 
                 start_idx: int = None, end_idx: int = None):
        """
        Initialize data loader
        
        Args:
            client_id: Client ID (1, 2, or 3)
            data_dir: Directory containing CSV files
            start_idx: Start index for data split (if None, auto-calculate)
            end_idx: End index for data split (if None, auto-calculate)
        """
        self.client_id = client_id
        self.data_dir = Path(data_dir)
        
        # Calculate data split for this client
        # Each client gets approximately 1/3 of the data
        if start_idx is None or end_idx is None:
            # Load patients to determine total count
            patients_df = pd.read_csv(self.data_dir / 'patients.csv')
            total_samples = len(patients_df)
            samples_per_client = total_samples // 3
            
            self.start_idx = (client_id - 1) * samples_per_client
            if client_id == 3:
                self.end_idx = total_samples  # Last client gets remaining data
            else:
                self.end_idx = client_id * samples_per_client
        else:
            self.start_idx = start_idx
            self.end_idx = end_idx
    
    def load_data(self) -> pd.DataFrame:
        """Load and merge patient data from CSV files"""
        # Load all CSV files
        patients_df = pd.read_csv(self.data_dir / 'patients.csv')
        physical_df = pd.read_csv(self.data_dir / 'patient_physical_measurements.csv')
        lifestyle_df = pd.read_csv(self.data_dir / 'patient_lifestyle.csv')
        socioeconomic_df = pd.read_csv(self.data_dir / 'patient_socioeconomic.csv')
        lab_results_df = pd.read_csv(self.data_dir / 'patient_lab_results.csv')
        
        # Merge all dataframes on patient_id
        # First, add patient_id to patients_df (it's the index + 1)
        patients_df = patients_df.copy()
        patients_df['patient_id'] = patients_df.index + 1
        
        # Merge all tables
        df = patients_df.merge(physical_df, on='patient_id', how='left')
        df = df.merge(lifestyle_df, on='patient_id', how='left', suffixes=('', '_lifestyle'))
        df = df.merge(socioeconomic_df, on='patient_id', how='left', suffixes=('', '_socio'))
        df = df.merge(lab_results_df, on='patient_id', how='left', suffixes=('', '_lab'))
        
        # Filter by client's data range (based on patient_id)
        df = df[(df['patient_id'] > self.start_idx) & (df['patient_id'] <= self.end_idx)].copy()
        
        # Calculate age from date_of_birth
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
        df['age'] = (datetime.now() - df['date_of_birth']).dt.days / 365.25
        
        # Filter out rows with missing insurance_cost
        df = df[df['insurance_cost'].notna()].copy()
        
        return df
    
    def preprocess_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess features and targets using enriched data"""
        # Encode categorical features
        df['sex_encoded'] = df['sex'].map({'male': 1.0, 'female': 0.0})
        
        # Smoking status from lifestyle
        df['smoker_encoded'] = df['smoking_status'].map({'current': 1.0, 'never': 0.0, 'former': 0.5})
        df['smoker_encoded'] = df['smoker_encoded'].fillna(0.0)
        
        # One-hot encode region
        region_dummies = pd.get_dummies(df['region'], prefix='region')
        df = pd.concat([df, region_dummies], axis=1)
        
        # Fill missing values with median
        numeric_cols = ['age', 'bmi', 'number_of_dependents', 'height_cm', 'weight_kg',
                       'systolic_bp', 'diastolic_bp', 'resting_heart_rate',
                       'total_cholesterol', 'glucose', 'hba1c']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        
        # Normalize features
        df['age_norm'] = (df['age'] - 18) / (64 - 18)  # Normalize to 0-1
        df['bmi_norm'] = (df['bmi'] - 15) / (50 - 15)  # Normalize to 0-1
        df['children_norm'] = df['number_of_dependents'] / 5.0  # Max 5 children
        df['height_norm'] = (df['height_cm'] - 140) / (210 - 140) if 'height_cm' in df.columns else 0.5
        df['weight_norm'] = (df['weight_kg'] - 40) / (200 - 40) if 'weight_kg' in df.columns else 0.5
        df['bp_systolic_norm'] = (df['systolic_bp'] - 90) / (180 - 90) if 'systolic_bp' in df.columns else 0.5
        df['bp_diastolic_norm'] = (df['diastolic_bp'] - 60) / (120 - 60) if 'diastolic_bp' in df.columns else 0.5
        df['heart_rate_norm'] = (df['resting_heart_rate'] - 50) / (100 - 50) if 'resting_heart_rate' in df.columns else 0.5
        df['cholesterol_norm'] = (df['total_cholesterol'] - 100) / (300 - 100) if 'total_cholesterol' in df.columns else 0.5
        df['glucose_norm'] = (df['glucose'] - 70) / (120 - 70) if 'glucose' in df.columns else 0.5
        
        # Activity level encoding
        activity_map = {'sedentary': 0.0, 'light': 0.25, 'moderate': 0.5, 'active': 0.75, 'very_active': 1.0}
        df['activity_encoded'] = df['physical_activity_level'].map(activity_map).fillna(0.5)
        
        # Select features - using enriched data
        feature_cols = [
            'age_norm', 'sex_encoded', 'bmi_norm', 'children_norm', 'smoker_encoded',
            'height_norm', 'weight_norm', 'bp_systolic_norm', 'bp_diastolic_norm',
            'heart_rate_norm', 'cholesterol_norm', 'glucose_norm', 'activity_encoded'
        ] + [col for col in df.columns if col.startswith('region_')]
        
        # Ensure we have exactly the right number of features
        # Count region columns
        region_cols = [col for col in df.columns if col.startswith('region_')]
        expected_features = 13 + len(region_cols)  # Base features + regions
        
        # Build feature matrix
        features_list = []
        for col in feature_cols:
            if col in df.columns:
                features_list.append(df[col].values)
            else:
                features_list.append(np.zeros(len(df)))
        
        features = np.column_stack(features_list)
        
        # Normalize targets (insurance_cost) - keep original scale for better training
        targets = df['insurance_cost'].values
        
        return features, targets
    
    def get_data_loaders(
        self, 
        train_ratio: float = 0.8,
        batch_size: int = 32
    ) -> Tuple[DataLoader, DataLoader]:
        """Get train and validation data loaders"""
        # Load data
        df = self.load_data()
        
        if len(df) == 0:
            raise ValueError(f"No data found for institution {self.institution_id}")
        
        # Preprocess
        features, targets = self.preprocess_features(df)
        
        # Split train/validation
        n_train = int(len(features) * train_ratio)
        train_features = features[:n_train]
        train_targets = targets[:n_train]
        val_features = features[n_train:]
        val_targets = targets[n_train:]
        
        # Create datasets
        train_dataset = PatientDataset(train_features, train_targets)
        val_dataset = PatientDataset(val_features, val_targets)
        
        # Create data loaders
        train_loader = DataLoader(
            train_dataset, 
            batch_size=batch_size, 
            shuffle=True
        )
        val_loader = DataLoader(
            val_dataset, 
            batch_size=batch_size, 
            shuffle=False
        )
        
        return train_loader, val_loader

