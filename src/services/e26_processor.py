import pandas as pd
import io

class E26Processor:
    """
    Module 2: E-26 Election Processor
    Updated for Strict Real Data: CSV Ingestion Only.
    """
    def __init__(self):
        # Hardcoded Geocoding DB for Medellín Voting Posts (Partial/Key Locations)
        self.geo_db = {
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
        
        # Comuna Centroids for Deterministic Fallback
        self.comuna_centroids = {
            "01": (6.295, -75.545), "02": (6.285, -75.555), "03": (6.275, -75.550), "04": (6.265, -75.560),
            "05": (6.290, -75.575), "06": (6.280, -75.585), "07": (6.270, -75.595), "08": (6.250, -75.545),
            "09": (6.235, -75.550), "10": (6.250, -75.570), "11": (6.245, -75.595), "12": (6.255, -75.605),
            "13": (6.255, -75.615), "14": (6.210, -75.570), "15": (6.220, -75.585), "16": (6.230, -75.605),
            "50": (6.340, -75.650), "60": (6.280, -75.630), "70": (6.210, -75.630), "80": (6.180, -75.640), "90": (6.210, -75.500)
        }

    def geocode_station(self, station_name, zone_id=None):
        """
        Tries to find coordinates for a station name.
        1. Exact/Fuzzy Match in DB.
        2. Deterministic Offset from Comuna Centroid (using Zone ID).
        """
        station_upper = str(station_name).upper()
        
        # 1. DB Match
        for key, coords in self.geo_db.items():
            if key in station_upper:
                return coords
        
        # 2. Deterministic Fallback (Coverage Engine)
        if zone_id:
            zone_str = str(zone_id).zfill(2)
            centroid = self.comuna_centroids.get(zone_str)
            if centroid:
                # Generate deterministic offset based on station name hash
                # This ensures the station always stays in the same place
                h = hash(station_upper)
                # Offset range: +/- 0.005 degrees (~500m)
                lat_offset = (h % 100 - 50) / 10000.0 
                lon_offset = ((h // 100) % 100 - 50) / 10000.0
                return (centroid[0] + lat_offset, centroid[1] + lon_offset)
        
        # 3. Ultimate Fallback (Centro)
        return (6.2442, -75.5812)

    def load_data_from_csv(self, uploaded_file):
        """
        Parses an uploaded CSV file (E-26 format).
        Supports both Official Registraduría (Semicolon) and Standard (Comma).
        """
        if uploaded_file is None:
            return pd.DataFrame() # Return empty if no file
            
        try:
            # Try reading with semicolon first (Official Standard)
            try:
                df = pd.read_csv(uploaded_file, sep=';')
                if 'PUESTO' not in df.columns:
                    # Fallback to comma if semicolon fails to find columns
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, sep=',')
            except:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=',')
            
            # Normalize Columns
            df.columns = [c.upper() for c in df.columns]
            
            # Map to internal standard
            if 'VOTOS' in df.columns and 'PUESTO' in df.columns:
                return df
                
            return pd.DataFrame() # Invalid format
            
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return pd.DataFrame()

    def load_demo_data(self):
        """
        Loads the High-Fidelity Preload CSV.
        """
        try:
            # Load the Official-Format Preload
            df = pd.read_csv("E26_MEDELLIN_2022_PRELOAD.csv", sep=';')
            return df
        except Exception as e:
            print(f"Error loading preload data: {e}")
            return pd.DataFrame()

    def load_raw_e26(self, file_path):
        """
        Parses raw, headerless E-26 CSVs.
        Mappings:
        - Col 5: ZONA (Zero-pad 2 digits)
        - Col 6: PUESTO
        - Col 9: COMUNA (Used for checking)
        - Col 16: CANDIDATE NAME
        - Col 17: VOTES
        """
        try:
            # Read without header
            df = pd.read_csv(file_path, header=None)
            
            # Select and Rename Columns
            # We strictly need indices 5, 6, 16, 17
            # Index 1 (Dept) and 3 (City) are assumed correct for this context (Medellin)
            
            target_df = pd.DataFrame()
            target_df['ZONA'] = df[5].astype(str).str.zfill(2)
            target_df['PUESTO'] = df[6]
            target_df['CANDIDATO'] = df[16].str.strip()
            target_df['VOTOS'] = df[17].fillna(0).astype(int)
            
            return target_df
            
        except Exception as e:
            print(f"Error loading raw E-26 file {file_path}: {e}")
            return pd.DataFrame()

    def process_data(self, df, target_candidates=None):
        """
        Aggregates votes by Puesto for a list of target candidates.
        Returns a DataFrame with columns: Puesto, lat, lon, Votos_Total, and Votos_{Candidate} for each target.
        """
        if df.empty:
            return pd.DataFrame()
            
        # Normalize columns
        df.columns = [c.upper() for c in df.columns]
        
        if "VOTOS" not in df.columns or "PUESTO" not in df.columns:
            return pd.DataFrame()

        # Default targets if none provided
        if not target_candidates:
            target_candidates = ["MARIA FERNANDA CABAL"]
            
        # 1. Base Aggregation (Total Votes per Puesto)
        base_group = df.groupby(["ZONA", "PUESTO"])["VOTOS"].sum().reset_index()
        base_group.rename(columns={"PUESTO": "Puesto", "VOTOS": "Votos_Total", "ZONA": "Zona"}, inplace=True)
        
        # 2. Target Specific Aggregation
        for target in target_candidates:
            target_upper = target.upper()
            # Filter for this specific candidate
            if "CANDIDATO" in df.columns:
                # Flexible matching
                mask = df["CANDIDATO"].str.contains(target_upper, na=False)
                target_votes = df[mask].groupby(["ZONA", "PUESTO"])["VOTOS"].sum().reset_index()
                
                # Merge into base
                col_name = f"Votos_{target.replace(' ', '_')}"
                base_group = pd.merge(base_group, target_votes, left_on=["Zona", "Puesto"], right_on=["ZONA", "PUESTO"], how="left")
                base_group.drop(columns=["ZONA", "PUESTO"], inplace=True)
                base_group.rename(columns={"VOTOS": col_name}, inplace=True)
                base_group[col_name] = base_group[col_name].fillna(0)
            else:
                base_group[f"Votos_{target.replace(' ', '_')}"] = 0

        # 3. Geocode
        base_group["coords"] = base_group.apply(lambda row: self.geocode_station(row["Puesto"], row["Zona"]), axis=1)
        base_group["lat"] = base_group["coords"].apply(lambda x: x[0])
        base_group["lon"] = base_group["coords"].apply(lambda x: x[1])
        
        # 4. Calculate Historical Strength (based on the first target in the list as 'primary')
        primary_col = f"Votos_{target_candidates[0].replace(' ', '_')}"
        max_votes = base_group[primary_col].max()
        if max_votes > 0:
            base_group["historical_strength"] = (base_group[primary_col] / max_votes) * 100
        else:
            base_group["historical_strength"] = 0
            
        # Backward Compatibility
        base_group["Votos"] = base_group["Votos_Total"]
            
        return base_group
