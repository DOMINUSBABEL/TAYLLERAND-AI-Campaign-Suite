import streamlit as st
import importlib
from src.services.e26_processor import E26Processor
from src.services.social_sentinel import SocialSentinel
from src.services.targeting_brain import TargetingBrain
from src.services.survey_handler import AutomatedSurveyHandler
from src.services.ad_engine import AdEngine

# Import UI Components
from src.components.layout import setup_page, load_css, render_header
from src.components.roster import render_roster
from src.components.profile import render_profile
from src.components.metrics import render_metrics
from src.components.map import render_map_tab
from src.components.tabs import render_simulation_tab, render_control_tab

from src.components.crm import render_crm
from src.components.ads import render_ads

# --- INITIALIZATION ---
setup_page()
load_css()

def load_modules():
    return E26Processor(), SocialSentinel(), TargetingBrain(), AutomatedSurveyHandler()

e26_mod, social_mod, brain_mod, survey_mod = load_modules()

# Initialize AdEngine in Session State
if 'ad_engine' not in st.session_state:
    st.session_state.ad_engine = AdEngine()
ad_mod = st.session_state.ad_engine

# --- CONFIGURATION & CONSTANTS ---
# EXACT NAMES FROM CSV
candidate_options = [
    "ANDERSON DUQUE MORALES",
    "CARLOS HUMBERTO GARCIA VELASQUEZ",
    "MARIA FERNANDA CABAL", # Keep for demo/fallback
    "JOSE LUIS NOREÑA",
    "CENTRO DEMOCRATICO"
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

# --- RENDER HEADER ---
render_header()

# --- LAYOUT: 3 COLUMNS (ROSTER | PROFILE | METRICS) ---
col_roster, col_profile, col_metrics = st.columns([1, 2, 2])

# --- COLUMN 1: CANDIDATE ROSTER ---
with col_roster:
    selected_candidate = render_roster(candidate_options)

# --- DATA PROCESSING ---
import os
import pandas as pd

# Use candidate_options directly to maintain stable order. 
# Ensure selected_candidate is included if it somehow isn't (unlikely with current logic).
specific_targets = [c for c in candidate_options] 
if st.session_state.selected_candidate not in specific_targets:
    specific_targets.insert(0, st.session_state.selected_candidate)


# Check for Real Data
real_files = ["resultado ANDERSON DUQUE.csv", "resultado carlos humberto garcía .csv"]
found_real_data = False
raw_df = pd.DataFrame()

dfs = []
for f in real_files:
    if os.path.exists(f):
        print(f"Loading real data: {f}")
        df_part = e26_mod.load_raw_e26(f)
        if not df_part.empty:
            dfs.append(df_part)
            found_real_data = True

if found_real_data:
    raw_df = pd.concat(dfs, ignore_index=True)
    st.session_state.is_demo = False
else:
    # Load Demo Data
    raw_df = e26_mod.load_demo_data()
    st.session_state.is_demo = True

df_history = e26_mod.process_data(raw_df, specific_targets)
df_social = social_mod.generate_verified_feed()
synthesized_data = brain_mod.synthesize(df_history, df_social)
synthesized_data = brain_mod.calculate_elasticity(synthesized_data)
synthesized_data = brain_mod.calculate_sentiment_correlation(synthesized_data, df_social)

# Metrics Calculation
target_col = f"Votos_{st.session_state.selected_candidate.replace(' ', '_')}"
total_votes = int(df_history[target_col].sum()) if target_col in df_history.columns else 0
social_vol = len(df_social)
growth_zones = len(synthesized_data[synthesized_data['growth_potential'] > 0.7]) if 'growth_potential' in synthesized_data.columns else 0

# --- COLUMN 2: CANDIDATE PROFILE ---
with col_profile:
    render_profile(st.session_state.selected_candidate)

# --- COLUMN 3: CAMPAIGN METRICS & MAP ---
with col_metrics:
    render_metrics(total_votes, social_vol, growth_zones, synthesized_data, target_col)

# --- MULTI-WINDOW INTERFACE (TABS) ---
tab_map, tab_sim, tab_control, tab_social, tab_crm, tab_ads = st.tabs(["🗺️ OPS GEOSPACIALES", "🔮 PLATAFORMA SIMULACIÓN", "🎛️ SALA DE CONTROL", "📡 INTEL SOCIAL", "👥 OPS DE CAMPO", "📢 EJECUCIÓN PUBLICITARIA"])

with tab_map:
    render_map_tab(synthesized_data, specific_targets, brain_mod)

with tab_sim:
    render_simulation_tab(synthesized_data, brain_mod)

with tab_control:
    render_control_tab(synthesized_data, brain_mod)

with tab_social:
    st.header("INTEL SOCIAL")
    st.dataframe(df_social)

with tab_crm:
    render_crm(survey_mod)

with tab_ads:
    render_ads(ad_mod)
