# Federated Medical Insurance Cost Prediction - Architecture

## System Overview

This system implements a federated learning solution for predicting medical insurance costs using Flower.ai. The architecture consists of multiple components working together to enable privacy-preserving machine learning across distributed medical institutions.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Login UI   │  │  Patient UI  │  │ Prediction UI│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Auth API    │  │  Patient API │  │ Prediction   │          │
│  │              │  │              │  │    API       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│   Central Server        │   │   Flower Server          │
│  ┌──────────────────┐   │   │  (Aggregation Cluster)   │
│  │   PostgreSQL     │   │   │                          │
│  │   Database       │   │   │  - Federated Averaging   │
│  └──────────────────┘   │   │  - Weight Aggregation    │
│  ┌──────────────────┐   │   │  - Model Distribution    │
│  │   Model Storage  │   │   └──────────────────────────┘
│  └──────────────────┘   │              │
└──────────────────────────┘              │
                                          │
                ┌─────────────────────────┴──────────────┐
                ▼                                          ▼
┌──────────────────────────┐              ┌──────────────────────────┐
│   Flower Client 1        │              │   Flower Client N        │
│  (Medical Institution)   │              │  (Medical Institution)   │
│                          │              │                          │
│  - Local Training        │              │  - Local Training        │
│  - Weight Upload         │              │  - Weight Upload         │
│  - Model Download        │              │  - Model Download        │
│  ┌──────────────────┐    │              │  ┌──────────────────┐    │
│  │  Local Database  │    │              │  │  Local Database  │    │
│  │  (PostgreSQL)    │    │              │  │  (PostgreSQL)    │    │
│  └──────────────────┘    │              │  └──────────────────┘    │
└──────────────────────────┘              └──────────────────────────┘
```

## Component Details

### 1. Frontend Layer

**Technology Stack:**
- React.js or Next.js for UI
- Material-UI or Tailwind CSS for styling
- Axios for API communication
- React Router for navigation

**Components:**
- **Login/Authentication Page**
  - Medical worker credentials (email/password or OAuth)
  - Role-based access control
  - JWT token management

- **Patient Management Dashboard**
  - View patient list with pagination
  - Search and filter patients
  - Add new patient records
  - Edit patient information
  - View patient details

- **Prediction Interface**
  - Input form for patient data
  - Real-time cost prediction
  - Historical predictions view
  - Model performance metrics

**State Management:**
- Redux or Context API for global state
- Local storage for authentication tokens

### 2. API Gateway Layer

**Technology Stack:**
- FastAPI (Python) for REST API
- JWT for authentication
- SQLAlchemy for ORM
- Pydantic for data validation

**Endpoints:**

```
POST   /api/auth/login          - Medical worker authentication
POST   /api/auth/logout         - Logout
POST   /api/auth/refresh        - Refresh JWT token

GET    /api/patients            - List all patients (paginated)
GET    /api/patients/{id}       - Get patient details
POST   /api/patients            - Add new patient
PUT    /api/patients/{id}       - Update patient
DELETE /api/patients/{id}       - Delete patient

POST   /api/predictions         - Get insurance cost prediction
GET    /api/predictions/history - Get prediction history
GET    /api/model/status        - Get federated model status
GET    /api/model/metrics       - Get model performance metrics
```

**Authentication Flow:**
1. Medical worker logs in with credentials
2. Server validates credentials against database
3. JWT token issued with role and institution ID
4. Token stored in HTTP-only cookie or localStorage
5. Subsequent requests include token in Authorization header

### 3. Central Server

**Technology Stack:**
- PostgreSQL for data storage
- SQLAlchemy for database operations
- Redis for caching (optional)
- Celery for background tasks (optional)

**Database Schema:**

```sql
-- Medical Workers Table
CREATE TABLE medical_workers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,  -- 'doctor', 'nurse', 'admin'
    institution_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Medical Institutions Table
CREATE TABLE institutions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patients Table
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    institution_id INTEGER REFERENCES institutions(id),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    sex VARCHAR(10) NOT NULL,
    bmi DECIMAL(5,2),
    children INTEGER DEFAULT 0,
    smoker VARCHAR(3) DEFAULT 'no',
    region VARCHAR(50),
    insurance_cost DECIMAL(10,2),
    created_by INTEGER REFERENCES medical_workers(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Model Versions Table
CREATE TABLE model_versions (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) UNIQUE NOT NULL,
    model_path VARCHAR(500) NOT NULL,
    training_round INTEGER,
    accuracy DECIMAL(5,4),
    mse DECIMAL(10,4),
    mae DECIMAL(10,4),
    trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT FALSE
);

