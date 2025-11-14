"""
Script to load Kaggle Insurance Dataset using kagglehub and enrich it with
generated data to match our complete database schema
"""
import kagglehub
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import random

load_dotenv()

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://medical_user:medical_pass@localhost:5432/medical_insurance"
)

# Random seed for reproducibility
np.random.seed(42)
random.seed(42)

def download_dataset():
    """Download dataset using kagglehub"""
    print("Downloading dataset from Kaggle...")
    try:
        path = kagglehub.dataset_download("mirichoi0218/insurance")
        print(f"Dataset downloaded to: {path}")
        return path
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        raise

def load_insurance_data(path):
    """Load insurance dataset from downloaded path"""
    # Find CSV file in the path
    csv_file = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv'):
                csv_file = os.path.join(root, file)
                break
        if csv_file:
            break
    
    if not csv_file:
        raise FileNotFoundError(f"No CSV file found in {path}")
    
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} records from {csv_file}")
    return df

def calculate_date_of_birth(age):
    """Calculate date of birth from age"""
    return datetime.now() - timedelta(days=int(age * 365.25))

def generate_height_weight_from_bmi(bmi, age, sex):
    """Generate realistic height and weight from BMI"""
    # Average heights by age and sex (in cm)
    if sex == 'male':
        base_height = 175 + (age - 30) * 0.1  # Slight decrease with age
        base_height = max(160, min(190, base_height))
    else:
        base_height = 162 + (age - 30) * 0.1
        base_height = max(150, min(180, base_height))
    
    # Add some variation
    height_cm = base_height + np.random.normal(0, 5)
    height_cm = max(140, min(210, height_cm))
    
    # Calculate weight from BMI and height
    height_m = height_cm / 100
    weight_kg = bmi * (height_m ** 2)
    weight_kg = max(40, min(200, weight_kg))
    
    return round(height_cm, 2), round(weight_kg, 2)

def generate_blood_pressure(age, bmi, smoker):
    """Generate realistic blood pressure based on age, BMI, and smoking"""
    # Base systolic BP increases with age
    base_systolic = 110 + (age - 18) * 0.5
    # Higher BMI increases BP
    base_systolic += (bmi - 25) * 0.8
    # Smoking increases BP
    if smoker == 'yes':
        base_systolic += 5
    
    systolic = base_systolic + np.random.normal(0, 8)
    systolic = max(90, min(180, int(systolic)))
    
    # Diastolic is typically 60-80% of systolic
    diastolic = systolic * 0.65 + np.random.normal(0, 5)
    diastolic = max(60, min(120, int(diastolic)))
    
    return systolic, diastolic

def generate_heart_rate(age, physical_activity):
    """Generate resting heart rate"""
    # Base heart rate decreases with age
    base_hr = 75 - (age - 18) * 0.1
    # Physical activity lowers resting HR
    if physical_activity in ['active', 'very_active']:
        base_hr -= 10
    elif physical_activity == 'moderate':
        base_hr -= 5
    
    hr = base_hr + np.random.normal(0, 5)
    hr = max(50, min(100, int(hr)))
    return hr

def generate_lab_results(age, sex, bmi, smoker, region):
    """Generate realistic laboratory results"""
    # Cholesterol - higher with age, BMI, smoking
    base_cholesterol = 180 + (age - 18) * 0.5 + (bmi - 25) * 2
    if smoker == 'yes':
        base_cholesterol += 15
    total_cholesterol = base_cholesterol + np.random.normal(0, 20)
    total_cholesterol = max(100, min(300, round(total_cholesterol, 2)))
    
    # LDL (bad cholesterol) - typically 60-70% of total
    ldl = total_cholesterol * 0.65 + np.random.normal(0, 15)
    ldl = max(50, min(250, round(ldl, 2)))
    
    # HDL (good cholesterol) - higher in women, lower with smoking
    base_hdl = 50 if sex == 'male' else 60
    if smoker == 'yes':
        base_hdl -= 5
    hdl = base_hdl + np.random.normal(0, 8)
    hdl = max(30, min(100, round(hdl, 2)))
    
    # Triglycerides - higher with BMI, smoking
    base_trig = 100 + (bmi - 25) * 5
    if smoker == 'yes':
        base_trig += 20
    triglycerides = base_trig + np.random.normal(0, 30)
    triglycerides = max(50, min(400, round(triglycerides, 2)))
    
    # Glucose - higher with age, BMI
    base_glucose = 85 + (age - 18) * 0.3 + (bmi - 25) * 0.5
    glucose = base_glucose + np.random.normal(0, 8)
    glucose = max(70, min(120, round(glucose, 2)))
    
    # HbA1c - correlates with glucose
    hba1c = (glucose + 46.7) / 28.7 + np.random.normal(0, 0.2)
    hba1c = max(4.0, min(6.5, round(hba1c, 2)))
    
    # Creatinine - higher in men, with age
    base_creatinine = 0.9 if sex == 'male' else 0.7
    base_creatinine += (age - 18) * 0.005
    creatinine = base_creatinine + np.random.normal(0, 0.1)
    creatinine = max(0.5, min(1.5, round(creatinine, 2)))
    
    # eGFR - decreases with age
    base_egfr = 120 - (age - 18) * 0.8
    egfr = base_egfr + np.random.normal(0, 10)
    egfr = max(60, min(120, round(egfr, 2)))
    
    return {
        'total_cholesterol': total_cholesterol,
        'ldl_cholesterol': ldl,
        'hdl_cholesterol': hdl,
        'triglycerides': triglycerides,
        'glucose': glucose,
        'hba1c': hba1c,
        'creatinine': creatinine,
        'egfr': egfr
    }

