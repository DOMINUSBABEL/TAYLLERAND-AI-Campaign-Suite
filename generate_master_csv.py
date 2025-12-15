import pandas as pd
import os

# 1. Load Unique Stations
try:
    df = pd.read_csv("E26_MEDELLIN_2022_PRELOAD.csv", sep=';')
    stations = df[['ZONA', 'PUESTO']].drop_duplicates()
except Exception as e:
    print(f"Error loading preload: {e}")
    exit()

# 2. Existing Knowledge (from e26_processor.py)
geo_db = {
    "EAFIT": (6.2005, -75.5785),
    "UPB": (6.2420, -75.5900),
    "MARYMOUNT": (6.2050, -75.5600),
    "SAN JOSE DE LA SALLE": (6.2205, -75.5685),
    "CLUB CAMPESTRE": (6.1900, -75.5750),
    "PLAZA MAYOR": (6.2430, -75.5750),
    "ESTADIO ATANASIO GIRARDOT": (6.2606, -75.5881),
    "INEM JOSE FELIX DE RESTREPO": (6.2080, -75.5700),
    "POLITECNICO JAIME ISAZA CADAVID": (6.2120, -75.5750),
    "COL SAN IGNACIO": (6.2445, -75.5638),
    "I.E. VILLA HERMOSA": (6.2550, -75.5450),
    "I.E. MANRIQUE CENTRAL": (6.2780, -75.5480),
    "I.E. EL PICACHO": (6.2950, -75.5850),
    "ITM ROBLEDO": (6.2750, -75.5950),
    "UNIV. DE MEDELLIN": (6.2310, -75.6100),
    "PARQUE BIBLIOTECA BELEN": (6.2300, -75.6050),
    "SAN CRISTOBAL PARQUE": (6.2780, -75.6350),
    "SAN ANTONIO DE PRADO": (6.1850, -75.6550),
    "SANTA ELENA": (6.2050, -75.5000),
}

comuna_centroids = {
    "01": (6.295, -75.545), "02": (6.285, -75.555), "03": (6.275, -75.550), "04": (6.265, -75.560),
    "05": (6.290, -75.575), "06": (6.280, -75.585), "07": (6.270, -75.595), "08": (6.250, -75.545),
    "09": (6.235, -75.550), "10": (6.250, -75.570), "11": (6.245, -75.595), "12": (6.255, -75.605),
    "13": (6.255, -75.615), "14": (6.210, -75.570), "15": (6.220, -75.585), "16": (6.230, -75.605),
    "50": (6.340, -75.650), "60": (6.280, -75.630), "70": (6.210, -75.630), "80": (6.180, -75.640), "90": (6.210, -75.500)
}

def get_coords(row):
    puesto = str(row['PUESTO']).upper()
    zona = str(row['ZONA']).zfill(2)
    
    # 1. Exact Match
    for key, coords in geo_db.items():
        if key in puesto:
            return coords
            
    # 2. Heuristic
    centroid = comuna_centroids.get(zona)
    if centroid:
        h = hash(puesto)
        lat_offset = (h % 100 - 50) / 10000.0 
        lon_offset = ((h // 100) % 100 - 50) / 10000.0
        return (centroid[0] + lat_offset, centroid[1] + lon_offset)
        
    return (6.2442, -75.5812) # Fallback Center

# 3. Apply
coords = stations.apply(get_coords, axis=1)
stations['LAT'] = coords.apply(lambda x: x[0])
stations['LON'] = coords.apply(lambda x: x[1])

# 4. Save
output_path = os.path.join("src", "data", "voting_stations.csv")
stations.to_csv(output_path, index=False)
print(f"Generated {output_path} with {len(stations)} stations.")
