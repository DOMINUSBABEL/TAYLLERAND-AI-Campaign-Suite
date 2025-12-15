import pandas as pd
import io
import os

class E26Processor:
    """
    Module 2: E-26 Election Processor
    Updated for Strict Real Data: CSV Ingestion Only.
    """
    def __init__(self):
        # Load Master Geocoding Table
        try:
            stations_path = os.path.join("src", "data", "voting_stations.csv")
            if os.path.exists(stations_path):
                self.stations_df = pd.read_csv(stations_path)
                # Optimize lookup
                self.stations_df['PUESTO_NORM'] = self.stations_df['PUESTO'].astype(str).str.upper()
                self.stations_df['ZONA_NORM'] = self.stations_df['ZONA'].astype(str).str.zfill(2)
            else:
                self.stations_df = pd.DataFrame()
        except Exception as e:
            print(f"Error loading voting stations CSV: {e}")
            self.stations_df = pd.DataFrame()

    def geocode_station(self, station_name, zone_id=None):
        """
        Tries to find coordinates for a station name.
        1. Exact Match in Loaded CSV.
        2. Fallback to centralized average (if CSV missing).
        """
        if self.stations_df.empty:
             return (6.2442, -75.5812)

        try:
            station_upper = str(station_name).upper()
            
            # Simple Filter Matching
            matches = self.stations_df[self.stations_df['PUESTO_NORM'] == station_upper]
            
            # Refine by Zone if provided
            if zone_id and not matches.empty:
                zone_str = str(zone_id).zfill(2)
                zone_matches = matches[matches['ZONA_NORM'] == zone_str]
                if not zone_matches.empty:
                    matches = zone_matches
            
            if not matches.empty:
                row = matches.iloc[0]
                return (float(row['LAT']), float(row['LON']))
                
        except Exception as e:
            # print(f"Geocoding Error: {e}")
            pass
        
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
