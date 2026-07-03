import pandas as pd
import numpy as np

# Load dataset
df = pd.read_excel("Dataset for Data Analytics P1.xlsx")

# Replace blank strings with NaN
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].replace(r'^\s*$', np.nan, regex=True)

# Trim whitespace in text columns
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype("string").str.strip()

# Standardize date columns
date_cols = [c for c in df.columns if "date" in c.lower()]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Remove duplicate rows
df = df.drop_duplicates()

# Remove duplicate IDs if an ID column exists
id_col = None
for c in df.columns:
    if c.lower() in ["orderid", "order_id", "id"]:
        id_col = c
        break

if id_col:
    df = df.drop_duplicates(subset=[id_col], keep="first")

# Handle missing values
for col in df.columns:
    if df[col].isna().sum() == 0:
        continue
    if pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].fillna(df[col].median())
    elif pd.api.types.is_datetime64_any_dtype(df[col]):
        mode_val = df[col].mode(dropna=True)
        fill_value = mode_val.iloc[0] if not mode_val.empty else pd.Timestamp("1970-01-01")
        df[col] = df[col].fillna(fill_value)
    else:
        mode_val = df[col].mode(dropna=True)
        fill_value = mode_val.iloc[0] if not mode_val.empty else "Unknown"
        df[col] = df[col].fillna(fill_value)

# Standardize selected text columns to title case
for col in df.select_dtypes(include="object").columns:
    if any(key in col.lower() for key in ["city", "status", "payment", "product", "referral", "address"]):
        df[col] = df[col].astype("string").str.title()

# Save cleaned dataset
df.to_excel("Project1_Cleaned_Dataset.xlsx", index=False)

print("Cleaning complete.")
print("Final shape:", df.shape)
print("Missing values after cleaning:")
print(df.isnull().sum())
if id_col:
    print(f"Duplicate {id_col} count after cleaning:", df[id_col].duplicated().sum())
print("Duplicate rows after cleaning:", df.duplicated().sum())
