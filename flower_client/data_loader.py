"""
Data loading and preprocessing for Flower client
"""
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from sqlalchemy import create_engine
import os
from typing import Tuple


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
    """Data loader for Flower client"""
    
    def __init__(self, institution_id: int, database_url: str):
        self.institution_id = institution_id
        self.database_url = database_url
        self.engine = create_engine(database_url)
    
    def load_data(self) -> pd.DataFrame:
        """Load patient data from database"""
        query = f"""
        SELECT age, sex, bmi, children, smoker, region, insurance_cost
        FROM patients
        WHERE institution_id = {self.institution_id}
        AND insurance_cost IS NOT NULL
        """
        df = pd.read_sql(query, self.engine)
        return df
    
    def preprocess_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess features and targets"""
        # Encode categorical features
        df['sex_encoded'] = df['sex'].map({'male': 1.0, 'female': 0.0})
        df['smoker_encoded'] = df['smoker'].map({'yes': 1.0, 'no': 0.0})
        
        # One-hot encode region
        region_dummies = pd.get_dummies(df['region'], prefix='region')
        df = pd.concat([df, region_dummies], axis=1)
        
        # Fill missing BMI with mean
        if df['bmi'].isna().any():
            df['bmi'].fillna(df['bmi'].mean(), inplace=True)
        
        # Normalize features
        df['age_norm'] = df['age'] / 100.0
        df['bmi_norm'] = df['bmi'] / 50.0
        df['children_norm'] = df['children'] / 10.0
        
        # Select features
        feature_cols = [
            'age_norm', 'sex_encoded', 'bmi_norm', 'children_norm', 'smoker_encoded'
        ] + [col for col in df.columns if col.startswith('region_')]
        
        # Ensure we have exactly 9 features (pad if needed)
        features = df[feature_cols].values
        if features.shape[1] < 9:
            # Pad with zeros
            padding = np.zeros((features.shape[0], 9 - features.shape[1]))
            features = np.hstack([features, padding])
        elif features.shape[1] > 9:
            # Take first 9 features
            features = features[:, :9]
        
        # Normalize targets (insurance_cost)
        targets = df['insurance_cost'].values / 10000.0  # Normalize to 0-1 range
        
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

