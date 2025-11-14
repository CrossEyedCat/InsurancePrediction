import pandas as pd
import os

output_dir = "output"
files = [
    'patients.csv',
    'patient_physical_measurements.csv',
    'patient_lifestyle.csv',
    'patient_socioeconomic.csv',
    'patient_medical_history.csv',
    'patient_lab_results.csv'
]

print("File Record Counts:")
print("=" * 50)
for f in files:
    path = os.path.join(output_dir, f)
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f"{f:40} {len(df):>8} records")
    else:
        print(f"{f:40} {'NOT FOUND':>8}")


