# Data Quality Assessment Report

**Generated:** 2025-11-14 19:03:50

**Dataset:** Insurance Prediction Dataset

---

## Executive Summary

- **Total Patients:** 50,000
- **Total Tables:** 6
- **Data Generation Method:** Synthetic data generation based on Kaggle Insurance dataset
- **Data Enrichment:** Extended with physical measurements, lifestyle, socioeconomic, medical history, and lab results

---

## Patients Table

### Basic Information
- **Total Records:** 50,000
- **Total Columns:** 11
- **Columns:** institution_id, created_by, first_name, last_name, date_of_birth, sex, marital_status, number_of_dependents, insurance_cost, created_at, updated_at

### Data Completeness
| Column | Null Count | Null % | Completeness % |
|--------|------------|--------|----------------|
| institution_id | 0 | 0.00% | 100.00% |
| created_by | 0 | 0.00% | 100.00% |
| first_name | 0 | 0.00% | 100.00% |
| last_name | 0 | 0.00% | 100.00% |
| date_of_birth | 0 | 0.00% | 100.00% |
| sex | 0 | 0.00% | 100.00% |
| marital_status | 0 | 0.00% | 100.00% |
| number_of_dependents | 0 | 0.00% | 100.00% |
| insurance_cost | 0 | 0.00% | 100.00% |
| created_at | 0 | 0.00% | 100.00% |
| updated_at | 0 | 0.00% | 100.00% |

### Data Types
| Column | Data Type |
|--------|-----------|
| institution_id | int64 |
| created_by | int64 |
| first_name | object |
| last_name | object |
| date_of_birth | object |
| sex | object |
| marital_status | object |
| number_of_dependents | int64 |
| insurance_cost | float64 |
| created_at | object |
| updated_at | object |

### Numeric Statistics
| Column | Mean | Median | Std Dev | Min | Max | Q25 | Q75 | Skewness |
|--------|------|--------|---------|-----|-----|-----|-----|----------|
| institution_id | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| created_by | 1.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| number_of_dependents | 1.10 | 1.00 | 1.21 | 0.00 | 5.00 | 0.00 | 2.00 | 0.92 |
| insurance_cost | 16537.29 | 15713.15 | 11243.27 | 1121.87 | 63770.43 | 7342.30 | 24199.65 | 0.49 |

### Outlier Detection (IQR Method)
| Column | Outlier Count | Outlier % | Lower Bound | Upper Bound |
|--------|---------------|-----------|------------|-------------|
| insurance_cost | 174 | 0.35% | -17943.73 | 49485.68 |

### Categorical Distributions
#### first_name
- **Unique Values:** 690
- **Most Common:** Patient (1,338 occurrences)
- **Distribution:**
  - Patient: 1,338 (2.68%)
  - Michael: 1,097 (2.19%)
  - David: 791 (1.58%)
  - Christopher: 717 (1.43%)
  - James: 702 (1.40%)
  - Jennifer: 690 (1.38%)
  - John: 678 (1.36%)
  - Robert: 666 (1.33%)
  - Matthew: 517 (1.03%)
  - William: 497 (0.99%)
  - ... and 680 more values

#### last_name
- **Unique Values:** 2338
- **Most Common:** Smith (1,069 occurrences)
- **Distribution:**
  - Smith: 1,069 (2.14%)
  - Johnson: 812 (1.62%)
  - Williams: 678 (1.36%)
  - Jones: 647 (1.29%)
  - Brown: 601 (1.20%)
  - Miller: 521 (1.04%)
  - Davis: 479 (0.96%)
  - Garcia: 409 (0.82%)
  - Rodriguez: 371 (0.74%)
  - Anderson: 339 (0.68%)
  - ... and 2328 more values

#### date_of_birth
- **Unique Values:** 50000
- **Most Common:** 1975-11-15 19:01:18.860416 (1 occurrences)
- **Distribution:**
  - 1975-11-15 19:01:18.860416: 1 (0.00%)
  - 1990-11-15 19:01:18.860190: 1 (0.00%)
  - 1980-11-14 19:01:18.859957: 1 (0.00%)
  - 1989-11-14 19:01:18.859697: 1 (0.00%)
  - 1990-11-15 19:01:18.859420: 1 (0.00%)
  - 2008-11-14 19:01:18.859157: 1 (0.00%)
  - 1961-11-14 19:01:18.858908: 1 (0.00%)
  - 1989-11-14 19:01:18.858658: 1 (0.00%)
  - 1992-11-14 19:01:18.858310: 1 (0.00%)
  - 1981-11-14 19:01:18.857967: 1 (0.00%)
  - ... and 49990 more values

#### sex
- **Unique Values:** 2
- **Most Common:** male (25,404 occurrences)
- **Distribution:**
  - male: 25,404 (50.81%)
  - female: 24,596 (49.19%)