def generate_lifestyle_data(age, sex, bmi, smoker, children):
    """Generate additional lifestyle data"""
    # Physical activity - inversely related to BMI, age
    activity_levels = ['sedentary', 'light', 'moderate', 'active', 'very_active']
    if bmi > 30:
        weights = [0.4, 0.3, 0.2, 0.08, 0.02]  # More sedentary
    elif bmi > 25:
        weights = [0.2, 0.3, 0.3, 0.15, 0.05]
    else:
        weights = [0.1, 0.2, 0.3, 0.3, 0.1]  # More active
    
    physical_activity = np.random.choice(activity_levels, p=weights)
    
    # Exercise hours - based on activity level
    exercise_hours_map = {
        'sedentary': (0, 1),
        'light': (1, 3),
        'moderate': (3, 5),
        'active': (5, 8),
        'very_active': (8, 15)
    }
    min_hours, max_hours = exercise_hours_map[physical_activity]
    exercise_hours = round(np.random.uniform(min_hours, max_hours), 2)
    
    # Steps per day
    steps_map = {
        'sedentary': (2000, 5000),
        'light': (5000, 7000),
        'moderate': (7000, 10000),
        'active': (10000, 15000),
        'very_active': (15000, 25000)
    }
    min_steps, max_steps = steps_map[physical_activity]
    steps_per_day = int(np.random.uniform(min_steps, max_steps))
    
    # Alcohol consumption
    alcohol_levels = ['none', 'occasional', 'moderate', 'heavy']
    if smoker == 'yes':
        # Smokers more likely to drink
        weights = [0.2, 0.3, 0.4, 0.1]
    else:
        weights = [0.3, 0.4, 0.25, 0.05]
    alcohol_consumption = np.random.choice(alcohol_levels, p=weights)
    
    drinks_per_week = {
        'none': 0,
        'occasional': (1, 3),
        'moderate': (4, 7),
        'heavy': (8, 20)
    }
    if alcohol_consumption == 'none':
        drinks = 0
    else:
        min_drinks, max_drinks = drinks_per_week[alcohol_consumption]
        drinks = int(np.random.uniform(min_drinks, max_drinks))
    
    # Diet type
    diet_types = ['omnivore', 'vegetarian', 'vegan', 'pescatarian', 'mediterranean']
    weights = [0.7, 0.15, 0.05, 0.05, 0.05]
    diet_type = np.random.choice(diet_types, p=weights)
    
    # Sleep hours - 7-9 is normal, varies slightly
    sleep_hours = round(np.random.normal(7.5, 1.0), 1)
    sleep_hours = max(5, min(10, sleep_hours))
    
    # Sleep quality
    sleep_quality = np.random.choice(['poor', 'fair', 'good', 'excellent'], 
                                     p=[0.15, 0.25, 0.45, 0.15])
    
    # Smoking details if smoker
    if smoker == 'yes':
        years_smoking = max(1, age - 18 - np.random.randint(0, 5))
        cigarettes_per_day = int(np.random.uniform(5, 30))
        pack_years = round((cigarettes_per_day / 20) * years_smoking, 2)
    else:
        years_smoking = 0
        cigarettes_per_day = 0
        pack_years = 0.0
    
    return {
        'physical_activity_level': physical_activity,
        'exercise_hours_per_week': exercise_hours,
        'steps_per_day': steps_per_day,
        'alcohol_consumption': alcohol_consumption,
        'drinks_per_week': drinks,
        'diet_type': diet_type,
        'sleep_hours_per_night': sleep_hours,
        'sleep_quality': sleep_quality,
        'years_smoking': years_smoking,
        'cigarettes_per_day': cigarettes_per_day,
        'pack_years': pack_years
    }

