import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

def render_metrics(total_votes, social_vol, growth_zones, synthesized_data, target_col):
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
