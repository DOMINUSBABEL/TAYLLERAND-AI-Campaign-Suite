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
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL VISUAL THEME (ELECTORAL COMMAND CENTER) ---
st.markdown("""
<style>
    /* 1. VARIABLES & PALETTE */
    :root {
        --bg-color: #0f172a; /* Deep Navy */
        --surface-color: #1e293b; /* Slate */
        --card-bg: #1e293b;
        --border-color: #334155;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --accent-blue: #3b82f6; /* Campaign Support */
        --accent-red: #ef4444; /* Opposition */
        --accent-gold: #f59e0b; /* Alerts/Money */
        --font-heading: 'Roboto', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }

    /* 2. CORE STREAMLIT OVERRIDES */
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-primary);
        font-family: var(--font-heading);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid var(--border-color);
    }
    
    /* Inputs */
    .stSelectbox, .stTextInput, .stNumberInput, .stSlider {
        color: var(--text-primary) !important;
    }
    div[data-baseweb="select"] > div {
        background-color: var(--surface-color) !important;
        border-color: var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: var(--surface-color);
        border-radius: 4px 4px 0 0;
        border: 1px solid var(--border-color);
        color: var(--text-secondary);
        padding: 0 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--accent-blue) !important;
        color: white !important;
        border-color: var(--accent-blue) !important;
    }

    /* 3. CUSTOM COMPONENT CLASSES */
    
    /* HUD Card */
    .hud-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 4px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .hud-title {
        font-family: var(--font-heading);
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-secondary);
        margin-bottom: 10px;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 5px;
    }
    
    /* Ticker */
    .ticker-container {
        display: flex;
        justify-content: space-between;
        background-color: #020617;
        border-bottom: 1px solid var(--border-color);
        padding: 10px 20px;
        margin-bottom: 20px;
        font-family: var(--font-mono);
    }
    .ticker-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .ticker-label {
        font-size: 0.7rem;
        color: var(--text-secondary);
        margin-bottom: 2px;
    }
    .ticker-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    .ticker-value.up { color: var(--accent-blue); }
    .ticker-value.down { color: var(--accent-red); }
    
    /* Order Book / Feed */
    .order-book-container {
        background-color: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: 4px;
        font-family: var(--font-mono);
        font-size: 0.8rem;
    }
    .order-book-header {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        padding: 8px 12px;
        background-color: #0f172a;
        color: var(--text-secondary);
        font-weight: bold;
        border-bottom: 1px solid var(--border-color);
    }
    .order-row {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        padding: 6px 12px;
        border-bottom: 1px solid #33415533;
    }
    .order-row:hover { background-color: #334155; cursor: pointer; }
    .order-row.ask span:first-child { color: var(--accent-red); }
    .order-row.bid span:first-child { color: var(--accent-blue); }
    
    /* Alerts */
    .alert-box {
        background-color: rgba(245, 158, 11, 0.1);
        border-left: 4px solid var(--accent-gold);
        color: var(--accent-gold);
        padding: 10px;
        font-size: 0.8rem;
        margin-bottom: 10px;
    }

</style>
""", unsafe_allow_html=True)
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
st.markdown(f"# 📊 INTELIGENCIA DE CAMPAÑA // <span style='color:#0ecb81'>{target_candidate}</span>", unsafe_allow_html=True)

