# Complete Patient Data Schema for Insurance Cost Prediction

## Overview

This document describes all patient data fields that can be useful for training a federated learning model to predict medical insurance costs. The data is categorized by type and includes both structured and unstructured data.

## 1. Basic Demographics

### Personal Information
- **Age** (integer, 0-120)
  - Primary factor in insurance cost calculation
  - Age groups: infant, child, adolescent, adult, senior
  
- **Sex/Gender** (categorical: male, female, other)
  - Biological sex for medical risk assessment
  
- **Date of Birth** (date)
  - Allows calculation of exact age
  - Can identify generational health patterns

- **Marital Status** (categorical: single, married, divorced, widowed, domestic_partner)
  - Married individuals often have lower rates
  - Affects family coverage calculations

- **Number of Dependents** (integer, 0-20)
  - Children count for family plans
  - Affects total coverage cost

## 2. Physical Characteristics

### Body Metrics
- **Height** (float, cm or inches)
  - Used with weight to calculate BMI
  
- **Weight** (float, kg or lbs)
  - Used with height to calculate BMI
  
- **BMI (Body Mass Index)** (float, 10-50)
  - Calculated: weight(kg) / height(m)²
  - Strong predictor of health risks
  - Categories: underweight (<18.5), normal (18.5-24.9), overweight (25-29.9), obese (≥30)

- **Body Fat Percentage** (float, 5-50%)
  - More accurate than BMI for health assessment
  
- **Waist Circumference** (float, cm)
  - Indicator of abdominal obesity
  - Metabolic risk factor

- **Hip Circumference** (float, cm)
  - Used with waist for waist-to-hip ratio

- **Waist-to-Hip Ratio** (float, 0.5-1.5)
  - Indicator of fat distribution
  - Health risk assessment

### Physical Measurements
- **Blood Pressure** (systolic/diastolic, mmHg)
  - Systolic: 90-200
  - Diastolic: 60-120
  - Hypertension indicators
  
- **Resting Heart Rate** (integer, 40-120 bpm)
  - Cardiovascular health indicator
  
- **Maximum Heart Rate** (integer, bpm)
  - Calculated or measured
  - Exercise capacity indicator

## 3. Lifestyle Factors

### Smoking and Substance Use
- **Smoking Status** (categorical: never, former, current)
  - Current smoker: yes/no
  - Years of smoking (integer, 0-80)
  - Cigarettes per day (integer, 0-100)
  - Pack-years (float)
  - Quit date (date, if former smoker)
  - Years since quitting (integer)

- **Alcohol Consumption** (categorical: none, occasional, moderate, heavy)
  - Drinks per week (integer, 0-100)
  - Drinking frequency (daily, weekly, monthly, rarely)
  - Type of alcohol (beer, wine, spirits, mixed)

- **Recreational Drug Use** (boolean)
  - Type of drugs (categorical)
  - Frequency of use
  - Years of use

### Exercise and Activity
- **Physical Activity Level** (categorical: sedentary, light, moderate, active, very_active)
  - Hours of exercise per week (float, 0-50)
  - Type of exercise (cardio, strength, flexibility, sports)
  - Exercise intensity (low, moderate, high)
  - Steps per day (integer, 0-50000)
  - Active minutes per week (integer)

- **Sedentary Hours per Day** (float, 0-24)
  - Screen time
  - Desk job indicator

- **Sleep Patterns**
  - Average hours of sleep per night (float, 3-12)
  - Sleep quality (categorical: poor, fair, good, excellent)
  - Sleep disorders (boolean: insomnia, sleep apnea, restless leg)

### Diet and Nutrition
- **Diet Type** (categorical: omnivore, vegetarian, vegan, pescatarian, keto, paleo, mediterranean)
  - Meals per day (integer, 1-6)
  - Fast food consumption (frequency: daily, weekly, monthly, rarely)
  - Processed food consumption (frequency)
  - Fruit and vegetable servings per day (float, 0-20)
  - Water intake per day (liters, 0-10)

## 4. Medical History

### Chronic Conditions
- **Diabetes** (boolean)
  - Type (Type 1, Type 2, gestational, prediabetes)
  - Years since diagnosis (integer)
  - HbA1c level (float, 4-15%)
  - Medication use (boolean)
  - Complications (boolean: neuropathy, retinopathy, nephropathy)

