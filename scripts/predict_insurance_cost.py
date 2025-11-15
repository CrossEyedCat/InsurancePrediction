"""
Script to predict insurance cost for a patient using trained model
"""
import torch
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "flower_server"))
sys.path.insert(0, str(Path(__file__).parent.parent / "flower_client"))

from model import InsuranceCostModel
from predict_utils import preprocess_patient_features


def load_model(model_path: str = None):
    """Load trained model"""
    if model_path is None:
        # Try different possible locations
        possible_paths = [
            Path(__file__).parent.parent / "flower_server" / "models" / "active_model.pt",
            Path(__file__).parent.parent / "models" / "active_model.pt",
            Path(__file__).parent.parent / "flower_server" / "models" / "model_round_5.pt",
        ]
        
        for path in possible_paths:
            if path.exists():
                model_path = path
                break
        
        if model_path is None:
            raise FileNotFoundError("No trained model found. Please train the model first.")
    
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    print(f"Loading model from: {model_path}")
    
    model = InsuranceCostModel(input_size=17)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    
    print("Model loaded successfully!")
    return model


def preprocess_patient_data(patient_data: dict):
    """Preprocess patient data to match training format"""
    return preprocess_patient_features(patient_data)


def predict_insurance_cost(model, patient_features):
    """Make prediction for a patient"""
    model.eval()
    with torch.no_grad():
        # Convert to tensor and add batch dimension
        features_tensor = torch.FloatTensor(patient_features).unsqueeze(0)
        
        # Make prediction
        prediction = model(features_tensor)
        
        # Return prediction value (insurance cost)
        return prediction.item()


def create_example_patient():
    """Create an example patient for testing"""
    return {
        'date_of_birth': '1985-05-15',  # Will calculate age ~39
        'sex': 'male',
        'number_of_dependents': 2,
        'region': 'southeast',
        # Physical measurements
        'height_cm': 175.0,
        'weight_kg': 80.0,
        'bmi': 26.1,
        'systolic_bp': 125,
        'diastolic_bp': 82,
        'resting_heart_rate': 72,
        # Lifestyle
        'smoking_status': 'never',
        'physical_activity_level': 'moderate',
        # Lab results
        'total_cholesterol': 195.0,
        'glucose': 92.0,
    }


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Predict insurance cost for a patient")
    parser.add_argument("--model-path", type=str, default=None,
                       help="Path to trained model (default: auto-detect)")
    parser.add_argument("--example", action="store_true",
                       help="Use example patient data")
    args = parser.parse_args()
    
    print("=" * 70)
    print("Insurance Cost Prediction")
    print("=" * 70)
    print()
    
    # Load model
    try:
        model = load_model(args.model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    # Get patient data
    if args.example:
        print("Using example patient data:")
        patient_data = create_example_patient()
    else:
        print("Enter patient information:")
        patient_data = {
            'date_of_birth': input("Date of birth (YYYY-MM-DD): "),
            'sex': input("Sex (male/female): ").lower(),
            'number_of_dependents': int(input("Number of dependents: ")),
            'region': input("Region (northeast/southeast/southwest/northwest): ").lower(),
            'height_cm': float(input("Height (cm): ")),
            'weight_kg': float(input("Weight (kg): ")),
            'bmi': float(input("BMI: ")),
            'systolic_bp': int(input("Systolic BP: ")),
            'diastolic_bp': int(input("Diastolic BP: ")),
            'resting_heart_rate': int(input("Resting heart rate: ")),
            'smoking_status': input("Smoking status (never/current/former): ").lower(),
            'physical_activity_level': input("Activity level (sedentary/light/moderate/active/very_active): ").lower(),
            'total_cholesterol': float(input("Total cholesterol: ")),
            'glucose': float(input("Glucose: ")),
        }
    
    # Display patient info
    print("\n" + "=" * 70)
    print("Patient Information:")
    print("=" * 70)
    for key, value in patient_data.items():
        print(f"  {key}: {value}")
    
    # Preprocess data
    try:
        print("\nPreprocessing patient data...")
        patient_features = preprocess_patient_data(patient_data)
        print(f"Features extracted: {len(patient_features)} features")
    except Exception as e:
        print(f"Error preprocessing data: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Make prediction
    try:
        print("\nMaking prediction...")
        predicted_cost = predict_insurance_cost(model, patient_features)
        
        print("\n" + "=" * 70)
        print("PREDICTION RESULT")
        print("=" * 70)
        print(f"\nPredicted Insurance Cost: ${predicted_cost:,.2f}")
        print()
        
        # Compare with statistics from training data
        try:
            patients_df = pd.read_csv("output/patients.csv")
            avg_cost = patients_df['insurance_cost'].mean()
            median_cost = patients_df['insurance_cost'].median()
            
            print("Comparison with dataset:")
            print(f"  Dataset average: ${avg_cost:,.2f}")
            print(f"  Dataset median: ${median_cost:,.2f}")
            print(f"  Predicted cost: ${predicted_cost:,.2f}")
            
            if predicted_cost < median_cost:
                print(f"\n  → Below median (${predicted_cost - median_cost:,.2f} lower)")
            elif predicted_cost > median_cost:
                print(f"\n  → Above median (${predicted_cost - median_cost:,.2f} higher)")
            else:
                print(f"\n  → Near median")
        except:
            pass
        
    except Exception as e:
        print(f"Error making prediction: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()

