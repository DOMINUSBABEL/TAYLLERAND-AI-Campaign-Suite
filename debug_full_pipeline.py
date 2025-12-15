import pandas as pd
import os
from src.services.e26_processor import E26Processor

print("--- FULL PIPELINE DEBUG ---")

p = E26Processor()
files = ["resultado ANDERSON DUQUE.csv", "resultado carlos humberto garcía .csv"]
dfs = []

# 1. Load
for f in files:
    if os.path.exists(f):
        print(f"Loading {f}...")
        df = p.load_raw_e26(f)
        dfs.append(df)
    else:
        print(f"MISSING: {f}")

raw_df = pd.concat(dfs, ignore_index=True)
print(f"Concatenated Rows: {len(raw_df)}")

# 2. Process
targets = [
    "ANDERSON DUQUE MORALES",
    "CARLOS HUMBERTO GARCIA VELASQUEZ"
]

processed = p.process_data(raw_df, targets)
print(f"Processed Rows: {len(processed)}")

# 3. Check Carlos
c_name = "CARLOS HUMBERTO GARCIA VELASQUEZ"
c_col = f"Votos_{c_name.replace(' ', '_')}"

if c_col in processed.columns:
    subset = processed[processed[c_col] > 0]
    print(f"\nRows with votes for {c_name}: {len(subset)}")
    print(f"Total votes: {subset[c_col].sum()}")
    
    if len(subset) > 0:
        print("First 5 rows locations:")
        print(subset[['Puesto', 'lat', 'lon', c_col]].head())
else:
    print(f"COLUMN MISSING: {c_col}")
    print("Columns found:", processed.columns.tolist())