- **Hypertension** (boolean)
  - Years since diagnosis
  - Medication use
  - Controlled/Uncontrolled status

- **Heart Disease** (boolean)
  - Type (coronary artery disease, heart failure, arrhythmia, etc.)
  - Years since diagnosis
  - Previous heart attack (boolean)
  - Previous stroke (boolean)

- **Respiratory Conditions**
  - Asthma (boolean, severity: mild, moderate, severe)
  - COPD (boolean, stages 1-4)
  - Chronic bronchitis (boolean)
  - Emphysema (boolean)

- **Mental Health**
  - Depression (boolean, severity)
  - Anxiety (boolean, severity)
  - Bipolar disorder (boolean)
  - Schizophrenia (boolean)
  - PTSD (boolean)
  - Other mental health conditions

- **Autoimmune Diseases**
  - Rheumatoid arthritis (boolean)
  - Lupus (boolean)
  - Multiple sclerosis (boolean)
  - Crohn's disease (boolean)
  - Ulcerative colitis (boolean)
  - Other autoimmune conditions

- **Cancer History** (boolean)
  - Type of cancer
  - Stage at diagnosis
  - Years since diagnosis
  - Treatment status (active, remission, cured)
  - Recurrence (boolean)

### Family Medical History
- **Parental Health**
  - Father's age at death (integer, or alive)
  - Mother's age at death (integer, or alive)
  - Father's cause of death (categorical)
  - Mother's cause of death (categorical)
  - Parental diabetes (boolean)
  - Parental heart disease (boolean)
  - Parental cancer (boolean, type)

- **Sibling Health**
  - Number of siblings (integer)
  - Sibling health conditions (list)
  - Genetic conditions in family (boolean)

## 5. Current Medications

### Medication List
- **Prescription Medications** (list)
  - Medication name
  - Dosage
  - Frequency
  - Years of use
  - Condition treated

- **Over-the-Counter Medications** (list)
  - Type and frequency

- **Supplements** (list)
  - Vitamins, minerals, herbal supplements

- **Medication Adherence** (categorical: excellent, good, fair, poor)
  - Percentage of medications taken as prescribed (0-100%)

## 6. Laboratory Results

### Blood Tests
- **Complete Blood Count (CBC)**
  - Hemoglobin (g/dL, 10-20)
  - Hematocrit (%, 30-60)
  - White blood cell count (cells/μL)
  - Platelet count (cells/μL)

- **Lipid Panel**
  - Total cholesterol (mg/dL, 100-400)
  - LDL cholesterol (mg/dL, 50-300)
  - HDL cholesterol (mg/dL, 20-100)
  - Triglycerides (mg/dL, 50-1000)

- **Metabolic Panel**
  - Glucose (mg/dL, 70-200)
  - HbA1c (%, 4-15)
  - Creatinine (mg/dL, 0.5-2.0)
  - eGFR (mL/min/1.73m², 15-120)
  - BUN (mg/dL, 5-30)

- **Liver Function**
  - ALT (U/L, 5-50)
  - AST (U/L, 5-50)
  - Bilirubin (mg/dL, 0.1-2.0)
  - Albumin (g/dL, 3.0-5.5)

- **Thyroid Function**
  - TSH (mIU/L, 0.5-5.0)
  - T3 (ng/dL)
  - T4 (μg/dL)

- **Vitamin Levels**
  - Vitamin D (ng/mL, 10-100)
  - Vitamin B12 (pg/mL, 200-900)
  - Folate (ng/mL, 3-20)

### Other Tests
- **Kidney Function**
  - Creatinine clearance
  - Urine protein

- **Cardiac Markers**
  - Troponin (ng/mL)
  - BNP (pg/mL)

## 7. Healthcare Utilization

### Medical Visits
- **Primary Care Visits per Year** (integer, 0-50)
- **Specialist Visits per Year** (integer, 0-100)
- **Emergency Room Visits per Year** (integer, 0-50)
- **Hospitalizations per Year** (integer, 0-20)
- **Average Hospital Stay Length** (days, 0-365)
- **ICU Admissions** (integer, 0-10)
- **Surgical Procedures** (integer, 0-50)
  - Type of procedures
  - Years since last surgery

