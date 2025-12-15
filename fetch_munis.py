import requests
import pandas as pd
import time
import os

def geocode_municipalities():
    # 1. Get List of Municipalities from Files
    files = [
        "resultado ANDERSON DUQUE.csv",
        "resultado carlos humberto garcía .csv"
    ]
    
    unique_munis = set()
    
    for f in files:
        if os.path.exists(f):
            try:
                df = pd.read_csv(f, header=None, dtype=str)
                # Col 3 is Muni Name based on previous checks
                munis = df[3].dropna().unique()
                for m in munis:
                    unique_munis.add(m.strip().upper())
            except Exception as e:
                print(f"Error reading {f}: {e}")
                
    print(f"Found {len(unique_munis)} unique municipalities.")
    
    # 2. Geocode Loop
    results = []
    
    # Cache to avoid re-fetching if file exists (simple retry logic)
    if os.path.exists("src/data/municipios_coords.csv"):
        existing = pd.read_csv("src/data/municipios_coords.csv")
        results = existing.to_dict('records')
        existing_names = set([r['MUNICIPIO'] for r in results])
        unique_munis = [m for m in unique_munis if m not in existing_names]
        print(f"Resuming... {len(unique_munis)} left to fetch.")
    
    for i, muni in enumerate(unique_munis):
        query = f"{muni}, Antioquia, Colombia"
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': query,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'TayllerandElectionApp/1.0'
        }
        
        try:
            print(f"Geocoding {i+1}/{len(unique_munis)}: {muni}...")
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            
            if data:
                lat = data[0]['lat']
                lon = data[0]['lon']
                results.append({'MUNICIPIO': muni, 'LAT': lat, 'LON': lon})
                print(f"  -> Found: {lat}, {lon}")
            else:
                print(f"  -> Not found!")
                # Fallback slightly?
                
            time.sleep(1.1) # Respect Nominatim rate limits (1 per sec)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)
            
    # 3. Save
    out_df = pd.DataFrame(results)
    if not out_df.empty:
        out_df.to_csv("src/data/municipios_coords.csv", index=False)
        print("Saved src/data/municipios_coords.csv")

if __name__ == "__main__":
    geocode_municipalities()
