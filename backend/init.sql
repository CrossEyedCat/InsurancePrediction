-- Initialize database with sample data

-- Create sample institutions
INSERT INTO institutions (id, name, address) VALUES
(1, 'City General Hospital', '123 Main St, City'),
(2, 'Regional Medical Center', '456 Oak Ave, City')
ON CONFLICT (id) DO NOTHING;

-- Create sample medical workers (password: 'password123' hashed)
-- In production, use proper password hashing
INSERT INTO medical_workers (id, email, password_hash, name, role, institution_id) VALUES
(1, 'doctor1@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'Dr. John Smith', 'doctor', 1),
(2, 'nurse1@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'Jane Doe', 'nurse', 1),
(3, 'doctor2@medical.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'Dr. Sarah Johnson', 'doctor', 2)
ON CONFLICT (id) DO NOTHING;

