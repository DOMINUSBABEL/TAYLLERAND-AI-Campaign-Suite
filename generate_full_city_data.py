import pandas as pd
import numpy as np
import random

# Comuna Definitions (Approximate Centroids and Vote Bias)
# Bias: 1.0 = High Support (Poblado), 0.1 = Low Support (Popular)
comunas = [
    {"id": 1, "name": "POPULAR", "lat": 6.295, "lon": -75.545, "bias_cabal": 0.15, "bias_petro": 0.80, "bias_fico": 0.30, "stations": 10},
    {"id": 2, "name": "SANTA CRUZ", "lat": 6.285, "lon": -75.555, "bias_cabal": 0.15, "bias_petro": 0.85, "bias_fico": 0.25, "stations": 10},
    {"id": 3, "name": "MANRIQUE", "lat": 6.275, "lon": -75.550, "bias_cabal": 0.20, "bias_petro": 0.75, "bias_fico": 0.35, "stations": 12},
    {"id": 4, "name": "ARANJUEZ", "lat": 6.265, "lon": -75.560, "bias_cabal": 0.25, "bias_petro": 0.70, "bias_fico": 0.40, "stations": 12},
    {"id": 5, "name": "CASTILLA", "lat": 6.290, "lon": -75.575, "bias_cabal": 0.20, "bias_petro": 0.75, "bias_fico": 0.35, "stations": 15},
    {"id": 6, "name": "DOCE DE OCTUBRE", "lat": 6.280, "lon": -75.585, "bias_cabal": 0.20, "bias_petro": 0.70, "bias_fico": 0.35, "stations": 12},
    {"id": 7, "name": "ROBLEDO", "lat": 6.270, "lon": -75.595, "bias_cabal": 0.30, "bias_petro": 0.60, "bias_fico": 0.45, "stations": 18},
    {"id": 8, "name": "VILLA HERMOSA", "lat": 6.250, "lon": -75.545, "bias_cabal": 0.25, "bias_petro": 0.65, "bias_fico": 0.40, "stations": 12},
    {"id": 9, "name": "BUENOS AIRES", "lat": 6.235, "lon": -75.550, "bias_cabal": 0.35, "bias_petro": 0.55, "bias_fico": 0.50, "stations": 12},
    {"id": 10, "name": "LA CANDELARIA", "lat": 6.250, "lon": -75.570, "bias_cabal": 0.40, "bias_petro": 0.50, "bias_fico": 0.55, "stations": 15},
    {"id": 11, "name": "LAURELES", "lat": 6.245, "lon": -75.595, "bias_cabal": 0.85, "bias_petro": 0.20, "bias_fico": 0.90, "stations": 20},
    {"id": 12, "name": "LA AMERICA", "lat": 6.255, "lon": -75.605, "bias_cabal": 0.60, "bias_petro": 0.35, "bias_fico": 0.70, "stations": 12},
    {"id": 13, "name": "SAN JAVIER", "lat": 6.255, "lon": -75.615, "bias_cabal": 0.25, "bias_petro": 0.70, "bias_fico": 0.35, "stations": 15},
    {"id": 14, "name": "EL POBLADO", "lat": 6.210, "lon": -75.570, "bias_cabal": 0.95, "bias_petro": 0.10, "bias_fico": 0.95, "stations": 25},
    {"id": 15, "name": "GUAYABAL", "lat": 6.220, "lon": -75.585, "bias_cabal": 0.50, "bias_petro": 0.40, "bias_fico": 0.60, "stations": 12},
    {"id": 16, "name": "BELEN", "lat": 6.230, "lon": -75.605, "bias_cabal": 0.65, "bias_petro": 0.30, "bias_fico": 0.75, "stations": 18},
    {"id": 50, "name": "PALMITAS", "lat": 6.340, "lon": -75.650, "bias_cabal": 0.10, "bias_petro": 0.80, "bias_fico": 0.20, "stations": 3},
    {"id": 60, "name": "SAN CRISTOBAL", "lat": 6.280, "lon": -75.630, "bias_cabal": 0.20, "bias_petro": 0.70, "bias_fico": 0.30, "stations": 5},
    {"id": 70, "name": "ALTAVISTA", "lat": 6.210, "lon": -75.630, "bias_cabal": 0.15, "bias_petro": 0.75, "bias_fico": 0.25, "stations": 4},
    {"id": 80, "name": "SAN ANTONIO", "lat": 6.180, "lon": -75.640, "bias_cabal": 0.25, "bias_petro": 0.60, "bias_fico": 0.40, "stations": 6},
    {"id": 90, "name": "SANTA ELENA", "lat": 6.210, "lon": -75.500, "bias_cabal": 0.30, "bias_petro": 0.65, "bias_fico": 0.45, "stations": 4}
]

data = []

candidates = [
    {"name": "MARIA FERNANDA CABAL", "bias_key": "bias_cabal"},
    {"name": "GUSTAVO PETRO", "bias_key": "bias_petro"},
    {"name": "FEDERICO GUTIERREZ", "bias_key": "bias_fico"}
]

for comuna in comunas:
    for i in range(comuna["stations"]):
        # Generate Station Name
        station_name = f"PUESTO {comuna['name']} {i+1:02d}"
        if i == 0: station_name = f"I.E. {comuna['name']} CENTRAL"
        if i == 1: station_name = f"PARQUE {comuna['name']}"
        
        # Generate Votes for each candidate
        for cand in candidates:
            # Base vote per station ~ 200-500
            base_vote = random.randint(100, 400)
            bias = comuna[cand["bias_key"]]
            votes = int(base_vote * bias * random.uniform(0.8, 1.2))
            
            # Ensure at least some votes
            if votes < 5: votes = random.randint(5, 20)
            
            data.append({
                "NOMBRE_DEP": "ANTIOQUIA",
                "NOMBRE_MUN": "MEDELLIN",
                "ZONA": f"{comuna['id']:02d}",
                "PUESTO": station_name,
                "CANDIDATO": cand["name"],
                "VOTOS": votes
            })

df = pd.DataFrame(data)
df.to_csv("E26_MEDELLIN_2022_PRELOAD.csv", sep=";", index=False)
print(f"Generated {len(df)} records. Total Votes: {df['VOTOS'].sum()}")