### Preventive Care
- **Annual Physical Exam** (boolean, last date)
- **Vaccination Status** (boolean)
  - Flu vaccine (current year)
  - COVID-19 vaccine (doses, dates)
  - Other vaccinations

- **Screening Tests**
  - Mammography (last date, frequency)
  - Colonoscopy (last date, frequency)
  - Pap smear (last date, frequency)
  - PSA test (last date, for males)
  - Bone density scan (last date)

## 8. Socioeconomic Factors

### Employment and Income
- **Employment Status** (categorical: employed, unemployed, retired, disabled, student)
- **Occupation** (categorical: professional, service, manual, healthcare, education, etc.)
- **Industry** (categorical)
- **Annual Income** (float, $0-$10M+)
  - Income brackets
- **Education Level** (categorical: less_than_high_school, high_school, some_college, bachelor, master, doctorate)

### Living Situation
- **Residential Area** (categorical: urban, suburban, rural)
- **Region** (categorical: northeast, northwest, southeast, southwest, midwest)
- **State** (categorical, 50 US states)
- **Zip Code** (string, 5 digits)
- **Housing Type** (categorical: owned, rented, other)
- **Household Size** (integer, 1-20)

### Insurance Information
- **Current Insurance Type** (categorical: employer, individual, medicare, medicaid, uninsured)
- **Insurance Plan Type** (categorical: HMO, PPO, EPO, POS, HDHP)
- **Deductible** (float, $0-$50,000)
- **Co-pay Amount** (float, $0-$500)
- **Out-of-Pocket Maximum** (float, $0-$100,000)
- **Previous Insurance Claims** (float, total annual)
- **Insurance History** (years with insurance, gaps in coverage)

## 9. Behavioral and Psychosocial Factors

### Stress and Mental Well-being
- **Stress Level** (categorical: low, moderate, high, very_high)
- **Perceived Stress Scale** (integer, 0-40)
- **Work-Life Balance** (categorical: poor, fair, good, excellent)
- **Social Support** (categorical: none, low, moderate, high)
- **Marital Satisfaction** (categorical, if applicable)

### Health Behaviors
- **Health Literacy** (categorical: low, moderate, high)
- **Health Seeking Behavior** (categorical: proactive, reactive, avoidant)
- **Preventive Care Adherence** (percentage, 0-100%)
- **Medication Adherence** (percentage, 0-100%)

## 10. Environmental Factors

### Living Environment
- **Air Quality Index** (integer, 0-500)
  - Based on location
- **Water Quality** (categorical: excellent, good, fair, poor)
- **Proximity to Healthcare** (float, miles to nearest hospital)
- **Number of Healthcare Facilities Nearby** (integer, 0-50)
- **Rural/Urban Classification** (categorical)

### Occupational Hazards
- **Occupational Risk Level** (categorical: low, moderate, high, very_high)
- **Exposure to Toxins** (boolean)
- **Physical Demands** (categorical: sedentary, light, moderate, heavy, very_heavy)
- **Work Schedule** (categorical: day, night, shift, irregular)

## 11. Pregnancy and Reproductive Health

### For Females
- **Pregnancy Status** (boolean)
- **Number of Pregnancies** (integer, 0-20)
- **Number of Live Births** (integer, 0-20)
- **Complications During Pregnancy** (boolean, list)
- **Gestational Diabetes** (boolean)
- **Pre-eclampsia** (boolean)
- **Menopause Status** (categorical: pre, peri, post, not_applicable)
- **Age at Menopause** (integer, if applicable)
- **Hormone Replacement Therapy** (boolean)

## 12. Additional Health Indicators

### Functional Status
- **Activities of Daily Living (ADL) Score** (integer, 0-6)
- **Instrumental ADL Score** (integer, 0-8)
- **Mobility Status** (categorical: independent, assistive_device, wheelchair, bedbound)
- **Fall Risk** (categorical: low, moderate, high)
- **Number of Falls in Past Year** (integer, 0-50)

### Pain and Symptoms
- **Chronic Pain** (boolean)
- **Pain Level** (integer, 0-10 scale)
- **Pain Locations** (list: back, joint, headache, etc.)
- **Pain Duration** (categorical: acute, chronic)

### Quality of Life
- **Quality of Life Score** (integer, 0-100)
- **Health-Related Quality of Life** (HRQoL, 0-100)
- **Functional Status** (categorical: excellent, good, fair, poor)

