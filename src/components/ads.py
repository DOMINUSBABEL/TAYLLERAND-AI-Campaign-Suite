import streamlit as st
import pandas as pd
from src.services.ad_engine import AdEngine

def render_ads(ad_mod: AdEngine):
    st.header("EJECUCIÓN PUBLICITARIA")
    st.markdown("---")

    col_form, col_stats = st.columns([1, 2])

    with col_form:
        st.subheader("Lanzar Nueva Campaña")
        with st.form("new_campaign_form"):
            camp_name = st.text_input("Nombre de la Campaña", "Campaña Táctica 1")
            
            target_persona = st.selectbox(
                "Persona Objetivo",
                ["Jóvenes Universitarios", "Amas de Casa", "Empresarios", "Pensionados", "General"]
            )
            
            budget = st.number_input("Presupuesto (COP)", min_value=100000, value=1000000, step=100000)
            
            channels = st.multiselect(
                "Canales",
                ["Facebook", "Instagram", "WhatsApp", "Audience Network"],
                default=["Facebook", "Instagram"]
            )
            
            submitted = st.form_submit_button("Lanzar Campaña")
            
            if submitted:
                # Mock persona data
                persona_data = {"Persona": target_persona, "Temas Clave": "Seguridad, Empleo"}
                
                result = ad_mod.launch_campaign(camp_name, persona_data, budget, channels)
                st.success(f"Campaña {result['id']} lanzada exitosamente!")

    with col_stats:
        st.subheader("Campañas Activas")
        active_df = ad_mod.get_active_campaigns_df()
        
        if not active_df.empty:
            st.dataframe(active_df, use_container_width=True)
            
            # Aggregate Metrics
            total_spend = active_df["Inversión"].str.replace("$", "").str.replace(",", "").astype(float).sum()
            total_impressions = active_df["Impresiones"].str.replace(",", "").astype(int).sum()
            total_conversions = active_df["Conversiones"].sum()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Inversión Total", f"${total_spend:,.0f}")
            m2.metric("Impresiones Totales", f"{total_impressions:,}")
            m3.metric("Conversiones Totales", f"{total_conversions:,}")
        else:
            st.info("No hay campañas activas. Lanza una nueva campaña desde el panel izquierdo.")
