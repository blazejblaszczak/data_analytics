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

# AGGREGATIONS
df.groupby("country")["amount"].sum()
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