#### marital_status
- **Unique Values:** 2
- **Most Common:** married (28,753 occurrences)
- **Distribution:**
  - married: 28,753 (57.51%)
  - single: 21,247 (42.49%)

#### created_at
- **Unique Values:** 50000
- **Most Common:** 2025-11-14 19:01:18.860417 (1 occurrences)
- **Distribution:**
  - 2025-11-14 19:01:18.860417: 1 (0.00%)
  - 2025-11-14 19:01:18.860191: 1 (0.00%)
  - 2025-11-14 19:01:18.859958: 1 (0.00%)
  - 2025-11-14 19:01:18.859699: 1 (0.00%)
  - 2025-11-14 19:01:18.859422: 1 (0.00%)
  - 2025-11-14 19:01:18.859158: 1 (0.00%)
  - 2025-11-14 19:01:18.858910: 1 (0.00%)
  - 2025-11-14 19:01:18.858660: 1 (0.00%)
  - 2025-11-14 19:01:18.858313: 1 (0.00%)
  - 2025-11-14 19:01:18.857968: 1 (0.00%)
  - ... and 49990 more values

#### updated_at
- **Unique Values:** 50000
- **Most Common:** 2025-11-14 19:01:18.860417 (1 occurrences)
- **Distribution:**
  - 2025-11-14 19:01:18.860417: 1 (0.00%)
  - 2025-11-14 19:01:18.860191: 1 (0.00%)
  - 2025-11-14 19:01:18.859959: 1 (0.00%)
  - 2025-11-14 19:01:18.859699: 1 (0.00%)
  - 2025-11-14 19:01:18.859422: 1 (0.00%)
  - 2025-11-14 19:01:18.859158: 1 (0.00%)
  - 2025-11-14 19:01:18.858910: 1 (0.00%)
  - 2025-11-14 19:01:18.858661: 1 (0.00%)
  - 2025-11-14 19:01:18.858314: 1 (0.00%)
  - 2025-11-14 19:01:18.857968: 1 (0.00%)
  - ... and 49990 more values

---

## Physical Measurements Table

### Basic Information
- **Total Records:** 50,000
- **Total Columns:** 13
- **Columns:** patient_id, height_cm, weight_kg, bmi, body_fat_percentage, waist_circumference, hip_circumference, systolic_bp, diastolic_bp, resting_heart_rate, max_heart_rate, measured_at, updated_at

### Data Completeness
| Column | Null Count | Null % | Completeness % |
|--------|------------|--------|----------------|
| patient_id | 0 | 0.00% | 100.00% |
| height_cm | 0 | 0.00% | 100.00% |
| weight_kg | 0 | 0.00% | 100.00% |
| bmi | 0 | 0.00% | 100.00% |
| body_fat_percentage | 0 | 0.00% | 100.00% |
| waist_circumference | 0 | 0.00% | 100.00% |
| hip_circumference | 0 | 0.00% | 100.00% |
| systolic_bp | 0 | 0.00% | 100.00% |
| diastolic_bp | 0 | 0.00% | 100.00% |
| resting_heart_rate | 0 | 0.00% | 100.00% |
| max_heart_rate | 0 | 0.00% | 100.00% |
| measured_at | 0 | 0.00% | 100.00% |
| updated_at | 0 | 0.00% | 100.00% |

### Data Types
| Column | Data Type |
|--------|-----------|
| patient_id | int64 |
| height_cm | float64 |
| weight_kg | float64 |
| bmi | float64 |
| body_fat_percentage | float64 |
| waist_circumference | float64 |
| hip_circumference | float64 |
| systolic_bp | int64 |
| diastolic_bp | int64 |
| resting_heart_rate | int64 |
| max_heart_rate | int64 |
| measured_at | object |
| updated_at | object |

### Numeric Statistics
| Column | Mean | Median | Std Dev | Min | Max | Q25 | Q75 | Skewness |
|--------|------|--------|---------|-----|-----|-----|-----|----------|
| patient_id | 25000.50 | 25000.50 | 14433.90 | 1.00 | 50000.00 | 12500.75 | 37500.25 | 0.00 |
| height_cm | 169.50 | 169.62 | 8.27 | 140.54 | 193.39 | 162.93 | 176.02 | -0.03 |
| weight_kg | 88.34 | 87.50 | 19.55 | 40.00 | 172.16 | 74.71 | 101.07 | 0.26 |
| bmi | 30.67 | 30.63 | 6.05 | 15.96 | 53.13 | 26.55 | 34.74 | 0.07 |
| body_fat_percentage | 34.85 | 34.83 | 9.51 | 6.86 | 69.63 | 28.23 | 41.44 | 0.02 |
| waist_circumference | 84.70 | 84.72 | 6.47 | 59.84 | 110.11 | 80.25 | 89.18 | -0.02 |
| hip_circumference | 101.67 | 101.69 | 7.04 | 75.45 | 129.22 | 96.84 | 106.59 | -0.00 |
| systolic_bp | 125.45 | 125.00 | 11.54 | 90.00 | 168.00 | 118.00 | 133.00 | 0.03 |
| diastolic_bp | 81.01 | 81.00 | 8.96 | 60.00 | 120.00 | 75.00 | 87.00 | 0.08 |
| resting_heart_rate | 69.42 | 70.00 | 6.47 | 50.00 | 93.00 | 65.00 | 74.00 | -0.15 |
| max_heart_rate | 181.18 | 181.00 | 12.90 | 156.00 | 203.00 | 172.00 | 191.00 | -0.09 |

