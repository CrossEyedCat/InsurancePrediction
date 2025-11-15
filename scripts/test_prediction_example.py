"""
Quick test script with example patient data
"""
import torch
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "flower_server"))
sys.path.insert(0, str(Path(__file__).parent.parent / "flower_client"))

from model import InsuranceCostModel
from predict_utils import preprocess_patient_features


def load_model():
    """Load trained model"""
    possible_paths = [
        Path(__file__).parent.parent / "flower_server" / "models" / "active_model.pt",
        Path(__file__).parent.parent / "models" / "active_model.pt",
    ]
    
    for path in possible_paths:
        if path.exists():
            print(f"Loading model from: {path}")
            model = InsuranceCostModel(input_size=17)
            model.load_state_dict(torch.load(path, map_location='cpu'))
            model.eval()
            return model
    
    raise FileNotFoundError("No trained model found!")


def predict_example():
    """Test prediction with example patients"""
    print("=" * 70)
    print("Insurance Cost Prediction - Example Test")
    print("=" * 70)
    print()
    
    # Load model
    try:
        model = load_model()
        print("Model loaded successfully!\n")
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # No need for data loader - using direct preprocessing
    
    # Example patients
    examples = [
        {
            'name': 'Young Non-Smoker',
            'data': {
                'date_of_birth': '2000-01-15',
                'sex': 'female',
                'number_of_dependents': 0,
                'region': 'northeast',
                'height_cm': 165.0,
                'weight_kg': 60.0,
                'bmi': 22.0,
                'systolic_bp': 110,
                'diastolic_bp': 70,
                'resting_heart_rate': 65,
                'smoking_status': 'never',
                'physical_activity_level': 'active',
                'total_cholesterol': 180.0,
                'glucose': 85.0,
            }
        },
        {
            'name': 'Middle-Aged Smoker',
            'data': {
                'date_of_birth': '1980-06-20',
                'sex': 'male',
                'number_of_dependents': 2,
                'region': 'southeast',
                'height_cm': 180.0,
                'weight_kg': 95.0,
                'bmi': 29.3,
                'systolic_bp': 140,
                'diastolic_bp': 90,
                'resting_heart_rate': 80,
                'smoking_status': 'current',
                'physical_activity_level': 'sedentary',
                'total_cholesterol': 220.0,
                'glucose': 105.0,
            }
        },
        {
            'name': 'Senior Healthy',
            'data': {
                'date_of_birth': '1960-03-10',
                'sex': 'male',
                'number_of_dependents': 0,
                'region': 'northwest',
                'height_cm': 175.0,
                'weight_kg': 75.0,
                'bmi': 24.5,
                'systolic_bp': 130,
                'diastolic_bp': 80,
                'resting_heart_rate': 68,
                'smoking_status': 'never',
                'physical_activity_level': 'moderate',
                'total_cholesterol': 190.0,
                'glucose': 90.0,
            }
        }
    ]
    
    # Load dataset statistics for comparison
    try:
        patients_df = pd.read_csv("output/patients.csv")
        avg_cost = patients_df['insurance_cost'].mean()
        median_cost = patients_df['insurance_cost'].median()
    except:
        avg_cost = None
        median_cost = None
    
    # Make predictions
    print("Making predictions for example patients:\n")
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['name']}")
        print("-" * 70)
        
        # Display key info
        patient = example['data']
        age = (datetime.now() - pd.to_datetime(patient['date_of_birth'])).days / 365.25
        print(f"   Age: {age:.0f} years")
        print(f"   Sex: {patient['sex']}")
        print(f"   BMI: {patient['bmi']}")
        print(f"   Smoker: {patient['smoking_status']}")
        print(f"   Activity: {patient['physical_activity_level']}")
        
        # Preprocess
        try:
            patient_features = preprocess_patient_features(patient)
            
            # Predict
            model.eval()
            with torch.no_grad():
                features_tensor = torch.FloatTensor(patient_features).unsqueeze(0)
                prediction = model(features_tensor)
                predicted_cost = prediction.item()
            
            print(f"\n   Predicted Insurance Cost: ${predicted_cost:,.2f}")
            
            if avg_cost:
                diff = predicted_cost - avg_cost
                pct_diff = (diff / avg_cost) * 100
                print(f"   vs Dataset Average: ${avg_cost:,.2f} ({pct_diff:+.1f}%)")
            
        except Exception as e:
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
        
        print()
    
    print("=" * 70)
    print("Test completed!")
    print("=" * 70)


if __name__ == "__main__":
    predict_example()

