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
# detect outliers
threshold = df["amount"].quantile(0.95)
df["outlier"] = df["amount"] > threshold

### 2. Fill missing values + normalization
# Replace missing amount with median and missing country with "Unknown"
df["amount"] = df["amount"].fillna(df["amount"].median())
df["country"] = df["country"].fillna("Unknown")
# Normalize text values
df["country"] = df["country"].str.strip().str.lower()

### 3. Grouping
# Calculate total/average amount by country.
df.groupby("country")["amount"].sum().reset_index()
df.groupby("country")["amount"].mean().reset_index()
# How many users signed up each month?
df["month"] = df["signup_date"].dt.to_period("M")
df.groupby("month")["user_id"].count().reset_index()

### 4. Creating columns
# segment column on condition
df["segment"] = np.select(
    [
        df["amount"] >= 200,
        df["amount"] >= 100
    ],
    [
        "High",
        "Medium"
    ],
    default="Low"
)
df["segment"] = "Low"
df.loc[df["amount"] >= 100, "segment"] = "Medium"
df.loc[df["amount"] >= 200, "segment"] = "High"
# running total amount
df["running_total"] = df["amount"].fillna(0).cumsum()
# rolling average
df["rolling_avg_3"] = (
    df["amount"]
      .rolling(window=3)
      .mean()
)
df["rolling_avg"] = (
    df.groupby("user_id")["amount"]
      .rolling(3)
      .mean()
      .reset_index(level=0, drop=True)
)
# days since signup
df["days_since_signup"] = (
    pd.Timestamp.today() - df["signup_date"]
).dt.days
# rank higherst amount per country
df["rank_in_country"] = (
    df.groupby("country")["amount"]
      .rank(method="dense", ascending=False)
)

### 5. Merging dataframes
plans = pd.DataFrame({
    "user_id": [1,2,3,4,5],
    "plan": ["Free","Premium","Free","Metal","Free"]
})
df.merge(plans, on="user_id", how="left")

### 6. Pivot for additional dataframe
# Users per country pivot
pd.pivot_table(
    df,
    values="user_id",
    index="country",
    aggfunc="count"
)

### 7.Example on time difference between two timestamps
df["start_time"] = pd.to_datetime([
    "2024-01-01 10:00",
    "2024-01-01 11:30"
])

df["end_time"] = pd.to_datetime([
    "2024-01-01 10:25",
    "2024-01-01 12:10"
])

df["minutes_diff"] = (
    df["end_time"] - df["start_time"]
).dt.total_seconds() / 60

### 8. Potential forward fill
df["amount"] = df["amount"].fillna(method="ffill")