### Outlier Detection (IQR Method)
| Column | Outlier Count | Outlier % | Lower Bound | Upper Bound |
|--------|---------------|-----------|------------|-------------|
| height_cm | 3 | 0.01% | 143.30 | 195.66 |
| weight_kg | 357 | 0.71% | 35.17 | 140.61 |
| bmi | 216 | 0.43% | 14.26 | 47.03 |
| body_fat_percentage | 148 | 0.30% | 8.42 | 61.25 |
| waist_circumference | 242 | 0.48% | 66.85 | 102.58 |
| hip_circumference | 202 | 0.40% | 82.22 | 121.22 |
| systolic_bp | 401 | 0.80% | 95.50 | 155.50 |
| diastolic_bp | 160 | 0.32% | 57.00 | 105.00 |
| resting_heart_rate | 208 | 0.42% | 51.50 | 87.50 |

### Categorical Distributions
#### measured_at
- **Unique Values:** 50000
- **Most Common:** 2025-11-14 19:01:18.860423 (1 occurrences)
- **Distribution:**
  - 2025-11-14 19:01:18.860423: 1 (0.00%)
  - 2025-11-14 19:01:18.860197: 1 (0.00%)
  - 2025-11-14 19:01:18.859965: 1 (0.00%)
  - 2025-11-14 19:01:18.859705: 1 (0.00%)
  - 2025-11-14 19:01:18.859431: 1 (0.00%)
  - 2025-11-14 19:01:18.859166: 1 (0.00%)
  - 2025-11-14 19:01:18.858916: 1 (0.00%)
  - 2025-11-14 19:01:18.858669: 1 (0.00%)
  - 2025-11-14 19:01:18.858334: 1 (0.00%)
  - 2025-11-14 19:01:18.857974: 1 (0.00%)
  - ... and 49990 more values

#### updated_at
- **Unique Values:** 50000
- **Most Common:** 2025-11-14 19:01:18.860424 (1 occurrences)
- **Distribution:**
  - 2025-11-14 19:01:18.860424: 1 (0.00%)
  - 2025-11-14 19:01:18.860197: 1 (0.00%)
  - 2025-11-14 19:01:18.859966: 1 (0.00%)
  - 2025-11-14 19:01:18.859706: 1 (0.00%)
  - 2025-11-14 19:01:18.859431: 1 (0.00%)
  - 2025-11-14 19:01:18.859167: 1 (0.00%)
  - 2025-11-14 19:01:18.858917: 1 (0.00%)
  - 2025-11-14 19:01:18.858669: 1 (0.00%)
  - 2025-11-14 19:01:18.858335: 1 (0.00%)
  - 2025-11-14 19:01:18.857974: 1 (0.00%)
  - ... and 49990 more values

---

## Lifestyle Table

### Basic Information
- **Total Records:** 50,000
- **Total Columns:** 15
- **Columns:** patient_id, smoking_status, years_smoking, cigarettes_per_day, pack_years, alcohol_consumption, drinks_per_week, drinking_frequency, physical_activity_level, exercise_hours_per_week, steps_per_day, diet_type, sleep_hours_per_night, sleep_quality, updated_at

### Data Completeness
| Column | Null Count | Null % | Completeness % |
|--------|------------|--------|----------------|
| patient_id | 0 | 0.00% | 100.00% |
| smoking_status | 0 | 0.00% | 100.00% |
| years_smoking | 0 | 0.00% | 100.00% |
| cigarettes_per_day | 0 | 0.00% | 100.00% |
| pack_years | 0 | 0.00% | 100.00% |
| alcohol_consumption | 0 | 0.00% | 100.00% |
| drinks_per_week | 0 | 0.00% | 100.00% |
| drinking_frequency | 0 | 0.00% | 100.00% |
| physical_activity_level | 0 | 0.00% | 100.00% |
| exercise_hours_per_week | 0 | 0.00% | 100.00% |
| steps_per_day | 0 | 0.00% | 100.00% |
| diet_type | 0 | 0.00% | 100.00% |
| sleep_hours_per_night | 0 | 0.00% | 100.00% |
| sleep_quality | 0 | 0.00% | 100.00% |
| updated_at | 0 | 0.00% | 100.00% |

