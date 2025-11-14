"""
Script to generate extended dataset (up to 50000 records) based on existing data patterns
Uses Faker for realistic names and statistical distributions from existing data
"""
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import random

load_dotenv()

# Output directory for CSV files
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

# Random seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)

# Load existing data to analyze distributions
def load_existing_data():
    """Load existing CSV files to analyze patterns"""
    print("Loading existing data to analyze patterns...")
    
    patients_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'patients.csv'))
    physical_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'patient_physical_measurements.csv'))
    lifestyle_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'patient_lifestyle.csv'))
    socioeconomic_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'patient_socioeconomic.csv'))
    lab_results_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'patient_lab_results.csv'))
    
    return patients_df, physical_df, lifestyle_df, socioeconomic_df, lab_results_df

def analyze_distributions(patients_df, physical_df, lifestyle_df, socioeconomic_df, lab_results_df):
    """Analyze distributions from existing data"""
    print("Analyzing data distributions...")
    
    # Age distribution (from date_of_birth)
    patients_df['age'] = (datetime.now() - pd.to_datetime(patients_df['date_of_birth'])).dt.days / 365.25
    age_mean = patients_df['age'].mean()
    age_std = patients_df['age'].std()
    age_min = patients_df['age'].min()
    age_max = patients_df['age'].max()
    
    # Sex distribution
    sex_dist = patients_df['sex'].value_counts(normalize=True).to_dict()
    
    # BMI distribution
    bmi_mean = physical_df['bmi'].mean()
    bmi_std = physical_df['bmi'].std()
    bmi_min = physical_df['bmi'].min()
    bmi_max = physical_df['bmi'].max()
    
    # Insurance cost distribution
    cost_mean = patients_df['insurance_cost'].mean()
    cost_std = patients_df['insurance_cost'].std()
    cost_min = patients_df['insurance_cost'].min()
    cost_max = patients_df['insurance_cost'].max()
    
    # Children distribution
    children_dist = patients_df['number_of_dependents'].value_counts(normalize=True).to_dict()
    
    # Region distribution
    region_dist = socioeconomic_df['region'].value_counts(normalize=True).to_dict()
    
    # Smoking status distribution
    smoking_dist = lifestyle_df['smoking_status'].value_counts(normalize=True).to_dict()
    
    # Activity level distribution
    activity_dist = lifestyle_df['physical_activity_level'].value_counts(normalize=True).to_dict()
    
    # Education distribution
    education_dist = socioeconomic_df['education_level'].value_counts(normalize=True).to_dict()
    
    # Employment distribution
    employment_dist = socioeconomic_df['employment_status'].value_counts(normalize=True).to_dict()
    
    return {
        'age': {'mean': age_mean, 'std': age_std, 'min': age_min, 'max': age_max},
        'sex': sex_dist,
        'bmi': {'mean': bmi_mean, 'std': bmi_std, 'min': bmi_min, 'max': bmi_max},
        'insurance_cost': {'mean': cost_mean, 'std': cost_std, 'min': cost_min, 'max': cost_max},
        'children': children_dist,
        'region': region_dist,
        'smoking': smoking_dist,
        'activity': activity_dist,
        'education': education_dist,
        'employment': employment_dist
    }

def generate_age(dist):
    """Generate age based on distribution"""
    age = np.random.normal(dist['mean'], dist['std'])
    age = max(dist['min'], min(dist['max'], age))
    return int(age)

def generate_bmi(dist, age, sex):
    """Generate BMI based on distribution and demographics"""
    bmi = np.random.normal(dist['mean'], dist['std'])
    # Slight adjustment based on age and sex
    if sex == 'male':
        bmi += (age - dist['mean']) * 0.01
    else:
        bmi -= (age - dist['mean']) * 0.005
    bmi = max(dist['min'], min(dist['max'], bmi))
    return round(bmi, 3)

def generate_insurance_cost(dist, age, bmi, smoker, children):
    """Generate insurance cost based on factors"""
    # Base cost
    cost = np.random.normal(dist['mean'], dist['std'])
    
    # Adjustments
    cost += (age - 40) * 100  # Age factor
    cost += (bmi - 25) * 200  # BMI factor
    if smoker == 'yes':
        cost += 5000
    cost += children * 500
    
    cost = max(dist['min'], min(dist['max'], cost))
    return round(cost, 2)

