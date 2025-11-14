# Public Medical Datasets for Insurance Cost Prediction

## Overview

This document lists publicly available medical datasets that are similar to our patient data schema and can be used for training federated learning models to predict medical insurance costs.

## 1. Medical Cost Personal Datasets (Kaggle)

### Description
One of the most popular datasets for medical insurance cost prediction. Contains patient demographics and insurance charges.

**URL**: https://www.kaggle.com/datasets/mirichoi0218/insurance

**Features**:
- Age
- Sex (male/female)
- BMI (Body Mass Index)
- Number of children
- Smoking status (yes/no)
- Region (northeast, northwest, southeast, southwest)
- **Charges** (insurance cost - target variable)

**Size**: ~1,300 records

**Format**: CSV

**License**: Open Database License

**Similarity to Our Schema**: ⭐⭐⭐⭐⭐ (Very High)
- Matches our core features exactly
- Perfect for initial model training
- Can be easily extended with additional features

**Usage Notes**:
- Ideal starting point for the project
- Can be split by region to simulate different institutions
- Clean, well-structured data

---

## 2. Medical Expenditure Panel Survey (MEPS)

### Description
Comprehensive dataset from the Agency for Healthcare Research and Quality (AHRQ) containing detailed information about medical expenditures, insurance coverage, and patient demographics.

**URL**: 
- Main site: https://meps.ahrq.gov/mepsweb/
- Data files: https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp

**Features**:
- Demographics (age, sex, race, education, income)
- Health conditions and chronic diseases
- Medical visits (primary care, specialist, ER, hospitalizations)
- Prescription medications
- Insurance coverage details
- Medical expenditures (total costs, out-of-pocket)
- Healthcare utilization metrics

**Size**: ~200,000+ records annually (multiple years available)

**Format**: SAS, SPSS, Stata, CSV

**License**: Public domain (US Government)

**Similarity to Our Schema**: ⭐⭐⭐⭐⭐ (Very High)
- Comprehensive coverage of our schema
- Includes socioeconomic factors
- Healthcare utilization data
- Multiple years for temporal analysis

**Usage Notes**:
- Requires registration (free)
- Data available for multiple years
- Can simulate federated learning across different years/regions
- Includes detailed documentation

---

## 3. Health Insurance Marketplace Public Use Files

### Description
CMS (Centers for Medicare & Medicaid Services) provides public data about health insurance plans available through the Marketplace.

**URL**: https://www.cms.gov/healthinsurance/marketplace-puf

**Features**:
- Plan premiums
- Deductibles
- Copayments
- Out-of-pocket maximums
- Plan types (HMO, PPO, etc.)
- Geographic information (state, county)
- Metal levels (Bronze, Silver, Gold, Platinum)

**Size**: Varies by year, typically 50,000+ plan records

**Format**: CSV, Excel

**License**: Public domain (US Government)

**Similarity to Our Schema**: ⭐⭐⭐⭐ (High)
- Insurance plan details match our schema
- Geographic data
- Cost-related features

**Usage Notes**:
- Focuses on plan characteristics rather than individual patients
- Can be combined with patient data
- Useful for understanding insurance market

---

## 4. MIMIC-III (Medical Information Mart for Intensive Care)

### Description
Large, freely available database of de-identified health-related data associated with patients who stayed in critical care units.

**URL**: https://mimic.mit.edu/

**Features**:
- Demographics (age, gender, ethnicity)
- Vital signs (blood pressure, heart rate, temperature)
- Laboratory results (comprehensive lab tests)
- Medications
- Procedures
- Diagnoses (ICD-9 codes)
- Hospital length of stay
- Mortality outcomes
- Insurance information

**Size**: ~40,000+ ICU patients, 58,000+ hospital admissions

**Format**: PostgreSQL database, CSV exports

**License**: Requires completion of data use agreement (free)

**Similarity to Our Schema**: ⭐⭐⭐⭐ (High)
- Comprehensive clinical data
- Laboratory results
- Medical history
- Healthcare utilization
- Some insurance data

**Usage Notes**:
- Requires CITI training and data use agreement
- Focus on ICU patients (may not be representative)
- Rich clinical data for advanced models
- Can extract insurance cost-related features

---

## 5. NHANES (National Health and Nutrition Examination Survey)

### Description
Program of studies designed to assess the health and nutritional status of adults and children in the United States.

**URL**: https://www.cdc.gov/nchs/nhanes/index.htm

**Features**:
- Demographics (age, sex, race, education, income)
- Physical measurements (height, weight, BMI, waist circumference)
- Blood pressure
- Laboratory results (cholesterol, glucose, HbA1c, etc.)
- Medical conditions
- Medication use
- Dietary information
- Physical activity
- Insurance coverage

