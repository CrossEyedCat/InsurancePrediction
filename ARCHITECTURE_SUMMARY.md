# Architecture Summary - Federated Medical Insurance Cost Prediction

## System Overview

This system implements a **federated learning** solution for predicting medical insurance costs using **Flower.ai**. The architecture enables privacy-preserving machine learning where medical institutions train models locally on their patient data, and only model weights (not raw data) are shared with a central aggregation server.

## Key Components

### 1. **Frontend Layer** (React.js)
- **Authentication**: Medical workers login with credentials
- **Patient Management**: View, add, edit patient records
- **Predictions**: Real-time insurance cost predictions
- **Dashboard**: System overview and metrics

### 2. **API Gateway** (FastAPI)
- **REST API** for all frontend operations
- **JWT Authentication** for secure access
- **Patient CRUD** operations
- **Prediction endpoints** for model inference
- **Model status** and metrics endpoints

### 3. **Central Database** (PostgreSQL)
- **Medical Workers**: User accounts and authentication
- **Institutions**: Medical facility information
- **Patients**: Patient records with insurance cost data
- **Model Versions**: Track trained model versions
- **Training Rounds**: Federated learning round history

### 4. **Flower Server** (Aggregation Cluster)
- **Federated Averaging (FedAvg)**: Aggregates model weights from clients
- **Model Distribution**: Sends aggregated model to clients
- **Round Management**: Coordinates training rounds
- **Model Storage**: Saves model checkpoints

### 5. **Flower Clients** (Medical Institutions)
- **Local Training**: Train models on institution's patient data
- **Weight Upload**: Send model weights to server (not raw data)
- **Model Download**: Receive aggregated model from server
- **Data Privacy**: Patient data never leaves the institution

## Data Flow

### Training Cycle

```
1. Server Initialization
   └─ Initialize global model with random weights
   └─ Broadcast model to selected clients

2. Client Training (Parallel)
   ├─ Client 1: Load local data → Train → Send weights
   ├─ Client 2: Load local data → Train → Send weights
   └─ Client N: Load local data → Train → Send weights

3. Server Aggregation
   └─ Receive weights from all clients
   └─ Aggregate using Federated Averaging
   └─ Update global model
   └─ Save model checkpoint

4. Model Distribution
   └─ Send aggregated model to all clients
   └─ Clients update local models

5. Repeat for next round
```

### Prediction Flow

```
1. Medical Worker → Frontend
   └─ Inputs patient data

2. Frontend → API
   └─ POST /api/predictions
   └─ JWT authentication

3. API → Prediction Service
   └─ Load active model
   └─ Preprocess features
   └─ Run inference

4. Prediction Service → API
   └─ Return predicted cost

5. API → Frontend
   └─ Display prediction
```

## Privacy & Security

### Data Privacy
- ✅ **Federated Learning**: Patient data never leaves institution
- ✅ **Weight Sharing Only**: Only model weights/gradients shared
- ✅ **No Raw Data Transmission**: Original patient records stay local

### Security Measures
- ✅ **JWT Authentication**: Secure API access
- ✅ **Role-Based Access**: Different permissions for doctors, nurses, admins
- ✅ **Institution Isolation**: Data access restricted by institution
- ✅ **HTTPS/TLS**: Encrypted communication (in production)

## Model Architecture

### Neural Network
- **Input Layer**: 9 features (age, sex, bmi, children, smoker, region)
- **Hidden Layers**: 128 → 64 → 32 neurons
- **Output Layer**: 1 neuron (insurance cost)
- **Activation**: ReLU with BatchNorm and Dropout
- **Loss Function**: Mean Squared Error (MSE)
- **Optimizer**: Adam

### Training Configuration
- **Local Epochs**: 5 per round
- **Batch Size**: 32
- **Learning Rate**: 0.001
- **Rounds**: 10-20 (configurable)
- **Min Clients**: 2 (configurable)

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Load Balancer / Nginx            │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────┐      ┌──────────────┐
│   Frontend   │      │  API Server  │
│  (React)     │      │  (FastAPI)   │
└──────────────┘      └──────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │  PostgreSQL  │
                    │   Database   │
                    └──────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │Flower Server │
                    │ (Aggregation)│
                    └──────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Institution  │    │ Institution  │    │ Institution  │
│   Client 1   │    │   Client 2   │    │   Client N   │
│              │    │              │    │              │
│ Local Data   │    │ Local Data   │    │ Local Data   │
│ Local Train  │    │ Local Train  │    │ Local Train  │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Key Features

### For Medical Workers
- 🔐 Secure authentication and authorization
- 👥 Patient record management (CRUD operations)
- 📊 Real-time insurance cost predictions
- 📈 View model performance metrics

### For System Administrators
- 🤖 Federated learning orchestration
- 📊 Training round monitoring
- 🔄 Model version management
- 📈 System health monitoring

### For Data Scientists
- 🧪 Federated learning experimentation
- 📊 Training metrics and analytics
- 🔄 Model versioning and rollback
- 📈 Performance tracking

## Scalability

### Horizontal Scaling
- Multiple API server instances
- Multiple Flower clients (institutions)
- Database read replicas
- Load balancing

### Performance Optimization
- Model caching
- Database indexing
- Batch predictions
- Async processing

## Future Enhancements

1. **Advanced Aggregation**
   - FedProx for non-IID data
   - Adaptive aggregation strategies
   - Differential privacy

2. **Model Improvements**
   - Hyperparameter tuning
   - Model compression
   - Ensemble methods

3. **Additional Features**
   - Real-time training monitoring
   - Model explainability
   - A/B testing framework
   - Automated retraining

## Technology Stack

- **Frontend**: React.js, Material-UI
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Federated Learning**: Flower (flwr)
- **ML Framework**: PyTorch
- **Containerization**: Docker, Docker Compose
- **Authentication**: JWT

## Benefits

1. **Privacy-Preserving**: Patient data never leaves institutions
2. **Collaborative Learning**: Multiple institutions contribute to model
3. **Regulatory Compliance**: Meets data privacy regulations
4. **Scalable**: Easy to add new institutions
5. **Accurate**: Better predictions with more diverse data

