from src.services.e26_processor import E26Processor
import pandas as pd

def debug_candidate_flow():
    print("--- DEBUGGING CANDIDATE DATA FLOW ---")
    processor = E26Processor()
    
    # 1. Load Data
    print("Loading data...")
    df = processor.load_demo_data()
    print(f"Loaded {len(df)} rows.")
    
    # 2. Check Raw Presence
    anderson_mask = df['CANDIDATO'].str.contains("ANDERSON", na=False)
    print(f"Raw rows matching 'ANDERSON': {anderson_mask.sum()}")
    
    if anderson_mask.sum() > 0:
        sample = df[anderson_mask].head(1)
        print(f"Sample Row:\n{sample}")
    
    # 3. Process Data
    target_list = ["ANDERSON DUQUE", "CARLOS HUMBERTO GARCIA"]
    print(f"Processing for targets: {target_list}")
    
    processed = processor.process_data(df, target_list)
    
    # 4. Analyze Result
    if processed.empty:
        print("Processed DataFrame is EMPTY.")
    else:
        print(f"Processed DataFrame has {len(processed)} rows.")
        if "Votos_ANDERSON_DUQUE" in processed.columns:
            total_votes = processed["Votos_ANDERSON_DUQUE"].sum()
            print(f"Total Votes for ANDERSON DUQUE: {total_votes}")
            
            non_zero = processed[processed["Votos_ANDERSON_DUQUE"] > 0]
            print(f"Stations with > 0 votes: {len(non_zero)}")
            
            print("First 5 stations with votes:")
            print(non_zero[['Puesto', 'Votos_ANDERSON_DUQUE', 'lat', 'lon']].head(5))
        else:
            print("Column 'Votos_ANDERSON_DUQUE' NOT FOUND in result.")

if __name__ == "__main__":
    debug_candidate_flow()
