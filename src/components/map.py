import streamlit as st
import folium
from folium.plugins import HeatMap, Fullscreen
from streamlit_folium import st_folium
import pandas as pd

def render_map_tab(synthesized_data, specific_targets, brain_mod):
    # --- GEO-ANALYSIS PANEL ---
    col_map, col_controls = st.columns([3, 1])

    with col_controls:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>CAPAS ESTRATÉGICAS</span>
                <span>⚙️</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📡 CONTROL DE CAPAS")
        layer_select = st.radio("CAPA ACTIVA", [
            "Densidad de Votos (Consolidación)", 
            "Potencial Crecimiento (Expansión)", 
            "Matriz Estrategia (Cuadrantes)",
            "Elasticidad Votante (Zonas Swing)",
            "Mapa Calor Sentimiento (Social)",
            "Ruta Logística (TSP)",
            "Mapa Calor Crisis (Fx 16)",
            "Propensión Donantes (Fx 29)"
        ], label_visibility="collapsed")
        
        st.markdown("---")
        
        # Sub-selector for Vote Density
        density_target = st.session_state.selected_candidate
        if layer_select == "Densidad de Votos (Consolidación)":
            density_target = st.selectbox("OBJETIVO", specific_targets, index=specific_targets.index(st.session_state.selected_candidate))
        
        st.markdown("#### ⚠️ ALERTS")
        is_demo = st.session_state.is_demo
        if is_demo:
            st.markdown("""<div class="alert-box">MODO DEMO ACTIVO<br>Usando Datos Reconstruidos</div>""", unsafe_allow_html=True)
        if synthesized_data.empty:
            st.markdown("""<div class="alert-box">NO SE DETECTARON DATOS<br>Verificar Selección Candidato</div>""", unsafe_allow_html=True)
            
        # CRM File Uploader
        st.markdown("---")
        st.markdown("#### 📤 CRM UPLOAD")
        uploaded_crm_file = st.file_uploader("Cargar CSV de Contactos", type=["csv"])
        if uploaded_crm_file is not None:
            st.session_state.crm_file = uploaded_crm_file
            st.success("CRM cargado exitosamente.")
        
        st.markdown("</div></div>", unsafe_allow_html=True)

    with col_map:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>MAPA DE INTELIGENCIA DISTRITAL</span>
                <span>EN VIVO</span>
            </div>
            <div class="panel-content" style="padding: 0;">
        """, unsafe_allow_html=True)
        
        # MAP RENDERING LOGIC (ROBUST)
        m = folium.Map(location=[6.2442, -75.5812], zoom_start=12, tiles="CartoDB dark_matter")
        Fullscreen().add_to(m)
        
        # Initialize logistics_route and strategic_points for this scope
        logistics_route = st.session_state.logistics_route
        strategic_points = st.session_state.strategic_points

        if not synthesized_data.empty:
            
            if layer_select == "Densidad de Votos (Consolidación)":
                # Dynamic Heatmap based on selection
                target_col = f"Votos_{density_target.replace(' ', '_')}"
                
                # Check if column exists (it should)
                if target_col in synthesized_data.columns:
                    # Filter out zero votes for cleaner map
                    heat_df = synthesized_data[synthesized_data[target_col] > 0]
                    
                    # Normalize for this specific target for visualization
                    max_val = heat_df[target_col].max()
                    if max_val > 0:
                        heat_data = heat_df[['lat', 'lon', target_col]].values.tolist()
                        # Weight the heatmap by votes
                        HeatMap(heat_data, radius=25, blur=15, gradient={0.4: '#1e3a8a', 0.7: '#3b82f6', 1.0: '#93c5fd'}, name=density_target).add_to(m)
                        
                        # Vote Bubbles
                        for _, row in heat_df.iterrows():
                            folium.CircleMarker(
                                location=[row['lat'], row['lon']],
                                radius=row[target_col] / max_val * 20 + 2, # Dynamic radius
                                color='#3b82f6',
                                fill=True,
                                fill_opacity=0.6,
                                weight=1,
                                popup=f"<b>{row['Puesto']}</b><br>{density_target}: {row[target_col]} votos"
                            ).add_to(m)
                else:
                    st.warning(f"No se encontraron datos para {density_target}")
                        
            elif layer_select == "Potencial Crecimiento (Expansión)":
                # Red Heatmap for Growth
                if 'growth_potential' in synthesized_data.columns:
                    growth_data = synthesized_data[['lat', 'lon', 'growth_potential']].values.tolist()
                    HeatMap(growth_data, radius=25, blur=15, gradient={0.4: '#7f1d1d', 0.7: '#dc2626', 1.0: '#fca5a5'}, name="Crecimiento").add_to(m)
            
            elif layer_select == "Matriz Estrategia (Cuadrantes)":
                # Color-coded markers
                colors = {'STRONGHOLD': '#22c55e', 'BATTLEGROUND': '#f59e0b', 'OPPORTUNITY': '#ef4444', 'OBSERVATION': '#64748b'}
                
                # Translation map for display
                strat_map = {
                    'STRONGHOLD': 'BASTIÓN',
                    'BATTLEGROUND': 'CAMPO DE BATALLA',
                    'OPPORTUNITY': 'OPORTUNIDAD',
                    'OBSERVATION': 'OBSERVACIÓN'
                }
                
                # Generate strategic points if not already generated
                if not st.session_state.strategic_points:
                    st.session_state.strategic_points = brain_mod.generate_strategic_points(synthesized_data)
                strategic_points = st.session_state.strategic_points

                for _, row in synthesized_data.iterrows():
                    strat = row.get('strategy_class', 'OBSERVATION')
                    strat_display = strat_map.get(strat, strat)
                    
                    folium.CircleMarker(
                        location=[row['lat'], row['lon']],
                        radius=6,
                        color=colors.get(strat, 'gray'),
                        fill=True,
                        fill_opacity=0.9,
                        popup=f"<b>{row['Puesto']}</b><br>Estrategia: {strat_display}<br>Votos: {row['Votos']}"
                    ).add_to(m)

            elif layer_select == "Elasticidad Votante (Zonas Swing)":
                # Purple Heatmap
                if 'elasticity' in synthesized_data.columns:
                    elasticity_data = synthesized_data[['lat', 'lon', 'elasticity']].values.tolist()
                    HeatMap(elasticity_data, radius=30, blur=20, gradient={0.4: '#581c87', 0.7: '#a855f7', 1.0: '#e9d5ff'}, name="Elasticidad").add_to(m)

            elif layer_select == "Mapa Calor Sentimiento (Social)":
                # Green/Red Heatmap
                if 'sentiment_score' in synthesized_data.columns:
                    for _, row in synthesized_data.iterrows():
                        if row['sentiment_score'] != 0:
                            color = '#22c55e' if row['sentiment_score'] > 0 else '#ef4444'
                            folium.CircleMarker(
                                location=[row['lat'], row['lon']],
                                radius=12,
                                color=color,
                                fill=True,
                                fill_opacity=0.5,
                                popup=f"Puntaje Sentimiento: {row['sentiment_score']}"
                            ).add_to(m)
                            
            elif layer_select == "Ruta Logística (TSP)":
                # Function 8: Draw Route
                if not st.session_state.logistics_route:
                    st.session_state.logistics_route = brain_mod.calculate_optimal_route(synthesized_data)
                logistics_route = st.session_state.logistics_route

                if logistics_route:
                    points = [[p['lat'], p['lon']] for p in logistics_route]
                    folium.PolyLine(points, color="#00f2ff", weight=5, opacity=0.9, dash_array='10').add_to(m)
                    for p in logistics_route:
                        folium.Marker(
                            [p['lat'], p['lon']], 
                            popup=f"PARADA {p['order']}: {p['location']}", 
                            icon=folium.Icon(color='blue', icon='road', prefix='fa')
                        ).add_to(m)
            
            elif layer_select == "Mapa Calor Crisis (Fx 16)":
                # Orange Heatmap
                synthesized_data = brain_mod.generate_crisis_heatmap(synthesized_data)
                crisis_data = synthesized_data[['lat', 'lon', 'crisis_risk']].values.tolist()
                HeatMap(crisis_data, radius=30, blur=20, gradient={0.4: '#f97316', 0.7: '#ea580c', 1.0: '#c2410c'}, name="Crisis").add_to(m)

            elif layer_select == "Propensión Donantes (Fx 29)":
                # Gold Heatmap
                synthesized_data = brain_mod.map_donor_propensity(synthesized_data)
                donor_data = synthesized_data[['lat', 'lon', 'donor_score']].values.tolist()
                HeatMap(donor_data, radius=25, blur=15, gradient={0.4: '#facc15', 0.7: '#eab308', 1.0: '#ca8a04'}, name="Donantes").add_to(m)

            # Strategic Points (Always Visible)
            if st.session_state.strategic_points:
                for point in st.session_state.strategic_points:
                    folium.Marker(
                        location=[point['lat'], point['lon']],
                        icon=folium.Icon(color=point['color'], icon=point['icon'], prefix='fa'),
                        tooltip=point['title'],
                        popup=f"<b>{point['title']}</b><br>{point['desc']}"
                    ).add_to(m)
                
        # Function 10: CRM Visualization
        crm_file = st.session_state.crm_file
        if crm_file:
            try:
                df_crm = pd.read_csv(crm_file)
                if {'lat', 'lon', 'name'}.issubset(df_crm.columns):
                    for _, row in df_crm.iterrows():
                        folium.Marker(
                            location=[row['lat'], row['lon']],
                            icon=folium.Icon(color='purple', icon='user', prefix='fa'),
                            tooltip=f"LÍDER: {row['name']}",
                            popup=f"<b>{row['name']}</b><br>Rol: {row.get('role', 'N/A')}"
                        ).add_to(m)
                    st.success(f"Cargados {len(df_crm)} contactos CRM.")
                else:
                    st.error("CSV CRM falta columnas: lat, lon, name")
            except Exception as e:
                st.error(f"Error loading CRM: {e}")
                
        st_folium(m, width=1200, height=600, returned_objects=[])
        st.markdown("</div></div>", unsafe_allow_html=True)
