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

# --- SCI-FI / CYBERPUNK UI THEME & ANIMATIONS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;500;700&family=Share+Tech+Mono&display=swap');

    /* ANIMATIONS */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideInLeft {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 5px #00f2ff; }
        50% { box-shadow: 0 0 20px #00f2ff; }
        100% { box-shadow: 0 0 5px #00f2ff; }
    }

    /* GLOBAL THEME */
    .stApp {
        background-color: #02040a; /* Deep Space Black */
        color: #e0fbfc;
        font-family: 'Rajdhani', sans-serif;
    }

    /* HEADERS */
    h1, h2, h3 {
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #00f2ff; /* Neon Cyan */
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #050a14;
        border-right: 1px solid #1e3a8a;
        box-shadow: 5px 0 15px rgba(0, 242, 255, 0.1);
    }
    
    /* METRIC CARDS (HUD STYLE) */
    .hud-card {
        background: rgba(10, 20, 40, 0.7);
        border: 1px solid #00f2ff;
        border-left: 4px solid #00f2ff;
        border-radius: 0px; /* Sharp edges */
        padding: 15px;
        margin-bottom: 10px;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
        animation: fadeIn 1s ease-in-out;
    }
    .hud-card:hover {
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
        transform: translateX(5px);
        border-color: #fff;
    }
    .hud-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .hud-value {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    
    /* WARNING / ALERT BOX */
    .alert-box {
        background: rgba(220, 38, 38, 0.1);
        border: 1px solid #ef4444;
        color: #fca5a5;
        padding: 10px;
        font-family: 'Share Tech Mono', monospace;
        border-left: 4px solid #ef4444;
        animation: pulseGlow 2s infinite;
    }

    /* DATAFRAME STYLING */
    [data-testid="stDataFrame"] {
        border: 1px solid #1e3a8a;
        border-radius: 0px;
    }
    
    /* BUTTONS */
    .stButton button {
        background-color: transparent;
        border: 1px solid #00f2ff;
        color: #00f2ff;
        font-family: 'Share Tech Mono', monospace;
        text-transform: uppercase;
        border-radius: 0px;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #00f2ff;
        color: #000;
        box-shadow: 0 0 20px #00f2ff;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: 1px solid #1e3a8a;
        color: #94a3b8;
        border-radius: 0px;
        padding: 10px 20px;
        transition: all 0.3s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(0, 242, 255, 0.05);
        color: #fff;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: rgba(0, 242, 255, 0.1);
        border-color: #00f2ff;
        color: #00f2ff;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
    }

</style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
def load_modules():
    return E26Processor(), SocialSentinel(), TargetingBrain()

e26_mod, social_mod, brain_mod = load_modules()

# --- SIDEBAR: COMMAND DECK ---
with st.sidebar:
    st.markdown("## 🦅 TAYLLERAND_OS `v3.0`")
    st.markdown("<div style='font-family: Share Tech Mono; color: #00f2ff; font-size: 0.8rem;'>SYSTEM ONLINE // WAITING FOR INPUT</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 📂 DATA LINK")
    uploaded_file = st.file_uploader("E-26 DATA STREAM", type=["csv"])
    crm_file = st.file_uploader("CRM UPLINK (Líderes)", type=["csv"])
    
    st.markdown("---")
    st.markdown("### 🎯 TARGET LOCK")
    
    # Fixed: Use Selectbox with candidates actually in the data
    target_candidate = st.selectbox("SELECT CANDIDATE", ["GUSTAVO PETRO", "FEDERICO GUTIERREZ", "MARIA FERNANDA CABAL"])
    
    st.markdown("---")
    st.markdown("### 🎚️ STRATEGIC PARAMETERS")
    
    w_security = st.slider("SECURITY WEIGHT", 0.5, 2.0, 1.0, 0.1)
    w_opinion = st.slider("OPINION WEIGHT", 0.5, 2.0, 1.0, 0.1)
    w_growth = st.slider("GROWTH FACTOR", 0.5, 2.0, 1.0, 0.1)
    turnout_factor = st.slider("TURNOUT SIM (Fx 5)", 0.5, 1.5, 1.0, 0.1)
    
    weights = {
        'security': w_security,
        'opinion': w_opinion,
        'growth': w_growth
    }
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; font-family: Share Tech Mono; color: #475569;'>SECURE CONNECTION ESTABLISHED</div>", unsafe_allow_html=True)

# --- DATA PROCESSING ENGINE ---
# 1. Load Real Data (or Demo)
if uploaded_file:
    raw_df = e26_mod.load_data_from_csv(uploaded_file)
    df_history = e26_mod.process_data(raw_df, target_candidate)
    data_source_label = "OFFICIAL UPLOAD"
    is_demo = False
else:
    # Load High-Fidelity Preload by default
    raw_df = e26_mod.load_demo_data()
    df_history = e26_mod.process_data(raw_df, target_candidate)
    data_source_label = "PRELOADED OFFICIAL"
    is_demo = True

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
st.markdown(f"# 📊 CAMPAIGN INTELLIGENCE // <span style='color:#00f2ff'>{target_candidate}</span>", unsafe_allow_html=True)

# Function 9: Campaign Brief (Collapsible)
with st.expander("📄 OFFICIAL CAMPAIGN BRIEF (Function 9)", expanded=False):
    st.markdown(campaign_brief)

# --- HUD METRICS ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# Use Projected Votes if Turnout != 1.0
total_votes = synthesized_data['Votos_Projected'].sum() if not synthesized_data.empty else 0
social_vol = len(df_social)
points_count = len(strategic_points)
growth_zones = len([p for p in strategic_points if p['type'] == 'GROWTH'])

with kpi1:
    st.markdown(f"""<div class="hud-card"><div class="hud-label">PROJECTED VOTES</div><div class="hud-value">{total_votes:,}</div></div>""", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"""<div class="hud-card"><div class="hud-label">NEWS MENTIONS</div><div class="hud-value">{social_vol}</div></div>""", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"""<div class="hud-card"><div class="hud-label">GROWTH ZONES</div><div class="hud-value">{growth_zones}</div></div>""", unsafe_allow_html=True)
with kpi4:
    st.markdown(f"""<div class="hud-card"><div class="hud-label">DATA SOURCE</div><div class="hud-value" style="font-size: 1.5rem;">{data_source_label}</div></div>""", unsafe_allow_html=True)

# --- MULTI-WINDOW INTERFACE (TABS) ---
tab_map, tab_sim, tab_control, tab_social, tab_crm = st.tabs(["🗺️ GEOSPATIAL OPS", "🔮 SIMULATION DECK", "🎛️ CONTROL ROOM", "📡 SOCIAL INTEL", "👥 FIELD OPS"])

with tab_map:
    st.markdown("### 🗺️ GEOSPATIAL STRATEGY DECK")

    col_map, col_controls = st.columns([3, 1])

    with col_controls:
        st.markdown("#### 📡 LAYER CONTROL")
        layer_select = st.radio("ACTIVE LAYER", [
            "Vote Density (Consolidation)", 
            "Growth Potential (Expansion)", 
            "Strategy Matrix (Quadrants)",
            "Voter Elasticity (Swing Zones)",
            "Sentiment Heatmap (Social)",
            "Logistics Route (TSP)",
            "Crisis Heatmap (Fx 16)",
            "Donor Propensity (Fx 29)"
        ])
        
        st.markdown("#### ⚠️ ALERTS")
        if is_demo:
            st.markdown("""<div class="alert-box">DEMO MODE ACTIVE<br>Using Reconstructed Data</div>""", unsafe_allow_html=True)
        if synthesized_data.empty:
            st.markdown("""<div class="alert-box">NO DATA DETECTED<br>Check Candidate Selection</div>""", unsafe_allow_html=True)

    with col_map:
        # MAP RENDERING LOGIC (ROBUST)
        m = folium.Map(location=[6.2442, -75.5812], zoom_start=12, tiles="CartoDB dark_matter")
        Fullscreen().add_to(m)
        
        if not synthesized_data.empty:
            
            if layer_select == "Vote Density (Consolidation)":
                # Blue Heatmap for Votes
                heat_data = synthesized_data[['lat', 'lon', 'historical_strength']].values.tolist()
                HeatMap(heat_data, radius=25, blur=15, gradient={0.4: '#1e3a8a', 0.7: '#3b82f6', 1.0: '#93c5fd'}, name="Votes").add_to(m)
                
                # Vote Bubbles
                for _, row in synthesized_data.iterrows():
                    if row['historical_strength'] > 0:
                        folium.CircleMarker(
                            location=[row['lat'], row['lon']],
                            radius=row['historical_strength'] / 10 + 2,
                            color='#3b82f6',
                            fill=True,
                            fill_opacity=0.6,
                            weight=1,
                            popup=f"{row['Puesto']}: {row['Votos']} votes"
                        ).add_to(m)
                        
            elif layer_select == "Growth Potential (Expansion)":
                # Red Heatmap for Growth
                if 'growth_potential' in synthesized_data.columns:
                    growth_data = synthesized_data[['lat', 'lon', 'growth_potential']].values.tolist()
                    HeatMap(growth_data, radius=25, blur=15, gradient={0.4: '#7f1d1d', 0.7: '#dc2626', 1.0: '#fca5a5'}, name="Growth").add_to(m)
            
            elif layer_select == "Strategy Matrix (Quadrants)":
                # Color-coded markers
                colors = {'STRONGHOLD': '#22c55e', 'BATTLEGROUND': '#f59e0b', 'OPPORTUNITY': '#ef4444', 'OBSERVATION': '#64748b'}
                for _, row in synthesized_data.iterrows():
                    strat = row.get('strategy_class', 'OBSERVATION')
                    folium.CircleMarker(
                        location=[row['lat'], row['lon']],
                        radius=6,
                        color=colors.get(strat, 'gray'),
                        fill=True,
                        fill_opacity=0.9,
                        popup=f"<b>{row['Puesto']}</b><br>Strategy: {strat}<br>Votes: {row['Votos']}"
                    ).add_to(m)

            elif layer_select == "Voter Elasticity (Swing Zones)":
                # Purple Heatmap
                if 'elasticity' in synthesized_data.columns:
                    elasticity_data = synthesized_data[['lat', 'lon', 'elasticity']].values.tolist()
                    HeatMap(elasticity_data, radius=30, blur=20, gradient={0.4: '#581c87', 0.7: '#a855f7', 1.0: '#e9d5ff'}, name="Elasticity").add_to(m)

            elif layer_select == "Sentiment Heatmap (Social)":
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
                                popup=f"Sentiment Score: {row['sentiment_score']}"
                            ).add_to(m)
                            
            elif layer_select == "Logistics Route (TSP)":
                # Function 8: Draw Route
                if logistics_route:
                    points = [[p['lat'], p['lon']] for p in logistics_route]
                    folium.PolyLine(points, color="#00f2ff", weight=5, opacity=0.9, dash_array='10').add_to(m)
                    for p in logistics_route:
                        folium.Marker(
                            [p['lat'], p['lon']], 
                            popup=f"STOP {p['order']}: {p['location']}", 
                            icon=folium.Icon(color='blue', icon='road', prefix='fa')
                        ).add_to(m)
            
            elif layer_select == "Crisis Heatmap (Fx 16)":
                # Orange Heatmap
                synthesized_data = brain_mod.generate_crisis_heatmap(synthesized_data)
                crisis_data = synthesized_data[['lat', 'lon', 'crisis_risk']].values.tolist()
                HeatMap(crisis_data, radius=30, blur=20, gradient={0.4: '#f97316', 0.7: '#ea580c', 1.0: '#c2410c'}, name="Crisis").add_to(m)

            elif layer_select == "Donor Propensity (Fx 29)":
                # Gold Heatmap
                synthesized_data = brain_mod.map_donor_propensity(synthesized_data)
                donor_data = synthesized_data[['lat', 'lon', 'donor_score']].values.tolist()
                HeatMap(donor_data, radius=25, blur=15, gradient={0.4: '#facc15', 0.7: '#eab308', 1.0: '#ca8a04'}, name="Donors").add_to(m)

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
                            popup=f"<b>{row['name']}</b><br>Role: {row.get('role', 'N/A')}"
                        ).add_to(m)
                    st.success(f"Loaded {len(df_crm)} CRM contacts.")
                else:
                    st.error("CRM CSV missing columns: lat, lon, name")
            except Exception as e:
                st.error(f"Error loading CRM: {e}")
                
        st_folium(m, width="100%", height=600)

with tab_sim:
    st.markdown("### 🔮 SIMULATION DECK (Functions 11-20)")
    
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        st.markdown("#### 📈 COMPARATIVE GROWTH (Fx 11)")
        synthesized_data = brain_mod.calculate_comparative_growth(synthesized_data)
        st.line_chart(synthesized_data.set_index('Puesto')['growth_velocity'].head(20))
        
        st.markdown("#### 🌪️ DIGITAL TWIN (Fx 13)")
        synthesized_data = brain_mod.run_digital_twin(synthesized_data)
        st.bar_chart(synthesized_data['win_probability'].head(10))

    with sim_col2:
        st.markdown("#### 🤝 COALITION BUILDER (Fx 19)")
        synthesized_data = brain_mod.build_coalition(synthesized_data)
        st.metric("Coalition Boost", "+15%", "Votes")
        
        st.markdown("#### 🏆 VICTORY PATH (Fx 20)")
        victory_path = brain_mod.generate_victory_path(synthesized_data)
        st.dataframe(victory_path, use_container_width=True)

with tab_control:
    st.markdown("### 🎛️ CONTROL ROOM (Functions 21-30)")
    
    c_col1, c_col2, c_col3 = st.columns(3)
    
    with c_col1:
        st.markdown("#### 🎭 PERSONA GEN (Fx 21)")
        persona = brain_mod.generate_personas(synthesized_data)
        st.json(persona)
        
        st.markdown("#### 🦠 VIRAL LOOP (Fx 22)")
        viral_data = brain_mod.simulate_viral_loop()
        st.line_chart(viral_data.set_index('Day'))

    with c_col2:
        st.markdown("#### 💸 BUDGET BURN (Fx 25)")
        budget_data = brain_mod.forecast_budget_burn()
        st.area_chart(budget_data.set_index('Week')['Spend'])
        
        st.markdown("#### 🎮 GOTV GAMIFICATION (Fx 26)")
        gotv_data = brain_mod.gamify_gotv()
        st.dataframe(gotv_data, use_container_width=True)

    with c_col3:
        st.markdown("#### 🕵️ OPPOSITION INTEL (Fx 24)")
        opp_data = brain_mod.get_opposition_intel()
        st.table(opp_data)
        
        st.markdown("#### 🌦️ WEATHER IMPACT (Fx 27)")
        weather = brain_mod.correlate_weather()
        st.metric("Forecast", weather['Forecast'], weather['Turnout Impact'])

with tab_social:
    st.markdown("### 📡 LIVE INTEL FEED")
    with st.container(height=600):
        for _, row in df_social.iterrows():
            st.markdown(f"""
            <div style="border-left: 2px solid #00f2ff; padding-left: 10px; margin-bottom: 15px; background: rgba(0,0,0,0.3); animation: fadeIn 1s ease-in;">
                <div style="color: #00f2ff; font-weight: bold; font-size: 0.9rem;">@{row['user_id']}</div>
                <div style="color: #cbd5e1; font-size: 0.85rem;">{row['text']}</div>
                <div style="font-size: 0.7rem; color: #64748b; margin-top: 5px;">SOURCE: VERIFIED • <a href="{row['url']}" style="color: #3b82f6;">LINK</a></div>
            </div>
            """, unsafe_allow_html=True)

with tab_crm:
    st.markdown("### 👥 FIELD OPERATIONS")
    if crm_file:
        st.dataframe(pd.read_csv(crm_file), use_container_width=True)
    else:
        st.info("Upload CRM Data in Sidebar to Activate Field Ops Module")

# --- FOOTER ---
st.markdown("---")
st.markdown("<center style='font-family: Share Tech Mono; color: #475569; font-size: 0.8rem;'>TAYLLERAND SYSTEM v3.0 | CLASSIFIED | AUTHORIZED EYES ONLY</center>", unsafe_allow_html=True)
