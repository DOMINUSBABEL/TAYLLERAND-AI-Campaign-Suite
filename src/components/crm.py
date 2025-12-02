import streamlit as st
import pandas as pd
from src.services.survey_handler import AutomatedSurveyHandler

def render_crm(survey_mod: AutomatedSurveyHandler):
    st.header("OPS DE CAMPO")
    st.markdown("---")

    # Generate mock data if needed (in a real app this would come from a DB)
    if 'crm_data' not in st.session_state:
        st.session_state.crm_data = survey_mod.generate_mock_data(count=50)
    
    # Prioritize contacts
    # Define some mock strategic zones for the demo
    strategic_zones = [{'lat': 6.2442, 'lon': -75.5812}] # Example: Laureles center
    
    prioritized_df = survey_mod.prioritize_contacts(st.session_state.crm_data, strategic_zones)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        high_prio_count = len(prioritized_df[prioritized_df['priority_tier'] == 'ALTA'])
        st.metric("Contactos Prioridad Alta", high_prio_count)
    with col2:
        avg_affinity = prioritized_df['afinidad_score'].mean()
        st.metric("Afinidad Promedio", f"{avg_affinity:.1f}%")
    with col3:
        total_contacts = len(prioritized_df)
        st.metric("Total Contactos", total_contacts)

    st.markdown("### Listado de Contactos Priorizados")
    
    # Filters
    tier_filter = st.multiselect(
        "Filtrar por Prioridad",
        options=["ALTA", "MEDIA", "BAJA"],
        default=["ALTA", "MEDIA"]
    )
    
    if tier_filter:
        filtered_df = prioritized_df[prioritized_df['priority_tier'].isin(tier_filter)]
    else:
        filtered_df = prioritized_df

    # Display Table
    st.dataframe(
        filtered_df[[
            'name', 'phone', 'priority_tier', 'priority_score', 
            'afinidad_score', 'last_contact_date', 'location_text'
        ]].style.applymap(
            lambda x: 'background-color: #ff4b4b; color: white' if x == 'ALTA' else '',
            subset=['priority_tier']
        ),
        use_container_width=True
    )
