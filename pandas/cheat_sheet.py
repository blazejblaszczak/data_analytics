import pandas as pd
import numpy as np

df = pd.read_csv("data.csv")

# READ / SAVE DATA
pd.read_csv("file.csv")
pd.read_excel("file.xlsx")
pd.read_parquet("file.parquet")
pd.read_json("file.json")

df.to_csv("out.csv", index=False)
df.to_parquet("out.parquet")

# DATA INSPECTION
df.head()
df.tail()
df.sample(5)

df.shape
df.columns

df.dtypes
df.info()

df.describe()
df.describe(include="object")

# value counts / unique
df["country"].value_counts()
df["country"].nunique()
df["country"].unique()

# NULL HANDLING
# count nulls
df.isna().sum()
df.isnull().sum()
# filter null rows
df[df["country"].isna()]
# fill nulls
df["country"] = df["country"].fillna("Unknown")
df["amount"] = df["amount"].fillna(0)
df.fillna(method="ffill") # forward fill
# drop nulls
df.dropna()
df.dropna(subset=["user_id"])

# DUPLICATES HANDLING
# find duplicates
df.duplicated()
df[df.duplicated()]
df[df.duplicated(subset=["user_id"], keep=False)] # by specific column
# remove duplicates
df.drop_duplicates()
df.drop_duplicates(subset=["user_id"])

# SORT / RENAME / CREATE COLUMNS
df.sort_values("amount", ascending=False)
df.sort_values(["country", "amount"])
df.rename(columns={"amt": "amount"})
df["amount_eur"] = df["amount"] * 0.93
df["high_value"] = np.where(df["amount"] > 1000, 1, 0) # conditional column
df["flag"] = df["amount"].apply(lambda x: "high" if x > 100 else "low") # lambda function

# AGGREGATIONS
df.groupby(["user_id", "country"])["amount"].sum()
df.groupby("country").agg({
    "amount": ["sum", "mean", "count"],
    "user_id": "nunique"
})
df.groupby("country").agg(
    total_amount=("amount", "sum"),
    avg_amount=("amount", "mean"),
    users=("user_id", "nunique")
)

# MERGE / JOIN
df1.merge(df2, on="user_id", how="inner")
df1.merge(df2, left_on="id", right_on="user_id")

# STRING FUNCTIONS
df["email"].str.lower()
df["country"].str.upper()
df["name"].str.strip()
df[df["email"].str.contains("@gmail.com", na=False)]
df["phone"].str.replace("-", "", regex=False)
df["email"].str.split("@").str[1]
df["phone"].str.len()

# DATE FUNCTIONS
df["date"] = pd.to_datetime(df["date"])
df["refreshed_at"] = datetime.now(timezone.utc)
# extract parts
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["weekday"] = df["date"].dt.day_name()
df["days_since"] = (pd.Timestamp.today() - df["date"]).dt.days # date diff
df["month_start"] = df["date"].dt.to_period("M") # floot to month

# WINDOW-LIKE OPERATIONS
df["running_total"] = df["amount"].cumsum() # cumulative sum
df["rank"] = df["amount"].rank(ascending=False) # rank
df["prev_amount"] = df["amount"].shift(1) # lag
df["prev_amt"] = df.groupby("user_id")["amount"].shift(1) # group lag
prize_per_year = df_data.groupby(by='year').count().prize
moving_average = prize_per_year.rolling(window=5).mean() # rolling window

# PIVOT TABLE
pd.pivot_table(
    df,
    values="amount",
    index="country",
    columns="plan",
    aggfunc="sum"
)

# STACK
stack = df_apps_clean["Genres"].str.split(';', expand=True).stack() # stack the prescribed level(s) from columns to index

# READ DATA EXTRA
# CSV
df = pd.read_csv(
    "data.csv",
    sep=",",              # delimiter (default)
    header=0,             # row with column names
    na_values=["NA", ""], # treat as NaN
    parse_dates=["date"], # auto-convert to datetime
    encoding="utf-8"
)
# JSON
df = pd.read_json("data.json")
# Nested JSON
from pandas import json_normalize
import json

with open("data.json") as f:
    data = json.load(f)

df = json_normalize(data)
# JSON lines
df = pd.read_json("data.json", lines=True)

# TXT on positions
df = pd.read_fwf(
    "data.txt",
    colspecs=[(0, 3), (3, 12), (12, 16)], # on position
    names=["id", "name", "year"]
)
df = pd.read_fwf(
    "data.txt",
    widths=[3, 9, 4], # on widths
    names=["id", "name", "year"]
)
