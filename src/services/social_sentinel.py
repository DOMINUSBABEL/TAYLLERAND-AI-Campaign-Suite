import pandas as pd
import random
import requests
from datetime import datetime, timedelta
import numpy as np
from collections import Counter

# NLP & ML Libraries
try:
    import tweepy
    from textblob import TextBlob
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import nltk
    # Ensure NLTK data is downloaded (quietly)
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
except ImportError:
    # Fallback for environments where these aren't installed yet
    tweepy = None
    TextBlob = None
    TfidfVectorizer = None
    cosine_similarity = None
    print("Warning: Advanced NLP libraries not found. Running in degraded mode.")

class IngestionEngine:
    """
    Handles connection to external Social Media APIs.
    """
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.x_client = None
        self._setup_x_client()

    def _setup_x_client(self):
        if self.api_keys.get("X") and tweepy:
            try:
                self.x_client = tweepy.Client(bearer_token=self.api_keys["X"])
            except Exception as e:
                print(f"Error initializing X Client: {e}")

    def fetch_x_data(self, query="Medellín", max_results=10):
        """Fetches recent tweets using Tweepy (v2 API)."""
        if not self.x_client:
            return []
        
        try:
            tweets = self.x_client.search_recent_tweets(
                query=query, 
                max_results=max_results,
                tweet_fields=['created_at', 'geo', 'author_id', 'public_metrics'],
                expansions=['author_id']
            )
            
            if not tweets.data:
                return []

            # Map users
            users = {u.id: u for u in tweets.includes['users']} if tweets.includes else {}
            
            processed_data = []
            for tweet in tweets.data:
                user = users.get(tweet.author_id)
                processed_data.append({
                    "user_name": user.name if user else "Unknown",
                    "user_id": f"@{user.username}" if user else "@unknown",
                    "text": tweet.text,
                    "date": tweet.created_at,
                    "platform": "X",
                    "raw_metrics": tweet.public_metrics
                })
            return processed_data

        except Exception as e:
            print(f"X Fetch Error: {e}")
            return []

    def fetch_instagram_data(self, hashtag="Medellin"):
        """Placeholder for Instagram Graph API (Requires Business Account)."""
        # In a real implementation, this would use facebook-sdk
        return []

    def fetch_tiktok_data(self):
        """Placeholder for TikTok Data."""
        return []

class VoterProfiler:
    """
    Analyzes raw text to generate a 'Voter Vector'.
    Vector Dimensions: [Security, Economy, Social, Tradition, Change]
    """
    def __init__(self):
        self.dimensions = ["SEGURIDAD", "ECONOMIA", "SOCIAL", "TRADICION", "CAMBIO"]
        self.keywords = {
            "SEGURIDAD": ["seguridad", "policía", "robo", "hurto", "orden", "miedo", "armas", "violencia"],
            "ECONOMIA": ["empleo", "dinero", "impuestos", "negocio", "pobreza", "costo", "inversión", "precio"],
            "SOCIAL": ["salud", "educación", "hambre", "paz", "derechos", "igualdad", "ayuda", "comunidad"],
            "TRADICION": ["familia", "dios", "valores", "patria", "historia", "conservar", "fe", "respeto"],
            "CAMBIO": ["futuro", "nuevo", "transformación", "reformar", "avanzar", "moderno", "tecnología", "jóvenes"]
        }

    def analyze_text(self, text):
        """Returns a sentiment score and a dimension vector."""
        if not text:
            return 0, [0.0] * 5

        # 1. Sentiment Analysis
        sentiment = 0.0
        if TextBlob:
            blob = TextBlob(text)
            # Simple translation hack or direct spanish model would be better
            # For now, assuming mixed/english or using simple polarity
            sentiment = blob.sentiment.polarity 
        
        # 2. Dimension Vectorization
        text_lower = text.lower()
        vector = []
        for dim in self.dimensions:
            score = 0
            for word in self.keywords[dim]:
                if word in text_lower:
                    score += 1
            vector.append(min(1.0, score * 0.5)) # Cap at 1.0
            
        return sentiment, vector

class MatchEngine:
    """
    Calculates affinity between a Candidate Avatar and a Voter Profile.
    """
    def __init__(self):
        pass

    def calculate_match(self, candidate_vector, voter_vector):
        """
        Calculates Cosine Similarity between two vectors.
        """
        if not cosine_similarity or not candidate_vector or not voter_vector:
            # Fallback Euclidean-ish similarity
            dist = np.linalg.norm(np.array(candidate_vector) - np.array(voter_vector))
            return max(0, 100 - (dist * 20))

        # Reshape for sklearn
        cand_matrix = np.array(candidate_vector).reshape(1, -1)
        voter_matrix = np.array(voter_vector).reshape(1, -1)
        
        similarity = cosine_similarity(cand_matrix, voter_matrix)[0][0]
        return similarity * 100 # Return as percentage

