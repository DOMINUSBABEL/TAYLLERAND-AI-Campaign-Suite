import pandas as pd
from src.services.e26_processor import E26Processor

processor = E26Processor()
file_carlos = "resultado carlos humberto garcía .csv"

print(f"--- DEBUGGING {file_carlos} ---")
try:
    df = processor.load_raw_e26(file_carlos)
    print("DataFrame Loaded. Shape:", df.shape)
    if not df.empty:
        unique_candidates = df['CANDIDATO'].unique()
        print("\nUnique Candidates Found in File:")
        for c in unique_candidates:
            print(f"'{c}' (Len: {len(c)})")
            
        # Check against expected
        expected = "CARLOS HUMBERTO GARCIA VELASQUEZ"
        if expected in unique_candidates:
            print(f"\nMATCH FOUND: '{expected}'")
        else:
            print(f"\nNO MATCH for '{expected}'")

        # Check votes
        print(f"Total Votes: {df['VOTOS'].sum()}")
            
except Exception as e:
    print(f"Error: {e}")
