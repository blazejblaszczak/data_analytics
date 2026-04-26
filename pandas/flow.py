import pandas as pd
import numpy as np

df = pd.DataFrame({
    "user_id": [1,2,3,4,5,6,7,8,9,10],
    "amount": [120.5, 80.0, np.nan, 300.0, 50.5, 120.5, 400.0, 90.0, 75.0, 300.0],
    "country": ["PL", "DE", "PL", "FR", None, "PL", "DE", "FR", "PL", "DE"],
    "signup_date": [
        "2024-01-10","2024-01-15","2024-02-01","2024-02-10","2024-03-05",
        "2024-03-08","2024-03-12","2024-04-01","2024-04-10","2024-04-20"
    ]
})

df["signup_date"] = pd.to_datetime(df["signup_date"])

### 1. Inspect data quality
df.info()
df.isna().sum()
df.duplicated().sum()

### 2. Fill missing values
# Replace missing amount with median and missing country with "Unknown"
df["amount"] = df["amount"].fillna(df["amount"].median())
df["country"] = df["country"].fillna("Unknown")

### 3. Grouping
# Calculate total/average amount by country.
df.groupby("country")["amount"].sum().reset_index()
df.groupby("country")["amount"].mean().reset_index()
# How many users signed up each month?
df["month"] = df["signup_date"].dt.to_period("M")
df.groupby("month")["user_id"].count().reset_index()