class SocialSentinel:
    """
    Module 3: Social Sentinel (Upgraded)
    Integrates Ingestion, Profiling, and Matching.
    """
    def __init__(self):
        self.api_keys = {"X": None, "META": None, "TIKTOK": None}
        self.mode = "SIMULATION"
        
        # Sub-Engines
        self.ingestion = None
        self.profiler = VoterProfiler()
        self.matcher = MatchEngine()
        
        # Cache
        self.cached_feed = None

        # Legacy attributes for compatibility
        self.affinities = ["URIBISMO", "PETRISMO", "INDEPENDIENTES", "OPOSICIÓN", "GENERAL"]
        self.topics = ["SEGURIDAD", "ECONOMÍA", "CORRUPCIÓN", "PERSONAL", "CAMPAÑA", "MOVILIDAD", "SALUD"]
        self.interests_pool = ["Fútbol", "Tecnología", "Religión", "Negocios", "Familia", "Mascotas", "Viajes", "Moda", "Política", "Cultura"]
        self.tastes_pool = ["Conservador", "Liberal", "Pragmático", "Idealista", "Radical", "Moderado"]
        self.age_groups = ["18-25", "26-35", "36-50", "50-65", "65+"]

    def set_api_keys(self, x_key=None, meta_key=None, tiktok_key=None):
        self.api_keys["X"] = x_key
        self.api_keys["META"] = meta_key
        self.api_keys["TIKTOK"] = tiktok_key
        # Re-init ingestion with new keys
        self.ingestion = IngestionEngine(self.api_keys)

    def generate_verified_feed(self):
        """
        Generates the main feed. Uses Live data if available, else Synthetic.
        """
        if self.mode == "LIVE" and self.ingestion:
            raw_data = self.ingestion.fetch_x_data()
            if raw_data:
                return self._process_live_data(raw_data)
        
        # Fallback to Synthetic
        return self._generate_synthetic_feed()

    def _process_live_data(self, raw_list):
        """Enriches raw API data with Profiler analysis."""
        processed = []
        for item in raw_list:
            sentiment, vector = self.profiler.analyze_text(item['text'])
            
            # Determine Affinity based on Vector
            # Simple heuristic: Max dimension determines topic/affinity
            dims = ["SEGURIDAD", "ECONOMIA", "SOCIAL", "TRADICION", "CAMBIO"]
            max_idx = np.argmax(vector)
            dominant_dim = dims[max_idx] if vector[max_idx] > 0 else "GENERAL"
            
            processed.append({
                "user_name": item['user_name'],
                "user_id": item['user_id'],
                "avatar": "", # APIs often don't give this easily in search
                "text": item['text'],
                "url": f"https://twitter.com/user/status/123", # Placeholder
                "date": item['date'].strftime("%Y-%m-%d %H:%M") if isinstance(item['date'], datetime) else str(item['date']),
                "sentiment": sentiment,
                "lat": 6.24 + random.uniform(-0.05, 0.05), # Mock Geo for privacy
                "lon": -75.57 + random.uniform(-0.05, 0.05),
                "type": "LIVE_CITIZEN",
                "affinity": dominant_dim, # Mapped from vector
                "topic": dominant_dim,
                "voter_vector": vector,
                "influence_score": random.randint(10, 90), # Mock influence
                "interests": ["General"], # Placeholder
                "tastes": "Moderado", # Placeholder
                "age_group": "N/A" # Placeholder
            })
        return pd.DataFrame(processed)

    def _generate_synthetic_feed(self):
        """
        Original synthetic generation logic (preserved for offline mode).
        """
        base_date = datetime.now()
        data = []
        
        profiles = [
            ("Álvaro Uribe Vélez", "@AlvaroUribeVel", "URIBISMO", "SEGURIDAD", [0.9, 0.6, 0.1, 0.9, 0.1]),
            ("Gustavo Petro", "@petrogustavo", "PETRISMO", "SOCIAL", [0.1, 0.4, 0.9, 0.1, 0.9]),
            ("Daniel Quintero", "@QuinteroCalle", "INDEPENDIENTES", "CAMBIO", [0.2, 0.5, 0.7, 0.1, 0.8]),
            ("Fico Gutiérrez", "@FicoGutierrez", "URIBISMO", "SEGURIDAD", [0.8, 0.7, 0.3, 0.8, 0.2]),
        ]

        for name, handle, aff, topic, vec in profiles:
            data.append({
                "user_name": name, "user_id": handle, "avatar": "",
                "text": f"Mensaje simulado sobre {topic} y el futuro de Medellín.",
                "url": "#", "date": (base_date - timedelta(hours=random.randint(1,5))).strftime("%Y-%m-%d %H:%M"),
                "sentiment": random.uniform(-0.8, 0.8),
                "lat": 6.25 + random.uniform(-0.02, 0.02), "lon": -75.56 + random.uniform(-0.02, 0.02),
                "type": "INFLUENCER", "affinity": aff, "topic": topic,
                "voter_vector": vec, "influence_score": random.randint(80, 100),
                "interests": ["Política"], "tastes": "Radical", "age_group": "50+"
            })

        # Generate Citizens
        for i in range(30):
            # Random Vector
            vec = [random.random() for _ in range(5)]
            dims = ["SEGURIDAD", "ECONOMIA", "SOCIAL", "TRADICION", "CAMBIO"]
            topic = dims[np.argmax(vec)]
            
            data.append({
                "user_name": f"Ciudadano {i}", "user_id": f"@ciudadano_{i}", "avatar": "",
                "text": f"Opinión ciudadana sobre {topic}. #Medellin",
                "url": "#", "date": (base_date - timedelta(hours=random.randint(1,48))).strftime("%Y-%m-%d %H:%M"),
                "sentiment": random.uniform(-1, 1),
                "lat": 6.2 + random.uniform(0, 0.1), "lon": -75.6 + random.uniform(0, 0.1),
                "type": "CITIZEN", "affinity": "GENERAL", "topic": topic,
                "voter_vector": vec, "influence_score": random.randint(10, 60),
                "interests": random.sample(self.interests_pool, 2), 
                "tastes": random.choice(self.tastes_pool), 
                "age_group": random.choice(self.age_groups)
            })
            
        return pd.DataFrame(data)

    def listen(self, affinity_filter=None, topic_filter=None):
        """
        The core 'Listener' function.
        Filters the feed based on specific criteria requested by other modules.
        """
        if self.mode == "LIVE":
            df = self.fetch_live_feed()
        else:
            df = self.generate_verified_feed()
        
        if affinity_filter:
            if isinstance(affinity_filter, str):
                affinity_filter = [affinity_filter]
            if 'affinity' in df.columns:
                df = df[df['affinity'].isin(affinity_filter)]
            
        if topic_filter:
            if isinstance(topic_filter, str):
                topic_filter = [topic_filter]
            if 'topic' in df.columns:
                df = df[df['topic'].isin(topic_filter)]
            
        return df.sort_values(by="date", ascending=False)

    def match_candidate_to_voter(self, candidate_vector, voter_id):
        """
        Public method to match a candidate strategy against a specific voter.
        """
        df = self.generate_verified_feed()
        voter = df[df['user_id'] == voter_id]
        
        if voter.empty:
            return 0
            
        voter_vec = voter.iloc[0]['voter_vector']
        return self.matcher.calculate_match(candidate_vector, voter_vec)

    def generate_voter_profile(self, user_id):
        """
        Generates a detailed profile for a specific user ID.
        """
        df = self.generate_verified_feed()
        user_row = df[df['user_id'] == user_id]
        
        if not user_row.empty:
            row = user_row.iloc[0]
            return {
                "ID Usuario": row['user_id'],
                "Nombre": row['user_name'],
                "Afinidad": row['affinity'],
                "Puntaje Influencia": row['influence_score'],
                "Intereses": ", ".join(row['interests']) if isinstance(row['interests'], list) else row['interests'],
                "Gusto Político": row['tastes'],
                "Grupo Edad": row['age_group'],
                "Última Actividad": str(row['date']),
                "Historial Sentimiento": "Positivo" if row['sentiment'] > 0 else "Negativo",
                "Potencial Compromiso": "Alto" if row['influence_score'] > 70 else "Medio"
            }
        else:
            return {
                "ID Usuario": user_id,
                "Nombre": "Usuario Simulado",
                "Afinidad": "INDEPENDIENTES",
                "Puntaje Influencia": 50,
                "Intereses": "General",
                "Gusto Político": "Moderado",
                "Grupo Edad": "N/A",
                "Última Actividad": "Hoy",
                "Historial Sentimiento": "Neutral",
                "Potencial Compromiso": "Bajo"
            }

    def analyze_message_impact(self, message, target_audience):
        """
        (Preserved from original) Simulates impact.
        """
        base_score = len(message) / 10
        keywords = {"seguridad": 15, "familia": 10, "futuro": 10}
        keyword_score = sum([val for key, val in keywords.items() if key in message.lower()])
        final_impact = min(100, base_score + keyword_score)
        
        return {
            "Puntaje Impacto": int(final_impact),
            "Alcance Proyectado": int(final_impact * 150),
            "Cambio Sentimiento": "+2.5%",
            "Resonancia": "Alta" if final_impact > 60 else "Media"
        }