def calculate_date_of_birth(age):
    """Calculate date of birth from age"""
    return datetime.now() - timedelta(days=int(age * 365.25))

def generate_height_weight_from_bmi(bmi, age, sex):
    """Generate realistic height and weight from BMI"""
    if sex == 'male':
        base_height = 175 + (age - 30) * 0.1
        base_height = max(160, min(190, base_height))
    else:
        base_height = 162 + (age - 30) * 0.1
        base_height = max(150, min(180, base_height))
    
    height_cm = base_height + np.random.normal(0, 5)
    height_cm = max(140, min(210, height_cm))
    
    height_m = height_cm / 100
    weight_kg = bmi * (height_m ** 2)
    weight_kg = max(40, min(200, weight_kg))
    
    return round(height_cm, 2), round(weight_kg, 2)

def generate_blood_pressure(age, bmi, smoker):
    """Generate realistic blood pressure"""
    base_systolic = 110 + (age - 18) * 0.5
    base_systolic += (bmi - 25) * 0.8
    if smoker == 'yes':
        base_systolic += 5
    
    systolic = base_systolic + np.random.normal(0, 8)
    systolic = max(90, min(180, int(systolic)))
    
    diastolic = systolic * 0.65 + np.random.normal(0, 5)
    diastolic = max(60, min(120, int(diastolic)))
    
    return systolic, diastolic

def generate_heart_rate(age, physical_activity):
    """Generate resting heart rate"""
    base_hr = 75 - (age - 18) * 0.1
    if physical_activity in ['active', 'very_active']:
        base_hr -= 10
    elif physical_activity == 'moderate':
        base_hr -= 5
    
    hr = base_hr + np.random.normal(0, 5)
    hr = max(50, min(100, int(hr)))
    return hr

def generate_lab_results(age, sex, bmi, smoker, region):
    """Generate realistic laboratory results"""
    base_cholesterol = 180 + (age - 18) * 0.5 + (bmi - 25) * 2
    if smoker == 'yes':
        base_cholesterol += 15
    total_cholesterol = base_cholesterol + np.random.normal(0, 20)
    total_cholesterol = max(100, min(300, round(total_cholesterol, 2)))
    
    ldl = total_cholesterol * 0.65 + np.random.normal(0, 15)
    ldl = max(50, min(250, round(ldl, 2)))
    
    base_hdl = 50 if sex == 'male' else 60
    if smoker == 'yes':
        base_hdl -= 5
    hdl = base_hdl + np.random.normal(0, 8)
    hdl = max(30, min(100, round(hdl, 2)))
    
    base_trig = 100 + (bmi - 25) * 5
    if smoker == 'yes':
        base_trig += 20
    triglycerides = base_trig + np.random.normal(0, 30)
    triglycerides = max(50, min(400, round(triglycerides, 2)))
    
    base_glucose = 85 + (age - 18) * 0.3 + (bmi - 25) * 0.5
    glucose = base_glucose + np.random.normal(0, 8)
    glucose = max(70, min(120, round(glucose, 2)))
    
    hba1c = (glucose + 46.7) / 28.7 + np.random.normal(0, 0.2)
    hba1c = max(4.0, min(6.5, round(hba1c, 2)))
    
    base_creatinine = 0.9 if sex == 'male' else 0.7
    base_creatinine += (age - 18) * 0.005
    creatinine = base_creatinine + np.random.normal(0, 0.1)
    creatinine = max(0.5, min(1.5, round(creatinine, 2)))
    
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

def generate_lifestyle_data(age, sex, bmi, smoker, children, dists):
    """Generate lifestyle data based on distributions"""
    # Physical activity
    activity_levels = list(dists['activity'].keys())
    activity_weights = list(dists['activity'].values())
    physical_activity = np.random.choice(activity_levels, p=activity_weights)
    
    exercise_hours_map = {
        'sedentary': (0, 1),
        'light': (1, 3),
        'moderate': (3, 5),
        'active': (5, 8),
        'very_active': (8, 15)
    }
    min_hours, max_hours = exercise_hours_map[physical_activity]
    exercise_hours = round(np.random.uniform(min_hours, max_hours), 2)
    
    steps_map = {
        'sedentary': (2000, 5000),
        'light': (5000, 7000),
        'moderate': (7000, 10000),
        'active': (10000, 15000),
        'very_active': (15000, 25000)
    }
    min_steps, max_steps = steps_map[physical_activity]
    steps_per_day = int(np.random.uniform(min_steps, max_steps))
    
    # Alcohol
    alcohol_levels = ['none', 'occasional', 'moderate', 'heavy']
    if smoker == 'yes':
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
    
    # Diet
    diet_types = ['omnivore', 'vegetarian', 'vegan', 'pescatarian', 'mediterranean']
    weights = [0.7, 0.15, 0.05, 0.05, 0.05]
    diet_type = np.random.choice(diet_types, p=weights)
    
    # Sleep
    sleep_hours = round(np.random.normal(7.5, 1.0), 1)
    sleep_hours = max(5, min(10, sleep_hours))
    
    sleep_quality = np.random.choice(['poor', 'fair', 'good', 'excellent'], 
                                     p=[0.15, 0.25, 0.45, 0.15])
    
    # Smoking details
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

