# Project Structure

## Complete File Tree

```
federated-medical-insurance/
│
├── ARCHITECTURE.md              # Detailed architecture documentation
├── ARCHITECTURE_SUMMARY.md      # Architecture summary
├── DEPLOYMENT.md                # Deployment guide
├── PROJECT_STRUCTURE.md         # This file
├── QUICK_START.md               # Quick start guide
├── README.md                    # Main README
├── requirements.txt             # Root requirements (if needed)
├── docker-compose.yml           # Docker orchestration
├── .gitignore                   # Git ignore rules
│
├── backend/                     # FastAPI Backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── init.sql                 # Database initialization
│   └── app/
│       ├── __init__.py
│       ├── main.py              # FastAPI application
│       ├── database.py           # Database configuration
│       │
│       ├── api/                  # API Routes
│       │   ├── __init__.py
│       │   ├── auth.py          # Authentication endpoints
│       │   ├── patients.py      # Patient management
│       │   ├── predictions.py   # Prediction endpoints
│       │   └── model.py         # Model status/metrics
│       │
│       ├── models/              # Database Models
│       │   ├── __init__.py
│       │   ├── medical_worker.py
│       │   ├── institution.py
│       │   ├── patient.py
│       │   ├── model_version.py
│       │   └── training_round.py
│       │
│       ├── schemas/             # Pydantic Schemas
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── patient.py
│       │   └── prediction.py
│       │
│       ├── services/            # Business Logic
│       │   ├── __init__.py
│       │   └── prediction_service.py
│       │
│       └── utils/               # Utilities
│           └── __init__.py
│
├── flower_server/               # Flower Aggregation Server
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── __init__.py
│   ├── server.py                # Flower server implementation
│   └── model.py                 # Neural network model
│
├── flower_client/               # Flower Clients
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── __init__.py
│   ├── client.py                # Flower client implementation
│   └── data_loader.py          # Data loading and preprocessing
│
└── frontend/                    # React Frontend
    ├── Dockerfile
    ├── package.json
    ├── public/
    │   └── index.html
    └── src/
        ├── index.js
        ├── index.css
        ├── App.js
        ├── context/
        │   └── AuthContext.js   # Authentication context
        ├── components/
        │   └── Layout.js        # Main layout component
        └── pages/
            ├── Login.js         # Login page
            ├── Dashboard.js     # Dashboard
            ├── Patients.js      # Patient management
            └── Predictions.js   # Prediction interface
```

## Component Descriptions

### Backend (`backend/`)

**FastAPI Application** providing REST API for:
- Authentication and authorization
- Patient CRUD operations
- Insurance cost predictions
- Model status and metrics

**Key Files:**
- `app/main.py`: FastAPI app initialization
- `app/database.py`: SQLAlchemy database setup
- `app/api/`: API route handlers
- `app/models/`: SQLAlchemy database models
- `app/schemas/`: Pydantic validation schemas
- `app/services/`: Business logic services

### Flower Server (`flower_server/`)

**Federated Learning Aggregation Server** that:
- Coordinates training rounds
- Aggregates model weights from clients
- Distributes aggregated model to clients
- Saves model checkpoints

**Key Files:**
- `server.py`: Flower server with FedAvg strategy
- `model.py`: Neural network architecture

### Flower Client (`flower_client/`)

**Federated Learning Clients** for each medical institution:
- Load local patient data
- Train models locally
- Send weights to server (not raw data)
- Receive aggregated model

**Key Files:**
- `client.py`: Flower client implementation
- `data_loader.py`: Data loading and preprocessing

### Frontend (`frontend/`)

**React.js Web Application** with:
- User authentication
- Patient management interface
- Prediction interface
- Dashboard and metrics

**Key Files:**
- `src/App.js`: Main application component
- `src/context/AuthContext.js`: Authentication state management
- `src/pages/`: Page components
- `src/components/`: Reusable components

## Data Flow

### Training Flow
1. Flower Server initializes global model
2. Server selects clients for training round
3. Clients train locally on their data
4. Clients send weights to server
5. Server aggregates weights (FedAvg)
6. Server distributes aggregated model
7. Repeat for next round

### Prediction Flow
1. User inputs patient data in frontend
2. Frontend sends request to API
3. API validates and preprocesses data
4. Prediction service loads active model
5. Model makes prediction
6. Result returned to frontend

### Data Storage
- **PostgreSQL**: All persistent data
  - Medical workers
  - Institutions
  - Patients
  - Model versions
  - Training rounds
- **File System**: Model checkpoints
  - Saved in `models/` directory
  - Versioned by training round

## Configuration

### Environment Variables

**Backend:**
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration

**Flower Server:**
- `SERVER_ADDRESS`: Server bind address
- `SERVER_PORT`: Server port
- `NUM_ROUNDS`: Number of training rounds
- `MIN_CLIENTS`: Minimum clients per round
- `FRACTION_FIT`: Fraction of clients for training

**Flower Client:**
- `INSTITUTION_ID`: Institution identifier
- `DATABASE_URL`: Database connection
- `FLOWER_SERVER_URL`: Server address
- `LOCAL_EPOCHS`: Local training epochs
- `BATCH_SIZE`: Training batch size
- `LEARNING_RATE`: Learning rate

## Dependencies

### Backend
- FastAPI: Web framework
- SQLAlchemy: ORM
- Pydantic: Data validation
- PyTorch: ML framework (for predictions)
- JWT: Authentication

### Flower Server/Client
- Flower (flwr): Federated learning framework
- PyTorch: Neural network framework
- NumPy, Pandas: Data processing

### Frontend
- React: UI framework
- Material-UI: Component library
- Axios: HTTP client
- React Router: Routing

## Deployment

All components are containerized with Docker:
- `docker-compose.yml`: Orchestrates all services
- Individual `Dockerfile` in each component directory
- Shared volumes for model storage
- Network configuration for service communication

## Development

Each component can be developed independently:
- Backend: `cd backend && uvicorn app.main:app --reload`
- Flower Server: `cd flower_server && python server.py`
- Flower Client: `cd flower_client && python client.py --institution-id 1`
- Frontend: `cd frontend && npm start`

## Testing

- Backend: `pytest` (when tests are added)
- Frontend: `npm test` (when tests are added)
- Integration: Manual testing via API and UI

## Next Steps

1. Add unit tests for each component
2. Add integration tests
3. Set up CI/CD pipeline
4. Add monitoring and logging
5. Implement model versioning
6. Add automated retraining
7. Enhance security measures
8. Optimize performance

