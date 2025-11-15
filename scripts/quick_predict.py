"""
Quick prediction script - simple interface for insurance cost prediction
"""
import torch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "flower_server"))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from model import InsuranceCostModel
from predict_utils import preprocess_patient_features


def quick_predict(age=35, sex='male', bmi=25.0, children=0, smoker='never', 
                  region='northeast', height_cm=175.0, weight_kg=75.0,
                  systolic_bp=120, diastolic_bp=80, heart_rate=70,
                  cholesterol=200.0, glucose=90.0, activity='moderate'):
    """
    Quick prediction function
    
    Args:
        age: Patient age
        sex: 'male' or 'female'
        bmi: Body Mass Index
        children: Number of dependents
        smoker: 'never', 'current', or 'former'
        region: 'northeast', 'southeast', 'southwest', or 'northwest'
        height_cm: Height in cm
        weight_kg: Weight in kg
        systolic_bp: Systolic blood pressure
        diastolic_bp: Diastolic blood pressure
        heart_rate: Resting heart rate
        cholesterol: Total cholesterol
        glucose: Blood glucose level
        activity: 'sedentary', 'light', 'moderate', 'active', or 'very_active'
    
    Returns:
        Predicted insurance cost
    """
    # Load model
    possible_paths = [
        Path(__file__).parent.parent / "flower_server" / "models" / "active_model.pt",
        Path(__file__).parent.parent / "models" / "active_model.pt",
    ]
    
    model_path = None
    for path in possible_paths:
        if path.exists():
            model_path = path
            break
    
    if model_path is None:
        raise FileNotFoundError("No trained model found!")
    
    model = InsuranceCostModel(input_size=17)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    
    # Prepare patient data
    patient_data = {
        'age': float(age),
        'sex': sex.lower(),
        'number_of_dependents': int(children),
        'region': region.lower(),
        'height_cm': float(height_cm),
        'weight_kg': float(weight_kg),
        'bmi': float(bmi),
        'systolic_bp': int(systolic_bp),
        'diastolic_bp': int(diastolic_bp),
        'resting_heart_rate': int(heart_rate),
        'smoking_status': smoker.lower(),
        'physical_activity_level': activity.lower(),
        'total_cholesterol': float(cholesterol),
        'glucose': float(glucose),
    }
    
    # Preprocess and predict
    features = preprocess_patient_features(patient_data)
    
    with torch.no_grad():
        features_tensor = torch.FloatTensor(features).unsqueeze(0)
        prediction = model(features_tensor)
        cost = prediction.item()
    
    return cost


def main():
    """Interactive prediction"""
    print("=" * 70)
    print("Insurance Cost Prediction - Quick Test")
    print("=" * 70)
    print()
    
    # Example 1: Young healthy non-smoker
    print("Example 1: Young Healthy Non-Smoker")
    print("-" * 70)
    cost1 = quick_predict(
        age=25, sex='female', bmi=22.0, children=0, smoker='never',
        region='northeast', height_cm=165, weight_kg=60,
        systolic_bp=110, diastolic_bp=70, heart_rate=65,
        cholesterol=180, glucose=85, activity='active'
    )
    print(f"Predicted Cost: ${cost1:,.2f}\n")
    
    # Example 2: Middle-aged smoker
    print("Example 2: Middle-Aged Smoker")
    print("-" * 70)
    cost2 = quick_predict(
        age=45, sex='male', bmi=29.3, children=2, smoker='current',
        region='southeast', height_cm=180, weight_kg=95,
        systolic_bp=140, diastolic_bp=90, heart_rate=80,
        cholesterol=220, glucose=105, activity='sedentary'
    )
    print(f"Predicted Cost: ${cost2:,.2f}\n")
    
    # Example 3: Senior healthy
    print("Example 3: Senior Healthy")
    print("-" * 70)
    cost3 = quick_predict(
        age=65, sex='male', bmi=24.5, children=0, smoker='never',
        region='northwest', height_cm=175, weight_kg=75,
        systolic_bp=130, diastolic_bp=80, heart_rate=68,
        cholesterol=190, glucose=90, activity='moderate'
    )
    print(f"Predicted Cost: ${cost3:,.2f}\n")
    
    print("=" * 70)
    print("All predictions completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

