-- ============================================================================
-- Federated Medical Insurance Cost Prediction - Database Schema
-- PostgreSQL CREATE Statements
-- ============================================================================

-- Enable UUID extension (if needed)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- Core Tables
-- ============================================================================

-- Institutions (Medical Facilities)
CREATE TABLE IF NOT EXISTS institutions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(50),
    email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Medical Workers
CREATE TABLE IF NOT EXISTS medical_workers (
    id SERIAL PRIMARY KEY,
    institution_id INTEGER NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('doctor', 'nurse', 'admin', 'physician_assistant', 'nurse_practitioner')),
    phone VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_medical_workers_institution ON medical_workers(institution_id);
CREATE INDEX idx_medical_workers_email ON medical_workers(email);

-- ============================================================================
-- Patient Core Table
-- ============================================================================

CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    institution_id INTEGER NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,
    created_by INTEGER REFERENCES medical_workers(id) ON DELETE SET NULL,
    
    -- Basic Demographics
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    age INTEGER GENERATED ALWAYS AS (EXTRACT(YEAR FROM AGE(date_of_birth))) STORED,
    sex VARCHAR(10) NOT NULL CHECK (sex IN ('male', 'female', 'other')),
    marital_status VARCHAR(50) CHECK (marital_status IN ('single', 'married', 'divorced', 'widowed', 'domestic_partner')),
    number_of_dependents INTEGER DEFAULT 0 CHECK (number_of_dependents >= 0 AND number_of_dependents <= 20),
    
    -- Insurance Cost (target variable for training)
    insurance_cost DECIMAL(10, 2),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patients_institution ON patients(institution_id);
CREATE INDEX idx_patients_created_by ON patients(created_by);
CREATE INDEX idx_patients_age ON patients(age);
CREATE INDEX idx_patients_sex ON patients(sex);

-- ============================================================================
-- Physical Measurements
-- ============================================================================

