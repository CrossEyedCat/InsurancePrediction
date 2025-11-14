"""
Neural network model for insurance cost prediction
"""
import torch
import torch.nn as nn


class InsuranceCostModel(nn.Module):
    """
    Neural network model for predicting medical insurance costs
    
    Input features:
    - age (normalized)
    - sex (encoded: 0=female, 1=male)
    - bmi (normalized)
    - children (normalized)
    - smoker (encoded: 0=no, 1=yes)
    - region (one-hot encoded: 4 features)
    
    Total input size: 9 features
    """
    
    def __init__(self, input_size: int = 9, hidden_size1: int = 128, 
                 hidden_size2: int = 64, hidden_size3: int = 32):
        super(InsuranceCostModel, self).__init__()
        
        self.fc1 = nn.Linear(input_size, hidden_size1)
        self.bn1 = nn.BatchNorm1d(hidden_size1)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.2)
        
        self.fc2 = nn.Linear(hidden_size1, hidden_size2)
        self.bn2 = nn.BatchNorm1d(hidden_size2)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.2)
        
        self.fc3 = nn.Linear(hidden_size2, hidden_size3)
        self.relu3 = nn.ReLU()
        
        self.fc4 = nn.Linear(hidden_size3, 1)
        
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
        x = self.relu3(x)
        
        x = self.fc4(x)
        return x


def get_model_parameters(model: nn.Module):
    """Get model parameters as list of numpy arrays"""
    return [val.cpu().numpy() for _, val in model.state_dict().items()]


def set_model_parameters(model: nn.Module, parameters):
    """Set model parameters from list of numpy arrays"""
    params_dict = zip(model.state_dict().keys(), parameters)
    state_dict = {k: torch.tensor(v) for k, v in params_dict}
    model.load_state_dict(state_dict, strict=True)
    return model

