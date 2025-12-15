import pandas as pd

# Load the CSV
try:
    df = pd.read_csv("E26_MEDELLIN_2022_PRELOAD.csv", sep=';')
    # Get unique combinations of ZONA and PUESTO
    stations = df[['ZONA', 'PUESTO']].drop_duplicates().sort_values(by=['ZONA', 'PUESTO'])
    
    print(f"Found {len(stations)} unique stations.")
    
    # Save to a temporary file for me to read or just print some
    print(stations.to_csv(index=False))
except Exception as e:
    print(e)
