import pandas as pd
import os
from src.services.e26_processor import E26Processor

processor = E26Processor()
files = ["resultado ANDERSON DUQUE.csv", "resultado carlos humberto garcía .csv"]

print("--- ANALYZING MUNICIPALITIES ---")
for f in files:
    if os.path.exists(f):
        print(f"\nScanning {f}...")
        try:
            # Load raw, but we need the Municipality column (Index 3 usually)
            df = pd.read_csv(f, header=None)
            
            # Col 1: Dept, Col 3: Mun
            if 1 in df.columns and 3 in df.columns:
                depts = df[1].unique()
                muns = df[3].unique()
                
                print(f"Departments found: {depts}")
                print(f"Municipalities count: {len(muns)}")
                if len(muns) < 20: 
                    print(f"Municipalities: {muns}")
                else:
                    print(f"First 10 munis: {muns[:10]}")
            else:
                print("Columns 1 or 3 missing.")
        except Exception as e:
            print(f"Error reading {f}: {e}")
