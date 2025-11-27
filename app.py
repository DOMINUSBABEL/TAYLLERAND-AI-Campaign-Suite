import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, Fullscreen, MarkerCluster
import altair as alt
import importlib
import time

# Force reload of modules
import src.e26_processor
import src.social_sentinel
import src.targeting_brain

importlib.reload(src.e26_processor)
importlib.reload(src.social_sentinel)
importlib.reload(src.targeting_brain)

from src.e26_processor import E26Processor
from src.social_sentinel import SocialSentinel
from src.targeting_brain import TargetingBrain

# Page Config
st.set_page_config(
    page_title="TAYLLERAND | SIGLO XXIII",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZATION ---
def load_modules():
    return E26Processor(), SocialSentinel(), TargetingBrain()

e26_mod, social_mod, brain_mod = load_modules()

# --- CONFIGURATION & CONSTANTS ---
# Define Specific Targets for E-14 Analysis (Available for Selection)
candidate_options = [
    "MARIA FERNANDA CABAL",
    "CARLOS HUMBERTO GARCIA",
    "JOSE LUIS NOREÑA",
    "ANDERSON DUQUE",
    "CENTRO DEMOCRATICO", # For Logo/Party
    "CANDIDATO 1" # Head of List
]

# --- SIDEBAR: COMMAND DECK ---
with st.sidebar:
    st.image("logo.png", width=100)
    st.markdown("## 🦅 TAYLLERAND_OS `v3.0`")
    st.markdown("<div style='font-family: Roboto Condensed; color: #94a3b8; font-size: 0.8rem;'>SISTEMA EN LÍNEA // ESPERANDO ENTRADA</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 📂 ENLACE DE DATOS")
    uploaded_file = st.file_uploader("FLUJO DE DATOS E-26", type=["csv"])
    crm_file = st.file_uploader("ENLACE CRM (Líderes)", type=["csv"])
    
    st.markdown("---")
    st.markdown("### 🎯 OBJETIVO FIJADO")
    
    # Fixed: Use Selectbox with candidates actually in the data
    target_candidate = st.selectbox("SELECCIONAR CANDIDATO", candidate_options)
    
    st.markdown("---")
    st.markdown("### 🎚️ PARÁMETROS ESTRATÉGICOS")
    
    w_security = st.slider("PESO SEGURIDAD", 0.5, 2.0, 1.0, 0.1)
    w_opinion = st.slider("PESO OPINIÓN", 0.5, 2.0, 1.0, 0.1)
    w_growth = st.slider("FACTOR CRECIMIENTO", 0.5, 2.0, 1.0, 0.1)
    turnout_factor = st.slider("SIM PARTICIPACIÓN (Fx 5)", 0.5, 1.5, 1.0, 0.1)
    
    weights = {
        'security': w_security,
        'opinion': w_opinion,
        'growth': w_growth
    }
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; font-family: Roboto Condensed; color: #64748b;'>CONEXIÓN SEGURA ESTABLECIDA</div>", unsafe_allow_html=True)

# --- DATA PROCESSING ENGINE ---
# Use the selected candidate plus the full list for processing context
specific_targets = list(set([target_candidate] + candidate_options))

# 1. Load Real Data (or Demo)
if uploaded_file:
    raw_df = e26_mod.load_data_from_csv(uploaded_file)
    df_history = e26_mod.process_data(raw_df, specific_targets)
    data_source_label = "CARGA OFICIAL"
    is_demo = False
else:
    # Load High-Fidelity Preload by default
    raw_df = e26_mod.load_demo_data()
    df_history = e26_mod.process_data(raw_df, specific_targets)
    data_source_label = "OFICIAL PRECARGADO"
    is_demo = True

# --- SUMMARY TABLE FOR SPECIFIC CANDIDATES ---
st.markdown("### 📋 RESUMEN DE CANDIDATOS")
summary_data = []
for t in specific_targets:
    col_name = f"Votos_{t.replace(' ', '_')}"
    if col_name in df_history.columns:
        total_votes_t = df_history[col_name].sum()
        summary_data.append({"CANDIDATO": t, "VOTOS TOTALES": total_votes_t})
    else:
         summary_data.append({"CANDIDATO": t, "VOTOS TOTALES": 0})

st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

# 2. Load Verified Social (Static/Real)
df_social = social_mod.generate_verified_feed()

# 3. Synthesize & Project
synthesized_data = brain_mod.synthesize(df_history, df_social, weights=weights)

# Apply Advanced Functions (5, 6, 7)
synthesized_data = brain_mod.simulate_turnout(synthesized_data, turnout_factor)
synthesized_data = brain_mod.calculate_elasticity(synthesized_data)
synthesized_data = brain_mod.calculate_sentiment_correlation(synthesized_data, df_social)

strategic_points = brain_mod.generate_strategic_points(synthesized_data)
resource_plan = brain_mod.optimize_resources(synthesized_data)
logistics_route = brain_mod.calculate_optimal_route(synthesized_data)
campaign_brief = brain_mod.generate_campaign_brief(synthesized_data, strategic_points)

# --- MAIN COMMAND CENTER ---
st.markdown(f"# 📊 INTELIGENCIA DE CAMPAÑA // <span style='color:#2563eb'>{target_candidate}</span>", unsafe_allow_html=True)

# Function 9: Campaign Brief (Collapsible)
with st.expander("📄 INFORME OFICIAL DE CAMPAÑA (Función 9)", expanded=False):
    st.markdown(campaign_brief)

# --- HUD METRICS ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# Use Projected Votes if Turnout != 1.0
total_votes = synthesized_data['Votos_Projected'].sum() if not synthesized_data.empty else 0
social_vol = len(df_social)
points_count = len(strategic_points)
growth_zones = len([p for p in strategic_points if p['type'] == 'GROWTH'])

with kpi1:
    st.markdown(f"""<div class="hud-card"><div class="hud-label">VOTOS PROYECTADOS</div><div class="hud-value">{total_votes:,}</div></div>""", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"""<div class="hud-card"><div class="hud-label">MENCIONES NOTICIAS</div><div class="hud-value">{social_vol}</div></div>""", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"""<div class="hud-card"><div class="hud-label">ZONAS DE CRECIMIENTO</div><div class="hud-value">{growth_zones}</div></div>""", unsafe_allow_html=True)
with kpi4:
    st.markdown(f"""<div class="hud-card alert"><div class="hud-label">FUENTE DE DATOS</div><div class="hud-value" style="font-size: 1.5rem;">{data_source_label}</div></div>""", unsafe_allow_html=True)

# --- MULTI-WINDOW INTERFACE (TABS) ---
tab_map, tab_sim, tab_control, tab_social, tab_crm = st.tabs(["🗺️ OPS GEOSPACIALES", "🔮 PLATAFORMA SIMULACIÓN", "🎛️ SALA DE CONTROL", "📡 INTEL SOCIAL", "👥 OPS DE CAMPO"])

with tab_map:
    st.markdown("### 🗺️ PLATAFORMA DE ESTRATEGIA GEOSPACIAL")

    col_map, col_controls = st.columns([3, 1])

    with col_controls:
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
        ])
        
        # Sub-selector for Vote Density
        if layer_select == "Densidad de Votos (Consolidación)":
            density_target = st.selectbox("SELECCIONAR OBJETIVO DENSIDAD", specific_targets, index=0)
        
        st.markdown("#### ⚠️ ALERTAS")
        if is_demo:
            st.markdown("""<div class="alert-box">MODO DEMO ACTIVO<br>Usando Datos Reconstruidos</div>""", unsafe_allow_html=True)
        if synthesized_data.empty:
            st.markdown("""<div class="alert-box">NO SE DETECTARON DATOS<br>Verificar Selección Candidato</div>""", unsafe_allow_html=True)

    with col_map:
        # MAP RENDERING LOGIC (ROBUST)
        m = folium.Map(location=[6.2442, -75.5812], zoom_start=12, tiles="CartoDB dark_matter")
        Fullscreen().add_to(m)
        
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
            for point in strategic_points:
                folium.Marker(
                    location=[point['lat'], point['lon']],
                    icon=folium.Icon(color=point['color'], icon=point['icon'], prefix='fa'),
                    tooltip=point['title'],
                    popup=f"<b>{point['title']}</b><br>{point['desc']}"
                ).add_to(m)
                
        # Function 10: CRM Visualization
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