def generate_socioeconomic_data(age, region, children):
    """Generate socioeconomic data"""
    # Employment status
    if age < 18:
        employment_status = 'student'
    elif age < 65:
        employment_status = np.random.choice(
            ['employed', 'unemployed', 'student'],
            p=[0.85, 0.1, 0.05]
        )
    else:
        employment_status = np.random.choice(
            ['retired', 'employed'],
            p=[0.9, 0.1]
        )
    
    # Education level
    education_levels = [
        'less_than_high_school', 'high_school', 'some_college',
        'bachelor', 'master', 'doctorate'
    ]
    if age < 25:
        weights = [0.1, 0.3, 0.4, 0.15, 0.04, 0.01]
    else:
        weights = [0.15, 0.25, 0.25, 0.25, 0.08, 0.02]
    education_level = np.random.choice(education_levels, p=weights)
    
    # Income - correlates with education and age
    income_base = {
        'less_than_high_school': 25000,
        'high_school': 35000,
        'some_college': 45000,
        'bachelor': 65000,
        'master': 85000,
        'doctorate': 120000
    }
    base_income = income_base[education_level]
    # Income increases with age (up to 50)
    if age < 50:
        age_multiplier = 1 + (age - 25) * 0.02
    else:
        age_multiplier = 1.5
    annual_income = base_income * age_multiplier * np.random.uniform(0.8, 1.3)
    annual_income = max(10000, round(annual_income, 2))
    
    # Housing type
    if annual_income > 50000:
        housing_weights = [0.7, 0.25, 0.05]  # More owned
    else:
        housing_weights = [0.3, 0.6, 0.1]  # More rented
    housing_type = np.random.choice(['owned', 'rented', 'other'], p=housing_weights)
    
    # Household size
    household_size = 1 + children + (1 if np.random.random() > 0.3 else 0)  # Partner
    household_size = max(1, min(8, household_size))
    
    # Insurance type
    if employment_status == 'employed':
        insurance_type = np.random.choice(
            ['employer', 'individual'],
            p=[0.8, 0.2]
        )
    else:
        insurance_type = np.random.choice(
            ['individual', 'medicare', 'medicaid', 'uninsured'],
            p=[0.3, 0.2, 0.3, 0.2]
        )
    
    # Insurance plan details
    if insurance_type != 'uninsured':
        plan_types = ['HMO', 'PPO', 'EPO', 'POS', 'HDHP']
        insurance_plan_type = np.random.choice(plan_types, p=[0.3, 0.4, 0.1, 0.1, 0.1])
        
        # Deductible based on plan type
        deductible_map = {
            'HMO': (500, 2000),
            'PPO': (1000, 5000),
            'EPO': (1000, 4000),
            'POS': (1500, 6000),
            'HDHP': (2000, 7000)
        }
        min_ded, max_ded = deductible_map[insurance_plan_type]
        deductible = round(np.random.uniform(min_ded, max_ded), 2)
        
        copay_amount = round(np.random.uniform(20, 50), 2)
        out_of_pocket_max = round(deductible * 2.5, 2)
    else:
        insurance_plan_type = None
        deductible = None
        copay_amount = None
        out_of_pocket_max = None
    
    # Residential area
    residential_area = np.random.choice(
        ['urban', 'suburban', 'rural'],
        p=[0.4, 0.45, 0.15]
    )
    
    return {
        'employment_status': employment_status,
        'education_level': education_level,
        'annual_income': annual_income,
        'housing_type': housing_type,
        'household_size': household_size,
        'insurance_type': insurance_type,
        'insurance_plan_type': insurance_plan_type,
        'deductible': deductible,
        'copay_amount': copay_amount,
        'out_of_pocket_max': out_of_pocket_max,
        'residential_area': residential_area,
        'years_with_insurance': max(1, int(np.random.uniform(1, 20))),
        'coverage_gaps': int(np.random.exponential(0.5)),
        'total_days_without_insurance': int(np.random.exponential(30))
    }

