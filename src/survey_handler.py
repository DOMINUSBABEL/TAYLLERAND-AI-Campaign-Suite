import random
import pandas as pd
import re

class AutomatedSurveyHandler:
    """
    Module 1: Automated Survey Handler
    Ingests survey responses and infers location if GPS is missing.
    """
    def __init__(self):
        # Mock database of neighborhoods/landmarks to coordinates (Medellín)
        self.location_db = {
            "poblado": (6.2083, -75.5636),
            "lleras": (6.2089, -75.5678),
            "laureles": (6.2442, -75.5964),
            "belen": (6.2308, -75.6044),
            "envigado": (6.1676, -75.5833), # Nearby
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
        Expected format: { "id": str, "afinidad": int, "location_text": str, "lat": float, "lon": float }
        """
        lat = response_data.get("lat")
        lon = response_data.get("lon")
        
        # If GPS missing, try to infer
        if lat is None or lon is None:
            inferred = self.infer_location(response_data.get("location_text"))
            if inferred:
                lat, lon = inferred
            else:
                # Default to center of Medellin if unknown (or handle as error)
                # For prototype, we'll skip or assign a default "Unknown" zone
                lat, lon = 6.2442, -75.5812 # Default generic center
        
        return {
            "id": response_data.get("id"),
            "afinidad_cabal": response_data.get("afinidad", 0),
            "lat": lat,
            "lon": lon,
            "source": "survey"
        }

    def generate_mock_data(self, count=50):
        """Generates mock survey data for testing."""
        data = []
        for i in range(count):
            # Randomly choose a location from DB or random GPS
            if random.random() > 0.3:
                loc_name = random.choice(list(self.location_db.keys()))
                loc_text = f"Vivo en {loc_name}"
                lat, lon = None, None
            else:
                loc_text = ""
                # Random coords in Medellin box
                lat = random.uniform(6.15, 6.35)
                lon = random.uniform(-75.65, -75.50)
            
            data.append({
                "id": f"user_{i}",
                "afinidad": random.randint(0, 100),
                "location_text": loc_text,
                "lat": lat,
                "lon": lon
            })
        return pd.DataFrame([self.ingest_response(d) for d in data])
