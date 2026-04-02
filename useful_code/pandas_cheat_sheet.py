# Loading and inspecting

df.head()
df.info()
df.describe()
df.shape
df.columns

# Filtering

df[df["amount"] > 100]
df[(df["country"] == "US") & (df["amount"] > 50)]

# Selecting columns

df["amount"]
df[["user_id", "amount"]]

# Handling missing values

df.isna()
df.dropna()
df.fillna(0)

# Grouping

df.groupby("user_id")["amount"].sum()
df.groupby(["user_id", "country"])["amount"].mean()
df.groupby("user_id").agg({
    "amount": "sum",
    "transaction_id": "count"
})

# Sorting

df.sort_values("amount", ascending=False)

# Merging

df1.merge(df2, on="user_id", how="left")

# Custom logic

df["category"] = df["amount"].apply(lambda x: "high" if x > 100 else "low")

# Unique values and duplicates

df["user_id"].nunique()
df["country"].value_counts()
df.drop_duplicates()
df.duplicated()

# Renaming columns

df.rename(columns={"old": "new"})

# String operations

df["email"].str.contains("@gmail.com")
df["name"].str.lower()
df["name"] = df["name"].str.strip()

# Date handling

df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year

# Loading files
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
