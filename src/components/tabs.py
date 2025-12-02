import streamlit as st
import pandas as pd

def render_simulation_tab(synthesized_data, brain_mod):
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

def render_control_tab(synthesized_data, brain_mod):
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
