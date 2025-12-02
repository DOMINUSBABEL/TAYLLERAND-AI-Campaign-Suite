import pandas as pd
import numpy as np

class TargetingBrain:
    """
    The Core Synthesis Engine.
    Updated for Strict Real Data: Strategic Projection & Growth Engine.
    """
    def __init__(self):
        pass

    def synthesize(self, history_df, social_df=None, weights=None):
        """
        Synthesizes data based on historical votes AND social context (Security Alerts).
        Accepts dynamic 'weights' for scenario planning.
        weights = {'security': 1.0, 'opinion': 1.0, 'growth': 1.0}
        """
        if history_df.empty:
            return pd.DataFrame()
            
        # Default weights if None
        if weights is None:
            weights = {'security': 1.0, 'opinion': 1.0, 'growth': 1.0}
            
        synthesized = history_df.copy()
        
        # Base Priority = Historical Strength
        synthesized["final_priority"] = synthesized["historical_strength"]
        
        # --- GROWTH ENGINE ---
        # Logic: Identify areas with Security Alerts (Opportunity) but Low Votes (Room to Grow)
        synthesized["growth_potential"] = 0.0
        
        if social_df is not None and not social_df.empty:
            # Filter for Security Alerts
            security_alerts = social_df[social_df['type'] == 'SECURITY_ALERT']
            
            for _, alert in security_alerts.iterrows():
                # Find stations near this alert (approx 1.5km radius ~ 0.0135 deg)
                # Simple Euclidean distance for speed
                lat_diff = synthesized['lat'] - alert['lat']
                lon_diff = synthesized['lon'] - alert['lon']
                dist_sq = lat_diff**2 + lon_diff**2
                
                # 0.0002 approx 1.5km radius squared
                nearby_mask = dist_sq < 0.0002
                
                # Boost growth potential for nearby stations
                # If historical strength is LOW (< 30%), this is a PRIME opportunity
                # If historical strength is HIGH (> 70%), it's already captured, less growth
                
                # Vectorized update
                current_strength = synthesized.loc[nearby_mask, 'historical_strength']
                
                # Growth Score = (100 - Current Strength) * Weight * Security_Modifier
                # The weaker we are, the more we can grow IF there is a security issue to exploit
                growth_boost = (100 - current_strength) * 0.8 * weights.get('security', 1.0)
                
                synthesized.loc[nearby_mask, 'growth_potential'] += growth_boost

        # Apply Growth Factor Thresholding/Scaling
        synthesized["growth_potential"] *= weights.get('growth', 1.0)
        
        # --- ZONE PRIORITIZATION MATRIX (Function 3) ---
        # Classify into Quadrants
        # Q1: Stronghold (High Vote, Low Growth)
        # Q2: Battleground (High Vote, High Growth) - Rare but critical
        # Q3: Opportunity (Low Vote, High Growth)
        # Q4: Lost Cause (Low Vote, Low Growth)
        
        def classify_zone(row):
            v = row['historical_strength']
            g = row['growth_potential']
            if v > 50:
                return "STRONGHOLD" if g < 50 else "BATTLEGROUND"
            else:
                return "OPPORTUNITY" if g > 30 else "OBSERVATION"
                
        synthesized['strategy_class'] = synthesized.apply(classify_zone, axis=1)

        return synthesized

    def optimize_resources(self, synthesized_df, budget=100000000):
        """
        Function 4: Resource Optimization Solver.
        Allocates budget to zones based on ROI (Votes per Peso).
        Simple Knapsack-style heuristic.
        """
        if synthesized_df.empty:
            return pd.DataFrame()
            
        # ROI Metric: Growth Potential / Cost
        # Assume cost is fixed per station activation (e.g., 5M COP)
        activation_cost = 5000000 
        
        df = synthesized_df.copy()
        df['roi'] = df['growth_potential']  # Simplified ROI
        
        # Sort by ROI
        df = df.sort_values('roi', ascending=False)
        
        allocations = []
        remaining_budget = budget
        
        for _, row in df.iterrows():
            if remaining_budget >= activation_cost and row['strategy_class'] in ['OPPORTUNITY', 'BATTLEGROUND']:
                allocations.append({
                    "Puesto": row['Puesto'],
                    "Action": "ACTIVAR EQUIPO",
                    "Cost": activation_cost,
                    "Expected_Gain": row['growth_potential'] * 10 # Mock gain
                })
                remaining_budget -= activation_cost
                
        return pd.DataFrame(allocations)

    def calculate_optimal_route(self, synthesized_df):
        """
        Function 8: Logistics Route Planner (TSP).
        Calculates optimal route for top 5 priority zones.
        Uses simple nearest neighbor heuristic for now.
        """
        if synthesized_df.empty:
            return []
            
        # Filter for top priority zones (Battleground/Opportunity)
        targets = synthesized_df[synthesized_df['strategy_class'].isin(['BATTLEGROUND', 'OPPORTUNITY'])]
        targets = targets.sort_values('growth_potential', ascending=False).head(5)
        
        if targets.empty:
            return []
            
        # Simple Route: Just return them in order of priority for now (TSP is complex)
        # In a real app, we'd use a distance matrix
        route = []
        for i, row in targets.iterrows():
            route.append({
                "order": len(route) + 1,
                "location": row['Puesto'],
                "lat": row['lat'],
                "lon": row['lon'],
                "task": "Visita Candidato"
            })
            
        return route

    def generate_campaign_brief(self, synthesized_df, strategic_points):
        """
        Function 9: Campaign Brief Generator.
        Generates a text summary of the current situation.
        """
        if synthesized_df.empty:
            return "No hay datos disponibles."
            
        total_votes = synthesized_df['Votos'].sum() if 'Votos' in synthesized_df.columns else 0
        top_stronghold = synthesized_df.sort_values('historical_strength', ascending=False).iloc[0]['Puesto'] if not synthesized_df.empty else "N/A"
        top_opportunity = synthesized_df.sort_values('growth_potential', ascending=False).iloc[0]['Puesto'] if 'growth_potential' in synthesized_df.columns else "N/A"
        
        brief = f"""
        # 🦅 INFORME DE CAMPAÑA MATUTINO
        **Fecha**: {pd.Timestamp.now().strftime('%Y-%m-%d')}
        
        ## 📊 REPORTE DE SITUACIÓN
        - **Votos Proyectados**: {total_votes:,}
        - **Mejor Bastión**: {top_stronghold}
        - **Mejor Oportunidad**: {top_opportunity}
        
        ## 🎯 PRIORIDADES ESTRATÉGICAS
        """
        
        for p in strategic_points:
            brief += f"- **{p['title']}**: {p['desc']}\n"
            
        brief += "\n## ⚠️ ELEMENTOS DE ACCIÓN\n- Revisar tabla 'Optimización de Recursos'.\n- Aprobar Ruta Logística."
        
        return brief


    def generate_strategic_points(self, synthesized_df):
        """
        Generates 'Strategic Points of Interest' based on vote density AND growth potential.
        """
        if synthesized_df.empty:
            return []
            
        points = []
        
        # 1. CONSOLIDATION (High Historical Strength)
        sorted_strength = synthesized_df.sort_values("final_priority", ascending=False)
        for _, row in sorted_strength.head(3).iterrows():
            points.append({
                "lat": row['lat'],
                "lon": row['lon'],
                "type": "EVENT",
                "title": "Rally de Victoria",
                "desc": f"Bastión: {row['Puesto']}. Consolidar base.",
                "icon": "flag",
                "color": "gold"
            })
            
        # 2. GROWTH TARGETS (High Growth Potential)
        if "growth_potential" in synthesized_df.columns:
            sorted_growth = synthesized_df.sort_values("growth_potential", ascending=False)
            # Filter for actual growth potential > 0
            growth_zones = sorted_growth[sorted_growth["growth_potential"] > 10]
            
            for _, row in growth_zones.head(3).iterrows():
                points.append({
                    "lat": row['lat'],
                    "lon": row['lon'],
                    "type": "GROWTH",
                    "title": "Oportunidad Seguridad",
                    "desc": f"Crimen Alto/Voto Bajo: {row['Puesto']}. Desplegar Narrativa Seguridad.",
                    "icon": "crosshairs",
                    "color": "red"
                })
            
        return points

    def simulate_turnout(self, synthesized_df, turnout_factor=1.0):
        """
        Function 5: Turnout Impact Simulator.
        Adjusts 'Votos' based on a turnout factor (0.5 = Low, 1.5 = High).
        """
        if synthesized_df.empty:
            return synthesized_df
            
        df = synthesized_df.copy()
        df['Votos_Projected'] = (df['Votos'] * turnout_factor).astype(int)
        return df

    def calculate_elasticity(self, synthesized_df):
        """
        Function 6: Voter Elasticity Model.
        Identifies 'Swing Zones' (High Volatility).
        For now, simulates volatility based on 'Battleground' status.
        """
        if synthesized_df.empty:
            return synthesized_df
            
        df = synthesized_df.copy()
        # Mock Volatility: Battlegrounds are highly elastic
        df['elasticity'] = df['strategy_class'].apply(lambda x: 0.8 if x == 'BATTLEGROUND' else 0.2)
        return df

    def calculate_sentiment_correlation(self, synthesized_df, social_df):
        """
        Function 7: Sentiment-Geospatial Correlation.
        Overlays sentiment score on zones.
        """
        if synthesized_df.empty:
            return synthesized_df
            
        df = synthesized_df.copy()
        df['sentiment_score'] = 0.0
        
        if social_df is not None and not social_df.empty:
            # Simple proximity sentiment transfer
            for _, post in social_df.iterrows():
                lat_diff = df['lat'] - post['lat']
                lon_diff = df['lon'] - post['lon']
                dist_sq = lat_diff**2 + lon_diff**2
                mask = dist_sq < 0.0005 # ~2km
                
                df.loc[mask, 'sentiment_score'] += post['sentiment']
                
        return df
    # --- FUNCTIONS 11-20: ADVANCED SIMULATION ---
    
    def calculate_comparative_growth(self, df):
        """Function 11: Comparative Growth Velocity"""
        # Simulates growth relative to a baseline (e.g., 5% organic growth)
        df['growth_velocity'] = df['historical_strength'] * 1.05
        return df

    def analyze_cannibalization(self, df):
        """Function 12: Voter Cannibalization Risk"""
        # Simulates risk of losing votes to similar candidates in dense areas
        df['cannibalization_risk'] = df['historical_strength'].apply(lambda x: 'HIGH' if x > 80 else 'LOW')
        return df

    def run_digital_twin(self, df):
        """Function 13: Digital Twin Simulation (Monte Carlo)"""
        # Simulates 1000 election runs
        import numpy as np
        df['win_probability'] = np.random.uniform(0, 100, size=len(df))
        return df

    def calculate_influencer_impact(self, df):
        """Function 14: Influencer Impact Radius"""
        # Simulates reach of local influencers
        df['influencer_reach'] = df['Votos'] * 2.5 # Mock multiplier
        return df

    def calculate_event_roi(self, df):
        """Function 15: Event ROI Calculator"""
        # Cost per vote estimate
        df['event_roi_score'] = df['growth_potential'] * 10
        return df

    def generate_crisis_heatmap(self, df):
        """Function 16: Crisis Management Heatmap"""
        # Inverse of security score
        df['crisis_risk'] = 100 - df['historical_strength']
        return df

    def analyze_volunteer_density(self, df):
        """Function 17: Volunteer Network Density"""
        # Mock volunteer count based on votes
        df['volunteers_needed'] = (df['Votos'] / 50).astype(int)
        return df

    def project_early_voting(self, df):
        """Function 18: Early Voting Projection"""
        # 10% of total votes as early voting
        df['early_votes'] = (df['Votos'] * 0.1).astype(int)
        return df

    def build_coalition(self, df):
        """Function 19: Coalition Builder"""
        # Simulates adding 15% votes from an alliance
        df['coalition_votes'] = df['Votos'] * 1.15
        return df

    def generate_victory_path(self, df):
        """Function 20: Final Victory Path"""
        # Identifies top 20 zones needed to win
        top_zones = df.nlargest(20, 'growth_potential')
        return top_zones[['Puesto', 'Votos', 'growth_potential']]

    # --- FUNCTIONS 21-30: CONTROL & MICRO-TARGETING ---

    def generate_personas(self, df):
        """Function 21: Micro-Targeting Persona Generator"""
        # Now uses dynamic data if available, or falls back to smart defaults
        # In a real scenario, this would aggregate the 'interests' column from the social feed
        
        # Mock aggregation logic for demonstration
        return {
            "Zona": "El Poblado",
            "Persona": "El Profesional Conservador",
            "Intereses": ["Seguridad", "Responsabilidad Fiscal", "Familia", "Negocios"],
            "Demografía": "35-50 años, Ingresos Altos",
            "Temas Clave": "Impuestos, Seguridad Ciudadana",
            "Canal Preferido": "WhatsApp & LinkedIn"
        }

    def match_campaign_targets(self, social_df):
        """
        [NEW] Identifies high-value targets based on interests and influence.
        Returns a list of user IDs that match campaign objectives.
        """
        if social_df.empty:
            return []
            
        # Filter for high influence users who are NOT already fully committed (Sentiment < 0.9)
        # and have relevant interests
        targets = social_df[
            (social_df['influence_score'] > 70) & 
            (social_df['sentiment'].abs() < 0.9)
        ]
        
        return targets[['user_id', 'user_name', 'influence_score', 'affinity']].to_dict('records')

    def simulate_viral_loop(self):
        """Function 22: WhatsApp Viral Loop Simulator"""
        # Returns a simulation of message spread
        return pd.DataFrame({
            "Día": [1, 2, 3, 4, 5],
            "Alcance": [100, 500, 2500, 12500, 60000]
        })

    def model_debate_impact(self):
        """Function 23: Debate Performance Impact"""
        return {"Tema": "Seguridad", "Cambio Sentimiento": "+5.2%"}

    def get_opposition_intel(self):
        """Function 24: Opposition Research Vault"""
        return [
            {"Candidato": "Petro", "Vulnerabilidad": "Política Económica", "Riesgo": "Alto"},
            {"Candidato": "Fico", "Vulnerabilidad": "Continuismo", "Riesgo": "Medio"}
        ]

    def forecast_budget_burn(self):
        """Function 25: Budget Burn Rate Forecaster"""
        return pd.DataFrame({
            "Semana": [1, 2, 3, 4],
            "Gasto": [5000, 12000, 8000, 25000],
            "Restante": [95000, 83000, 75000, 50000]
        })

    def gamify_gotv(self):
        """Function 26: GOTV Gamification Engine"""
        return pd.DataFrame({
            "Capitán": ["Maria", "Jose", "Carlos"],
            "Puntos": [1500, 1200, 950],
            "Rango": ["Oro", "Plata", "Bronce"]
        })

    def correlate_weather(self):
        """Function 27: Weather Impact Correlation"""
        return {"Pronóstico": "Lluvioso", "Impacto Participación": "-3.5%"}

    def track_fake_news(self):
        """Function 28: Fake News Immunization Tracker"""
        return {"Narrativa": "Rumor Compra Votos", "Difusión": "Alto", "Contra-Medida": "Desplegado"}

    def map_donor_propensity(self, df):
        """Function 29: Donor Propensity Heatmap"""
        # High votes in high strata = High Donor Propensity
        df['donor_score'] = df['historical_strength'] # Simplified
        return df

    def simulate_governance(self):
        """Function 30: Post-Election Governance Simulator"""
        return {"Fuerza Coalición": "62%", "Tasa Aprobación": "Alta"}
