import streamlit as st

def render_roster(candidate_options):
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
    return selected_candidate
