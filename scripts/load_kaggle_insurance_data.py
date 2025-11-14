"""
Script to load and transform Kaggle Insurance Dataset into our database schema
Dataset: https://www.kaggle.com/datasets/mirichoi0218/insurance
"""
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://medical_user:medical_pass@localhost:5432/medical_insurance"
)

def load_insurance_data(file_path='data/insurance.csv'):
    """Load insurance dataset from CSV"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Dataset not found at {file_path}. "
            "Please download from: https://www.kaggle.com/datasets/mirichoi0218/insurance"
        )
    
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} records from {file_path}")
    return df

def calculate_date_of_birth(age):
    """Calculate date of birth from age"""
    return datetime.now() - timedelta(days=int(age * 365.25))

def transform_to_patients(df, institution_id=1, created_by=1):
    """Transform dataset to patients table format"""
    patients = pd.DataFrame({
        'institution_id': institution_id,
        'created_by': created_by,
        'first_name': 'Patient',
        'last_name': df.index.astype(str).str.zfill(4),
        'date_of_birth': df['age'].apply(calculate_date_of_birth),
        'sex': df['sex'].str.lower(),
        'marital_status': 'single',  # Not in dataset, default value
        'number_of_dependents': df['children'].astype(int),
        'insurance_cost': df['charges'].astype(float),
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    })
    
    return patients

def transform_to_physical_measurements(df, patient_ids):
    """Transform to physical measurements table"""
    # Calculate BMI if not provided (assuming average height for age/sex)
    # In real scenario, we'd have height and weight
    physical = pd.DataFrame({
        'patient_id': patient_ids,
        'bmi': df['bmi'].astype(float),
        'height_cm': None,  # Not in dataset
        'weight_kg': None,  # Not in dataset
        'systolic_bp': None,  # Not in dataset
        'diastolic_bp': None,  # Not in dataset
        'resting_heart_rate': None,  # Not in dataset
        'measured_at': datetime.now(),
        'updated_at': datetime.now()
    })
    
    return physical

def transform_to_lifestyle(df, patient_ids):
    """Transform to lifestyle table"""
    lifestyle = pd.DataFrame({
        'patient_id': patient_ids,
        'smoking_status': df['smoker'].map({'yes': 'current', 'no': 'never'}),
        'years_smoking': None,  # Not in dataset
        'cigarettes_per_day': None,  # Not in dataset
        'alcohol_consumption': None,  # Not in dataset
        'physical_activity_level': None,  # Not in dataset
        'diet_type': None,  # Not in dataset
        'sleep_hours_per_night': None,  # Not in dataset
        'updated_at': datetime.now()
    })
    
    return lifestyle

def transform_to_socioeconomic(df, patient_ids):
    """Transform to socioeconomic table"""
    socioeconomic = pd.DataFrame({
        'patient_id': patient_ids,
        'employment_status': None,  # Not in dataset
        'occupation': None,  # Not in dataset
        'annual_income': None,  # Not in dataset
        'education_level': None,  # Not in dataset
        'residential_area': None,  # Not in dataset
        'region': df['region'].str.lower(),
        'state': None,  # Not in dataset
        'zip_code': None,  # Not in dataset
        'housing_type': None,  # Not in dataset
        'household_size': None,  # Not in dataset
        'insurance_type': 'individual',  # Default
        'insurance_plan_type': None,  # Not in dataset
        'deductible': None,  # Not in dataset
        'copay_amount': None,  # Not in dataset
        'out_of_pocket_max': None,  # Not in dataset
        'previous_claims_annual': None,  # Not in dataset
        'years_with_insurance': None,  # Not in dataset
        'coverage_gaps': 0,  # Default
        'total_days_without_insurance': 0,  # Default
        'updated_at': datetime.now()
    })
    
    return socioeconomic

def insert_data(engine, patients_df, physical_df, lifestyle_df, socioeconomic_df):
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
        patient_ids.reverse()  # Reverse to match order
    
    # Update dataframes with patient IDs
    physical_df['patient_id'] = patient_ids
    lifestyle_df['patient_id'] = patient_ids
    socioeconomic_df['patient_id'] = patient_ids
    
    # Insert physical measurements
    print(f"Inserting {len(physical_df)} physical measurements...")
    physical_df.to_sql('patient_physical_measurements', engine, if_exists='append', index=False, method='multi')
    
    # Insert lifestyle
    print(f"Inserting {len(lifestyle_df)} lifestyle records...")
    lifestyle_df.to_sql('patient_lifestyle', engine, if_exists='append', index=False, method='multi')
    
    # Insert socioeconomic
    print(f"Inserting {len(socioeconomic_df)} socioeconomic records...")
    socioeconomic_df.to_sql('patient_socioeconomic', engine, if_exists='append', index=False, method='multi')
    
    print("\nData insertion completed successfully!")

def main():
    """Main function"""
    print("=" * 60)
    print("Kaggle Insurance Dataset Loader")
    print("=" * 60)
    
    # Check if dataset exists
    dataset_path = 'data/insurance.csv'
    
    if not os.path.exists(dataset_path):
        print(f"\nError: Dataset not found at {dataset_path}")
        print("\nPlease download the dataset:")
        print("1. Visit: https://www.kaggle.com/datasets/mirichoi0218/insurance")
        print("2. Download insurance.csv")
        print("3. Place it in the 'data/' directory")
        print("\nOr use Kaggle API:")
        print("  kaggle datasets download -d mirichoi0218/insurance")
        print("  unzip insurance.zip -d data/")
        return
    
    # Load data
    df = load_insurance_data(dataset_path)
    
    # Display summary
    print(f"\nDataset Summary:")
    print(f"  Records: {len(df)}")
    print(f"  Features: {list(df.columns)}")
    print(f"\nSample data:")
    print(df.head())
    
    # Transform data
    print("\nTransforming data to match database schema...")
    patients_df = transform_to_patients(df)
    physical_df = transform_to_physical_measurements(df, range(1, len(df) + 1))
    lifestyle_df = transform_to_lifestyle(df, range(1, len(df) + 1))
    socioeconomic_df = transform_to_socioeconomic(df, range(1, len(df) + 1))
    
    # Connect to database
    print(f"\nConnecting to database...")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # Test connection
        print("Database connection successful!")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print(f"Please check your DATABASE_URL: {DATABASE_URL}")
        return
    
    # Insert data
    try:
        insert_data(engine, patients_df, physical_df, lifestyle_df, socioeconomic_df)
        
        # Display statistics
        print("\n" + "=" * 60)
        print("Data Loading Statistics")
        print("=" * 60)
        
        with engine.connect() as conn:
            # Count patients
            result = conn.execute(text("SELECT COUNT(*) FROM patients"))
            patient_count = result.scalar()
            print(f"Total patients in database: {patient_count}")
            
            # Count by region
            result = conn.execute(text("""
                SELECT ps.region, COUNT(*) 
                FROM patient_socioeconomic ps 
                GROUP BY ps.region
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
            
            # Insurance cost statistics
            result = conn.execute(text("""
                SELECT 
                    AVG(insurance_cost) as avg_cost,
                    MIN(insurance_cost) as min_cost,
                    MAX(insurance_cost) as max_cost,
                    STDDEV(insurance_cost) as std_cost
                FROM patients
                WHERE insurance_cost IS NOT NULL
            """))
            stats = result.fetchone()
            print("\nInsurance cost statistics:")
            print(f"  Average: ${stats[0]:,.2f}")
            print(f"  Minimum: ${stats[1]:,.2f}")
            print(f"  Maximum: ${stats[2]:,.2f}")
            print(f"  Std Dev: ${stats[3]:,.2f}")
        
    except Exception as e:
        print(f"\nError inserting data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

