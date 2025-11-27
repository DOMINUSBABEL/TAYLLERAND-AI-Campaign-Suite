import pandas as pd
import random
from datetime import datetime, timedelta

class SocialSentinel:
    """
    Module 3: Social Sentinel
    Acts as a 'Network Listener' for the campaign.
    Monitors specific affinities, topics, and sentiment across simulated networks.
    Now includes advanced profiling, geolocation, and message simulation.
    """
    def __init__(self):
        self.affinities = ["URIBISMO", "PETRISMO", "INDEPENDIENTES", "OPOSICIÓN", "GENERAL"]
        self.topics = ["SEGURIDAD", "ECONOMÍA", "CORRUPCIÓN", "PERSONAL", "CAMPAÑA", "MOVILIDAD", "SALUD"]
        
        # Enhanced Profiling Data
        self.interests_pool = ["Fútbol", "Tecnología", "Religión", "Negocios", "Familia", "Mascotas", "Viajes", "Moda", "Política", "Cultura"]
        self.tastes_pool = ["Conservador", "Liberal", "Pragmático", "Idealista", "Radical", "Moderado"]
        self.age_groups = ["18-25", "26-35", "36-50", "50-65", "65+"]

    def generate_verified_feed(self):
        """
        Generates a rich, synthetic dataset of social media content.
        Includes 'affinity', 'topic', 'interests', 'tastes', and 'influence_score'.
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
                "topic": "SEGURIDAD",
                "interests": ["Política", "Seguridad", "Campo"],
                "tastes": "Conservador",
                "age_group": "65+",
                "influence_score": 98
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
                "topic": "CAMPAÑA",
                "interests": ["Política", "Negocios", "Familia"],
                "tastes": "Radical",
                "age_group": "50-65",
                "influence_score": 92
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
                "topic": "SECURITY",
                "interests": ["Derecho", "Moda", "Lujo"],
                "tastes": "Conservador",
                "age_group": "36-50",
                "influence_score": 88
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
                "topic": "POLÍTICA",
                "interests": ["Política", "Medio Ambiente", "Social"],
                "tastes": "Radical",
                "age_group": "50-65",
                "influence_score": 99
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
                "topic": "CAMPAÑA",
                "interests": ["Tecnología", "Política", "Innovación"],
                "tastes": "Liberal",
                "age_group": "36-50",
                "influence_score": 90
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
                "topic": "SEGURIDAD",
                "interests": ["Noticias", "Seguridad"],
                "tastes": "Neutro",
                "age_group": "N/A",
                "influence_score": 85
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
                "topic": "CAMPAÑA",
                "interests": ["Noticias", "Política", "Economía"],
                "tastes": "Neutro",
                "age_group": "N/A",
                "influence_score": 90
            }
        ]
        
        # Augment with generic data to fill space and add variety
        for i in range(20):
            affinity = random.choice(self.affinities)
            topic = random.choice(self.topics)
            
            # Correlate sentiment with affinity (simplified)
            sentiment = random.uniform(-0.5, 0.5)
            if affinity == "URIBISMO": sentiment += 0.4
            if affinity == "PETRISMO": sentiment -= 0.4
            sentiment = max(-1.0, min(1.0, sentiment))
            
            # Generate random interests
            user_interests = random.sample(self.interests_pool, k=random.randint(2, 4))
            
            data.append({
                "user_name": f"Ciudadano {i}",
                "user_id": f"@ciudadano_{i}",
                "avatar": "",
                "text": f"Opinión sobre {topic.lower()} en la comuna {random.randint(1,16)}. #{topic} #Medellin",
                "url": "#",
                "date": (base_date - timedelta(hours=random.randint(1, 48))).strftime("%Y-%m-%d %H:%M"),
                "sentiment": sentiment,
                "lat": 6.2 + random.uniform(0, 0.1),
                "lon": -75.6 + random.uniform(0, 0.1),
                "type": "CITIZEN",
                "affinity": affinity,
                "topic": topic,
                "interests": user_interests,
                "tastes": random.choice(self.tastes_pool),
                "age_group": random.choice(self.age_groups),
                "influence_score": random.randint(10, 80)
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

    def generate_voter_profile(self, user_id):
        """
        Generates a detailed profile for a specific user ID.
        Used for the 'Voter Profiler' feature.
        """
        # In a real app, this would query a DB. Here we simulate consistency.
        # We'll regenerate the feed and find the user, or generate a consistent mock if not found.
        df = self.generate_verified_feed()
        user_row = df[df['user_id'] == user_id]
        
        if not user_row.empty:
            row = user_row.iloc[0]
            return {
                "ID Usuario": row['user_id'],
                "Nombre": row['user_name'],
                "Afinidad": row['affinity'],
                "Puntaje Influencia": row['influence_score'],
                "Intereses": ", ".join(row['interests']),
                "Gusto Político": row['tastes'],
                "Grupo Edad": row['age_group'],
                "Última Actividad": row['date'],
                "Historial Sentimiento": "Positivo" if row['sentiment'] > 0 else "Negativo",
                "Potencial Compromiso": "Alto" if row['influence_score'] > 70 else "Medio"
            }
        else:
            # Fallback for dynamic/mock users not in the static list
            return {
                "ID Usuario": user_id,
                "Nombre": "Usuario Simulado",
                "Afinidad": "INDEPENDIENTES",
                "Puntaje Influencia": random.randint(20, 60),
                "Intereses": "General, Noticias",
                "Gusto Político": "Moderado",
                "Grupo Edad": "26-35",
                "Última Actividad": "Hoy",
                "Historial Sentimiento": "Neutral",
                "Potencial Compromiso": "Bajo"
            }

    def analyze_message_impact(self, message, target_audience):
        """
        Simulates the impact of a drafted message on a specific target audience.
        Returns impact score, sentiment shift, and reach projection.
        """
        base_score = len(message) / 10 # Length factor
        
        # Keyword analysis (Mock)
        keywords = {
            "seguridad": 15, "familia": 10, "futuro": 10, "paz": 5, 
            "orden": 12, "libertad": 8, "cambio": 5
        }
        
        keyword_score = sum([val for key, val in keywords.items() if key in message.lower()])
        
        # Audience modifier
        audience_mod = 1.0
        if target_audience == "URIBISMO":
            if "seguridad" in message.lower() or "orden" in message.lower():
                audience_mod = 1.5
            elif "paz" in message.lower():
                audience_mod = 0.5
        elif target_audience == "PETRISMO":
            if "paz" in message.lower() or "cambio" in message.lower():
                audience_mod = 1.5
            elif "orden" in message.lower():
                audience_mod = 0.6
                
        final_impact = min(100, (base_score + keyword_score) * audience_mod)
        
        # Sentiment Shift Simulation
        sentiment_shift = (final_impact / 20) * (1 if audience_mod > 1.0 else -0.5)
        
        return {
            "Puntaje Impacto": int(final_impact),
            "Alcance Proyectado": int(final_impact * 150),
            "Cambio Sentimiento": f"{sentiment_shift:+.1f}%",
            "Resonancia": "Alta" if final_impact > 70 else "Media" if final_impact > 40 else "Baja"
        }
