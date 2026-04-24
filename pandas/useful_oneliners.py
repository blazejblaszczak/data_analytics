# list with all ID columns
id_int_cols = [col for col in df.columns if col.endswith("_id")]

# string with IDs that can be passed to query
payments_to_clean = ",".join(str(id) for id in df["id"])
