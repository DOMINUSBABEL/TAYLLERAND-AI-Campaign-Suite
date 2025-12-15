from src.services.e26_processor import E26Processor
import pandas as pd

def test_loading():
    print("Initializing E26Processor...")
    processor = E26Processor()
    
    if processor.stations_df.empty:
        print("FAIL: stations_df is empty.")
    else:
        print(f"PASS: Loaded {len(processor.stations_df)} stations.")

    # Test Known Location
    pt_coords = processor.geocode_station("EAFIT")
    target = (6.2005, -75.5785)
    if abs(pt_coords[0] - target[0]) < 0.0001:
        print(f"PASS: EAFIT found at {pt_coords}")
    else:
        print(f"FAIL: EAFIT found at {pt_coords}, expected {target}")

    # Test Generic Location (should match what's in CSV)
    generic_coords = processor.geocode_station("PUESTO SANTA ELENA 03", 90)
    print(f"Generic Station Coords: {generic_coords}")
    
    # Verify it matches CSV check
    csv_row = processor.stations_df[
        (processor.stations_df['PUESTO_NORM'] == "PUESTO SANTA ELENA 03") & 
        (processor.stations_df['ZONA_NORM'] == "90")
    ]
    if not csv_row.empty:
        csv_lat = float(csv_row.iloc[0]['LAT'])
        if abs(generic_coords[0] - csv_lat) < 0.0001:
             print("PASS: Generic station matches CSV.")
        else:
             print("FAIL: Generic station mismatch.")

if __name__ == "__main__":
    test_loading()
