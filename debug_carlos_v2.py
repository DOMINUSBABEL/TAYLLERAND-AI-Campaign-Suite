import pandas as pd
from src.services.e26_processor import E26Processor
import sys

# Redirect output to file
log = open("debug_output.txt", "w", encoding="utf-8")
sys.stdout = log

processor = E26Processor()
file_carlos = "resultado carlos humberto garcía .csv"
target_name = "CARLOS HUMBERTO GARCIA VELASQUEZ"

print(f"--- DEBUGGING {file_carlos} ---")
try:
    df = processor.load_raw_e26(file_carlos)
    print("DataFrame Loaded. Shape:", df.shape)
    
    if df.empty:
        print("DATAFRAME IS EMPTY!")
    else:
        unique_candidates = df['CANDIDATO'].unique()
        print("\nUnique Candidates Found in File:")
        for c in unique_candidates:
            print(f"'{c}' (Len: {len(c)})")
            
        print("\n--- MATCH CHECK ---")
        if target_name in unique_candidates:
             print(f"Perfect Match Found: '{target_name}'")
        else:
             print(f"NO Perfect Match for: '{target_name}'")
             # Fuzzy check
             for c in unique_candidates:
                 if "CARLOS" in c:
                     print(f"Partial match found: '{c}'")

        print("\n--- PROCESS DATA SIMULATION ---")
        # Simulate what happens in process_data
        target_upper = target_name.upper()
        mask = df["CANDIDATO"].str.contains(target_upper, na=False, regex=False)
        matched_rows = df[mask]
        print(f"Rows matching str.contains('{target_upper}'): {len(matched_rows)}")
        
        if len(matched_rows) == 0:
             print("WARNING: Zero rows matched during str.contains check!")
        
        # Check GroupBy
        base_group = df.groupby(["ZONA", "PUESTO"])["VOTOS"].sum().reset_index()
        print(f"Base Group Rows: {len(base_group)}")
        
        target_votes = df[mask].groupby(["ZONA", "PUESTO"])["VOTOS"].sum().reset_index()
        print(f"Target Votes Group Rows: {len(target_votes)}")
        
        # Merge Check
        merged = pd.merge(base_group, target_votes, on=["ZONA", "PUESTO"], how="left")
        print(f"Merged Rows: {len(merged)}")
        print("Merged Columns:", merged.columns.tolist())
        
except Exception as e:
    print(f"Error: {e}")

log.close()
