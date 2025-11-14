# Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM available
- Ports 3000, 5432, 8000, 8080 available

## Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd federated-medical-insurance
```

2. **Create environment files**

Create `.env` file in root directory:
```env
DB_USER=medical_user
DB_PASSWORD=medical_pass
DB_NAME=medical_insurance
SECRET_KEY=your-secret-key-change-in-production
```

3. **Start all services**
```bash
docker-compose up --build
```

This will start:
- PostgreSQL database
- FastAPI backend (http://localhost:8000)
- Flower server (http://localhost:8080)
- Flower clients (2 instances)
- React frontend (http://localhost:3000)

4. **Access the application**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Flower Server: http://localhost:8080

## Initial Setup

### Create Medical Workers

You can create medical workers through the database or API:

```sql
-- Example: Create a medical worker
-- Password: 'password123' (hash it properly in production)
INSERT INTO medical_workers (email, password_hash, name, role, institution_id)
VALUES ('doctor@hospital.com', '$2b$12$...', 'Dr. Smith', 'doctor', 1);
```

Or use the API:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "doctor@hospital.com", "password": "password123", "name": "Dr. Smith", "role": "doctor", "institution_id": 1}'
```

### Add Sample Data

Add patient data through the frontend or API:

```bash
curl -X POST "http://localhost:8000/api/patients" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "age": 45,
    "sex": "male",
    "bmi": 28.5,
    "children": 2,
    "smoker": "no",
    "region": "northeast",
    "insurance_cost": 8500.0
  }'
```

## Federated Training

### Manual Training Trigger

Training rounds can be triggered manually or automatically:

1. **Ensure clients are running** - Flower clients should be connected to the server
2. **Start training** - The server will automatically start training when clients connect
3. **Monitor progress** - Check logs or use the API to monitor training rounds

### Check Model Status

```bash
curl http://localhost:8000/api/model/status
```

### View Training Metrics

```bash
curl http://localhost:8000/api/model/metrics
```

## Production Deployment

### Environment Variables

Set proper environment variables for production:

```env
# Database
DB_USER=your_db_user
DB_PASSWORD=strong_password
DB_NAME=medical_insurance

# Security
SECRET_KEY=generate-strong-secret-key

# Flower
NUM_ROUNDS=20
MIN_CLIENTS=3
FRACTION_FIT=0.6
```

### Security Considerations

1. **Change default passwords** - Use strong passwords for database and JWT secret
2. **Enable HTTPS** - Use reverse proxy (nginx) with SSL certificates
3. **Firewall rules** - Restrict access to Flower server port
4. **Database backups** - Set up regular database backups
5. **Monitoring** - Set up logging and monitoring

### Scaling

To add more Flower clients:

1. Add new service to `docker-compose.yml`:
```yaml
flower-client-3:
  build:
    context: ./flower_client
  environment:
    CLIENT_ID: 3
    INSTITUTION_ID: 3
    DATABASE_URL: postgresql://...
    FLOWER_SERVER_URL: http://flower-server:8080
  command: python client.py --institution-id 3
```

2. Restart services:
```bash
docker-compose up -d flower-client-3
```

## Troubleshooting

### Database Connection Issues

Check if PostgreSQL is running:
```bash
docker-compose ps db
```

Check logs:
```bash
docker-compose logs db
```

### Flower Client Not Connecting

1. Check if Flower server is running
2. Verify network connectivity
3. Check client logs:
```bash
docker-compose logs flower-client-1
```

### Model Not Loading

1. Check if model file exists in `models/` directory
2. Verify model path in environment variables
3. Check prediction service logs

## Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f flower-server
```

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database
docker-compose exec db pg_isready -U medical_user
```

## Backup and Restore

### Backup Database

```bash
docker-compose exec db pg_dump -U medical_user medical_insurance > backup.sql
```

### Restore Database

```bash
docker-compose exec -T db psql -U medical_user medical_insurance < backup.sql
```

## Maintenance

### Update Models

1. Stop services
2. Backup current models
3. Update code
4. Restart services

### Database Migrations

Use Alembic for database migrations:
```bash
cd backend
alembic upgrade head
```

