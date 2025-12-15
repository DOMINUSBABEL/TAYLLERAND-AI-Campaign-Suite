import pandas as pd
import os

files = ["resultado ANDERSON DUQUE.csv", "resultado carlos humberto garcía .csv"]

with open("inspection_output.txt", "w", encoding="utf-8") as out:
    for f in files:
        out.write(f"\n\n--- INSPECTING: {f} ---\n")
        if os.path.exists(f):
            try:
                # header=None to see raw first rows
                df = pd.read_csv(f, header=None, nrows=5)
                out.write("Shape: " + str(df.shape) + "\n")
                out.write("First 5 rows (Comma):\n")
                out.write(df.to_string() + "\n")
            except Exception as e:
                out.write(f"Error reading {f} with default settings: {e}\n")
                try:
                    df = pd.read_csv(f, sep=';', header=None, nrows=5)
                    out.write("Shape: " + str(df.shape) + "\n")
                    out.write("First 5 rows (Semi-colon):\n")
                    out.write(df.to_string() + "\n")
                except Exception as e2:
                    out.write(f"Error reading {f} with semicolon: {e2}\n")
        else:
            out.write(f"File not found: {f}\n")