### Data Types
| Column | Data Type |
|--------|-----------|
| patient_id | int64 |
| smoking_status | object |
| years_smoking | int64 |
| cigarettes_per_day | int64 |
| pack_years | float64 |
| alcohol_consumption | object |
| drinks_per_week | int64 |
| drinking_frequency | object |
| physical_activity_level | object |
| exercise_hours_per_week | float64 |
| steps_per_day | int64 |
| diet_type | object |
| sleep_hours_per_night | float64 |
| sleep_quality | object |
| updated_at | object |

### Numeric Statistics
| Column | Mean | Median | Std Dev | Min | Max | Q25 | Q75 | Skewness |
|--------|------|--------|---------|-----|-----|-----|-----|----------|
| patient_id | 25000.50 | 25000.50 | 14433.90 | 1.00 | 50000.00 | 12500.75 | 37500.25 | 0.00 |
| years_smoking | 3.95 | 0.00 | 9.61 | 0.00 | 46.00 | 0.00 | 0.00 | 2.52 |
| cigarettes_per_day | 3.48 | 0.00 | 7.59 | 0.00 | 29.00 | 0.00 | 0.00 | 2.06 |
| pack_years | 3.36 | 0.00 | 8.97 | 0.00 | 66.70 | 0.00 | 0.00 | 3.24 |
| drinks_per_week | 2.79 | 2.00 | 3.47 | 0.00 | 19.00 | 0.00 | 5.00 | 2.23 |
| exercise_hours_per_week | 3.07 | 2.52 | 2.67 | 0.00 | 14.99 | 0.91 | 4.42 | 1.47 |
| steps_per_day | 7377.53 | 6520.00 | 3975.45 | 2000.00 | 24989.00 | 4738.75 | 9121.25 | 1.48 |
| sleep_hours_per_night | 7.50 | 7.50 | 0.99 | 5.00 | 10.00 | 6.80 | 8.20 | 0.01 |

### Outlier Detection (IQR Method)
| Column | Outlier Count | Outlier % | Lower Bound | Upper Bound |
|--------|---------------|-----------|------------|-------------|
| years_smoking | 10,208 | 20.42% | 0.00 | 0.00 |
| cigarettes_per_day | 10,208 | 20.42% | 0.00 | 0.00 |
| pack_years | 10,208 | 20.42% | 0.00 | 0.00 |
| drinks_per_week | 1,742 | 3.48% | -7.50 | 12.50 |
| exercise_hours_per_week | 1,443 | 2.89% | -4.35 | 9.68 |
| steps_per_day | 1,765 | 3.53% | -1835.00 | 15695.00 |

### Categorical Distributions
#### smoking_status
- **Unique Values:** 2
- **Most Common:** never (39,792 occurrences)
- **Distribution:**
  - never: 39,792 (79.58%)
  - current: 10,208 (20.42%)

#### alcohol_consumption
- **Unique Values:** 4
- **Most Common:** occasional (18,930 occurrences)
- **Distribution:**
  - occasional: 18,930 (37.86%)
  - moderate: 14,165 (28.33%)
  - none: 13,926 (27.85%)
  - heavy: 2,979 (5.96%)

#### drinking_frequency
- **Unique Values:** 2
- **Most Common:** weekly (36,074 occurrences)
- **Distribution:**
  - weekly: 36,074 (72.15%)
  - never: 13,926 (27.85%)

#### physical_activity_level
- **Unique Values:** 5
- **Most Common:** light (14,799 occurrences)
- **Distribution:**
  - light: 14,799 (29.60%)
  - sedentary: 13,727 (27.45%)
  - moderate: 12,712 (25.42%)
  - active: 6,839 (13.68%)
  - very_active: 1,923 (3.85%)

#### diet_type
- **Unique Values:** 5
- **Most Common:** omnivore (34,912 occurrences)
- **Distribution:**
  - omnivore: 34,912 (69.82%)
  - vegetarian: 7,495 (14.99%)
  - vegan: 2,571 (5.14%)
  - pescatarian: 2,521 (5.04%)
  - mediterranean: 2,501 (5.00%)

#### sleep_quality
- **Unique Values:** 4
- **Most Common:** good (22,518 occurrences)
- **Distribution:**
  - good: 22,518 (45.04%)
  - fair: 12,452 (24.90%)
  - excellent: 7,705 (15.41%)
  - poor: 7,325 (14.65%)

