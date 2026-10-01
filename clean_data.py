import pandas as pd
import numpy as np

df = pd.read_csv('marketing_campaign.csv', sep='\t')
print("--- Initial Data Shape ---")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')
print("\nCleaned Column Headers:\n", df.columns.tolist())

print("\nMissing values before cleaning:\n", df.isnull().sum()[df.isnull().sum() > 0])

if 'income' in df.columns:
    median_income = df['income'].median()
    df['income'] = df['income'].fillna(median_income)
    print(f"Filled missing income values with median: {median_income}")

duplicates = df.duplicated().sum()
print(f"\nDuplicate rows found: {duplicates}")
if duplicates > 0:
    df = df.drop_duplicates()
    print("Duplicates removed.")

if 'dt_customer' in df.columns:
    df['dt_customer'] = pd.to_datetime(df['dt_customer'], errors='coerce')
    df['dt_customer'] = df['dt_customer'].dt.strftime('%d-%m-%y')
    print("\nStandardized 'dt_customer' format to dd-mm-yyyy.")

if 'income' in df.columns:
    df['income'] = df['income'].astype(float)
if 'year_birth' in df.columns:
    df['year_birth'] = df['year_birth'].astype(int)
    
print("\nVerified Data Types (Subset):")
print(df[['year_birth', 'income', 'dt_customer']].dtypes)

if 'education' in df.columns:
    df['education'] = df['education'].str.strip().str.title()
    
if 'marital_status' in df.columns:
    df['marital_status'] = df['marital_status'].str.strip().str.title()
    status_mapping = {
        'Alone': 'Single', 
        'Absurd': 'Single', 
        'YOLO': 'Single', 
        'Together': 'Cohabiting'
    }
    df['marital_status'] = df['marital_status'].replace(status_mapping)

print("\nStandardized unique values for Marital Status:", df['marital_status'].unique())

df.to_csv('customer_personality_cleaned.csv', index=False)
print("\n--- Preprocessing Complete ---")
print(f"Final Data Shape -> Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print("Saved clean file to 'customer_personality_cleaned.csv'")