**Size**: ~5,000-10,000 participants per 2-year cycle

**Format**: SAS, SPSS, Stata, CSV

**License**: Public domain (US Government)

**Similarity to Our Schema**: ⭐⭐⭐⭐⭐ (Very High)
- Excellent match for physical measurements
- Laboratory results
- Lifestyle factors (diet, exercise)
- Socioeconomic data
- Insurance information

**Usage Notes**:
- Multiple cycles available (1999-present)
- Representative of US population
- Rich nutritional and health data
- Can combine multiple cycles for larger dataset

---

## 6. eICU Collaborative Research Database

### Description
Multi-center database comprising de-identified health-related data associated with patients admitted to ICUs.

**URL**: https://eicu-crd.mit.edu/

**Features**:
- Demographics
- Vital signs
- Laboratory results
- Medications
- Procedures
- Diagnoses
- Hospital and ICU length of stay
- Insurance information

**Size**: ~200,000+ ICU patients across multiple hospitals

**Format**: PostgreSQL database, CSV exports

**License**: Requires data use agreement (free)

**Similarity to Our Schema**: ⭐⭐⭐⭐ (High)
- Similar to MIMIC-III
- Multi-institutional (good for federated learning simulation)
- Comprehensive clinical data

**Usage Notes**:
- Requires data use agreement
- Multi-institutional data (perfect for federated learning)
- Can simulate different institutions
- Focus on ICU patients

---

## 7. UCI Machine Learning Repository - Health Datasets

### Description
Various health-related datasets available through UCI ML Repository.

**URL**: https://archive.ics.uci.edu/ml/index.php

**Relevant Datasets**:
- **Heart Disease Dataset**: Demographics, medical history, test results
- **Diabetes Dataset**: Patient characteristics, lab results, outcomes
- **Breast Cancer Dataset**: Patient demographics, diagnostic features

**Format**: CSV, ARFF

**License**: Various (mostly open)

**Similarity to Our Schema**: ⭐⭐⭐ (Moderate)
- Some relevant features
- May need combination with other datasets
- Good for specific conditions

---

## 8. Synthetic Medical Data Generators

### Description
Tools to generate synthetic medical data that follows realistic patterns.

### Synthea
**URL**: https://github.com/synthetichealth/synthea

**Features**:
- Generates realistic synthetic patient records
- Includes demographics, conditions, medications, procedures
- Can customize to match your schema
- HIPAA compliant (synthetic data)

**Usage Notes**:
- Generate unlimited synthetic data
- Perfect for testing and development
- Can be configured to match exact schema
- Useful for federated learning simulation

---

## Recommended Dataset Combinations

### For Initial Development (Quick Start)
1. **Medical Cost Personal Datasets (Kaggle)**
   - Small, clean, ready to use
   - Perfect for proof of concept
   - Can extend with synthetic data

### For Production-Like Training
2. **MEPS + NHANES**
   - Comprehensive patient data
   - Real-world patterns
   - Multiple years available
   - Can simulate different institutions by region/year

### For Advanced Clinical Models
3. **MIMIC-III or eICU + MEPS**
   - Rich clinical data
   - Insurance information
   - Multi-institutional (eICU)
   - Requires data use agreements

### For Federated Learning Simulation
4. **MEPS (by region) or eICU (by hospital)**
   - Natural data partitioning
   - Multiple "institutions"
   - Realistic federated learning scenario

---

## Data Preprocessing for Our Schema

### Mapping Common Datasets to Our Schema

#### From Kaggle Insurance Dataset:
```python
# Direct mapping
patients.age → age
patients.sex → sex
patient_physical_measurements.bmi → bmi
patients.number_of_dependents → children
patient_lifestyle.smoking_status → smoker
patient_socioeconomic.region → region
patients.insurance_cost → charges
```

#### From MEPS:
```python
# Demographics
patients.age → AGE
patients.sex → SEX
patient_socioeconomic.education_level → EDUC
patient_socioeconomic.annual_income → INCOME
patient_socioeconomic.region → REGION

# Health
patient_medical_history → CHRONIC CONDITIONS
patient_medications → PRESCRIPTIONS
patient_healthcare_visits → MEDICAL VISITS
patients.insurance_cost → TOTAL EXPENDITURES
```

