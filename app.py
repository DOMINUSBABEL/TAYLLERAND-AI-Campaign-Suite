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
import src.survey_handler
import src.ad_engine

importlib.reload(src.e26_processor)
importlib.reload(src.social_sentinel)
importlib.reload(src.targeting_brain)
importlib.reload(src.survey_handler)
importlib.reload(src.ad_engine)

from src.e26_processor import E26Processor
from src.social_sentinel import SocialSentinel
from src.targeting_brain import TargetingBrain
from src.survey_handler import AutomatedSurveyHandler
from src.ad_engine import AdEngine

# Page Config
st.set_page_config(
    page_title="TAYLLERAND | SIGLO XXIII",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL VISUAL THEME (TAYLLERAND OS - NEO CLASSICAL) ---
st.markdown("""
<style>
    /* 1. FONTS & IMPORTS */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Roboto+Condensed:wght@300;400;700&family=JetBrains+Mono:wght@400&display=swap');

    /* 2. VARIABLES & PALETTE (TAYLLERAND OS) */
    :root {
        --bg-color: #0f172a; /* Deep Navy Background */
        --surface-color: #1e293b; /* Panel Background */
        --border-color: #d4af37; /* Metallic Gold Border */
        --border-dim: #94a3b8; /* Dim Border for non-active */
        --text-primary: #ffffff; /* Pure White for better visibility */
        --text-secondary: #cbd5e1; /* Lighter Slate */
        --accent-gold: #d4af37; /* Primary Accent */
        --accent-blue: #3b82f6; /* Support/Positive */
        --accent-red: #ef4444; /* Opposition/Negative */
        
        --font-heading: 'Cinzel', serif; /* Neo-Classical Header */
        --font-body: 'Roboto Condensed', sans-serif; /* Technical Body */
        --font-mono: 'JetBrains Mono', monospace;
    }

    /* 3. CORE STREAMLIT OVERRIDES */
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-primary);
        font-family: var(--font-body);
    }
    
    /* Hide Default Header & Sidebar Toggle */
    header[data-testid="stHeader"] { display: none; }
    
    /* Sidebar (Hidden/Custom) */
    [data-testid="stSidebar"] { display: none; }

    /* 4. CUSTOM COMPONENTS */
    
    /* Top Navigation Bar */
    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #020617;
        border-bottom: 3px solid var(--accent-gold);
        padding: 10px 30px;
        margin-bottom: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.8);
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 15px;
        font-family: var(--font-heading);
        font-size: 1.8rem;
        color: var(--accent-gold);
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    .nav-links {
        display: flex;
        gap: 30px;
    }
    .nav-item {
        font-family: var(--font-heading);
        font-size: 1.0rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        cursor: pointer;
        transition: color 0.3s;
    }
    .nav-item:hover, .nav-item.active {
        color: var(--accent-gold);
        text-decoration: underline;
        text-underline-offset: 5px;
    }
    
    /* Panel Containers (Neo-Classical) */
    .panel-container {
        background-color: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: 4px;
        padding: 0;
        height: 100%;
        position: relative;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .panel-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        padding: 10px 15px;
        border-bottom: 1px solid var(--border-color);
        font-family: var(--font-heading);
        color: var(--accent-gold);
        font-size: 1.1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .panel-content {
        padding: 15px;
    }
    
    /* Roster Item */
    .roster-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px;
        border-bottom: 1px solid #334155;
        cursor: pointer;
        transition: background 0.2s;
    }
    .roster-item:hover { background-color: #334155; }
    .roster-item.active { background-color: rgba(212, 175, 55, 0.1); border-left: 3px solid var(--accent-gold); }
    
    /* Profile Header */
    .profile-header {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    .profile-img {
        width: 100px;
        height: 100px;
        border: 2px solid var(--accent-gold);
        border-radius: 4px;
        background-color: #000;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
    }
    .profile-info h1 {
        font-family: var(--font-heading);
        color: var(--text-primary);
        margin: 0;
        font-size: 1.8rem;
    }
    .profile-meta {
        font-family: var(--font-mono);
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    /* Metrics Grid */
    .metric-box {
        background-color: #0f172a;
        border: 1px solid #334155;
        padding: 10px;
        margin-bottom: 10px;
    }
    .metric-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        text-transform: uppercase;
    }
    .metric-val {
        font-size: 1.4rem;
        color: var(--accent-gold);
        font-family: var(--font-heading);
    }

    /* Alert Box */
    .alert-box {
        background-color: #334155;
        border-left: 4px solid var(--accent-red);
        padding: 10px;
        margin-top: 15px;
        font-size: 0.9rem;
        color: var(--text-primary);
        font-family: var(--font-mono);
    }

    /* Order Book Styles */
    .order-book-container {
        font-family: var(--font-mono);
        font-size: 0.85rem;
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 4px;
        overflow: hidden;
    }
    .order-book-header {
        display: grid;
        grid-template-columns: 1fr 1fr 1.5fr;
        background-color: #0f172a;
        padding: 8px 10px;
        border-bottom: 1px solid var(--border-dim);
        font-weight: bold;
        color: var(--text-secondary);
        text-transform: uppercase;
    }
    .order-row {
        display: grid;
        grid-template-columns: 1fr 1fr 1.5fr;
        padding: 6px 10px;
        border-bottom: 1px solid #334155;
    }
    .order-row.ask {
        color: var(--accent-red);
    }
    .order-row.bid {
        color: var(--accent-blue);
    }
    .order-row:nth-child(even) {
        background-color: #1e293b;
    }
    .order-row:hover {
        background-color: #334155;
    }

    /* HUD Card for Profiler */
    .hud-card {
        background-color: #0f172a;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        padding: 15px;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

</style>
""", unsafe_allow_html=True)

def load_modules():
    return E26Processor(), SocialSentinel(), TargetingBrain(), AutomatedSurveyHandler()

e26_mod, social_mod, brain_mod, survey_mod = load_modules()

# Initialize AdEngine in Session State for persistence
if 'ad_engine' not in st.session_state:
    st.session_state.ad_engine = AdEngine()
ad_mod = st.session_state.ad_engine

# --- CONFIGURATION & CONSTANTS ---
candidate_options = [
    "MARIA FERNANDA CABAL",
    "CARLOS HUMBERTO GARCIA",
    "JOSE LUIS NOREÑA",
    "ANDERSON DUQUE",
    "CENTRO DEMOCRATICO",
    "CANDIDATO 1"
]

# --- SESSION STATE ---
if 'selected_candidate' not in st.session_state:
    st.session_state.selected_candidate = candidate_options[0]
if 'is_demo' not in st.session_state:
    st.session_state.is_demo = True
if 'crm_file' not in st.session_state:
    st.session_state.crm_file = None
if 'logistics_route' not in st.session_state:
    st.session_state.logistics_route = []
if 'strategic_points' not in st.session_state:
    st.session_state.strategic_points = []

# --- TOP NAVIGATION (CUSTOM HTML) ---
st.markdown("""
<div class="top-nav">
    <div class="nav-brand">
        <img src="app/static/logo.png" style="height: 40px;"> <!-- Placeholder for Streamlit image serving -->
        <span>TAYLLERAND OS v3.5</span>
    </div>
    <div class="nav-links">
        <span class="nav-item active">TABLERO</span>
        <span class="nav-item">CAMPAÑAS</span>
        <span class="nav-item">CANDIDATOS</span>
        <span class="nav-item">ANÁLISIS</span>
        <span class="nav-item">AJUSTES</span>
    </div>
    <div class="nav-user" style="color: var(--accent-gold); font-family: var(--font-heading);">
        <span style="font-size: 1.2rem;">👤</span> A. TALLEYRAND
    </div>
</div>
""", unsafe_allow_html=True)

# --- LAYOUT: 3 COLUMNS (ROSTER | PROFILE | METRICS) ---
col_roster, col_profile, col_metrics = st.columns([1, 2, 2])

# --- COLUMN 1: CANDIDATE ROSTER ---
with col_roster:
    st.markdown("""
    <div class="panel-container">
        <div class="panel-header">
            <span>ROSTER DE CANDIDATOS</span>
            <span>▼</span>
        </div>
        <div class="panel-content" style="padding: 0;">
    """, unsafe_allow_html=True)
    
    # Selection Logic (Simulated Roster)
    selected_candidate = st.radio("Seleccionar Candidato", candidate_options, label_visibility="collapsed", key="roster_selection")
    st.session_state.selected_candidate = selected_candidate
    
    # Render Roster Items (Visual Only - Selection handled by radio above for functionality)
    # In a real app, these would be clickable divs triggering state changes
    st.markdown("</div></div>", unsafe_allow_html=True)

# --- DATA PROCESSING ---
specific_targets = list(set([st.session_state.selected_candidate] + candidate_options))
# Load Demo Data
raw_df = e26_mod.load_demo_data()
df_history = e26_mod.process_data(raw_df, specific_targets)
df_social = social_mod.generate_verified_feed()
synthesized_data = brain_mod.synthesize(df_history, df_social)

# Metrics Calculation
target_col = f"Votos_{st.session_state.selected_candidate.replace(' ', '_')}"
total_votes = int(df_history[target_col].sum()) if target_col in df_history.columns else 0
social_vol = len(df_social)
growth_zones = len(synthesized_data[synthesized_data['growth_potential'] > 0.7]) if 'growth_potential' in synthesized_data.columns else 0

# --- COLUMN 2: CANDIDATE PROFILE ---
with col_profile:
    st.markdown(f"""
    <div class="panel-container">
        <div class="panel-header">
            <span>PERFIL</span>
            <span style="font-size: 0.8rem; color: #22c55e;">● CAMPAÑA ACTIVA</span>
        </div>
        <div class="panel-content">
            <div class="profile-header">
                <div class="profile-img">🦅</div>
                <div class="profile-info">
                    <h1>{st.session_state.selected_candidate}</h1>
                    <div class="profile-meta">
                        PARTIDO: CENTRO DEMOCRATICO<br>
                        DISTRITO: ANTIOQUIA / MEDELLÍN<br>
                        ESTADO: INCUMBENTE / RETADOR
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 20px;">
                <h3 style="font-family: var(--font-heading); color: var(--accent-gold); border-bottom: 1px solid #334155;">CAPITAL POLÍTICO</h3>
                <div style="background: #0f172a; height: 20px; border: 1px solid #334155; margin-top: 10px; position: relative;">
                    <div style="background: linear-gradient(90deg, #d4af37, #f59e0b); width: 78%; height: 100%;"></div>
                    <span style="position: absolute; right: 5px; top: -2px; font-size: 0.8rem; color: #fff;">78% - ALTO</span>
                </div>
            </div>
            
            <div style="margin-top: 20px;">
                <h3 style="font-family: var(--font-heading); color: var(--accent-gold); border-bottom: 1px solid #334155;">RESUMEN DE PLATAFORMA</h3>
                <div style="margin-top: 10px; font-size: 0.9rem; color: var(--text-primary);">
                    <p><strong>🛡️ SEGURIDAD PRIMERO:</strong> Estrategia integral para seguridad urbana y control territorial.</p>
                    <p><strong>📈 LIBERTAD ECONÓMICA:</strong> Reducción de carga fiscal para estimular el crecimiento de PYMES.</p>
                    <p><strong>👪 VALORES DE FAMILIA:</strong> Protección de estructuras tradicionales y libertad educativa.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- COLUMN 3: CAMPAIGN METRICS & MAP ---
with col_metrics:
    # Top Row: Metrics
    st.markdown("""
    <div class="panel-container" style="margin-bottom: 20px;">
        <div class="panel-header">
            <span>MÉTRICAS DE RENDIMIENTO</span>
            <span>Últimas 24h</span>
        </div>
        <div class="panel-content">
    """, unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">VOTOS PROYECTADOS</div>
            <div class="metric-val">{total_votes:,}</div>
            <div style="color: #22c55e; font-size: 0.8rem;">▲ 1.2%</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">VOLUMEN SOCIAL</div>
            <div class="metric-val">{social_vol}</div>
            <div style="color: #22c55e; font-size: 0.8rem;">▲ 5.4%</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">ZONAS CRECIMIENTO</div>
            <div class="metric-val">{growth_zones}</div>
            <div style="color: #f59e0b; font-size: 0.8rem;">● ESTABLE</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Bottom Row: Map (Mini)
    st.markdown("""
    <div class="panel-container">
        <div class="panel-header">
            <span>INTELIGENCIA GEOSPACIAL</span>
            <span>EN VIVO</span>
        </div>
        <div class="panel-content" style="padding: 0;">
    """, unsafe_allow_html=True)
    
    # Simple Map Render
    m = folium.Map(location=[6.2442, -75.5812], zoom_start=11, tiles="CartoDB dark_matter")
    # Add Heatmap if data exists
    if target_col in synthesized_data.columns:
        heat_df = synthesized_data[synthesized_data[target_col] > 0]
        heat_data = heat_df[['lat', 'lon', target_col]].values.tolist()
        HeatMap(heat_data, radius=20, blur=15, gradient={0.4: '#1e3a8a', 0.7: '#3b82f6', 1.0: '#d4af37'}).add_to(m)
    
    st_folium(m, width=700, height=300, returned_objects=[])
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# --- MULTI-WINDOW INTERFACE (TABS) ---
tab_map, tab_sim, tab_control, tab_social, tab_crm, tab_ads = st.tabs(["🗺️ OPS GEOSPACIALES", "🔮 PLATAFORMA SIMULACIÓN", "🎛️ SALA DE CONTROL", "📡 INTEL SOCIAL", "👥 OPS DE CAMPO", "📢 EJECUCIÓN PUBLICITARIA"])

with tab_map:
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
                    st.session_state.strategic_points = brain_mod.identify_strategic_points(synthesized_data)
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

with tab_sim:
    # --- SIMULATION DECK ---
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>CRECIMIENTO COMPARATIVO</span>
                <span>Fx 11</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        synthesized_data = brain_mod.calculate_comparative_growth(synthesized_data)
        st.line_chart(synthesized_data.set_index('Puesto')['growth_velocity'].head(20))
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="panel-container" style="margin-top: 20px;">
            <div class="panel-header">
                <span>SIMULACIÓN GEMELO DIGITAL</span>
                <span>Fx 13</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        synthesized_data = brain_mod.run_digital_twin(synthesized_data)
        st.bar_chart(synthesized_data['win_probability'].head(10))
        st.markdown("</div></div>", unsafe_allow_html=True)

    with sim_col2:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>CONSTRUCTOR DE COALICIÓN</span>
                <span>Fx 19</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        synthesized_data = brain_mod.build_coalition(synthesized_data)
        st.metric("Impulso Coalición", "+15%", "Votos")
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="panel-container" style="margin-top: 20px;">
            <div class="panel-header">
                <span>CAMINO A LA VICTORIA</span>
                <span>Fx 20</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        victory_path = brain_mod.generate_victory_path(synthesized_data)
        st.dataframe(victory_path, use_container_width=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

with tab_control:
    # --- CONTROL ROOM ---
    c_col1, c_col2, c_col3 = st.columns(3)
    
    with c_col1:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>GENERADOR DE PERSONAS</span>
                <span>Fx 21</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        persona = brain_mod.generate_personas(synthesized_data)
        st.json(persona)
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="panel-container" style="margin-top: 20px;">
            <div class="panel-header">
                <span>SIMULACIÓN BUCLE VIRAL</span>
                <span>Fx 22</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        viral_data = brain_mod.simulate_viral_loop()
        st.line_chart(viral_data.set_index('Día'))
        st.markdown("</div></div>", unsafe_allow_html=True)

    with c_col2:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>TASA DE GASTO</span>
                <span>Fx 25</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        budget_data = brain_mod.forecast_budget_burn()
        st.area_chart(budget_data.set_index('Semana')['Gasto'])
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="panel-container" style="margin-top: 20px;">
            <div class="panel-header">
                <span>GAMIFICACIÓN GOTV</span>
                <span>Fx 26</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        gotv_data = brain_mod.gamify_gotv()
        st.dataframe(gotv_data, use_container_width=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with c_col3:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>INTELIGENCIA OPOSICIÓN</span>
                <span>Fx 24</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        opp_data = brain_mod.get_opposition_intel()
        st.table(opp_data)
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="panel-container" style="margin-top: 20px;">
            <div class="panel-header">
                <span>IMPACTO CLIMÁTICO</span>
                <span>Fx 27</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        weather = brain_mod.correlate_weather()
        st.metric("Pronóstico", weather['Pronóstico'], weather['Impacto Participación'])
        st.markdown("</div></div>", unsafe_allow_html=True)

with tab_social:
    # --- SOCIAL INTELLIGENCE ---
    col_feed, col_profile, col_designer = st.columns([1.5, 1, 1])
    
    # 1. FEED & LISTENER (ORDER BOOK STYLE)
    with col_feed:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>LIBRO DE ÓRDENES (SENTIMIENTO)</span>
                <span>EN VIVO</span>
            </div>
            <div class="panel-content" style="padding: 0;">
        """, unsafe_allow_html=True)
        
        # Filters
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            active_affinity = st.multiselect("AFINIDAD", social_mod.affinities, default=["URIBISMO", "GENERAL"])
        with f_col2:
            active_topic = st.multiselect("TEMA", social_mod.topics, default=["SEGURIDAD", "CAMPAÑA"])
            
        # API Configuration (New)
        with st.expander("⚙️ CONFIGURACIÓN DE FUENTE DE DATOS"):
            st.markdown("##### CONECTORES API (BETA)")
            data_mode = st.radio("MODO DE OPERACIÓN", ["SIMULACIÓN (Sintético)", "EN VIVO (API)"], horizontal=True)
            
            if data_mode == "EN VIVO (API)":
                social_mod.set_mode("LIVE")
                c_x, c_meta, c_tiktok = st.columns(3)
                with c_x:
                    x_key = st.text_input("X Bearer Token", type="password", help="API v2 Bearer Token")
                with c_meta:
                    meta_key = st.text_input("Meta Access Token", type="password", help="Graph API Token")
                with c_tiktok:
                    tiktok_key = st.text_input("TikTok Access Token", type="password", help="Research API Token")
                
                if st.button("ACTUALIZAR CREDENCIALES"):
                    social_mod.set_api_keys(x_key, meta_key, tiktok_key)
                    st.success("Credenciales actualizadas. Intentando conexión...")
            else:
                social_mod.set_mode("SIMULATION")
            
        # Fetch Data
        feed_data = social_mod.listen(affinity_filter=active_affinity, topic_filter=active_topic)
        
        # Order Book Visualization
        with st.container(height=600):
            if feed_data.empty:
                st.info("Sin datos de mercado.")
            else:
                st.markdown("""
                <div class="order-book-container">
                    <div class="order-book-header" style="grid-template-columns: 0.5fr 1fr 0.8fr 3fr 0.5fr;">
                        <span>PLAT</span>
                        <span>SENTIMIENTO</span>
                        <span>IMPACTO</span>
                        <span>CONTENIDO (EXTRACTO)</span>
                        <span>ACCIÓN</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Split into Asks (Negative) and Bids (Positive)
                asks = feed_data[feed_data['sentiment'] < 0].sort_values('sentiment', ascending=True)
                bids = feed_data[feed_data['sentiment'] >= 0].sort_values('sentiment', ascending=False)
                
                def render_row(row, type_class):
                    # Platform Icon Logic
                    plat_icon = "🌐"
                    if "twitter" in row.get('url', ''): plat_icon = "🐦" # X
                    elif "facebook" in row.get('url', ''): plat_icon = "📘" # Meta
                    elif "tiktok" in row.get('url', ''): plat_icon = "🎵" # TikTok
                    
                    # Content Truncation
                    content = row.get('text', '')
                    if len(content) > 60: content = content[:60] + "..."
                    
                    return f"""
                    <div class="order-row {type_class}" style="grid-template-columns: 0.5fr 1fr 0.8fr 3fr 0.5fr; align-items: center;">
                        <span style="font-size: 1.2rem;">{plat_icon}</span>
                        <span style="font-weight: bold;">{row['sentiment']:.2f}</span>
                        <span>{row.get('influence_score', 0)}</span>
                        <span style="color: var(--text-secondary); font-style: italic; font-size: 0.8rem;">"{content}"</span>
                        <a href="{row.get('url', '#')}" target="_blank" style="text-decoration: none; color: var(--accent-gold); font-size: 0.8rem; border: 1px solid var(--accent-gold); padding: 2px 5px; border-radius: 3px;">VER</a>
                    </div>
                    """

                # Render Asks (Red - Top)
                for _, row in asks.iterrows():
                    st.markdown(render_row(row, "ask"), unsafe_allow_html=True)
                    
                # Spread / Current Price
                avg_sentiment = feed_data['sentiment'].mean()
                price_color = "var(--accent-blue)" if avg_sentiment >= 0 else "var(--accent-red)"
                st.markdown(f"""
                <div style="padding: 10px; text-align: center; font-family: var(--font-mono); font-size: 16px; font-weight: bold; color: {price_color}; border-top: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color); background: var(--bg-color);">
                    {avg_sentiment:.4f} INDEX (AVG)
                </div>
                """, unsafe_allow_html=True)
                
                # Render Bids (Green - Bottom)
                for _, row in bids.iterrows():
                    st.markdown(render_row(row, "bid"), unsafe_allow_html=True)
                    
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    # 2. VOTER PROFILER
    with col_profile:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>PERFILADOR DE VOTANTES (KYC)</span>
                <span>OBJETIVO</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        
        # User Selection (Simulated from Feed)
        if not feed_data.empty:
            selected_user_id = st.selectbox("SELECCIONAR USUARIO", feed_data['user_id'].unique())
            
            if selected_user_id:
                profile = social_mod.generate_voter_profile(selected_user_id)
                
                # Profile Card (Electoral Command Style)
                st.markdown(f"""
                <div class="hud-card">
                    <div style="text-align: center; margin-bottom: 15px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px;">
                        <div style="font-size: 1.2rem; font-weight: 700; color: var(--text-primary);">{profile['Nombre']}</div>
                        <div style="color: var(--text-secondary); font-family: var(--font-mono); font-size: 0.8rem;">ID: {profile['ID Usuario']}</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.85rem; font-family: var(--font-mono);">
                        <div><span style="color:var(--text-secondary);">AFINIDAD</span><br><span style="color:var(--text-primary);">{profile['Afinidad']}</span></div>
                        <div><span style="color:var(--text-secondary);">SCORE</span><br><span style="color:var(--accent-gold);">{profile['Puntaje Influencia']}/100</span></div>
                        <div><span style="color:var(--text-secondary);">GUSTOS</span><br><span style="color:var(--text-primary);">{profile['Gusto Político']}</span></div>
                        <div><span style="color:var(--text-secondary);">EDAD</span><br><span style="color:var(--text-primary);">{profile['Grupo Edad']}</span></div>
                    </div>
                    <div style="margin-top: 15px;">
                        <span style="color:var(--text-secondary); font-size: 0.8rem;">INTERESES</span>
                        <div style="margin-top: 5px; display: flex; flex-wrap: wrap; gap: 5px;">
                            {''.join([f'<span style="background:var(--surface-color); color:var(--text-primary); padding:2px 6px; border-radius:2px; font-size:0.75rem;">{i}</span>' for i in profile['Intereses'].split(', ')])}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action Buttons
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    st.button("RECLUTAR (LONG)", key="btn_long", use_container_width=True)
                with c2:
                    st.button("NEUTRALIZAR (SHORT)", key="btn_short", use_container_width=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    # 3. MESSAGE DESIGNER
    with col_designer:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>SIMULADOR DE MENSAJES</span>
                <span>PRUEBA</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        
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
        st.markdown("</div></div>", unsafe_allow_html=True)

with tab_crm:
    # --- FIELD OPERATIONS ---
    
    # Initialize survey handler
    survey_mod = AutomatedSurveyHandler()
    
    # Load or generate contacts
    crm_file = st.session_state.crm_file
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
    strategic_points = st.session_state.strategic_points
    prioritized_contacts = survey_mod.prioritize_contacts(crm_df, strategic_zones=strategic_points)
    
    # Controls
    st.markdown("""
    <div class="panel-container" style="margin-bottom: 20px;">
        <div class="panel-header">
            <span>FILTROS OPS DE CAMPO</span>
            <span>CRM</span>
        </div>
        <div class="panel-content">
    """, unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns([1, 1, 2])
    
    with col_f1:
        tier_filter = st.multiselect(
            "NIVEL PRIORIDAD",
            ["ALTA", "MEDIA", "BAJA"],
            default=["ALTA", "MEDIA"]
        )
    
    with col_f2:
        min_affinity = st.slider("AFINIDAD MÍNIMA", 0, 100, 0, 5)
    
    with col_f3:
        st.metric("CONTACTOS TOTALES", len(prioritized_contacts))
        st.metric("ALTA PRIORIDAD", len(prioritized_contacts[prioritized_contacts['priority_tier'] == 'ALTA']))
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Filter based on controls
    filtered_contacts = prioritized_contacts[
        (prioritized_contacts['priority_tier'].isin(tier_filter)) &
        (prioritized_contacts['afinidad_score'] >= min_affinity)
    ]
    
    # Two-column layout: Map + Contact Table
    col_map_f, col_table_f = st.columns([2, 1])
    
    with col_map_f:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>MAPA DE CONTACTOS</span>
                <span>GPS</span>
            </div>
            <div class="panel-content" style="padding: 0;">
        """, unsafe_allow_html=True)
        
        # Create map
        m_contacts = folium.Map(location=[6.2442, -75.5812], zoom_start=12, tiles="CartoDB dark_matter")
        Fullscreen().add_to(m_contacts)
        
        # Color coding by priority tier
        tier_colors = {
            "ALTA": "#22c55e",
            "MEDIA": "#f59e0b",
            "BAJA": "#64748b"
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
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col_table_f:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>LISTA DE PRIORIDAD</span>
                <span>MARCADOR</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        
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
        st.markdown("</div></div>", unsafe_allow_html=True)

with tab_ads:
    # --- ADVERTISING EXECUTION PANEL ---
    col_ad_config, col_ad_perf = st.columns([1, 2])
    
    with col_ad_config:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>CONFIGURACIÓN DE CAMPAÑA</span>
                <span>META API</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        
        # 1. Select Persona
        st.markdown("#### 🎯 OBJETIVO (MICRO-SEGMENTO)")
        # Get persona from Brain
        default_persona = brain_mod.generate_personas(synthesized_data)
        persona_name = st.text_input("Nombre Segmento", value=default_persona.get("Persona", "Votante General"))
        
        # Audience Estimation
        audience_est = ad_mod.estimate_audience_size(default_persona)
        st.metric("Alcance Potencial", f"{audience_est['potential_reach']:,}", "Personas")
        
        st.markdown("---")
        
        # 2. Budget & Channels
        st.markdown("#### 💰 PRESUPUESTO Y CANALES")
        budget = st.slider("Presupuesto Diario (COP)", 100000, 5000000, 500000, step=50000)
        channels = st.multiselect("Canales de Distribución", ad_mod.channels, default=["Facebook", "Instagram"])
        
        st.markdown("---")
        
        # 3. Creative Preview
        st.markdown("#### 🎨 CREATIVOS GENERADOS")
        creatives = ad_mod.generate_ad_creatives(default_persona)
        selected_creative = st.selectbox("Seleccionar Variación", [c['headline'] for c in creatives])
        
        # Find selected creative dict
        creative_obj = next((c for c in creatives if c['headline'] == selected_creative), creatives[0])
        st.info(f"📄 **Copy**: {creative_obj['body']}")
        
        if st.button("🚀 LANZAR CAMPAÑA", use_container_width=True):
            with st.spinner("Conectando con Meta Ads Manager..."):
                time.sleep(1.5) # Simulating API call
                res = ad_mod.launch_campaign(f"CMP-{persona_name}", default_persona, budget, channels)
                st.success(f"Campaña {res['id']} Activada Exitosamente")
                st.rerun()
                
        st.markdown("</div></div>", unsafe_allow_html=True)
        
    with col_ad_perf:
        st.markdown("""
        <div class="panel-container">
            <div class="panel-header">
                <span>RENDIMIENTO EN VIVO</span>
                <span>DASHBOARD</span>
            </div>
            <div class="panel-content">
        """, unsafe_allow_html=True)
        
        # Metrics Overview
        active_df = ad_mod.get_active_campaigns_df()
        
        if not active_df.empty:
            # Aggregate Metrics
            total_spend = active_df["Inversión"].apply(lambda x: int(x.replace('$','').replace(',',''))).sum()
            total_clicks = active_df["Clicks"].apply(lambda x: int(x.replace(',',''))).sum()
            total_conv = active_df["Conversiones"].sum()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Inversión Total", f"${total_spend:,}")
            m2.metric("Clicks Totales", f"{total_clicks:,}")
            m3.metric("Conversiones (Leads)", f"{total_conv:,}")
            
            st.markdown("### 📋 CAMPAÑAS ACTIVAS")
            st.dataframe(active_df, use_container_width=True)
            
            st.markdown("### 📈 ANÁLISIS DE RENDIMIENTO")
            # Simple chart if data exists
            if total_clicks > 0:
                chart_data = pd.DataFrame({
                    "Campaña": active_df["Campaña"],
                    "Clicks": active_df["Clicks"].apply(lambda x: int(x.replace(',','')))
                })
                st.bar_chart(chart_data.set_index("Campaña"))
                
        else:
            st.info("No hay campañas activas. Inicie una campaña en el panel de configuración.")
            
            # Placeholder for visual appeal
            st.markdown("""
            <div style="text-align: center; padding: 50px; color: #64748b;">
                <h1>📡</h1>
                <p>ESPERANDO SEÑAL DE SATÉLITE...</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<center style='font-family: Cinzel; color: #64748b; font-size: 0.8rem;'>TAYLLERAND OS | EST. 2025 | SISTEMA CLASIFICADO</center>", unsafe_allow_html=True)