#### updated_at
- **Unique Values:** 50000
- **Most Common:** 2025-11-14 19:01:18.860425 (1 occurrences)
- **Distribution:**
  - 2025-11-14 19:01:18.860425: 1 (0.00%)
  - 2025-11-14 19:01:18.860198: 1 (0.00%)
  - 2025-11-14 19:01:18.859968: 1 (0.00%)
  - 2025-11-14 19:01:18.859706: 1 (0.00%)
  - 2025-11-14 19:01:18.859433: 1 (0.00%)
  - 2025-11-14 19:01:18.859169: 1 (0.00%)
  - 2025-11-14 19:01:18.858919: 1 (0.00%)
  - 2025-11-14 19:01:18.858670: 1 (0.00%)
  - 2025-11-14 19:01:18.858339: 1 (0.00%)
  - 2025-11-14 19:01:18.857975: 1 (0.00%)
  - ... and 49990 more values

---

## Socioeconomic Table

### Basic Information
- **Total Records:** 50,000
- **Total Columns:** 17
- **Columns:** patient_id, region, employment_status, education_level, annual_income, housing_type, household_size, insurance_type, insurance_plan_type, deductible, copay_amount, out_of_pocket_max, residential_area, years_with_insurance, coverage_gaps, total_days_without_insurance, updated_at

### Data Completeness
| Column | Null Count | Null % | Completeness % |
|--------|------------|--------|----------------|
| patient_id | 0 | 0.00% | 100.00% |
| region | 0 | 0.00% | 100.00% |
| employment_status | 0 | 0.00% | 100.00% |
| education_level | 0 | 0.00% | 100.00% |
| annual_income | 0 | 0.00% | 100.00% |
| housing_type | 0 | 0.00% | 100.00% |
| household_size | 0 | 0.00% | 100.00% |
| insurance_type | 0 | 0.00% | 100.00% |
| insurance_plan_type | 2,142 | 4.28% | 95.72% |
| deductible | 2,142 | 4.28% | 95.72% |
| copay_amount | 2,142 | 4.28% | 95.72% |
| out_of_pocket_max | 2,142 | 4.28% | 95.72% |
| residential_area | 0 | 0.00% | 100.00% |
| years_with_insurance | 0 | 0.00% | 100.00% |
| coverage_gaps | 0 | 0.00% | 100.00% |
| total_days_without_insurance | 0 | 0.00% | 100.00% |
| updated_at | 0 | 0.00% | 100.00% |

### Data Types
| Column | Data Type |
|--------|-----------|
| patient_id | int64 |
| region | object |
| employment_status | object |
| education_level | object |
| annual_income | float64 |
| housing_type | object |
| household_size | int64 |
| insurance_type | object |
| insurance_plan_type | object |
| deductible | float64 |
| copay_amount | float64 |
| out_of_pocket_max | float64 |
| residential_area | object |
| years_with_insurance | int64 |
| coverage_gaps | int64 |
| total_days_without_insurance | int64 |
| updated_at | object |

### Numeric Statistics
| Column | Mean | Median | Std Dev | Min | Max | Q25 | Q75 | Skewness |
|--------|------|--------|---------|-----|-----|-----|-----|----------|
| patient_id | 25000.50 | 25000.50 | 14433.90 | 1.00 | 50000.00 | 12500.75 | 37500.25 | 0.00 |
| annual_income | 62939.65 | 56165.31 | 29583.82 | 16826.13 | 233903.84 | 41669.61 | 78022.18 | 1.33 |
| household_size | 2.81 | 3.00 | 1.29 | 1.00 | 7.00 | 2.00 | 4.00 | 0.71 |
| deductible | 2652.78 | 2313.21 | 1471.46 | 500.02 | 6999.71 | 1440.62 | 3753.41 | 0.63 |
| copay_amount | 35.08 | 35.07 | 8.68 | 20.00 | 50.00 | 27.56 | 42.59 | -0.00 |
| out_of_pocket_max | 6631.95 | 5783.02 | 3678.66 | 1250.05 | 17499.28 | 3601.56 | 9383.51 | 0.63 |
| years_with_insurance | 10.01 | 10.00 | 5.47 | 1.00 | 19.00 | 5.00 | 15.00 | -0.01 |
| coverage_gaps | 0.16 | 0.00 | 0.43 | 0.00 | 5.00 | 0.00 | 0.00 | 3.11 |
| total_days_without_insurance | 29.54 | 20.00 | 30.00 | 0.00 | 318.00 | 8.00 | 41.00 | 1.98 |

### Outlier Detection (IQR Method)
| Column | Outlier Count | Outlier % | Lower Bound | Upper Bound |
|--------|---------------|-----------|------------|-------------|
| annual_income | 1,389 | 2.78% | -12859.23 | 132551.03 |
| coverage_gaps | 6,798 | 13.60% | 0.00 | 0.00 |
| total_days_without_insurance | 2,385 | 4.77% | -41.50 | 90.50 |

### Categorical Distributions
#### region
- **Unique Values:** 4
- **Most Common:** southeast (13,517 occurrences)
- **Distribution:**
  - southeast: 13,517 (27.03%)
  - southwest: 12,229 (24.46%)
  - northwest: 12,160 (24.32%)
  - northeast: 12,094 (24.19%)

