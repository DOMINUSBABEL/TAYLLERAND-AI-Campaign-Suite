import streamlit as st

def setup_page():
    st.set_page_config(
        page_title="TAYLLERAND | SIGLO XXIII",
        page_icon="🦅",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_css():
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

def render_header():
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
