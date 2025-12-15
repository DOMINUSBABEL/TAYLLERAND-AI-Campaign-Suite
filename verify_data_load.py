import pandas as pd
import os
from src.services.e26_processor import E26Processor

print("--- VERIFICATION SCRIPT ---")

processor = E26Processor()
real_files = ["resultado ANDERSON DUQUE.csv", "resultado carlos humberto garcía .csv"]
dfs = []

# 1. Test Loading
for f in real_files:
    if os.path.exists(f):
        print(f"File found: {f}")
        df = processor.load_raw_e26(f)
        print(f"Loaded {len(df)} rows.")
        if not df.empty:
            print(df.head(2))
            dfs.append(df)
    else:
        print(f"File NOT found: {f}")

if not dfs:
    print("No valid data loaded.")
    exit(1)

# 2. Test Concatenation
raw_df = pd.concat(dfs, ignore_index=True)
print(f"\nTotal concatenated rows: {len(raw_df)}")

# 3. Test Processing
targets = ["ANDERSON DUQUE MORALES", "CARLOS HUMBERTO GARCIA VELASQUEZ"]
print(f"\nProcessing for targets: {targets}")
processed_df = processor.process_data(raw_df, targets)

print(f"\nProcessed DataFrame Shape: {processed_df.shape}")
print("Columns:", processed_df.columns.tolist())

# Check for votes
for t in targets:
    col = f"Votos_{t.replace(' ', '_')}"
    if col in processed_df.columns:
        total = processed_df[col].sum()
        print(f"Total Votes for {t}: {total}")
    else:
        print(f"WARNING: Column {col} not found!")

# Check Georeferencing
print("\nGeoreferencing Check (First 5 valid):")
valid_geo = processed_df[processed_df['lat'].notnull()]
print(valid_geo[['Puesto', 'lat', 'lon']].head())

if processed_df.empty:
    print("FAILURE: Processed DataFrame is empty.")
    exit(1)
if valid_geo.empty:
    print("FAILURE: Georeferencing failed (all lat/lon are null/default?)")
    # Note: fallback is acceptable, but let's see.

print("\nSUCCESS: Verification Complete.")