#### employment_status
- **Unique Values:** 3
- **Most Common:** employed (39,766 occurrences)
- **Distribution:**
  - employed: 39,766 (79.53%)
  - student: 5,711 (11.42%)
  - unemployed: 4,523 (9.05%)

#### education_level
- **Unique Values:** 6
- **Most Common:** some_college (13,857 occurrences)
- **Distribution:**
  - some_college: 13,857 (27.71%)
  - high_school: 12,891 (25.78%)
  - bachelor: 11,276 (22.55%)
  - less_than_high_school: 7,461 (14.92%)
  - master: 3,708 (7.42%)
  - doctorate: 807 (1.61%)

#### housing_type
- **Unique Values:** 3
- **Most Common:** owned (26,960 occurrences)
- **Distribution:**
  - owned: 26,960 (53.92%)
  - rented: 19,568 (39.14%)
  - other: 3,472 (6.94%)

#### insurance_type
- **Unique Values:** 5
- **Most Common:** employer (31,780 occurrences)
- **Distribution:**
  - employer: 31,780 (63.56%)
  - individual: 11,000 (22.00%)
  - medicaid: 3,057 (6.11%)
  - uninsured: 2,142 (4.28%)
  - medicare: 2,021 (4.04%)

#### insurance_plan_type
- **Unique Values:** 5
- **Most Common:** PPO (19,107 occurrences)
- **Distribution:**
  - PPO: 19,107 (38.21%)
  - HMO: 14,406 (28.81%)
  - HDHP: 4,885 (9.77%)
  - POS: 4,781 (9.56%)
  - EPO: 4,679 (9.36%)

#### residential_area
- **Unique Values:** 3
- **Most Common:** suburban (22,520 occurrences)
- **Distribution:**
  - suburban: 22,520 (45.04%)
  - urban: 19,911 (39.82%)
  - rural: 7,569 (15.14%)

#### updated_at
- **Unique Values:** 50000
- **Most Common:** 2025-11-14 19:01:18.860426 (1 occurrences)
- **Distribution:**
  - 2025-11-14 19:01:18.860426: 1 (0.00%)
  - 2025-11-14 19:01:18.860199: 1 (0.00%)
  - 2025-11-14 19:01:18.859968: 1 (0.00%)
  - 2025-11-14 19:01:18.859707: 1 (0.00%)
  - 2025-11-14 19:01:18.859434: 1 (0.00%)
  - 2025-11-14 19:01:18.859170: 1 (0.00%)
  - 2025-11-14 19:01:18.858919: 1 (0.00%)
  - 2025-11-14 19:01:18.858671: 1 (0.00%)
  - 2025-11-14 19:01:18.858340: 1 (0.00%)
  - 2025-11-14 19:01:18.857975: 1 (0.00%)
  - ... and 49990 more values

---

## Medical History Table

### Basic Information
- **Total Records:** 13,959
- **Total Columns:** 8
- **Columns:** patient_id, condition_type, condition_name, severity, years_since_diagnosis, medication_controlled, diagnosis_date, created_at

### Data Completeness
| Column | Null Count | Null % | Completeness % |
|--------|------------|--------|----------------|
| patient_id | 0 | 0.00% | 100.00% |
| condition_type | 0 | 0.00% | 100.00% |
| condition_name | 0 | 0.00% | 100.00% |
| severity | 0 | 0.00% | 100.00% |
| years_since_diagnosis | 0 | 0.00% | 100.00% |
| medication_controlled | 0 | 0.00% | 100.00% |
| diagnosis_date | 0 | 0.00% | 100.00% |
| created_at | 0 | 0.00% | 100.00% |

### Data Types
| Column | Data Type |
|--------|-----------|
| patient_id | int64 |
| condition_type | object |
| condition_name | object |
| severity | object |
| years_since_diagnosis | int64 |
| medication_controlled | bool |
| diagnosis_date | object |
| created_at | object |

### Numeric Statistics
| Column | Mean | Median | Std Dev | Min | Max | Q25 | Q75 | Skewness |
|--------|------|--------|---------|-----|-----|-----|-----|----------|
| patient_id | 25331.29 | 25639.00 | 14384.23 | 8.00 | 49998.00 | 12995.50 | 37816.50 | -0.03 |
| years_since_diagnosis | 11.19 | 9.00 | 9.48 | 1.00 | 45.00 | 3.00 | 17.00 | 1.06 |

### Outlier Detection (IQR Method)
| Column | Outlier Count | Outlier % | Lower Bound | Upper Bound |
|--------|---------------|-----------|------------|-------------|
| years_since_diagnosis | 168 | 1.20% | -18.00 | 38.00 |

