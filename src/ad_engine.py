import pandas as pd
import numpy as np
import random

class AdEngine:
    """
    Simulates the 'Phase 2: Precision Advertising Execution' of the Electoral Pipeline.
    Mimics Meta Ads Manager capabilities: Segmentation, Budgeting, and Performance Tracking.
    """
    
    def __init__(self):
        self.active_campaigns = []
        self.channels = ["Facebook", "Instagram", "WhatsApp", "Audience Network"]
        
    def estimate_audience_size(self, persona_data):
        """
        Simulates Meta's 'Potential Reach' calculation based on a persona.
        """
        base_population = 2500000 # Approx voting pop of Medellin
        
        # Apply filters based on persona specificity
        specificity = 1.0
        if "Demografía" in persona_data:
            specificity *= 0.4 # Age/Income cuts
        if "Intereses" in persona_data:
            specificity *= 0.3 # Interest intersection
            
        estimated_reach = int(base_population * specificity)
        
        # Add some noise
        estimated_reach = int(estimated_reach * random.uniform(0.9, 1.1))
        
        return {
            "potential_reach": estimated_reach,
            "daily_reach_min": int(estimated_reach * 0.05),
            "daily_reach_max": int(estimated_reach * 0.15)
        }

    def generate_ad_creatives(self, persona):
        """
        Generates tailored ad copy based on the persona's key themes.
        """
        themes = persona.get("Temas Clave", "General").split(",")
        creatives = []
        
        for theme in themes:
            theme = theme.strip()
            if "Seguridad" in theme:
                creatives.append({
                    "headline": "Recuperemos la Tranquilidad",
                    "body": "No más miedo en las calles. Plan Candado 2.0 es la solución.",
                    "image": "security_shield.jpg",
                    "theme": "Seguridad"
                })
            elif "Economía" in theme or "Impuestos" in theme:
                creatives.append({
                    "headline": "Menos Impuestos, Más Empleo",
                    "body": "Apoyo total a los emprendedores y cero burocracia.",
                    "image": "growth_chart.jpg",
                    "theme": "Economía"
                })
            elif "Familia" in theme:
                creatives.append({
                    "headline": "El Futuro de Nuestros Hijos",
                    "body": "Defendemos los valores que construyen sociedad.",
                    "image": "family_park.jpg",
                    "theme": "Familia"
                })
            else:
                creatives.append({
                    "headline": "Un Cambio Real",
                    "body": "Es hora de que Medellín vuelva a brillar.",
                    "image": "candidate_portrait.jpg",
                    "theme": "General"
                })
                
        return creatives

    def launch_campaign(self, campaign_name, persona, budget, channel_mix):
        """
        Simulates launching a campaign. Returns a campaign object with projected results.
        """
        audience = self.estimate_audience_size(persona)
        
        # CPM (Cost Per Mille) simulation based on channel
        avg_cpm = 0
        if "Facebook" in channel_mix: avg_cpm += 4000
        if "Instagram" in channel_mix: avg_cpm += 6000
        if "WhatsApp" in channel_mix: avg_cpm += 2000 # Click to chat
        avg_cpm /= len(channel_mix) if channel_mix else 1
        
        impressions = (budget / avg_cpm) * 1000
        ctr = random.uniform(0.015, 0.045) # 1.5% to 4.5% CTR
        clicks = int(impressions * ctr)
        conversions = int(clicks * random.uniform(0.05, 0.12)) # 5-12% conversion rate
        
        campaign_result = {
            "id": f"CMP-{random.randint(1000, 9999)}",
            "name": campaign_name,
            "status": "ACTIVE",
            "target_persona": persona.get("Persona", "General"),
            "budget": budget,
            "channels": channel_mix,
            "metrics": {
                "impressions": int(impressions),
                "clicks": clicks,
                "conversions": conversions,
                "ctr": f"{ctr*100:.2f}%",
                "cpc": int(budget / clicks) if clicks > 0 else 0,
                "spend": budget
            }
        }
        
        self.active_campaigns.append(campaign_result)
        return campaign_result

    def get_active_campaigns_df(self):
        """Returns a DataFrame of active campaigns for the dashboard."""
        if not self.active_campaigns:
            return pd.DataFrame(columns=["ID", "Campaña", "Persona", "Canales", "Inversión", "Impresiones", "Clicks", "Conversiones"])
            
        data = []
        for c in self.active_campaigns:
            data.append({
                "ID": c["id"],
                "Campaña": c["name"],
                "Persona": c["target_persona"],
                "Canales": ", ".join(c["channels"]),
                "Inversión": f"${c['budget']:,}",
                "Impresiones": f"{c['metrics']['impressions']:,}",
                "Clicks": f"{c['metrics']['clicks']:,}",
                "Conversiones": c["metrics"]["conversions"]
            })
        return pd.DataFrame(data)