#### From NHANES:
```python
# Physical measurements
patient_physical_measurements.height_cm → BMXHT (height)
patient_physical_measurements.weight_kg → BMXWT (weight)
patient_physical_measurements.bmi → BMXBMI
patient_physical_measurements.waist_circumference → BMXWAIST
patient_physical_measurements.systolic_bp → BPXSY1
patient_physical_measurements.diastolic_bp → BPXDI1

# Lab results
patient_lab_results.total_cholesterol → LBXTC
patient_lab_results.ldl_cholesterol → LBDLDL
patient_lab_results.hdl_cholesterol → LBDHDD
patient_lab_results.glucose → LBXGLU
patient_lab_results.hba1c → LBXGH

# Lifestyle
patient_lifestyle.smoking_status → SMQ (smoking)
patient_lifestyle.physical_activity_level → PAQ (physical activity)
```

---

## Download and Usage Instructions

### Kaggle Insurance Dataset
```bash
# Option 1: Direct download from Kaggle
# Visit: https://www.kaggle.com/datasets/mirichoi0218/insurance
# Click "Download" button

# Option 2: Using Kaggle API
pip install kaggle
kaggle datasets download -d mirichoi0218/insurance
unzip insurance.zip
```

### MEPS Dataset
1. Visit: https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp
2. Select year and data file type
3. Complete free registration
4. Download data files
5. Use MEPS data tools for extraction

### NHANES Dataset
1. Visit: https://www.cdc.gov/nchs/nhanes/index.htm
2. Select survey cycle
3. Browse data files
4. Download CSV or use API
5. Combine multiple cycles if needed

### MIMIC-III
1. Visit: https://mimic.mit.edu/
2. Complete CITI training (free, online)
3. Sign data use agreement
4. Request access
5. Download PostgreSQL database or CSV exports

---

## Data Privacy and Compliance

### Important Considerations

1. **HIPAA Compliance**
   - All listed datasets are either:
     - Public domain (government data)
     - De-identified/anonymized
     - Synthetic data
   - Still follow best practices for data handling

2. **Data Use Agreements**
   - MIMIC-III and eICU require data use agreements
   - Free but requires completion of training
   - Ensures responsible data use

3. **Federated Learning Benefits**
   - Data never leaves institutions
   - Only model weights shared
   - Enhanced privacy protection
   - Regulatory compliance

---

## Quick Start Example

### Using Kaggle Insurance Dataset

```python
import pandas as pd
from sqlalchemy import create_engine

# Load dataset
df = pd.read_csv('insurance.csv')

# Map to our schema
patients_data = df[['age', 'sex', 'children', 'region']].copy()
patients_data['insurance_cost'] = df['charges']
patients_data['first_name'] = 'Patient'
patients_data['last_name'] = df.index.astype(str)
patients_data['date_of_birth'] = pd.Timestamp('2000-01-01') - pd.to_timedelta(df['age'], unit='Y')
patients_data['marital_status'] = 'single'
patients_data['institution_id'] = 1
patients_data['created_by'] = 1

# Physical measurements
physical_data = pd.DataFrame({
    'patient_id': df.index + 1,
    'bmi': df['bmi']
})

# Lifestyle
lifestyle_data = pd.DataFrame({
    'patient_id': df.index + 1,
    'smoking_status': df['smoker'].map({'yes': 'current', 'no': 'never'})
})

# Socioeconomic
socioeconomic_data = pd.DataFrame({
    'patient_id': df.index + 1,
    'region': df['region']
})

# Insert into database
engine = create_engine('postgresql://user:pass@localhost/db')
patients_data.to_sql('patients', engine, if_exists='append', index=False)
# ... insert other tables
```

---

## References and Links

1. **Kaggle Insurance Dataset**: https://www.kaggle.com/datasets/mirichoi0218/insurance
2. **MEPS**: https://meps.ahrq.gov/
3. **NHANES**: https://www.cdc.gov/nchs/nhanes/index.htm
4. **MIMIC-III**: https://mimic.mit.edu/
5. **eICU**: https://eicu-crd.mit.edu/
6. **Health Insurance Marketplace**: https://www.cms.gov/healthinsurance/marketplace-puf
7. **Synthea**: https://github.com/synthetichealth/synthea
8. **UCI ML Repository**: https://archive.ics.uci.edu/ml/index.php

---

## Summary

For your federated learning medical insurance cost prediction project, I recommend:

1. **Start with**: Kaggle Insurance Dataset (quick, easy, perfect match)
2. **Scale up with**: MEPS or NHANES (comprehensive, real-world data)
3. **Advanced**: MIMIC-III or eICU (rich clinical data, multi-institutional)
4. **Testing**: Synthea (unlimited synthetic data)

All datasets can be mapped to your database schema with appropriate preprocessing and feature engineering.

