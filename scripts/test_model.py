"""
Script to test the trained federated learning model
"""
import torch
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add flower_server to path
sys.path.insert(0, str(Path(__file__).parent.parent / "flower_server"))
from model import InsuranceCostModel
from flower_client.data_loader import DataLoaderClient

def load_model(model_path: str = "flower_server/models/active_model.pt"):
    """Load trained model"""
    model_path = Path(model_path)
    
    if not model_path.exists():
        print(f"Error: Model file not found at {model_path}")
        print("Please train the model first using federated learning.")
        return None
    
    model = InsuranceCostModel(input_size=17)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    
    print(f"Model loaded from {model_path}")
    return model

def predict_sample(model, features):
    """Make prediction for a single sample"""
    model.eval()
    with torch.no_grad():
        features_tensor = torch.FloatTensor(features).unsqueeze(0)
        prediction = model(features_tensor)
        return prediction.item()

def test_model_on_data(model, data_dir: str = "output", num_samples: int = 10):
    """Test model on real data"""
    print("\n" + "=" * 60)
    print("Testing Model on Real Data")
    print("=" * 60)
    
    # Load data
    data_loader = DataLoaderClient(client_id=1, data_dir=data_dir)
    df = data_loader.load_data()
    features, targets = data_loader.preprocess_features(df)
    
    # Select random samples
    indices = np.random.choice(len(features), min(num_samples, len(features)), replace=False)
    
    print(f"\nTesting on {len(indices)} samples:\n")
    print(f"{'Sample':<8} {'Actual':<15} {'Predicted':<15} {'Error':<15} {'Error %':<10}")
    print("-" * 70)
    
    total_error = 0
    total_abs_error = 0
    
    for idx in indices:
        sample_features = features[idx]
        actual = targets[idx]
        predicted = predict_sample(model, sample_features)
        
        error = predicted - actual
        error_pct = (error / actual) * 100 if actual > 0 else 0
        
        total_error += error
        total_abs_error += abs(error)
        
        print(f"{idx:<8} ${actual:<14.2f} ${predicted:<14.2f} ${error:<14.2f} {error_pct:<9.2f}%")
    
    avg_error = total_error / len(indices)
    mae = total_abs_error / len(indices)
    
    # Calculate RMSE
    predictions = []
    actuals = []
    for idx in indices:
        sample_features = features[idx]
        actual = targets[idx]
        predicted = predict_sample(model, sample_features)
        predictions.append(predicted)
        actuals.append(actual)
    
    mse = np.mean((np.array(predictions) - np.array(actuals)) ** 2)
    rmse = np.sqrt(mse)
    
    print("-" * 70)
    print(f"\nMetrics:")
    print(f"  Mean Absolute Error (MAE): ${mae:.2f}")
    print(f"  Root Mean Squared Error (RMSE): ${rmse:.2f}")
    print(f"  Mean Error: ${avg_error:.2f}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test trained model")
    parser.add_argument("--model-path", type=str, 
                       default="flower_server/models/active_model.pt",
                       help="Path to model file")
    parser.add_argument("--data-dir", type=str, default="output",
                       help="Directory containing CSV files")
    parser.add_argument("--num-samples", type=int, default=10,
                       help="Number of samples to test")
    args = parser.parse_args()
    
    # Load model
    model = load_model(args.model_path)
    if model is None:
        return
    
    # Test model
    test_model_on_data(model, args.data_dir, args.num_samples)

if __name__ == "__main__":
    main()