def generate_socioeconomic_data(age, region, children, dists):
    """Generate socioeconomic data"""
    # Employment
    if age < 18:
        employment_status = 'student'
    elif age < 65:
        emp_levels = list(dists['employment'].keys())
        emp_weights = list(dists['employment'].values())
        employment_status = np.random.choice(emp_levels, p=emp_weights)
    else:
        employment_status = np.random.choice(['retired', 'employed'], p=[0.9, 0.1])
    
    # Education
    edu_levels = list(dists['education'].keys())
    edu_weights = list(dists['education'].values())
    education_level = np.random.choice(edu_levels, p=edu_weights)
    
    # Income
    income_base = {
        'less_than_high_school': 25000,
        'high_school': 35000,
        'some_college': 45000,
        'bachelor': 65000,
        'master': 85000,
        'doctorate': 120000
    }
    base_income = income_base[education_level]
    if age < 50:
        age_multiplier = 1 + (age - 25) * 0.02
    else:
        age_multiplier = 1.5
    annual_income = base_income * age_multiplier * np.random.uniform(0.8, 1.3)
    annual_income = max(10000, round(annual_income, 2))
    
    # Housing
    if annual_income > 50000:
        housing_weights = [0.7, 0.25, 0.05]
    else:
        housing_weights = [0.3, 0.6, 0.1]
    housing_type = np.random.choice(['owned', 'rented', 'other'], p=housing_weights)
    
    # Household size
    household_size = 1 + children + (1 if np.random.random() > 0.3 else 0)
    household_size = max(1, min(8, household_size))
    
    # Insurance
    if employment_status == 'employed':
        insurance_type = np.random.choice(['employer', 'individual'], p=[0.8, 0.2])
    else:
        insurance_type = np.random.choice(['individual', 'medicare', 'medicaid', 'uninsured'],
                                         p=[0.3, 0.2, 0.3, 0.2])
    
    if insurance_type != 'uninsured':
        plan_types = ['HMO', 'PPO', 'EPO', 'POS', 'HDHP']
        insurance_plan_type = np.random.choice(plan_types, p=[0.3, 0.4, 0.1, 0.1, 0.1])
        
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
    
    residential_area = np.random.choice(['urban', 'suburban', 'rural'],
                                       p=[0.4, 0.45, 0.15])
    
    return {
        'region': region,
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
    """Generate medical history"""
    conditions = []
    
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

def generate_patients(num_records, dists, start_id=1):
    """Generate patient records"""
    print(f"\nGenerating {num_records} patient records...")
    
    patients = []
    physical_measurements = []
    lifestyle_records = []
    socioeconomic_records = []
    medical_history_records = []
    lab_results_records = []
    
    sex_list = list(dists['sex'].keys())
    sex_weights = list(dists['sex'].values())
    
    region_list = list(dists['region'].keys())
    region_weights = list(dists['region'].values())
    
    smoking_list = list(dists['smoking'].keys())
    smoking_weights = list(dists['smoking'].values())
    
    children_list = list(dists['children'].keys())
    children_weights = list(dists['children'].values())
    
    for idx in range(num_records):
        patient_id = start_id + idx
        
        # Generate basic demographics
        age = generate_age(dists['age'])
        sex = np.random.choice(sex_list, p=sex_weights)
        region = np.random.choice(region_list, p=region_weights)
        children = int(np.random.choice(children_list, p=children_weights))
        smoker_status = np.random.choice(smoking_list, p=smoking_weights)
        smoker = 'yes' if smoker_status == 'current' else 'no'
        
        # Generate derived data
        bmi = generate_bmi(dists['bmi'], age, sex)
        insurance_cost = generate_insurance_cost(dists['insurance_cost'], age, bmi, smoker, children)
        
        height_cm, weight_kg = generate_height_weight_from_bmi(bmi, age, sex)
        systolic_bp, diastolic_bp = generate_blood_pressure(age, bmi, smoker)
        lab_results = generate_lab_results(age, sex, bmi, smoker, region)
        lifestyle = generate_lifestyle_data(age, sex, bmi, smoker, children, dists)
        socioeconomic = generate_socioeconomic_data(age, region, children, dists)
        medical_history = generate_medical_history(age, bmi, smoker)
        
        heart_rate = generate_heart_rate(age, lifestyle['physical_activity_level'])
        
        # Patient record
        patients.append({
            'institution_id': 1,
            'created_by': 1,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'date_of_birth': calculate_date_of_birth(age),
            'sex': sex,
            'marital_status': 'single' if children == 0 else 'married',
            'number_of_dependents': children,
            'insurance_cost': insurance_cost,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        })
        
        # Physical measurements
        physical_measurements.append({
            'patient_id': patient_id,
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
            'patient_id': patient_id,
            'smoking_status': smoker_status,
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
            'patient_id': patient_id,
            **socioeconomic,
            'updated_at': datetime.now()
        })
        
        # Medical history
        for condition in medical_history:
            medical_history_records.append({
                'patient_id': patient_id,
                **condition,
                'diagnosis_date': datetime.now() - timedelta(days=condition['years_since_diagnosis'] * 365),
                'created_at': datetime.now()
            })
        
        # Lab results
        lab_results_records.append({
            'patient_id': patient_id,
            'test_date': datetime.now() - timedelta(days=np.random.randint(0, 365)),
            'test_type': 'comprehensive',
            **lab_results,
            'created_at': datetime.now()
        })
        
        if (idx + 1) % 1000 == 0:
            print(f"  Generated {idx + 1}/{num_records} records...")
    
    return (
        pd.DataFrame(patients),
        pd.DataFrame(physical_measurements),
        pd.DataFrame(lifestyle_records),
        pd.DataFrame(socioeconomic_records),
        pd.DataFrame(medical_history_records),
        pd.DataFrame(lab_results_records)
    )

def save_to_csv(patients_df, physical_df, lifestyle_df, 
                socioeconomic_df, medical_history_df, lab_results_df, append=False):
    """Save data to CSV files"""
    print("\nSaving data to CSV files...")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # File paths
    patients_file = os.path.join(OUTPUT_DIR, 'patients.csv')
    physical_file = os.path.join(OUTPUT_DIR, 'patient_physical_measurements.csv')
    lifestyle_file = os.path.join(OUTPUT_DIR, 'patient_lifestyle.csv')
    socioeconomic_file = os.path.join(OUTPUT_DIR, 'patient_socioeconomic.csv')
    medical_history_file = os.path.join(OUTPUT_DIR, 'patient_medical_history.csv')
    lab_results_file = os.path.join(OUTPUT_DIR, 'patient_lab_results.csv')
    
    if append:
        # Append mode
        print(f"Appending {len(patients_df)} patients to {patients_file}...")
        patients_df.to_csv(patients_file, mode='a', header=False, index=False)
        
        print(f"Appending {len(physical_df)} physical measurements...")
        physical_df.to_csv(physical_file, mode='a', header=False, index=False)
        
        print(f"Appending {len(lifestyle_df)} lifestyle records...")
        lifestyle_df.to_csv(lifestyle_file, mode='a', header=False, index=False)
        
        print(f"Appending {len(socioeconomic_df)} socioeconomic records...")
        socioeconomic_df.to_csv(socioeconomic_file, mode='a', header=False, index=False)
        
        if len(medical_history_df) > 0:
            print(f"Appending {len(medical_history_df)} medical history records...")
            medical_history_df.to_csv(medical_history_file, mode='a', header=False, index=False)
        
        print(f"Appending {len(lab_results_df)} lab results...")
        lab_results_df.to_csv(lab_results_file, mode='a', header=False, index=False)
    else:
        # Overwrite mode
        print(f"Saving {len(patients_df)} patients to {patients_file}...")
        patients_df.to_csv(patients_file, index=False)
        
        print(f"Saving {len(physical_df)} physical measurements...")
        physical_df.to_csv(physical_file, index=False)
        
        print(f"Saving {len(lifestyle_df)} lifestyle records...")
        lifestyle_df.to_csv(lifestyle_file, index=False)
        
        print(f"Saving {len(socioeconomic_df)} socioeconomic records...")
        socioeconomic_df.to_csv(socioeconomic_file, index=False)
        
        if len(medical_history_df) > 0:
            print(f"Saving {len(medical_history_df)} medical history records...")
            medical_history_df.to_csv(medical_history_file, index=False)
        
        print(f"Saving {len(lab_results_df)} lab results...")
        lab_results_df.to_csv(lab_results_file, index=False)
    
    print(f"\nData saved successfully to '{OUTPUT_DIR}' directory!")

def display_statistics(patients_df, physical_df, lifestyle_df, 
                       socioeconomic_df, medical_history_df, lab_results_df):
    """Display statistics"""
    print("\n" + "=" * 60)
    print("Generated Data Statistics")
    print("=" * 60)
    
    print(f"\nTotal patients: {len(patients_df)}")
    
    if 'region' in socioeconomic_df.columns:
        region_counts = socioeconomic_df['region'].value_counts()
        print("\nPatients by region:")
        for region, count in region_counts.items():
            print(f"  {region}: {count}")
    
    if 'smoking_status' in lifestyle_df.columns:
        smoking_counts = lifestyle_df['smoking_status'].value_counts()
        print("\nPatients by smoking status:")
        for status, count in smoking_counts.items():
            print(f"  {status}: {count}")
    
    if 'physical_activity_level' in lifestyle_df.columns:
        activity_counts = lifestyle_df['physical_activity_level'].value_counts()
        print("\nPatients by activity level:")
        for activity, count in activity_counts.items():
            print(f"  {activity}: {count}")
    
    if len(medical_history_df) > 0 and 'condition_type' in medical_history_df.columns:
        condition_counts = medical_history_df['condition_type'].value_counts()
        print("\nMedical conditions:")
        for condition, count in condition_counts.items():
            print(f"  {condition}: {count}")
    
    if 'insurance_cost' in patients_df.columns:
        costs = patients_df['insurance_cost'].dropna()
        if len(costs) > 0:
            print("\nInsurance cost statistics:")
            print(f"  Average: ${costs.mean():,.2f}")
            print(f"  Median: ${costs.median():,.2f}")
            print(f"  Minimum: ${costs.min():,.2f}")
            print(f"  Maximum: ${costs.max():,.2f}")
            print(f"  Std Dev: ${costs.std():,.2f}")

def main():
    """Main function"""
    print("=" * 60)
    print("Extended Dataset Generator (up to 50000 records)")
    print("=" * 60)
    
    # Load existing data
    try:
        (patients_df, physical_df, lifestyle_df, 
         socioeconomic_df, lab_results_df) = load_existing_data()
    except Exception as e:
        print(f"Error loading existing data: {e}")
        print("Please ensure existing CSV files exist in the output directory.")
        return
    
    # Analyze distributions
    try:
        dists = analyze_distributions(patients_df, physical_df, lifestyle_df, 
                                     socioeconomic_df, lab_results_df)
        print("Distribution analysis completed!")
    except Exception as e:
        print(f"Error analyzing distributions: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Determine how many records to generate
    existing_count = len(patients_df)
    target_count = 50000
    records_to_generate = target_count - existing_count
    
    if records_to_generate <= 0:
        print(f"\nAlready have {existing_count} records, which meets or exceeds target of {target_count}.")
        return
    
    print(f"\nExisting records: {existing_count}")
    print(f"Target records: {target_count}")
    print(f"Records to generate: {records_to_generate}")
    
    # Generate new records
    try:
        (new_patients_df, new_physical_df, new_lifestyle_df,
         new_socioeconomic_df, new_medical_history_df, new_lab_results_df) = generate_patients(
            records_to_generate, dists, start_id=existing_count + 1
        )
    except Exception as e:
        print(f"Error generating data: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Save new data (append to existing)
    try:
        save_to_csv(new_patients_df, new_physical_df, new_lifestyle_df,
                   new_socioeconomic_df, new_medical_history_df, new_lab_results_df,
                   append=True)
        display_statistics(new_patients_df, new_physical_df, new_lifestyle_df,
                          new_socioeconomic_df, new_medical_history_df, new_lab_results_df)
    except Exception as e:
        print(f"Error saving data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