def generate_medical_history(age, bmi, smoker):
    """Generate medical history based on risk factors"""
    conditions = []
    
    # Diabetes risk increases with age, BMI
    diabetes_risk = 0.01 + (age - 18) * 0.001 + (bmi - 25) * 0.01
    if np.random.random() < diabetes_risk:
        years = max(1, int(np.random.uniform(1, age - 18)))
        conditions.append({
            'condition_type': 'diabetes',
            'condition_name': 'Type 2 Diabetes',
            'severity': np.random.choice(['mild', 'moderate', 'severe'], p=[0.5, 0.4, 0.1]),
            'years_since_diagnosis': years,
            'medication_controlled': np.random.random() > 0.3
        })
    
    # Hypertension risk
    hypertension_risk = 0.05 + (age - 18) * 0.002 + (bmi - 25) * 0.01
    if smoker == 'yes':
        hypertension_risk += 0.1
    if np.random.random() < hypertension_risk:
        years = max(1, int(np.random.uniform(1, age - 18)))
        conditions.append({
            'condition_type': 'hypertension',
            'condition_name': 'Hypertension',
            'severity': np.random.choice(['mild', 'moderate'], p=[0.7, 0.3]),
            'years_since_diagnosis': years,
            'medication_controlled': np.random.random() > 0.2
        })
    
    # Heart disease (lower probability)
    heart_disease_risk = 0.01 + (age - 40) * 0.002 if age > 40 else 0.001
    if smoker == 'yes':
        heart_disease_risk *= 2
    if np.random.random() < heart_disease_risk:
        years = max(1, int(np.random.uniform(1, max(1, age - 40))))
        conditions.append({
            'condition_type': 'heart_disease',
            'condition_name': 'Coronary Artery Disease',
            'severity': np.random.choice(['mild', 'moderate', 'severe'], p=[0.6, 0.3, 0.1]),
            'years_since_diagnosis': years,
            'medication_controlled': np.random.random() > 0.4
        })
    
    return conditions

def transform_data(df):
    """Transform and enrich dataset"""
    print("\nTransforming and enriching data...")
    
    # Patients table
    patients = []
    physical_measurements = []
    lifestyle_records = []
    socioeconomic_records = []
    medical_history_records = []
    lab_results_records = []
    
    for idx, row in df.iterrows():
        age = int(row['age'])
        sex = row['sex'].lower()
        bmi = float(row['bmi'])
        smoker = row['smoker']
        children = int(row['children'])
        region = row['region'].lower()
        charges = float(row['charges'])
        
        # Generate additional data
        height_cm, weight_kg = generate_height_weight_from_bmi(bmi, age, sex)
        systolic_bp, diastolic_bp = generate_blood_pressure(age, bmi, smoker)
        heart_rate = generate_heart_rate(age, 'moderate')  # Will be updated with lifestyle
        lab_results = generate_lab_results(age, sex, bmi, smoker, region)
        lifestyle = generate_lifestyle_data(age, sex, bmi, smoker, children)
        socioeconomic = generate_socioeconomic_data(age, region, children)
        medical_history = generate_medical_history(age, bmi, smoker)
        
        # Update heart rate based on actual activity level
        heart_rate = generate_heart_rate(age, lifestyle['physical_activity_level'])
        
        # Patient record
        patients.append({
            'institution_id': 1,
            'created_by': 1,
            'first_name': 'Patient',
            'last_name': f"{idx + 1:04d}",
            'date_of_birth': calculate_date_of_birth(age),
            'sex': sex,
            'marital_status': 'single' if children == 0 else 'married',
            'number_of_dependents': children,
            'insurance_cost': charges,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        })
        
        # Physical measurements
        physical_measurements.append({
            'patient_id': idx + 1,  # Will be updated after insert
            'height_cm': height_cm,
            'weight_kg': weight_kg,
            'bmi': bmi,
            'body_fat_percentage': round(1.2 * bmi + 0.23 * age - 10.8 - 5.4 if sex == 'male' else 1.2 * bmi + 0.23 * age - 5.4, 2),
            'waist_circumference': round(0.5 * height_cm + np.random.normal(0, 5), 2),
            'hip_circumference': round(0.6 * height_cm + np.random.normal(0, 5), 2),
            'systolic_bp': systolic_bp,
            'diastolic_bp': diastolic_bp,
            'resting_heart_rate': heart_rate,
            'max_heart_rate': 220 - age,
            'measured_at': datetime.now(),
            'updated_at': datetime.now()
        })
        
        # Lifestyle
        lifestyle_records.append({
            'patient_id': idx + 1,
            'smoking_status': 'current' if smoker == 'yes' else 'never',
            'years_smoking': lifestyle['years_smoking'],
            'cigarettes_per_day': lifestyle['cigarettes_per_day'],
            'pack_years': lifestyle['pack_years'],
            'alcohol_consumption': lifestyle['alcohol_consumption'],
            'drinks_per_week': lifestyle['drinks_per_week'],
            'drinking_frequency': 'weekly' if lifestyle['drinks_per_week'] > 0 else 'never',
            'physical_activity_level': lifestyle['physical_activity_level'],
            'exercise_hours_per_week': lifestyle['exercise_hours_per_week'],
            'steps_per_day': lifestyle['steps_per_day'],
            'diet_type': lifestyle['diet_type'],
            'sleep_hours_per_night': lifestyle['sleep_hours_per_night'],
            'sleep_quality': lifestyle['sleep_quality'],
            'updated_at': datetime.now()
        })
        
        # Socioeconomic
        socioeconomic_records.append({
            'patient_id': idx + 1,
            **socioeconomic,
            'updated_at': datetime.now()
        })
        
        # Medical history
        for condition in medical_history:
            medical_history_records.append({
                'patient_id': idx + 1,
                **condition,
                'diagnosis_date': datetime.now() - timedelta(days=condition['years_since_diagnosis'] * 365),
                'created_at': datetime.now()
            })
        
        # Lab results
        lab_results_records.append({
            'patient_id': idx + 1,
            'test_date': datetime.now() - timedelta(days=np.random.randint(0, 365)),
            'test_type': 'comprehensive',
            **lab_results,
            'created_at': datetime.now()
        })
        
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1}/{len(df)} records...")
    
    return (
        pd.DataFrame(patients),
        pd.DataFrame(physical_measurements),
        pd.DataFrame(lifestyle_records),
        pd.DataFrame(socioeconomic_records),
        pd.DataFrame(medical_history_records),
        pd.DataFrame(lab_results_records)
    )

