import random
import pandas as pd
import re
from datetime import datetime, timedelta

class AutomatedSurveyHandler:
    """
    Module 1: Automated Survey Handler
    Ingests survey responses and infers location if GPS is missing.
    Implements contact prioritization for field operations.
    """
    def __init__(self):
        # Mock database of neighborhoods/landmarks to coordinates (Medellín)
        self.location_db = {
            "poblado": (6.2083, -75.5636),
            "lleras": (6.2089, -75.5678),
            "laureles": (6.2442, -75.5964),
            "belen": (6.2308, -75.6044),
            "envigado": (6.1676, -75.5833),
            "centro": (6.2518, -75.5636),
            "estadio": (6.2606, -75.5881),
            "robledo": (6.2814, -75.5978),
            "manrique": (6.2753, -75.5528),
            "aranjuez": (6.2856, -75.5617),
            "castilla": (6.2961, -75.5733),
            "doce de octubre": (6.3067, -75.5833),
            "buenos aires": (6.2333, -75.5500),
            "villa hermosa": (6.2500, -75.5333),
            "san javier": (6.2500, -75.6167),
            "america": (6.2500, -75.6000),
            "guayabal": (6.2167, -75.5833),
            "candelaria": (6.2500, -75.5667),
        }

    def infer_location(self, text_location):
        """
        Infers (Lat, Lon) from a text description using the mock DB.
        Returns None if no match found.
        """
        if not text_location:
            return None
        
        text_lower = text_location.lower()
        for key, coords in self.location_db.items():
            if key in text_lower:
                # Add slight random jitter to avoid stacking points perfectly
                lat_jitter = random.uniform(-0.002, 0.002)
                lon_jitter = random.uniform(-0.002, 0.002)
                return (coords[0] + lat_jitter, coords[1] + lon_jitter)
        return None

    def ingest_response(self, response_data):
        """
        Processes a single survey response.
        Expected format includes: id, name, phone, afinidad, location_text, lat, lon, last_contact
        """
        lat = response_data.get("lat")
        lon = response_data.get("lon")
        
        # If GPS missing, try to infer
        if lat is None or lon is None:
            inferred = self.infer_location(response_data.get("location_text"))
            if inferred:
                lat, lon = inferred
            else:
                lat, lon = 6.2442, -75.5812  # Default generic center
        
        return {
            "id": response_data.get("id"),
            "name": response_data.get("name", "Desconocido"),
            "phone": response_data.get("phone", "N/A"),
            "afinidad_score": response_data.get("afinidad", 0),
            "lat": lat,
            "lon": lon,
            "last_contact_date": response_data.get("last_contact", None),
            "location_text": response_data.get("location_text", ""),
            "source": "survey"
        }

    def prioritize_contacts(self, contacts_df, strategic_zones=None):
        """
        Prioritizes contacts based on multiple factors:
        - Affinity Score (higher = better)
        - Geographic Proximity to strategic zones
        - Recency of last contact (older = higher priority for re-engagement)
        
        Returns the DataFrame with added 'priority_score' and 'priority_tier' columns.
        """
        if contacts_df.empty:
            return contacts_df
        
        df = contacts_df.copy()
        
        # 1. Affinity Score (0-100) - normalize to 0-1
        df['affinity_norm'] = df['afinidad_score'] / 100
        
        # 2. Geographic Score - proximity to strategic zones (if provided)
        if strategic_zones and len(strategic_zones) > 0:
            # Calculate minimum distance to any strategic zone
            def min_distance_to_zones(row):
                contact_lat, contact_lon = row['lat'], row['lon']
                distances = []
                for zone in strategic_zones:
                    zone_lat, zone_lon = zone['lat'], zone['lon']
                    # Simple Euclidean distance (not perfect for lat/lon but sufficient for demo)
                    dist = ((contact_lat - zone_lat)**2 + (contact_lon - zone_lon)**2)**0.5
                    distances.append(dist)
                return min(distances) if distances else 1.0
            
            df['min_zone_distance'] = df.apply(min_distance_to_zones, axis=1)
            # Normalize: closer = higher score (inverse)
            max_dist = df['min_zone_distance'].max()
            df['geo_score'] = 1 - (df['min_zone_distance'] / max_dist if max_dist > 0 else 0)
        else:
            df['geo_score'] = 0.5  # Neutral if no zones
        
        # 3. Engagement Recency Score
        if 'last_contact_date' in df.columns and df['last_contact_date'].notna().any():
            def days_since_contact(date_str):
                if pd.isna(date_str) or not date_str:
                    return 365  # Never contacted = max days
                try:
                    contact_date = datetime.strptime(str(date_str), "%Y-%m-%d")
                    return (datetime.now() - contact_date).days
                except:
                    return 365
            
            df['days_since'] = df['last_contact_date'].apply(days_since_contact)
            # Normalize: older contact = higher priority (inverse decay)
            max_days = df['days_since'].max()
            df['engagement_score'] = df['days_since'] / max_days if max_days > 0 else 0.5
        else:
            df['engagement_score'] = 0.5  # Neutral
        
        # 4. Weighted Priority Score
        df['priority_score'] = (
            df['affinity_norm'] * 0.5 +       # 50% weight on affinity
            df['geo_score'] * 0.3 +            # 30% weight on proximity
            df['engagement_score'] * 0.2       # 20% weight on re-engagement
        ) * 100  # Scale to 0-100
        
        # 5. Assign Priority Tiers
        def assign_tier(score):
            if score >= 70:
                return "ALTA"
            elif score >= 40:
                return "MEDIA"
            else:
                return "BAJA"
        
        df['priority_tier'] = df['priority_score'].apply(assign_tier)
        
        # Sort by priority score descending
        df = df.sort_values('priority_score', ascending=False)
        
        return df

    def generate_mock_data(self, count=50):
        """Generates mock survey/CRM data for testing."""
        first_names = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Sofia", "Miguel", "Laura", "Pedro", "Carmen"]
        last_names = ["Garcia", "Rodriguez", "Martinez", "Lopez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores"]
        
        data = []
        base_date = datetime.now()
        
        for i in range(count):
            # Randomly choose a location from DB or random GPS
            if random.random() > 0.3:
                loc_name = random.choice(list(self.location_db.keys()))
                loc_text = f"Vivo en {loc_name}"
                lat, lon = None, None
            else:
                loc_text = ""
                lat = random.uniform(6.15, 6.35)
                lon = random.uniform(-75.65, -75.50)
            
            # Generate last contact date (some recent, some old)
            days_ago = random.randint(1, 180)
            last_contact = (base_date - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            
            data.append({
                "id": f"contact_{i}",
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "phone": f"+57 {random.randint(300, 350)} {random.randint(1000000, 9999999)}",
                "afinidad": random.randint(0, 100),
                "location_text": loc_text,
                "lat": lat,
                "lon": lon,
                "last_contact": last_contact if random.random() > 0.2 else None  # 20% never contacted
            })
        
        return pd.DataFrame([self.ingest_response(d) for d in data])