### Categorical Distributions
#### condition_type
- **Unique Values:** 3
- **Most Common:** hypertension (8,447 occurrences)
- **Distribution:**
  - hypertension: 8,447 (60.51%)
  - diabetes: 4,590 (32.88%)
  - heart_disease: 922 (6.61%)

#### condition_name
- **Unique Values:** 3
- **Most Common:** Hypertension (8,447 occurrences)
- **Distribution:**
  - Hypertension: 8,447 (60.51%)
  - Type 2 Diabetes: 4,590 (32.88%)
  - Coronary Artery Disease: 922 (6.61%)

#### severity
- **Unique Values:** 3
- **Most Common:** mild (8,760 occurrences)
- **Distribution:**
  - mild: 8,760 (62.76%)
  - moderate: 4,677 (33.51%)
  - severe: 522 (3.74%)

#### diagnosis_date
- **Unique Values:** 13959
- **Most Common:** 2024-11-14 19:01:18.863874 (1 occurrences)
- **Distribution:**
  - 2024-11-14 19:01:18.863874: 1 (0.01%)
  - 2022-11-15 18:38:25.464775: 1 (0.01%)
  - 2004-11-19 18:38:25.465285: 1 (0.01%)
  - 2016-11-16 18:38:25.467017: 1 (0.01%)
  - 1989-11-23 18:38:25.467178: 1 (0.01%)
  - 2015-11-17 18:38:25.467340: 1 (0.01%)
  - 2019-11-16 18:38:25.469433: 1 (0.01%)
  - 2014-11-17 19:01:18.850486: 1 (0.01%)
  - 2018-11-16 19:01:18.849501: 1 (0.01%)
  - 2021-11-15 19:01:18.847782: 1 (0.01%)
  - ... and 13949 more values

#### created_at
- **Unique Values:** 13958
- **Most Common:** 2025-11-14 19:01:15.940458 (2 occurrences)
- **Distribution:**
  - 2025-11-14 19:01:15.940458: 2 (0.01%)
  - 2025-11-14 19:01:18.863875: 1 (0.01%)
  - 2025-11-14 18:38:25.464776: 1 (0.01%)
  - 2025-11-14 18:38:25.465286: 1 (0.01%)
  - 2025-11-14 18:38:25.467018: 1 (0.01%)
  - 2025-11-14 18:38:25.467179: 1 (0.01%)
  - 2025-11-14 19:01:18.850725: 1 (0.01%)
  - 2025-11-14 19:01:18.851174: 1 (0.01%)
  - 2025-11-14 19:01:18.851857: 1 (0.01%)
  - 2025-11-14 19:01:18.852779: 1 (0.01%)
  - ... and 13948 more values

---

## Lab Results Table

### Basic Information
- **Total Records:** 50,000
- **Total Columns:** 12
- **Columns:** patient_id, test_date, test_type, total_cholesterol, ldl_cholesterol, hdl_cholesterol, triglycerides, glucose, hba1c, creatinine, egfr, created_at

### Data Completeness
| Column | Null Count | Null % | Completeness % |
|--------|------------|--------|----------------|
| patient_id | 0 | 0.00% | 100.00% |
| test_date | 0 | 0.00% | 100.00% |
| test_type | 0 | 0.00% | 100.00% |
| total_cholesterol | 0 | 0.00% | 100.00% |
| ldl_cholesterol | 0 | 0.00% | 100.00% |
| hdl_cholesterol | 0 | 0.00% | 100.00% |
| triglycerides | 0 | 0.00% | 100.00% |
| glucose | 0 | 0.00% | 100.00% |
| hba1c | 0 | 0.00% | 100.00% |
| creatinine | 0 | 0.00% | 100.00% |
| egfr | 0 | 0.00% | 100.00% |
| created_at | 0 | 0.00% | 100.00% |

### Data Types
| Column | Data Type |
|--------|-----------|
| patient_id | int64 |
| test_date | object |
| test_type | object |
| total_cholesterol | float64 |
| ldl_cholesterol | float64 |
| hdl_cholesterol | float64 |
| triglycerides | float64 |
| glucose | float64 |
| hba1c | float64 |
| creatinine | float64 |
| egfr | float64 |
| created_at | object |

