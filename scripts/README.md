# Data Loading Scripts

## Kaggle Insurance Dataset Loader

### Prerequisites

1. **Download the dataset**:
   ```bash
   # Option 1: Direct download
   # Visit: https://www.kaggle.com/datasets/mirichoi0218/insurance
   # Download insurance.csv to data/ directory
   
   # Option 2: Using Kaggle API
   pip install kaggle
   kaggle datasets download -d mirichoi0218/insurance
   unzip insurance.zip -d data/
   ```

2. **Install dependencies**:
   ```bash
   pip install pandas sqlalchemy psycopg2-binary python-dotenv
   ```

3. **Set up database**:
   - Ensure PostgreSQL is running
   - Database schema is created (run `database_schema.sql`)
   - Set `DATABASE_URL` in `.env` file

### Usage

```bash
# From project root
python scripts/load_kaggle_insurance_data.py
```

### What it does

1. Loads `insurance.csv` from `data/` directory
2. Transforms data to match our database schema:
   - `patients` table
   - `patient_physical_measurements` table
   - `patient_lifestyle` table
   - `patient_socioeconomic` table
3. Inserts data into PostgreSQL database
4. Displays loading statistics

### Dataset Features

The Kaggle Insurance dataset includes:
- Age
- Sex (male/female)
- BMI
- Number of children
- Smoking status (yes/no)
- Region (northeast, northwest, southeast, southwest)
- Charges (insurance cost - target variable)

### Notes

- Some fields will be NULL as they're not in the original dataset
- Patient names are auto-generated (Patient0001, Patient0002, etc.)
- Date of birth is calculated from age
- Institution ID defaults to 1
- You can modify the script to add more realistic data or use other datasets

