import pandas as pd
import random
from datetime import datetime, timedelta

class SocialSentinel:
    """
    Module 3: Social Sentinel
    Acts as a 'Network Listener' for the campaign.
    Monitors specific affinities, topics, and sentiment across simulated networks.
    """
    def __init__(self):
        self.affinities = ["URIBISMO", "PETRISMO", "INDEPENDIENTES", "OPOSICIÓN", "GENERAL"]
        self.topics = ["SEGURIDAD", "ECONOMÍA", "CORRUPCIÓN", "PERSONAL", "CAMPAÑA"]

    def generate_verified_feed(self):
        """
        Generates a rich, synthetic dataset of social media content.
        Includes 'affinity' and 'topic' fields for granular filtering.
        """
        base_date = datetime.now()
        
        data = [
            # URIBISMO / RIGHT WING
            {
                "user_name": "Álvaro Uribe Vélez",
                "user_id": "@AlvaroUribeVel",
                "avatar": "https://pbs.twimg.com/profile_images/1511346075865030659/Hqj4x4x4_400x400.jpg",
                "text": "La seguridad democrática es el camino. Apoyo total a nuestros candidatos en Medellín. Mano firme. #CentroDemocratico",
                "url": "https://twitter.com/AlvaroUribeVel",
                "date": (base_date - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
                "sentiment": 1.0,
                "lat": 6.2518, "lon": -75.5636,
                "type": "OPINION",
                "affinity": "URIBISMO",
                "topic": "SEGURIDAD"
            },
            {
                "user_name": "Maria Fernanda Cabal",
                "user_id": "@MariaFdaCabal",
                "avatar": "https://pbs.twimg.com/profile_images/1356976596637163522/4x4x4x4x_400x400.jpg",
                "text": "No permitiremos que la izquierda destruya a Medellín. ¡A recuperar la ciudad! #SoyCabal",
                "url": "https://twitter.com/MariaFdaCabal",
                "date": (base_date - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
                "sentiment": 0.9,
                "lat": 6.2093, "lon": -75.5714,
                "type": "RALLY",
                "affinity": "URIBISMO",
                "topic": "CAMPAÑA"
            },
            {
                "user_name": "Abelardo De La Espriella",
                "user_id": "@DELAESPRIELLAE",
                "avatar": "https://pbs.twimg.com/profile_images/1488168168/elcolombiano_400x400.png", # Placeholder
                "text": "La ley y el orden deben imperar. Medellín necesita autoridad. Todo mi respaldo.",
                "url": "https://twitter.com/DELAESPRIELLAE",
                "date": (base_date - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
                "sentiment": 0.85,
                "lat": 6.2442, "lon": -75.5812,
                "type": "OPINION",
                "affinity": "URIBISMO",
                "topic": "SECURITY"
            },
            
            # PETRISMO / OPPOSITION (From Campaign Perspective)
            {
                "user_name": "Gustavo Petro",
                "user_id": "@petrogustavo",
                "avatar": "https://pbs.twimg.com/profile_images/1414968971863056386/9s8z8w8__400x400.jpg",
                "text": "El cambio en Medellín es imparable. La paz total llegará a cada comuna.",
                "url": "https://twitter.com/petrogustavo",
                "date": (base_date - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
                "sentiment": -0.9, # Negative for our campaign
                "lat": 6.2451, "lon": -75.5736,
                "type": "NEWS",
                "affinity": "PETRISMO",
                "topic": "POLÍTICA"
            },
            {
                "user_name": "Daniel Quintero",
                "user_id": "@QuinteroCalle",
                "avatar": "https://pbs.twimg.com/profile_images/1323360523463630850/4x4x4x4x_400x400.jpg", # Placeholder
                "text": "Medellín Futuro no se detiene. Seguimos adelante a pesar de los ataques.",
                "url": "https://twitter.com/QuinteroCalle",
                "date": (base_date - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
                "sentiment": -0.8,
                "lat": 6.2442, "lon": -75.5812,
                "type": "OPINION",
                "affinity": "PETRISMO",
                "topic": "CAMPAÑA"
            },

            # GENERAL / NEWS / SECURITY ALERTS
            {
                "user_name": "Minuto30",
                "user_id": "@minuto30com",
                "avatar": "https://pbs.twimg.com/profile_images/1323360523463630850/4x4x4x4x_400x400.jpg",
                "text": "Aumento de hurtos en El Poblado preocupa a comerciantes. Piden más policía.",
                "url": "https://www.minuto30.com",
                "date": (base_date - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M"),
                "sentiment": -0.6, # Crisis = Opportunity
                "lat": 6.2080, "lon": -75.5680,
                "type": "SECURITY_ALERT",
                "affinity": "GENERAL",
                "topic": "SEGURIDAD"
            },
             {
                "user_name": "El Colombiano",
                "user_id": "@elcolombiano",
                "avatar": "https://pbs.twimg.com/profile_images/1488168168/elcolombiano_400x400.png",
                "text": "Encuesta revela empate técnico en la alcaldía. Voto indeciso será clave.",
                "url": "https://www.elcolombiano.com",
                "date": (base_date - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
                "sentiment": 0.0,
                "lat": 6.2300, "lon": -75.5900,
                "type": "NEWS",
                "affinity": "GENERAL",
                "topic": "CAMPAÑA"
            }
        ]
        
        # Augment with generic data to fill space
        for i in range(10):
            data.append({
                "user_name": f"Ciudadano {i}",
                "user_id": f"@ciudadano_{i}",
                "avatar": "",
                "text": f"Necesitamos más seguridad en la comuna {random.randint(1,16)}. #Medellin",
                "url": "#",
                "date": (base_date - timedelta(hours=random.randint(1, 48))).strftime("%Y-%m-%d %H:%M"),
                "sentiment": -0.5,
                "lat": 6.2 + random.uniform(0, 0.1),
                "lon": -75.6 + random.uniform(0, 0.1),
                "type": "CITIZEN",
                "affinity": "INDEPENDIENTES",
                "topic": "SEGURIDAD"
            })

        return pd.DataFrame(data)

    def listen(self, affinity_filter=None, topic_filter=None):
        """
        The core 'Listener' function.
        Filters the feed based on specific criteria requested by other modules.
        """
        df = self.generate_verified_feed()
        
        if affinity_filter:
            # Allow for single string or list of affinities
            if isinstance(affinity_filter, str):
                affinity_filter = [affinity_filter]
            df = df[df['affinity'].isin(affinity_filter)]
            
        if topic_filter:
            if isinstance(topic_filter, str):
                topic_filter = [topic_filter]
            df = df[df['topic'].isin(topic_filter)]
            
        return df.sort_values(by="date", ascending=False)
