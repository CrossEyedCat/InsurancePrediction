"""
Prediction service for insurance cost prediction
"""
import torch
import numpy as np
from typing import Dict, Optional
import os
from pathlib import Path


class PredictionService:
    """Service for making predictions using trained model"""
    
    def __init__(self):
        self.model = None
        self.model_version = None
        self.model_path = os.getenv("MODEL_PATH", "./models/active_model.pt")
        self._load_model()
    
    def _load_model(self):
        """Load the active model"""
        model_path = Path(self.model_path)
        if model_path.exists():
            try:
                # Load model architecture and weights
                # This will be implemented with actual model loading
                self.model_version = "v1.0.0"
                # self.model = torch.load(model_path)
                # self.model.eval()
            except Exception as e:
                print(f"Error loading model: {e}")
    
    def _preprocess_features(self, features: Dict) -> np.ndarray:
        """Preprocess input features for model"""
        # Encode categorical features
        sex_encoded = 1.0 if features["sex"] == "male" else 0.0
        smoker_encoded = 1.0 if features["smoker"] == "yes" else 0.0
        
        # Region encoding (one-hot)
        region_map = {"northeast": [1, 0, 0, 0], "northwest": [0, 1, 0, 0],
                     "southeast": [0, 0, 1, 0], "southwest": [0, 0, 0, 1]}
        region_encoded = region_map.get(features.get("region", "northeast"), [1, 0, 0, 0])
        
        # Normalize features (using simple normalization)
        age_norm = features["age"] / 100.0
        bmi_norm = (features.get("bmi", 25.0) or 25.0) / 50.0
        children_norm = features["children"] / 10.0
        
        # Combine features
        feature_vector = np.array([
            age_norm,
            sex_encoded,
            bmi_norm,
            children_norm,
            smoker_encoded,
            *region_encoded
        ])
        
        return feature_vector
    
    async def predict(self, features: Dict) -> float:
        """Make prediction for given features"""
        if self.model is None:
            # Fallback to simple rule-based prediction
            return self._fallback_prediction(features)
        
        try:
            # Preprocess features
            feature_vector = self._preprocess_features(features)
            
            # Convert to tensor
            input_tensor = torch.FloatTensor(feature_vector).unsqueeze(0)
            
            # Make prediction
            with torch.no_grad():
                prediction = self.model(input_tensor).item()
            
            # Denormalize (if needed)
            return max(0, prediction * 10000)  # Scale back to actual cost range
        
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._fallback_prediction(features)
    
    def _fallback_prediction(self, features: Dict) -> float:
        """Simple fallback prediction based on rules"""
        base_cost = 5000
        
        # Age factor
        age_factor = features["age"] * 100
        
        # BMI factor
        bmi = features.get("bmi", 25.0) or 25.0
        bmi_factor = (bmi - 25) * 200
        
        # Smoker factor
        smoker_factor = 10000 if features["smoker"] == "yes" else 0
        
        # Children factor
        children_factor = features["children"] * 500
        
        total = base_cost + age_factor + bmi_factor + smoker_factor + children_factor
        return max(1000, total)
    
    def get_active_model_version(self) -> Optional[str]:
        """Get active model version"""
        return self.model_version

