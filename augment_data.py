import pandas as pd
import random

# Load existing data
input_file = "E26_MEDELLIN_2022_PRELOAD.csv"
try:
    df = pd.read_csv(input_file, sep=';')
except:
    df = pd.read_csv(input_file, sep=',')

# Ensure columns are correct
df.columns = [c.upper() for c in df.columns]

# Get unique Puestos to iterate over
puestos = df[['ZONA', 'PUESTO']].drop_duplicates()

new_rows = []

# Define targets and their vote distribution logic (approximate range per puesto)
targets = [
    {"name": "CENTRO DEMOCRATICO", "min": 50, "max": 300}, # Party Logo
    {"name": "CANDIDATO 1", "min": 40, "max": 250},       # Head of List
    {"name": "CARLOS HUMBERTO GARCIA", "min": 10, "max": 80},
    {"name": "JOSE LUIS NOREÑA", "min": 5, "max": 60},
    {"name": "ANDERSON DUQUE", "min": 5, "max": 50}
]

print(f"Augmenting data for {len(puestos)} polling stations...")

for _, row in puestos.iterrows():
    zona = row['ZONA']
    puesto = row['PUESTO']
    
    for target in targets:
        # Generate random vote count
        votes = random.randint(target["min"], target["max"])
        
        # Add some variability based on zone (e.g., Zone 14 El Poblado gets more votes for CD)
        if str(zona) == "14":
            votes = int(votes * 1.5)
            
        new_rows.append({
            "NOMBRE_DEP": "ANTIOQUIA",
            "NOMBRE_MUN": "MEDELLIN",
            "ZONA": zona,
            "PUESTO": puesto,
            "CANDIDATO": target["name"],
            "VOTOS": votes
        })

# Create DataFrame from new rows
new_df = pd.DataFrame(new_rows)

# Append to original
final_df = pd.concat([df, new_df], ignore_index=True)

# Save back to CSV
final_df.to_csv(input_file, sep=';', index=False)

print("Data augmentation complete. Saved to E26_MEDELLIN_2022_PRELOAD.csv")