### Numeric Statistics
| Column | Mean | Median | Std Dev | Min | Max | Q25 | Q75 | Skewness |
|--------|------|--------|---------|-----|-----|-----|-----|----------|
| patient_id | 25000.50 | 25000.50 | 14433.90 | 1.00 | 50000.00 | 12500.75 | 37500.25 | 0.00 |
| total_cholesterol | 204.62 | 204.58 | 25.03 | 100.00 | 300.00 | 187.53 | 221.43 | 0.02 |
| ldl_cholesterol | 133.03 | 133.05 | 22.07 | 50.00 | 224.49 | 118.06 | 147.79 | 0.01 |
| hdl_cholesterol | 53.93 | 53.92 | 9.62 | 30.00 | 98.68 | 47.28 | 60.60 | 0.01 |
| triglycerides | 132.74 | 132.06 | 42.44 | 50.00 | 298.91 | 102.73 | 161.52 | 0.16 |
| glucose | 94.11 | 94.09 | 9.33 | 70.00 | 120.00 | 87.78 | 100.43 | 0.01 |
| hba1c | 4.91 | 4.90 | 0.38 | 4.00 | 6.50 | 4.65 | 5.16 | 0.05 |
| creatinine | 0.91 | 0.90 | 0.16 | 0.50 | 1.49 | 0.79 | 1.02 | 0.02 |
| egfr | 102.58 | 103.58 | 12.94 | 60.00 | 120.00 | 93.47 | 113.45 | -0.44 |

### Outlier Detection (IQR Method)
| Column | Outlier Count | Outlier % | Lower Bound | Upper Bound |
|--------|---------------|-----------|------------|-------------|
| total_cholesterol | 313 | 0.63% | 136.68 | 272.29 |
| ldl_cholesterol | 355 | 0.71% | 73.47 | 192.38 |
| hdl_cholesterol | 97 | 0.19% | 27.30 | 80.58 |
| triglycerides | 174 | 0.35% | 14.55 | 249.71 |
| glucose | 148 | 0.30% | 68.80 | 119.41 |
| hba1c | 164 | 0.33% | 3.89 | 5.92 |
| creatinine | 30 | 0.06% | 0.45 | 1.36 |
| egfr | 84 | 0.17% | 63.50 | 143.42 |

### Categorical Distributions
#### test_date
- **Unique Values:** 50000
- **Most Common:** 2024-12-02 19:01:18.860427 (1 occurrences)
- **Distribution:**
  - 2024-12-02 19:01:18.860427: 1 (0.00%)
  - 2025-08-29 19:01:18.860199: 1 (0.00%)
  - 2025-10-25 19:01:18.859970: 1 (0.00%)
  - 2025-01-21 19:01:18.859708: 1 (0.00%)
  - 2025-07-12 19:01:18.859434: 1 (0.00%)
  - 2025-08-09 19:01:18.859173: 1 (0.00%)
  - 2025-02-21 19:01:18.858920: 1 (0.00%)
  - 2025-01-08 19:01:18.858671: 1 (0.00%)
  - 2025-07-03 19:01:18.858341: 1 (0.00%)
  - 2025-07-01 19:01:18.857976: 1 (0.00%)
  - ... and 49990 more values

#### test_type
- **Unique Values:** 1
- **Most Common:** comprehensive (50,000 occurrences)
- **Distribution:**
  - comprehensive: 50,000 (100.00%)

#### created_at
- **Unique Values:** 50000
- **Most Common:** 2025-11-14 19:01:18.860430 (1 occurrences)
- **Distribution:**
  - 2025-11-14 19:01:18.860430: 1 (0.00%)
  - 2025-11-14 19:01:18.860203: 1 (0.00%)
  - 2025-11-14 19:01:18.859974: 1 (0.00%)
  - 2025-11-14 19:01:18.859713: 1 (0.00%)
  - 2025-11-14 19:01:18.859439: 1 (0.00%)
  - 2025-11-14 19:01:18.859176: 1 (0.00%)
  - 2025-11-14 19:01:18.858924: 1 (0.00%)
  - 2025-11-14 19:01:18.858678: 1 (0.00%)
  - 2025-11-14 19:01:18.858350: 1 (0.00%)
  - 2025-11-14 19:01:18.857979: 1 (0.00%)
  - ... and 49990 more values

---

## Data Consistency Across Tables

✅ **No consistency issues found** - All patient IDs are properly linked across tables.

## Key Data Quality Insights

### Patient Demographics
- **Age Range:** 17.0 - 64.0 years
- **Average Age:** 38.8 years
- **Sex Distribution:**
  - male: 25,404 (50.8%)
  - female: 24,596 (49.2%)

### Insurance Cost Analysis
- **Average Cost:** $16,537.29
- **Median Cost:** $15,713.15
- **Cost Range:** $1,121.87 - $63,770.43

### Medical Conditions Coverage
- **Patients with Medical History:** 12,691
- **Total Medical Conditions:** 13,959
  - hypertension: 8,447
  - diabetes: 4,590
  - heart_disease: 922

## Overall Data Quality Score

### Quality Metrics:
- **Completeness Score:** 99.8/100
- **Consistency Score:** 100.0/100
- **Range Validity Score:** 100.0/100
- **Overall Quality Score:** 99.9/100

## Recommendations

- ✅ Data is suitable for machine learning model training
- ✅ Data distributions appear realistic and well-balanced
- ✅ All tables are properly linked via patient_id

---

*Report generated automatically on 2025-11-14 19:03:50*