## 13. Temporal and Historical Data

### Time-Based Features
- **Days Since Last Medical Visit** (integer, 0-3650)
- **Days Since Last Hospitalization** (integer, 0-3650)
- **Days Since Last Emergency Visit** (integer, 0-3650)
- **Years with Current Insurance** (float, 0-100)
- **Insurance Coverage Gaps** (integer, number of gaps)
- **Total Days Without Insurance** (integer, 0-36500)

### Historical Trends
- **BMI Trend** (categorical: increasing, stable, decreasing)
- **Blood Pressure Trend** (categorical)
- **Medication Changes** (integer, number of changes in past year)
- **Diagnosis Changes** (integer, new diagnoses in past year)

## 14. Derived and Calculated Features

### Risk Scores
- **Framingham Risk Score** (float, 0-100)
  - 10-year cardiovascular risk
- **Charlson Comorbidity Index** (integer, 0-30)
  - Predicts mortality risk
- **Elixhauser Comorbidity Index** (integer, 0-30)
- **Mortality Risk Score** (float, 0-100)

### Composite Metrics
- **Overall Health Score** (float, 0-100)
  - Composite of multiple factors
- **Risk Stratification** (categorical: low, moderate, high, very_high)
- **Complexity Score** (integer, 0-100)
  - Based on number of conditions, medications, visits

## 15. Unstructured Data (for Future NLP)

### Clinical Notes
- **Chief Complaint** (text)
- **History of Present Illness** (text)
- **Review of Systems** (text)
- **Physical Examination Notes** (text)
- **Assessment and Plan** (text)
- **Progress Notes** (text, multiple entries)

### Patient-Reported Outcomes
- **Patient Surveys** (text responses)
- **Symptom Descriptions** (text)
- **Quality of Life Questionnaires** (text)

## Data Preprocessing Considerations

### Categorical Encoding
- One-hot encoding for nominal categories
- Ordinal encoding for ordered categories
- Target encoding for high-cardinality categories

### Numerical Normalization
- StandardScaler for normally distributed features
- MinMaxScaler for bounded features
- RobustScaler for features with outliers

### Missing Data Handling
- Imputation strategies:
  - Mean/median for numerical
  - Mode for categorical
  - Forward fill for temporal data
  - Model-based imputation
  - Missing indicator variables

### Feature Engineering
- Age groups (bins)
- BMI categories
- Interaction terms (age × BMI, age × smoker)
- Polynomial features for non-linear relationships
- Time-based features (seasonality, trends)

## Data Privacy and Compliance

### HIPAA Compliance
- De-identification requirements
- Minimum necessary data
- Secure data transmission
- Access controls

### Federated Learning Benefits
- Raw data never leaves institution
- Only aggregated model weights shared
- Enhanced privacy protection
- Regulatory compliance

## Recommended Feature Set for Initial Model

### Core Features (Must Have)
1. Age
2. Sex
3. BMI
4. Number of children/dependents
5. Smoking status
6. Region

### Important Features (Should Have)
7. Blood pressure
8. Diabetes status
9. Heart disease status
10. Exercise level
11. Alcohol consumption
12. Family history of major diseases

### Enhanced Features (Nice to Have)
13. Laboratory results (cholesterol, glucose)
14. Number of medications
15. Healthcare utilization metrics
16. Income level
17. Education level
18. Chronic conditions count

### Advanced Features (Future)
19. Genetic markers
20. Social determinants of health
21. Environmental factors
22. Unstructured clinical notes (NLP)

## Data Collection Strategy

### Minimum Viable Dataset
- Start with core features (6 features)
- Expand gradually as data becomes available
- Prioritize high-impact, easily collectible features

### Data Quality
- Validation rules for each field
- Range checks for numerical values
- Format validation for categorical
- Consistency checks across related fields
- Outlier detection and handling

### Data Completeness
- Track missing data rates
- Set thresholds for model inclusion
- Implement data quality scores
- Regular data audits

## Conclusion

This comprehensive schema provides a roadmap for collecting and utilizing patient data for insurance cost prediction. The federated learning approach allows institutions to contribute to model improvement while maintaining patient privacy. Start with core features and gradually expand as more data becomes available and model performance improves.

