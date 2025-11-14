"""
Neural network model for insurance cost prediction
"""
import torch
import torch.nn as nn


class InsuranceCostModel(nn.Module):
    """
    Neural network model for predicting medical insurance costs
    
    Input features (17 total):
    - age, sex, bmi, children, smoker (5 basic)
    - height, weight, systolic_bp, diastolic_bp, heart_rate (5 physical)
    - cholesterol, glucose, activity_level (3 health)
    - region (one-hot encoded: 4 features)
    
    Total input size: 17 features (13 base + 4 regions)
    """
    
    def __init__(self, input_size: int = 17, hidden_size1: int = 256, 
                 hidden_size2: int = 128, hidden_size3: int = 64, hidden_size4: int = 32):
        super(InsuranceCostModel, self).__init__()
        
        self.fc1 = nn.Linear(input_size, hidden_size1)
        self.bn1 = nn.BatchNorm1d(hidden_size1)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.3)
        
        self.fc2 = nn.Linear(hidden_size1, hidden_size2)
        self.bn2 = nn.BatchNorm1d(hidden_size2)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.3)
        
        self.fc3 = nn.Linear(hidden_size2, hidden_size3)
        self.bn3 = nn.BatchNorm1d(hidden_size3)
        self.relu3 = nn.ReLU()
        self.dropout3 = nn.Dropout(0.2)
        
        self.fc4 = nn.Linear(hidden_size3, hidden_size4)
        self.relu4 = nn.ReLU()
        
        self.fc5 = nn.Linear(hidden_size4, 1)
        
    def forward(self, x):
        """Forward pass"""
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.dropout1(x)
        
        x = self.fc2(x)
        x = self.bn2(x)
        x = self.relu2(x)
        x = self.dropout2(x)
        
        x = self.fc3(x)
        x = self.bn3(x)
        x = self.relu3(x)
        x = self.dropout3(x)
        
        x = self.fc4(x)
        x = self.relu4(x)
        
        x = self.fc5(x)
        return x


def get_model_parameters(model: nn.Module):
    """Get model parameters as list of numpy arrays"""
    return [val.cpu().numpy() for _, val in model.state_dict().items()]


def set_model_parameters(model: nn.Module, parameters):
    """Set model parameters from Flower Parameters object or list of numpy arrays"""
    import flwr as fl
    
    # Convert Parameters object to list of numpy arrays if needed
    if isinstance(parameters, fl.common.Parameters):
        parameters = fl.common.parameters_to_ndarrays(parameters)
    
    # Ensure parameters is a list
    if not isinstance(parameters, list):
        raise TypeError(f"Expected list or Parameters object, got {type(parameters)}")
    
    params_dict = zip(model.state_dict().keys(), parameters)
    state_dict = {k: torch.tensor(v) for k, v in params_dict}
    model.load_state_dict(state_dict, strict=True)
    return model

