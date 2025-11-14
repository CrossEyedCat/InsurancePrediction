# Enriched Data Loading Script

## Overview

This script downloads the Kaggle Insurance dataset using `kagglehub` and enriches it with generated realistic data to match our complete database schema.

## Features

The script generates additional data that's not in the original dataset:

### Physical Measurements
- Height and weight (calculated from BMI)
- Body fat percentage
- Waist and hip circumference
- Blood pressure (systolic/diastolic)
- Resting and maximum heart rate

### Laboratory Results
- Complete lipid panel (total cholesterol, LDL, HDL, triglycerides)
- Metabolic panel (glucose, HbA1c, creatinine, eGFR)
- Generated based on age, sex, BMI, and smoking status

### Lifestyle Factors
- Physical activity level and exercise hours
- Steps per day
- Alcohol consumption patterns
- Diet type
- Sleep patterns (hours and quality)
- Detailed smoking history (if applicable)

### Socioeconomic Data
- Employment status
- Education level
- Annual income (correlated with education and age)
- Housing type
- Insurance details (type, plan, deductible, copay)
- Residential area

### Medical History
- Chronic conditions (diabetes, hypertension, heart disease)
- Generated based on risk factors (age, BMI, smoking)
- Includes severity and medication control status

## Installation

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Or install individually
pip install kagglehub pandas numpy sqlalchemy psycopg2-binary python-dotenv
```

## Usage

```bash
# From project root
python scripts/load_and_enrich_insurance_data.py
```

## What It Does

1. **Downloads dataset** using `kagglehub`
2. **Loads CSV file** from downloaded path
3. **Generates enriched data**:
   - Physical measurements based on BMI, age, sex
   - Lab results based on risk factors
   - Lifestyle data with realistic correlations
   - Socioeconomic data with logical relationships
   - Medical history based on probability models
4. **Transforms to database schema**:
   - `patients` table
   - `patient_physical_measurements` table
   - `patient_lifestyle` table
   - `patient_socioeconomic` table
   - `patient_medical_history` table
   - `patient_lab_results` table
5. **Inserts into PostgreSQL** database
6. **Displays statistics** about loaded data

## Data Generation Logic

### Realistic Correlations

The script uses realistic medical correlations:

- **Blood Pressure**: Increases with age, BMI, and smoking
- **Cholesterol**: Higher with age, BMI, smoking
- **Physical Activity**: Inversely related to BMI
- **Income**: Correlates with education level and age
- **Medical Conditions**: Probability based on risk factors
- **Lab Results**: Realistic ranges with medical correlations

### Example Correlations

- Smokers → Higher BP, cholesterol, heart disease risk
- Higher BMI → Lower activity, higher BP, diabetes risk
- Older age → Higher BP, cholesterol, medical conditions
- Higher education → Higher income → Better insurance

## Output

The script provides:
- Progress updates during processing
- Summary statistics after loading
- Breakdowns by region, smoking status, activity level
- Medical condition counts
- Insurance cost statistics
- Lab results averages

## Notes

- Uses random seed (42) for reproducibility
- Generated data follows realistic medical patterns
- Some fields may still be NULL if not applicable
- Can be run multiple times (appends to database)
- Patient IDs are auto-generated sequentially

## Customization

You can modify the script to:
- Adjust generation probabilities
- Add more medical conditions
- Change income distributions
- Modify lab result ranges
- Add more lifestyle factors

## Example Output

```
============================================================
Kaggle Insurance Dataset Loader with Data Enrichment
============================================================
Downloading dataset from Kaggle...
Dataset downloaded to: /path/to/dataset
Loaded 1338 records from /path/to/insurance.csv

Transforming and enriching data...
  Processed 100/1338 records...
  Processed 200/1338 records...
  ...

Inserting data into database...
Inserting 1338 patients...
Got patient IDs: 1 to 1338
Inserting 1338 physical measurements...
Inserting 1338 lifestyle records...
Inserting 1338 socioeconomic records...
Inserting 245 medical history records...
Inserting 1338 lab results...

Data Loading Statistics
============================================================
Total patients in database: 1338

Patients by region:
  southwest: 325
  southeast: 364
  northwest: 325
  northeast: 324

Patients by smoking status:
  never: 1064
  current: 274

Insurance cost statistics:
  Average: $13,270.42
  Median: $9,382.03
  Minimum: $1,121.87
  Maximum: $63,770.43
```