-- Training Rounds Table
CREATE TABLE training_rounds (
    id SERIAL PRIMARY KEY,
    round_number INTEGER NOT NULL,
    clients_participated INTEGER,
    aggregation_method VARCHAR(50),
    status VARCHAR(50),  -- 'started', 'in_progress', 'completed', 'failed'
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    metrics JSONB
);
```

**Data Flow:**
1. Frontend sends patient data to API
2. API validates and stores in PostgreSQL
3. Data is partitioned by institution_id for federated learning
4. Background job triggers training round periodically

### 4. Flower Server (Aggregation Cluster)

**Technology Stack:**
- Flower (flwr) framework
- PyTorch or TensorFlow for model definition
- NumPy for numerical operations

**Server Configuration:**

```python
# Aggregation Strategy
- Federated Averaging (FedAvg)
- Federated Stochastic Gradient Descent (FedSGD)
- Custom aggregation strategies

# Server Parameters
- Number of rounds: Configurable
- Minimum clients: 2
- Fraction fit: 0.5 (50% of clients per round)
- Fraction evaluate: 0.5
- Min available clients: 2
```

**Server Responsibilities:**
1. **Model Initialization**
   - Initialize global model with random weights
   - Define model architecture (neural network)
   - Set hyperparameters (learning rate, batch size, epochs)

2. **Client Selection**
   - Select subset of available clients for each round
   - Ensure minimum number of clients before starting

3. **Weight Aggregation**
   - Receive model weights/gradients from clients
   - Aggregate using Federated Averaging:
     ```
     w_global = Σ(n_i * w_i) / Σ(n_i)
     ```
     where n_i is the number of samples from client i

4. **Model Distribution**
   - Send aggregated model to all clients
   - Store model checkpoints
   - Track training metrics

5. **Evaluation**
   - Aggregate evaluation metrics from clients
   - Calculate global model performance
   - Store metrics in database

**Model Architecture:**
```python
Input Features:
- age (normalized)
- sex (one-hot encoded)
- bmi (normalized)
- children (normalized)
- smoker (one-hot encoded)
- region (one-hot encoded)

Model:
- Input Layer: 6 features
- Hidden Layer 1: 128 neurons, ReLU
- Hidden Layer 2: 64 neurons, ReLU
- Hidden Layer 3: 32 neurons, ReLU
- Output Layer: 1 neuron (insurance cost)

Loss Function: Mean Squared Error (MSE)
Optimizer: Adam
```

### 5. Flower Clients (Medical Institutions)

**Technology Stack:**
- Flower client library
- PyTorch/TensorFlow for local training
- PostgreSQL for local data storage
- NumPy, Pandas for data processing

**Client Responsibilities:**

1. **Data Management**
   - Connect to local PostgreSQL database
   - Load patient data for institution
   - Preprocess data (normalization, encoding)
   - Split into train/validation sets

2. **Local Training**
   - Receive global model from server
   - Train model on local data for N epochs
   - Use local optimizer (SGD/Adam)
   - Validate on local validation set

3. **Weight Upload**
   - Extract model weights after training
   - Send weights to Flower server
   - Optionally send gradients instead of weights
   - Send local metrics (loss, accuracy, sample count)

4. **Model Download**
   - Receive aggregated model from server
   - Update local model
   - Optionally save model checkpoint

**Client Configuration:**
```python
# Training Parameters
- Local epochs: 5
- Batch size: 32
- Learning rate: 0.001
- Optimizer: Adam

# Data Parameters
- Train/validation split: 80/20
- Data normalization: StandardScaler
- Feature encoding: One-hot for categorical
```

## Training Workflow

### Round-Based Training Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                    Training Round N                          │
└─────────────────────────────────────────────────────────────┘

1. Server Initialization
   ├─ Initialize/load global model
   ├─ Select clients for round (fraction_fit)
   └─ Broadcast model to selected clients

2. Client Training (Parallel)
   ├─ Client 1: Load local data → Train → Send weights
   ├─ Client 2: Load local data → Train → Send weights
   └─ Client N: Load local data → Train → Send weights

3. Server Aggregation
   ├─ Receive weights from all clients
   ├─ Aggregate weights (FedAvg)
   ├─ Update global model
   └─ Calculate global metrics

4. Model Evaluation (Optional)
   ├─ Broadcast model to evaluation clients
   ├─ Clients evaluate on local test set
   ├─ Aggregate evaluation metrics
   └─ Store metrics in database

5. Model Storage
   ├─ Save model checkpoint
   ├─ Update model version in database
   └─ Mark as active if best performance

6. Next Round
   └─ Repeat from step 1 until max_rounds
```

