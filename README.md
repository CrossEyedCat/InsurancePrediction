# Federated Medical Insurance Cost Prediction

A federated learning system for predicting medical insurance costs using Flower.ai, with a web interface for medical workers to manage patient data and get predictions.

## Architecture Overview

This project implements a federated learning solution where:
- Medical institutions train models locally on their patient data
- Model weights are aggregated on a central Flower server
- Predictions are made using the aggregated global model
- Patient data never leaves the institution (privacy-preserving)

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   └── requirements.txt
│
├── flower_server/          # Flower aggregation server
│   ├── server.py           # Main server script
│   ├── model.py            # Model architecture
│   └── strategy.py         # Aggregation strategy
│
├── flower_client/          # Flower client for institutions
│   ├── client.py           # Client implementation
│   ├── data_loader.py      # Data loading and preprocessing
│   └── train.py            # Local training logic
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utilities
│   └── package.json
│
├── docker-compose.yml      # Docker orchestration
└── ARCHITECTURE.md         # Detailed architecture docs
```

## Features

- 🔐 **Authentication**: Role-based access for medical workers
- 👥 **Patient Management**: Add, view, edit patient records
- 🤖 **Federated Learning**: Privacy-preserving model training
- 📊 **Predictions**: Real-time insurance cost predictions
- 📈 **Monitoring**: Training metrics and model performance

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Node.js 18+ (for frontend development)

### Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd federated-medical-insurance
```

2. **Start services with Docker Compose**
```bash
docker-compose up --build
```

This will start:
- PostgreSQL database (port 5432)
- FastAPI backend (port 8000)
- Flower server (port 8080)
- React frontend (port 3000)

3. **Access the application**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Flower Server: http://localhost:8080

### Manual Setup

See individual README files in each directory for manual setup instructions.

## Usage

### 1. Authentication

Medical workers can log in with their credentials to access the system.

### 2. Patient Management

- View list of patients
- Add new patient records
- Edit existing patient information
- Search and filter patients

### 3. Federated Training

Training rounds are triggered automatically or manually:
- Each institution trains locally on their data
- Weights are aggregated on the Flower server
- Global model is updated and distributed

### 4. Predictions

- Enter patient data
- Get real-time insurance cost prediction
- View prediction history

## API Endpoints

See [API Documentation](http://localhost:8000/docs) for complete API reference.

## Configuration

Environment variables are configured in `.env` files:
- `backend/.env` - Backend configuration
- `flower_server/.env` - Flower server configuration
- `flower_client/.env` - Client configuration

## Development

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Flower Server
```bash
cd flower_server
python server.py
```

### Flower Client
```bash
cd flower_client
python client.py --institution-id 1
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## License

MIT License

## Contributing

See CONTRIBUTING.md for guidelines.