with tab_sim:
    st.markdown("### 🔮 PLATAFORMA SIMULACIÓN (Funciones 11-20)")
    
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        st.markdown("#### 📈 CRECIMIENTO COMPARATIVO (Fx 11)")
        synthesized_data = brain_mod.calculate_comparative_growth(synthesized_data)
        st.line_chart(synthesized_data.set_index('Puesto')['growth_velocity'].head(20))
        
        st.markdown("#### 🌪️ GEMELO DIGITAL (Fx 13)")
        synthesized_data = brain_mod.run_digital_twin(synthesized_data)
        st.bar_chart(synthesized_data['win_probability'].head(10))

    with sim_col2:
        st.markdown("#### 🤝 CONSTRUCTOR COALICIÓN (Fx 19)")
        synthesized_data = brain_mod.build_coalition(synthesized_data)
        st.metric("Impulso Coalición", "+15%", "Votos")
        
        st.markdown("#### 🏆 CAMINO A LA VICTORIA (Fx 20)")
        victory_path = brain_mod.generate_victory_path(synthesized_data)
        st.dataframe(victory_path, use_container_width=True)

with tab_control:
    st.markdown("### 🎛️ SALA DE CONTROL (Funciones 21-30)")
    
    c_col1, c_col2, c_col3 = st.columns(3)
    
    with c_col1:
        st.markdown("#### 🎭 GEN PERSONAS (Fx 21)")
        persona = brain_mod.generate_personas(synthesized_data)
        st.json(persona)
        
        st.markdown("#### 🦠 BUCLE VIRAL (Fx 22)")
        viral_data = brain_mod.simulate_viral_loop()
        st.line_chart(viral_data.set_index('Day'))

    with c_col2:
        st.markdown("#### 💸 GASTO PRESUPUESTO (Fx 25)")
        budget_data = brain_mod.forecast_budget_burn()
        st.area_chart(budget_data.set_index('Week')['Spend'])
        
        st.markdown("#### 🎮 GAMIFICACIÓN GOTV (Fx 26)")
        gotv_data = brain_mod.gamify_gotv()
        st.dataframe(gotv_data, use_container_width=True)

    with c_col3:
        st.markdown("#### 🕵️ INTEL OPOSICIÓN (Fx 24)")
        opp_data = brain_mod.get_opposition_intel()
        st.table(opp_data)
        
        st.markdown("#### 🌦️ IMPACTO CLIMA (Fx 27)")
        weather = brain_mod.correlate_weather()
        st.metric("Pronóstico", weather['Forecast'], weather['Turnout Impact'])