### Periodic Training Trigger

**Option 1: Time-based**
- Cron job runs every X hours/days
- Checks if new data available
- Triggers training round if threshold met

**Option 2: Data-based**
- Monitor new patient records
- Trigger training when N new records added
- Queue training requests

**Option 3: Manual**
- Admin dashboard trigger
- On-demand training initiation
- Scheduled training rounds

## Prediction Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    Prediction Request                        │
└─────────────────────────────────────────────────────────────┘

1. Frontend Request
   ├─ Medical worker inputs patient data
   ├─ Sends POST /api/predictions
   └─ Includes JWT token

2. API Processing
   ├─ Validate JWT token
   ├─ Validate patient data
   ├─ Preprocess features
   └─ Request prediction from Flower server

3. Model Inference
   ├─ Load latest active model
   ├─ Preprocess input features
   ├─ Run forward pass
   └─ Return insurance cost prediction

4. Response
   ├─ Return prediction to frontend
   ├─ Optionally save prediction history
   └─ Display result to medical worker
```

## Security & Privacy

### Data Privacy
- **Federated Learning**: Patient data never leaves institution
- **Differential Privacy**: Add noise to gradients (optional)
- **Secure Aggregation**: Encrypt weights before transmission
- **Access Control**: Role-based permissions

### Authentication & Authorization
- JWT tokens with expiration
- Role-based access control (RBAC)
- Institution-level data isolation
- Audit logging for data access

### Network Security
- HTTPS/TLS for all communications
- Certificate-based authentication for Flower clients
- Firewall rules for Flower server
- VPN for client-server communication (optional)

## Deployment Architecture

### Development Environment
```
Frontend (localhost:3000)
    ↓
API Server (localhost:8000)
    ↓
PostgreSQL (localhost:5432)
    ↓
Flower Server (localhost:8080)
    ↓
Flower Clients (localhost:8081, 8082, ...)
```

### Production Environment
```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                        │
└─────────────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────┐      ┌──────────────┐
│  Frontend    │      │   API Server │
│  (CDN)       │      │  (Multiple)  │
└──────────────┘      └──────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │  PostgreSQL  │
                    │  (Primary +  │
                    │   Replicas)  │
                    └──────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │ Flower Server│
                    │  (Cluster)   │
                    └──────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Institution  │    │ Institution  │    │ Institution  │
│   Client 1   │    │   Client 2   │    │   Client N   │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Monitoring & Logging

### Metrics to Track
- Training rounds completed
- Number of clients per round
- Model accuracy/loss over time
- Prediction latency
- API request rates
- Error rates

### Logging
- Training events (round start/end, aggregation)
- API requests (endpoint, user, timestamp)
- Data operations (create, update, delete)
- Error logs with stack traces

### Dashboards
- Model performance over time
- Client participation rates
- Prediction statistics
- System health metrics

## Scalability Considerations

### Horizontal Scaling
- Multiple API server instances
- PostgreSQL read replicas
- Flower server cluster (future)
- Client auto-scaling

### Performance Optimization
- Database indexing on frequently queried columns
- Redis caching for predictions
- Model quantization for faster inference
- Batch prediction API

### Data Management
- Data partitioning by institution
- Archival strategy for old data
- Backup and recovery procedures
- Data retention policies

## Future Enhancements

1. **Advanced Aggregation**
   - FedProx for non-IID data
   - FedAvgM for momentum
   - Adaptive aggregation strategies

2. **Privacy Enhancements**
   - Differential privacy
   - Homomorphic encryption
   - Secure multi-party computation

3. **Model Improvements**
   - Hyperparameter tuning
   - Model compression
   - Ensemble methods

4. **Additional Features**
   - Real-time predictions
   - Batch predictions
   - Model explainability
   - A/B testing framework