def insert_data(engine, patients_df, physical_df, lifestyle_df, 
                socioeconomic_df, medical_history_df, lab_results_df):
    """Insert data into database"""
    print("\nInserting data into database...")
    
    # Insert patients
    print(f"Inserting {len(patients_df)} patients...")
    patients_df.to_sql('patients', engine, if_exists='append', index=False, method='multi')
    
    # Get inserted patient IDs
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id FROM patients 
            ORDER BY id DESC 
            LIMIT :limit
        """), {'limit': len(patients_df)})
        patient_ids = [row[0] for row in result]
        patient_ids.reverse()
    
    print(f"Got patient IDs: {patient_ids[0]} to {patient_ids[-1]}")
    
    # Update dataframes with patient IDs
    physical_df['patient_id'] = patient_ids
    lifestyle_df['patient_id'] = patient_ids
    socioeconomic_df['patient_id'] = patient_ids
    medical_history_df['patient_id'] = patient_ids
    lab_results_df['patient_id'] = patient_ids
    
    # Insert physical measurements
    print(f"Inserting {len(physical_df)} physical measurements...")
    physical_df.to_sql('patient_physical_measurements', engine, if_exists='append', 
                       index=False, method='multi')
    
    # Insert lifestyle
    print(f"Inserting {len(lifestyle_df)} lifestyle records...")
    lifestyle_df.to_sql('patient_lifestyle', engine, if_exists='append', 
                        index=False, method='multi')
    
    # Insert socioeconomic
    print(f"Inserting {len(socioeconomic_df)} socioeconomic records...")
    socioeconomic_df.to_sql('patient_socioeconomic', engine, if_exists='append', 
                            index=False, method='multi')
    
    # Insert medical history
    if len(medical_history_df) > 0:
        print(f"Inserting {len(medical_history_df)} medical history records...")
        medical_history_df.to_sql('patient_medical_history', engine, if_exists='append', 
                                   index=False, method='multi')
    
    # Insert lab results
    print(f"Inserting {len(lab_results_df)} lab results...")
    lab_results_df.to_sql('patient_lab_results', engine, if_exists='append', 
                          index=False, method='multi')
    
    print("\nData insertion completed successfully!")

def display_statistics(engine):
    """Display loading statistics"""
    print("\n" + "=" * 60)
    print("Data Loading Statistics")
    print("=" * 60)
    
    with engine.connect() as conn:
        # Count patients
        result = conn.execute(text("SELECT COUNT(*) FROM patients"))
        patient_count = result.scalar()
        print(f"\nTotal patients in database: {patient_count}")
        
        # Count by region
        result = conn.execute(text("""
            SELECT ps.region, COUNT(*) 
            FROM patient_socioeconomic ps 
            GROUP BY ps.region
            ORDER BY COUNT(*) DESC
        """))
        print("\nPatients by region:")
        for row in result:
            print(f"  {row[0]}: {row[1]}")
        
        # Count by smoking status
        result = conn.execute(text("""
            SELECT pl.smoking_status, COUNT(*) 
            FROM patient_lifestyle pl 
            WHERE pl.smoking_status IS NOT NULL
            GROUP BY pl.smoking_status
        """))
        print("\nPatients by smoking status:")
        for row in result:
            print(f"  {row[0]}: {row[1]}")
        
        # Count by activity level
        result = conn.execute(text("""
            SELECT pl.physical_activity_level, COUNT(*) 
            FROM patient_lifestyle pl 
            WHERE pl.physical_activity_level IS NOT NULL
            GROUP BY pl.physical_activity_level
            ORDER BY COUNT(*) DESC
        """))
        print("\nPatients by activity level:")
        for row in result:
            print(f"  {row[0]}: {row[1]}")
        
        # Medical conditions
        result = conn.execute(text("""
            SELECT condition_type, COUNT(*) 
            FROM patient_medical_history 
            GROUP BY condition_type
            ORDER BY COUNT(*) DESC
        """))
        print("\nMedical conditions:")
        for row in result:
            print(f"  {row[0]}: {row[1]}")
        
        # Insurance cost statistics
        result = conn.execute(text("""
            SELECT 
                AVG(insurance_cost) as avg_cost,
                MIN(insurance_cost) as min_cost,
                MAX(insurance_cost) as max_cost,
                STDDEV(insurance_cost) as std_cost,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY insurance_cost) as median_cost
            FROM patients
            WHERE insurance_cost IS NOT NULL
        """))
        stats = result.fetchone()
        print("\nInsurance cost statistics:")
        print(f"  Average: ${stats[0]:,.2f}")
        print(f"  Median: ${stats[4]:,.2f}")
        print(f"  Minimum: ${stats[1]:,.2f}")
        print(f"  Maximum: ${stats[2]:,.2f}")
        print(f"  Std Dev: ${stats[3]:,.2f}")
        
        # Lab results summary
        result = conn.execute(text("""
            SELECT 
                AVG(total_cholesterol) as avg_chol,
                AVG(glucose) as avg_glucose,
                AVG(hba1c) as avg_hba1c
            FROM patient_lab_results
            WHERE total_cholesterol IS NOT NULL
        """))
        lab_stats = result.fetchone()
        print("\nLab results averages:")
        print(f"  Total Cholesterol: {lab_stats[0]:.2f} mg/dL")
        print(f"  Glucose: {lab_stats[1]:.2f} mg/dL")
        print(f"  HbA1c: {lab_stats[2]:.2f}%")

def main():
    """Main function"""
    print("=" * 60)
    print("Kaggle Insurance Dataset Loader with Data Enrichment")
    print("=" * 60)
    
    # Download dataset
    try:
        path = download_dataset()
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Load data
    try:
        df = load_insurance_data(path)
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Display summary
    print(f"\nDataset Summary:")
    print(f"  Records: {len(df)}")
    print(f"  Features: {list(df.columns)}")
    print(f"\nSample data:")
    print(df.head())
    
    # Transform and enrich data
    try:
        (patients_df, physical_df, lifestyle_df, 
         socioeconomic_df, medical_history_df, lab_results_df) = transform_data(df)
    except Exception as e:
        print(f"Error transforming data: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Connect to database
    print(f"\nConnecting to database...")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful!")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print(f"Please check your DATABASE_URL: {DATABASE_URL}")
        return
    
    # Insert data
    try:
        insert_data(engine, patients_df, physical_df, lifestyle_df, 
                   socioeconomic_df, medical_history_df, lab_results_df)
        display_statistics(engine)
    except Exception as e:
        print(f"\nError inserting data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