CREATE TABLE IF NOT EXISTS patient_physical_measurements (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    
    -- Body Metrics
    height_cm DECIMAL(5, 2) CHECK (height_cm > 0 AND height_cm < 300),
    weight_kg DECIMAL(5, 2) CHECK (weight_kg > 0 AND weight_kg < 500),
    bmi DECIMAL(4, 2) CHECK (bmi >= 10 AND bmi <= 50),
    body_fat_percentage DECIMAL(4, 2) CHECK (body_fat_percentage >= 5 AND body_fat_percentage <= 50),
    waist_circumference DECIMAL(5, 2) CHECK (waist_circumference > 0),
    hip_circumference DECIMAL(5, 2) CHECK (hip_circumference > 0),
    waist_to_hip_ratio DECIMAL(3, 2) CHECK (waist_to_hip_ratio >= 0.5 AND waist_to_hip_ratio <= 1.5),
    
    -- Vital Signs
    systolic_bp INTEGER CHECK (systolic_bp >= 90 AND systolic_bp <= 200),
    diastolic_bp INTEGER CHECK (diastolic_bp >= 60 AND diastolic_bp <= 120),
    resting_heart_rate INTEGER CHECK (resting_heart_rate >= 40 AND resting_heart_rate <= 120),
    max_heart_rate INTEGER CHECK (max_heart_rate >= 100 AND max_heart_rate <= 220),
    
    measured_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_patient_physical_measurements_patient ON patient_physical_measurements(patient_id);
CREATE INDEX idx_patient_physical_measurements_bmi ON patient_physical_measurements(bmi);

-- ============================================================================
-- Lifestyle Factors
-- ============================================================================

CREATE TABLE IF NOT EXISTS patient_lifestyle (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    
    -- Smoking
    smoking_status VARCHAR(20) CHECK (smoking_status IN ('never', 'former', 'current')),
    years_smoking INTEGER CHECK (years_smoking >= 0 AND years_smoking <= 80),
    cigarettes_per_day INTEGER CHECK (cigarettes_per_day >= 0 AND cigarettes_per_day <= 100),
    pack_years DECIMAL(5, 2) CHECK (pack_years >= 0),
    quit_date DATE,
    years_since_quitting INTEGER CHECK (years_since_quitting >= 0),
    
    -- Alcohol
    alcohol_consumption VARCHAR(20) CHECK (alcohol_consumption IN ('none', 'occasional', 'moderate', 'heavy')),
    drinks_per_week INTEGER CHECK (drinks_per_week >= 0 AND drinks_per_week <= 100),
    drinking_frequency VARCHAR(20) CHECK (drinking_frequency IN ('daily', 'weekly', 'monthly', 'rarely', 'never')),
    alcohol_type VARCHAR(50),
    recreational_drug_use BOOLEAN DEFAULT FALSE,
    drug_types TEXT,
    
    -- Exercise
    physical_activity_level VARCHAR(20) CHECK (physical_activity_level IN ('sedentary', 'light', 'moderate', 'active', 'very_active')),
    exercise_hours_per_week DECIMAL(4, 2) CHECK (exercise_hours_per_week >= 0 AND exercise_hours_per_week <= 50),
    exercise_types VARCHAR(255),
    exercise_intensity VARCHAR(20) CHECK (exercise_intensity IN ('low', 'moderate', 'high')),
    steps_per_day INTEGER CHECK (steps_per_day >= 0 AND steps_per_day <= 50000),
    active_minutes_per_week INTEGER CHECK (active_minutes_per_week >= 0),
    sedentary_hours_per_day DECIMAL(3, 1) CHECK (sedentary_hours_per_day >= 0 AND sedentary_hours_per_day <= 24),
    
    -- Diet
    diet_type VARCHAR(50) CHECK (diet_type IN ('omnivore', 'vegetarian', 'vegan', 'pescatarian', 'keto', 'paleo', 'mediterranean', 'other')),
    meals_per_day INTEGER CHECK (meals_per_day >= 1 AND meals_per_day <= 6),
    fast_food_frequency VARCHAR(20) CHECK (fast_food_frequency IN ('daily', 'weekly', 'monthly', 'rarely', 'never')),
    processed_food_frequency VARCHAR(20) CHECK (processed_food_frequency IN ('daily', 'weekly', 'monthly', 'rarely', 'never')),
    fruit_vegetable_servings DECIMAL(4, 2) CHECK (fruit_vegetable_servings >= 0 AND fruit_vegetable_servings <= 20),
    water_intake_liters DECIMAL(4, 2) CHECK (water_intake_liters >= 0 AND water_intake_liters <= 10),
    
    -- Sleep
    sleep_hours_per_night DECIMAL(3, 1) CHECK (sleep_hours_per_night >= 3 AND sleep_hours_per_night <= 12),
    sleep_quality VARCHAR(20) CHECK (sleep_quality IN ('poor', 'fair', 'good', 'excellent')),
    sleep_disorders BOOLEAN DEFAULT FALSE,
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_patient_lifestyle_patient ON patient_lifestyle(patient_id);
CREATE INDEX idx_patient_lifestyle_smoking ON patient_lifestyle(smoking_status);

-- ============================================================================
-- Medical History
-- ============================================================================

CREATE TABLE IF NOT EXISTS patient_medical_history (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    condition_type VARCHAR(50) NOT NULL CHECK (condition_type IN (
        'diabetes', 'hypertension', 'heart_disease', 'asthma', 'copd', 
        'depression', 'anxiety', 'cancer', 'autoimmune', 'other'
    )),
    condition_name VARCHAR(255) NOT NULL,
    severity VARCHAR(20) CHECK (severity IN ('mild', 'moderate', 'severe', 'critical')),
    diagnosis_date DATE,
    years_since_diagnosis INTEGER CHECK (years_since_diagnosis >= 0),
    medication_controlled BOOLEAN,
    complications TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patient_medical_history_patient ON patient_medical_history(patient_id);
CREATE INDEX idx_patient_medical_history_condition ON patient_medical_history(condition_type);

-- ============================================================================
-- Medications
-- ============================================================================

CREATE TABLE IF NOT EXISTS patient_medications (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    medication_name VARCHAR(255) NOT NULL,
    dosage VARCHAR(100),
    frequency VARCHAR(100),
    years_of_use DECIMAL(4, 2) CHECK (years_of_use >= 0),
    condition_treated VARCHAR(255),
    medication_type VARCHAR(50) CHECK (medication_type IN ('prescription', 'otc', 'supplement')),
    adherence_level VARCHAR(20) CHECK (adherence_level IN ('excellent', 'good', 'fair', 'poor')),
    adherence_percentage DECIMAL(5, 2) CHECK (adherence_percentage >= 0 AND adherence_percentage <= 100),
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patient_medications_patient ON patient_medications(patient_id);
CREATE INDEX idx_patient_medications_type ON patient_medications(medication_type);

-- ============================================================================
-- Laboratory Results
-- ============================================================================

CREATE TABLE IF NOT EXISTS patient_lab_results (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    test_date DATE NOT NULL,
    test_type VARCHAR(50) NOT NULL,
    
    -- Complete Blood Count
    hemoglobin DECIMAL(4, 2) CHECK (hemoglobin >= 10 AND hemoglobin <= 20),
    hematocrit DECIMAL(4, 2) CHECK (hematocrit >= 30 AND hematocrit <= 60),
    white_blood_cell_count INTEGER CHECK (white_blood_cell_count > 0),
    platelet_count INTEGER CHECK (platelet_count > 0),
    
    -- Lipid Panel
    total_cholesterol DECIMAL(5, 2) CHECK (total_cholesterol >= 100 AND total_cholesterol <= 400),
    ldl_cholesterol DECIMAL(5, 2) CHECK (ldl_cholesterol >= 50 AND ldl_cholesterol <= 300),
    hdl_cholesterol DECIMAL(5, 2) CHECK (hdl_cholesterol >= 20 AND hdl_cholesterol <= 100),
    triglycerides DECIMAL(5, 2) CHECK (triglycerides >= 50 AND triglycerides <= 1000),
    
    -- Metabolic Panel
    glucose DECIMAL(5, 2) CHECK (glucose >= 70 AND glucose <= 200),
    hba1c DECIMAL(4, 2) CHECK (hba1c >= 4 AND hba1c <= 15),
    creatinine DECIMAL(4, 2) CHECK (creatinine >= 0.5 AND creatinine <= 2.0),
    egfr DECIMAL(5, 2) CHECK (egfr >= 15 AND egfr <= 120),
    bun DECIMAL(4, 2) CHECK (bun >= 5 AND bun <= 30),
    
    -- Liver Function
    alt DECIMAL(5, 2) CHECK (alt >= 5 AND alt <= 50),
    ast DECIMAL(5, 2) CHECK (ast >= 5 AND ast <= 50),
    bilirubin DECIMAL(4, 2) CHECK (bilirubin >= 0.1 AND bilirubin <= 2.0),
    albumin DECIMAL(3, 2) CHECK (albumin >= 3.0 AND albumin <= 5.5),
    
    -- Thyroid Function
    tsh DECIMAL(4, 2) CHECK (tsh >= 0.5 AND tsh <= 5.0),
    t3 DECIMAL(5, 2),
    t4 DECIMAL(5, 2),
    
    -- Vitamins
    vitamin_d DECIMAL(5, 2) CHECK (vitamin_d >= 10 AND vitamin_d <= 100),
    vitamin_b12 DECIMAL(6, 2) CHECK (vitamin_b12 >= 200 AND vitamin_b12 <= 900),
    folate DECIMAL(4, 2) CHECK (folate >= 3 AND folate <= 20),
    
    -- Other Tests
    creatinine_clearance DECIMAL(5, 2),
    urine_protein DECIMAL(5, 2),
    troponin DECIMAL(6, 2),
    bnp DECIMAL(6, 2),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patient_lab_results_patient ON patient_lab_results(patient_id);
CREATE INDEX idx_patient_lab_results_date ON patient_lab_results(test_date);
CREATE INDEX idx_patient_lab_results_type ON patient_lab_results(test_type);

-- ============================================================================
-- Healthcare Utilization
-- ============================================================================

CREATE TABLE IF NOT EXISTS patient_healthcare_visits (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    visit_date DATE NOT NULL,
    visit_type VARCHAR(50) NOT NULL CHECK (visit_type IN (
        'primary_care', 'specialist', 'emergency', 'hospitalization', 
        'urgent_care', 'preventive', 'screening', 'surgery'
    )),
    provider_type VARCHAR(100),
    diagnosis VARCHAR(255),
    cost DECIMAL(10, 2) CHECK (cost >= 0),
    hospital_stay_days INTEGER CHECK (hospital_stay_days >= 0 AND hospital_stay_days <= 365),
    icu_admission BOOLEAN DEFAULT FALSE,
    procedure_type VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patient_healthcare_visits_patient ON patient_healthcare_visits(patient_id);
CREATE INDEX idx_patient_healthcare_visits_date ON patient_healthcare_visits(visit_date);
CREATE INDEX idx_patient_healthcare_visits_type ON patient_healthcare_visits(visit_type);

-- ============================================================================
-- Family History
-- ============================================================================

CREATE TABLE IF NOT EXISTS patient_family_history (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    family_member_type VARCHAR(50) NOT NULL CHECK (family_member_type IN (
        'father', 'mother', 'sibling', 'grandfather_paternal', 'grandmother_paternal',
        'grandfather_maternal', 'grandmother_maternal', 'other'
    )),
    age_at_death INTEGER CHECK (age_at_death > 0 AND age_at_death <= 120),
    cause_of_death VARCHAR(255),
    alive BOOLEAN DEFAULT TRUE,
    health_conditions TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patient_family_history_patient ON patient_family_history(patient_id);
CREATE INDEX idx_patient_family_history_member ON patient_family_history(family_member_type);

-- ============================================================================
-- Socioeconomic Factors
-- ============================================================================

CREATE TABLE IF NOT EXISTS patient_socioeconomic (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    
    -- Employment
    employment_status VARCHAR(50) CHECK (employment_status IN (
        'employed', 'unemployed', 'retired', 'disabled', 'student', 'homemaker'
    )),
    occupation VARCHAR(100),
    industry VARCHAR(100),
    annual_income DECIMAL(12, 2) CHECK (annual_income >= 0),
    
    -- Education
    education_level VARCHAR(50) CHECK (education_level IN (
        'less_than_high_school', 'high_school', 'some_college', 
        'bachelor', 'master', 'doctorate'
    )),
    
    -- Living Situation
    residential_area VARCHAR(20) CHECK (residential_area IN ('urban', 'suburban', 'rural')),
    region VARCHAR(50) CHECK (region IN ('northeast', 'northwest', 'southeast', 'southwest', 'midwest')),
    state VARCHAR(2),
    zip_code VARCHAR(10),
    housing_type VARCHAR(20) CHECK (housing_type IN ('owned', 'rented', 'other')),
    household_size INTEGER CHECK (household_size >= 1 AND household_size <= 20),
    
    -- Insurance
    insurance_type VARCHAR(50) CHECK (insurance_type IN (
        'employer', 'individual', 'medicare', 'medicaid', 'uninsured', 'other'
    )),
    insurance_plan_type VARCHAR(20) CHECK (insurance_plan_type IN ('HMO', 'PPO', 'EPO', 'POS', 'HDHP')),
    deductible DECIMAL(10, 2) CHECK (deductible >= 0 AND deductible <= 50000),
    copay_amount DECIMAL(6, 2) CHECK (copay_amount >= 0 AND copay_amount <= 500),
    out_of_pocket_max DECIMAL(10, 2) CHECK (out_of_pocket_max >= 0 AND out_of_pocket_max <= 100000),
    previous_claims_annual DECIMAL(12, 2) CHECK (previous_claims_annual >= 0),
    years_with_insurance INTEGER CHECK (years_with_insurance >= 0),
    coverage_gaps INTEGER CHECK (coverage_gaps >= 0),
    total_days_without_insurance INTEGER CHECK (total_days_without_insurance >= 0),
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_patient_socioeconomic_patient ON patient_socioeconomic(patient_id);
CREATE INDEX idx_patient_socioeconomic_income ON patient_socioeconomic(annual_income);
CREATE INDEX idx_patient_socioeconomic_region ON patient_socioeconomic(region);

-- ============================================================================
-- Environmental Factors
-- ============================================================================

CREATE TABLE IF NOT EXISTS patient_environmental (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    air_quality_index INTEGER CHECK (air_quality_index >= 0 AND air_quality_index <= 500),
    water_quality VARCHAR(20) CHECK (water_quality IN ('excellent', 'good', 'fair', 'poor')),
    proximity_to_healthcare_miles DECIMAL(6, 2) CHECK (proximity_to_healthcare_miles >= 0),
    healthcare_facilities_nearby INTEGER CHECK (healthcare_facilities_nearby >= 0 AND healthcare_facilities_nearby <= 50),
    rural_urban_classification VARCHAR(20) CHECK (rural_urban_classification IN ('urban', 'suburban', 'rural')),
    occupational_risk_level VARCHAR(20) CHECK (occupational_risk_level IN ('low', 'moderate', 'high', 'very_high')),
    exposure_to_toxins BOOLEAN DEFAULT FALSE,
    physical_demands VARCHAR(20) CHECK (physical_demands IN ('sedentary', 'light', 'moderate', 'heavy', 'very_heavy')),
    work_schedule VARCHAR(20) CHECK (work_schedule IN ('day', 'night', 'shift', 'irregular')),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_patient_environmental_patient ON patient_environmental(patient_id);

-- ============================================================================
-- Reproductive Health (for females)
-- ============================================================================

CREATE TABLE IF NOT EXISTS patient_reproductive_health (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    pregnancy_status BOOLEAN DEFAULT FALSE,
    number_of_pregnancies INTEGER CHECK (number_of_pregnancies >= 0 AND number_of_pregnancies <= 20),
    number_of_live_births INTEGER CHECK (number_of_live_births >= 0 AND number_of_live_births <= 20),
    pregnancy_complications BOOLEAN DEFAULT FALSE,
    gestational_diabetes BOOLEAN DEFAULT FALSE,
    preeclampsia BOOLEAN DEFAULT FALSE,
    menopause_status VARCHAR(20) CHECK (menopause_status IN ('pre', 'peri', 'post', 'not_applicable')),
    age_at_menopause INTEGER CHECK (age_at_menopause >= 0 AND age_at_menopause <= 120),
    hormone_replacement_therapy BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_reproductive_health_female CHECK (
        (SELECT sex FROM patients WHERE id = patient_id) = 'female' OR
        pregnancy_status = FALSE
    )
);

CREATE UNIQUE INDEX idx_patient_reproductive_health_patient ON patient_reproductive_health(patient_id);

-- ============================================================================
-- Functional Status
-- ============================================================================

CREATE TABLE IF NOT EXISTS patient_functional_status (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    adl_score INTEGER CHECK (adl_score >= 0 AND adl_score <= 6),
    instrumental_adl_score INTEGER CHECK (instrumental_adl_score >= 0 AND instrumental_adl_score <= 8),
    mobility_status VARCHAR(20) CHECK (mobility_status IN ('independent', 'assistive_device', 'wheelchair', 'bedbound')),
    fall_risk VARCHAR(20) CHECK (fall_risk IN ('low', 'moderate', 'high')),
    falls_past_year INTEGER CHECK (falls_past_year >= 0 AND falls_past_year <= 50),
    chronic_pain BOOLEAN DEFAULT FALSE,
    pain_level INTEGER CHECK (pain_level >= 0 AND pain_level <= 10),
    pain_locations TEXT,
    pain_duration VARCHAR(20) CHECK (pain_duration IN ('acute', 'chronic')),
    quality_of_life_score INTEGER CHECK (quality_of_life_score >= 0 AND quality_of_life_score <= 100),
    hrqol_score INTEGER CHECK (hrqol_score >= 0 AND hrqol_score <= 100),
    functional_status VARCHAR(20) CHECK (functional_status IN ('excellent', 'good', 'fair', 'poor')),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_patient_functional_status_patient ON patient_functional_status(patient_id);

-- ============================================================================
-- Risk Scores
-- ============================================================================

CREATE TABLE IF NOT EXISTS patient_risk_scores (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    calculated_at DATE NOT NULL,
    framingham_risk_score DECIMAL(5, 2) CHECK (framingham_risk_score >= 0 AND framingham_risk_score <= 100),
    charlson_comorbidity_index INTEGER CHECK (charlson_comorbidity_index >= 0 AND charlson_comorbidity_index <= 30),
    elixhauser_comorbidity_index INTEGER CHECK (elixhauser_comorbidity_index >= 0 AND elixhauser_comorbidity_index <= 30),
    mortality_risk_score DECIMAL(5, 2) CHECK (mortality_risk_score >= 0 AND mortality_risk_score <= 100),
    overall_health_score DECIMAL(5, 2) CHECK (overall_health_score >= 0 AND overall_health_score <= 100),
    risk_stratification VARCHAR(20) CHECK (risk_stratification IN ('low', 'moderate', 'high', 'very_high')),
    complexity_score INTEGER CHECK (complexity_score >= 0 AND complexity_score <= 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patient_risk_scores_patient ON patient_risk_scores(patient_id);
CREATE INDEX idx_patient_risk_scores_date ON patient_risk_scores(calculated_at);

-- ============================================================================
-- Clinical Notes
-- ============================================================================

CREATE TABLE IF NOT EXISTS clinical_notes (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    medical_worker_id INTEGER REFERENCES medical_workers(id) ON DELETE SET NULL,
    note_date DATE NOT NULL,
    note_type VARCHAR(50) CHECK (note_type IN (
        'chief_complaint', 'history_present_illness', 'review_of_systems',
        'physical_examination', 'assessment_plan', 'progress_note', 'other'
    )),
    chief_complaint TEXT,
    history_present_illness TEXT,
    review_of_systems TEXT,
    physical_examination TEXT,
    assessment_plan TEXT,
    progress_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_clinical_notes_patient ON clinical_notes(patient_id);
CREATE INDEX idx_clinical_notes_worker ON clinical_notes(medical_worker_id);
CREATE INDEX idx_clinical_notes_date ON clinical_notes(note_date);

-- ============================================================================
-- Insurance Claims
-- ============================================================================

CREATE TABLE IF NOT EXISTS insurance_claims (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    claim_date DATE NOT NULL,
    claim_amount DECIMAL(10, 2) CHECK (claim_amount >= 0),
    claim_type VARCHAR(50),
    diagnosis_code VARCHAR(20),
    procedure_code VARCHAR(20),
    approved BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_insurance_claims_patient ON insurance_claims(patient_id);
CREATE INDEX idx_insurance_claims_date ON insurance_claims(claim_date);

-- ============================================================================
-- Model Versions (from existing schema)
-- ============================================================================

CREATE TABLE IF NOT EXISTS model_versions (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) UNIQUE NOT NULL,
    model_path VARCHAR(500) NOT NULL,
    training_round INTEGER,
    accuracy DECIMAL(5, 4),
    mse DECIMAL(10, 4),
    mae DECIMAL(10, 4),
    trained_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_model_versions_active ON model_versions(is_active);

-- ============================================================================
-- Training Rounds (from existing schema)
-- ============================================================================

CREATE TABLE IF NOT EXISTS training_rounds (
    id SERIAL PRIMARY KEY,
    round_number INTEGER NOT NULL,
    clients_participated INTEGER,
    aggregation_method VARCHAR(50),
    status VARCHAR(50) CHECK (status IN ('started', 'in_progress', 'completed', 'failed')),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    metrics JSONB
);

CREATE INDEX idx_training_rounds_number ON training_rounds(round_number);

-- ============================================================================
-- Triggers for Updated At
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_institutions_updated_at BEFORE UPDATE ON institutions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_medical_workers_updated_at BEFORE UPDATE ON medical_workers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patient_physical_measurements_updated_at BEFORE UPDATE ON patient_physical_measurements
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patient_lifestyle_updated_at BEFORE UPDATE ON patient_lifestyle
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patient_medications_updated_at BEFORE UPDATE ON patient_medications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patient_socioeconomic_updated_at BEFORE UPDATE ON patient_socioeconomic
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patient_environmental_updated_at BEFORE UPDATE ON patient_environmental
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patient_reproductive_health_updated_at BEFORE UPDATE ON patient_reproductive_health
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_patient_functional_status_updated_at BEFORE UPDATE ON patient_functional_status
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Views for Common Queries
-- ============================================================================

-- View: Patient Summary with Key Metrics
CREATE OR REPLACE VIEW patient_summary AS
SELECT 
    p.id,
    p.institution_id,
    p.first_name,
    p.last_name,
    p.age,
    p.sex,
    p.insurance_cost,
    pm.bmi,
    pm.systolic_bp,
    pm.diastolic_bp,
    pl.smoking_status,
    pl.physical_activity_level,
    ps.region,
    ps.annual_income,
    ps.education_level,
    COUNT(DISTINCT pmh.id) as chronic_conditions_count,
    COUNT(DISTINCT pmed.id) as medications_count,
    COUNT(DISTINCT phv.id) as healthcare_visits_count
FROM patients p
LEFT JOIN patient_physical_measurements pm ON p.id = pm.patient_id
LEFT JOIN patient_lifestyle pl ON p.id = pl.patient_id
LEFT JOIN patient_socioeconomic ps ON p.id = ps.patient_id
LEFT JOIN patient_medical_history pmh ON p.id = pmh.patient_id
LEFT JOIN patient_medications pmed ON p.id = pmed.patient_id
LEFT JOIN patient_healthcare_visits phv ON p.id = phv.patient_id
GROUP BY p.id, pm.bmi, pm.systolic_bp, pm.diastolic_bp, pl.smoking_status, 
         pl.physical_activity_level, ps.region, ps.annual_income, ps.education_level;

-- View: Latest Lab Results per Patient
CREATE OR REPLACE VIEW patient_latest_labs AS
SELECT DISTINCT ON (patient_id)
    patient_id,
    test_date,
    total_cholesterol,
    ldl_cholesterol,
    hdl_cholesterol,
    glucose,
    hba1c,
    creatinine,
    egfr
FROM patient_lab_results
ORDER BY patient_id, test_date DESC;

-- ============================================================================
-- Comments for Documentation
-- ============================================================================

COMMENT ON TABLE patients IS 'Core patient demographic information';
COMMENT ON TABLE patient_physical_measurements IS 'Physical measurements and vital signs';
COMMENT ON TABLE patient_lifestyle IS 'Lifestyle factors including smoking, alcohol, exercise, diet, sleep';
COMMENT ON TABLE patient_medical_history IS 'Chronic conditions and medical history';
COMMENT ON TABLE patient_medications IS 'Current and past medications';
COMMENT ON TABLE patient_lab_results IS 'Laboratory test results over time';
COMMENT ON TABLE patient_healthcare_visits IS 'Healthcare utilization including visits, hospitalizations, procedures';
COMMENT ON TABLE patient_family_history IS 'Family medical history';
COMMENT ON TABLE patient_socioeconomic IS 'Socioeconomic factors including employment, income, education, insurance';
COMMENT ON TABLE patient_environmental IS 'Environmental and occupational factors';
COMMENT ON TABLE patient_reproductive_health IS 'Reproductive health information (primarily for females)';
COMMENT ON TABLE patient_functional_status IS 'Functional status, mobility, pain, quality of life';
COMMENT ON TABLE patient_risk_scores IS 'Calculated risk scores (Framingham, Charlson, etc.)';
COMMENT ON TABLE clinical_notes IS 'Unstructured clinical notes and documentation';
COMMENT ON TABLE insurance_claims IS 'Insurance claim history';

-- ============================================================================
-- End of Schema
-- ============================================================================