with tab_social:
    st.markdown("### 📡 INTELIGENCIA SOCIAL AVANZADA")
    
    # --- LAYOUT: 3 COLUMNS (Feed, Profiler, Message Designer) ---
    col_feed, col_profile, col_designer = st.columns([1.2, 1, 1])
    
    # 1. FEED & LISTENER
    with col_feed:
        st.markdown("#### 👂 ESCUCHA ACTIVA")
        
        # Filters
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            active_affinity = st.multiselect("AFINIDAD", social_mod.affinities, default=["URIBISMO", "GENERAL"])
        with f_col2:
            active_topic = st.multiselect("TEMA", social_mod.topics, default=["SEGURIDAD", "CAMPAÑA"])
            
        # Fetch Data
        feed_data = social_mod.listen(affinity_filter=active_affinity, topic_filter=active_topic)
        
        # Feed Visualization
        with st.container(height=600):
            if feed_data.empty:
                st.info("Sin señal.")
            else:
                for _, row in feed_data.iterrows():
                    # Dynamic Border Color
                    b_color = "#22c55e" if row['sentiment'] > 0 else "#ef4444"
                    if row['sentiment'] == 0: b_color = "#94a3b8"
                    
                    # Card HTML
                    st.markdown(f"""
                    <div style="
                        border-left: 4px solid {b_color}; 
                        background: #1e293b; 
                        padding: 15px; 
                        margin-bottom: 10px; 
                        border-radius: 4px;
                        border: 1px solid #334155;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="color: #f8fafc; font-weight: 700; font-size: 0.95rem;">{row['user_name']}</span>
                            <span style="font-size: 0.7rem; color: #cbd5e1; background: #334155; padding: 2px 6px; border-radius: 4px;">{row['affinity']}</span>
                        </div>
                        <div style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.4; margin-bottom: 10px;">{row['text']}</div>
                        <div style="display: flex; gap: 10px; font-size: 0.75rem; color: #94a3b8; font-family: 'Roboto Condensed';">
                            <span>📅 {row['date']}</span>
                            <span>🏷️ {row['topic']}</span>
                            <span>⚡ {row.get('influence_score', 0)} INF</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # 2. VOTER PROFILER
    with col_profile:
        st.markdown("#### 👤 PERFILADOR DE OBJETIVOS")
        
        # User Selection (Simulated from Feed)
        if not feed_data.empty:
            selected_user_id = st.selectbox("SELECCIONAR OBJETIVO", feed_data['user_id'].unique())
            
            if selected_user_id:
                profile = social_mod.generate_voter_profile(selected_user_id)
                
                # Profile Card
                st.markdown(f"""
                <div class="hud-card" style="border-top: 4px solid #f59e0b;">
                    <div style="text-align: center; margin-bottom: 15px;">
                        <div style="font-size: 1.4rem; font-weight: 800; color: #fff;">{profile['Name']}</div>
                        <div style="color: #94a3b8; font-family: 'Roboto Condensed';">{profile['User ID']}</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 0.9rem;">
                        <div><span style="color:#94a3b8; font-weight:700;">AFINIDAD:</span><br>{profile['Affinity']}</div>
                        <div><span style="color:#94a3b8; font-weight:700;">INFLUENCIA:</span><br>{profile['Influence Score']}/100</div>
                        <div><span style="color:#94a3b8; font-weight:700;">GUSTOS:</span><br>{profile['Political Taste']}</div>
                        <div><span style="color:#94a3b8; font-weight:700;">EDAD:</span><br>{profile['Age Group']}</div>
                    </div>
                    <div style="margin-top: 20px;">
                        <span style="color:#94a3b8; font-size: 0.8rem; font-weight:700;">INTERESES CLAVE:</span>
                        <div style="margin-top: 8px; display: flex; flex-wrap: wrap; gap: 5px;">
                            {''.join([f'<span style="background:#334155; color:#f1f5f9; padding:4px 10px; border-radius:4px; font-size:0.75rem;">{i}</span>' for i in profile['Primary Interests'].split(', ')])}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action Buttons
                st.button("🎯 AGREGAR A LISTA DE OBJETIVOS", use_container_width=True)
                st.button("⚠️ MARCAR COMO HOSTIL", use_container_width=True)

    # 3. MESSAGE DESIGNER
    with col_designer:
        st.markdown("#### 💬 DISEÑADOR DE MENSAJES")
        
        target_audience = st.selectbox("AUDIENCIA OBJETIVO", ["URIBISMO", "PETRISMO", "INDEPENDIENTES", "GENERAL"])
        draft_msg = st.text_area("BORRADOR DE MENSAJE", height=150, placeholder="Escribe tu mensaje aquí para simular impacto...")
        
        if st.button("🚀 SIMULAR IMPACTO", use_container_width=True):
            if draft_msg:
                impact = social_mod.analyze_message_impact(draft_msg, target_audience)
                
                # Results Display
                st.markdown("##### RESULTADOS DE SIMULACIÓN")
                
                r1, r2 = st.columns(2)
                with r1:
                    st.metric("PUNTAJE IMPACTO", f"{impact['Impact Score']}/100", impact['Sentiment Shift'])
                with r2:
                    st.metric("ALCANCE EST.", f"{impact['Projected Reach']}", impact['Resonance'])
                
                # Visual Bar
                st.progress(impact['Impact Score'] / 100)
                
                if impact['Impact Score'] > 70:
                    st.success("¡Mensaje de Alto Impacto! Recomendado para difusión.")
                elif impact['Impact Score'] < 40:
                    st.warning("Impacto bajo. Revisa palabras clave.")
            else:
                st.error("Escribe un mensaje primero.")

with tab_crm:
    st.markdown("### 👥 OPERACIONES DE CAMPO - PRIORIZACIÓN CONTACTOS")
    
    # Initialize survey handler
    from src.survey_handler import AutomatedSurveyHandler
    survey_mod = AutomatedSurveyHandler()
    
    # Load or generate contacts
    if crm_file:
        try:
            crm_df = pd.read_csv(crm_file)
            # Ensure required columns exist
            if not {'lat', 'lon', 'name'}.issubset(crm_df.columns):
                st.error("CSV CRM debe incluir: lat, lon, name")
                crm_df = survey_mod.generate_mock_data(50)
            else:
                # Standardize column names if needed
                if 'afinidad' not in crm_df.columns and 'afinidad_score' in crm_df.columns:
                    crm_df.rename(columns={'afinidad_score': 'afinidad'}, inplace=True)
        except Exception as e:
            st.error(f"Error cargando CRM: {e}")
            crm_df = survey_mod.generate_mock_data(50)
    else:
        # Generate mock data
        crm_df = survey_mod.generate_mock_data(50)
    
    # Prioritize contacts using strategic points from targeting brain
    prioritized_contacts = survey_mod.prioritize_contacts(crm_df, strategic_zones=strategic_points)
    
    # Controls
    col_f1, col_f2, col_f3 = st.columns([1, 1, 2])
    
    with col_f1:
        tier_filter = st.multiselect(
            "NIVEL PRIORIDAD",
            ["HIGH", "MEDIUM", "LOW"],
            default=["HIGH", "MEDIUM"]
        )
    
    with col_f2:
        min_affinity = st.slider("AFINIDAD MÍNIMA", 0, 100, 0, 5)
    
    with col_f3:
        st.metric("CONTACTOS TOTALES", len(prioritized_contacts))
        st.metric("ALTA PRIORIDAD", len(prioritized_contacts[prioritized_contacts['priority_tier'] == 'HIGH']))
    
    # Filter based on controls
    filtered_contacts = prioritized_contacts[
        (prioritized_contacts['priority_tier'].isin(tier_filter)) &
        (prioritized_contacts['afinidad_score'] >= min_affinity)
    ]
    
    st.markdown("---")
    
    # Two-column layout: Map + Contact Table
    col_map_f, col_table_f = st.columns([2, 1])
    
    with col_map_f:
        st.markdown("#### 🗺️ MAPA DE CONTACTOS")
        
        # Create map
        m_contacts = folium.Map(location=[6.2442, -75.5812], zoom_start=12, tiles="CartoDB dark_matter")
        Fullscreen().add_to(m_contacts)
        
        # Color coding by priority tier
        tier_colors = {
            "HIGH": "#22c55e",
            "MEDIUM": "#f59e0b",
            "LOW": "#64748b"
        }
        
        for _, contact in filtered_contacts.iterrows():
            color = tier_colors.get(contact['priority_tier'], 'gray')
            folium.CircleMarker(
                location=[contact['lat'], contact['lon']],
                radius=8,
                color=color,
                fill=True,
                fill_opacity=0.8,
                weight=2,
                popup=f"""
                    <b>{contact['name']}</b><br>
                    Tel: {contact['phone']}<br>
                    Afinidad: {contact['afinidad_score']}/100<br>
                    Prioridad: {contact['priority_tier']} ({contact['priority_score']:.1f})
                """
            ).add_to(m_contacts)
        
        st_folium(m_contacts, width=800, height=400, returned_objects=[])
    
    with col_table_f:
        st.markdown("#### 📞 LISTA DE LLAMADAS PRIORITARIAS")
        
        # Display top contacts
        call_list = filtered_contacts[['name', 'phone', 'priority_tier', 'priority_score']].head(20)
        
        st.dataframe(
            call_list,
            use_container_width=True,
            height=400
        )
        
        # Export button
        csv = filtered_contacts.to_csv(index=False)
        st.download_button(
            label="📥 EXPORTAR LISTA LLAMADAS",
            data=csv,
            file_name="tayllerand_call_list.csv",
            mime="text/csv"
        )

# --- FOOTER ---
st.markdown("---")
st.markdown("<center style='font-family: Roboto Condensed; color: #64748b; font-size: 0.8rem;'>TAYLLERAND SYSTEM v3.0 | CLASIFICADO | SOLO OJOS AUTORIZADOS</center>", unsafe_allow_html=True)