# TICKER BAR
st.markdown(f"""
<div class="ticker-container">
    <div class="ticker-item">
        <span class="ticker-label">VOTOS PROYECTADOS</span>
        <span class="ticker-value up">{total_votes:,}</span>
    </div>
    <div class="ticker-item">
        <span class="ticker-label">VOLUMEN SOCIAL</span>
        <span class="ticker-value">{social_vol}</span>
    </div>
    <div class="ticker-item">
        <span class="ticker-label">ZONAS CRECIMIENTO</span>
        <span class="ticker-value up">+{growth_zones}</span>
    </div>
    <div class="ticker-item">
        <span class="ticker-label">DÍAS RESTANTES</span>
        <span class="ticker-value">45</span>
    </div>
    <div class="ticker-item">
        <span class="ticker-label">PRESUPUESTO (24H)</span>
        <span class="ticker-value down">- $12.5M</span>
    </div>
</div>
""", unsafe_allow_html=True)

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
    
    # --- LAYOUT: 3 COLUMNS (Feed/Order Book, Profiler, Message Designer) ---
    col_feed, col_profile, col_designer = st.columns([1.5, 1, 1])
    
    # 1. FEED & LISTENER (ORDER BOOK STYLE)
    with col_feed:
        st.markdown("#### 📖 LIBRO DE ÓRDENES (SOCIAL)")
        
        # Filters
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            active_affinity = st.multiselect("AFINIDAD", social_mod.affinities, default=["URIBISMO", "GENERAL"])
        with f_col2:
            active_topic = st.multiselect("TEMA", social_mod.topics, default=["SEGURIDAD", "CAMPAÑA"])
            
        # Fetch Data
        feed_data = social_mod.listen(affinity_filter=active_affinity, topic_filter=active_topic)
        
        # Order Book Visualization
        with st.container(height=600):
            if feed_data.empty:
                st.info("Sin datos de mercado.")
            else:
                st.markdown("""
                <div class="order-book-container">
                    <div class="order-book-header">
                        <span>PRECIO (SENTIMIENTO)</span>
                        <span>CANTIDAD (INF)</span>
                        <span>USUARIO</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Split into Asks (Negative) and Bids (Positive)
                asks = feed_data[feed_data['sentiment'] < 0].sort_values('sentiment', ascending=True)
                bids = feed_data[feed_data['sentiment'] >= 0].sort_values('sentiment', ascending=False)
                
                # Render Asks (Red - Top)
                for _, row in asks.iterrows():
                    st.markdown(f"""
                    <div class="order-row ask">
                        <span>{row['sentiment']:.2f} ▼</span>
                        <span>{row.get('influence_score', 0)}</span>
                        <span>{row['user_name']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                # Spread / Current Price
                avg_sentiment = feed_data['sentiment'].mean()
                # Use theme colors: Blue for Positive (Support), Red for Negative (Opposition)
                price_color = "var(--accent-blue)" if avg_sentiment >= 0 else "var(--accent-red)"
                st.markdown(f"""
                <div style="padding: 10px; text-align: center; font-family: var(--font-mono); font-size: 16px; font-weight: bold; color: {price_color}; border-top: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color); background: var(--bg-color);">
                    {avg_sentiment:.4f} INDEX (AVG)
                </div>
                """, unsafe_allow_html=True)
                
                # Render Bids (Green - Bottom)
                for _, row in bids.iterrows():
                    st.markdown(f"""
                    <div class="order-row bid">
                        <span>{row['sentiment']:.2f} ▲</span>
                        <span>{row.get('influence_score', 0)}</span>
                        <span>{row['user_name']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                st.markdown("</div>", unsafe_allow_html=True)

    # 2. VOTER PROFILER
    with col_profile:
        st.markdown("#### 👤 PERFILADOR (KYC)")
        
        # User Selection (Simulated from Feed)
        if not feed_data.empty:
            selected_user_id = st.selectbox("SELECCIONAR USUARIO", feed_data['user_id'].unique())
            
            if selected_user_id:
                profile = social_mod.generate_voter_profile(selected_user_id)
                
                # Profile Card (Electoral Command Style)
                st.markdown(f"""
                <div class="hud-card">
                    <div style="text-align: center; margin-bottom: 15px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px;">
                        <div style="font-size: 1.2rem; font-weight: 700; color: var(--text-primary);">{profile['Name']}</div>
                        <div style="color: var(--text-secondary); font-family: var(--font-mono); font-size: 0.8rem;">ID: {profile['User ID']}</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.85rem; font-family: var(--font-mono);">
                        <div><span style="color:var(--text-secondary);">AFINIDAD</span><br><span style="color:var(--text-primary);">{profile['Affinity']}</span></div>
                        <div><span style="color:var(--text-secondary);">SCORE</span><br><span style="color:var(--accent-gold);">{profile['Influence Score']}/100</span></div>
                        <div><span style="color:var(--text-secondary);">GUSTOS</span><br><span style="color:var(--text-primary);">{profile['Political Taste']}</span></div>
                        <div><span style="color:var(--text-secondary);">EDAD</span><br><span style="color:var(--text-primary);">{profile['Age Group']}</span></div>
                    </div>
                    <div style="margin-top: 15px;">
                        <span style="color:var(--text-secondary); font-size: 0.8rem;">INTERESES</span>
                        <div style="margin-top: 5px; display: flex; flex-wrap: wrap; gap: 5px;">
                            {''.join([f'<span style="background:var(--surface-color); color:var(--text-primary); padding:2px 6px; border-radius:2px; font-size:0.75rem;">{i}</span>' for i in profile['Primary Interests'].split(', ')])}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action Buttons
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                c1, c2 = st.columns(2)
                with c1:
                    st.button("RECLUTAR (LONG)", key="btn_long", use_container_width=True)
                with c2:
                    st.button("NEUTRALIZAR (SHORT)", key="btn_short", use_container_width=True)

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
