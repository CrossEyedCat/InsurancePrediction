# Quick Start Guide

## Prerequisites

- Docker and Docker Compose
- 4GB+ RAM
- Ports 3000, 5432, 8000, 8080 available

## Step 1: Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd federated-medical-insurance

# Create .env file (optional, defaults are set)
cat > .env << EOF
DB_USER=medical_user
DB_PASSWORD=medical_pass
DB_NAME=medical_insurance
SECRET_KEY=your-secret-key-change-in-production
EOF
```

## Step 2: Start Services

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

This starts:
- PostgreSQL (port 5432)
- FastAPI Backend (port 8000)
- Flower Server (port 8080)
- Flower Clients (2 instances)
- React Frontend (port 3000)

## Step 3: Access Application

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Step 4: Create Test User

The database is initialized with sample data. You can also create users via SQL:

```sql
-- Connect to database
docker-compose exec db psql -U medical_user medical_insurance

-- Create user (password: password123)
-- Note: In production, use proper password hashing
INSERT INTO medical_workers (email, password_hash, name, role, institution_id)
VALUES ('test@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'Test User', 'doctor', 1);
```

## Step 5: Login and Use

1. Open http://localhost:3000
2. Login with test credentials
3. Add patients through the UI
4. Get predictions for insurance costs
5. Monitor federated training rounds

## Step 6: Trigger Training

Training starts automatically when:
- Clients connect to Flower server
- Minimum number of clients available
- Training rounds configured

Monitor training:
```bash
# View Flower server logs
docker-compose logs -f flower-server

# View client logs
docker-compose logs -f flower-client-1

# Check model status via API
curl http://localhost:8000/api/model/status
```

## Troubleshooting

### Services not starting
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart
```

### Database connection issues
```bash
# Check database status
docker-compose ps db

# View database logs
docker-compose logs db
```

### Flower clients not connecting
```bash
# Check if server is running
docker-compose ps flower-server

# View client logs
docker-compose logs flower-client-1
```

## Next Steps

1. Add more patient data through the UI
2. Monitor training rounds
3. Check model performance metrics
4. Make predictions for new patients
5. Review [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture
6. Review [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment

## Development Mode

For development, you can run services separately:

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Flower Server
cd flower_server
python server.py

# Flower Client
cd flower_client
python client.py --institution-id 1

# Frontend
cd frontend
npm install
npm start
```

