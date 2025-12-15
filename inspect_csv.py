import pandas as pd
import os

files = ["resultado ANDERSON DUQUE.csv", "resultado carlos humberto garcía .csv"]

for f in files:
    print(f"\n--- INSPECTING: {f} ---")
    if os.path.exists(f):
        try:
            # Try sniffing first
            df = pd.read_csv(f, nrows=5)
            print("Columns:", df.columns.tolist())
            print("Head:\n", df.head())
        except Exception as e:
            print(f"Error reading {f} with default settings: {e}")
            try:
                # Try semicolon
                df = pd.read_csv(f, sep=';', nrows=5)
                print("Columns (Semi-colon):", df.columns.tolist())
                print("Head:\n", df.head())
            except Exception as e2:
                print(f"Error reading {f} with semicolon: {e2}")
    else:
        print(f"File not found: {f}")
