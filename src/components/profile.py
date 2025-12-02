import streamlit as st

def render_profile(selected_candidate):
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
                    <h1>{selected_candidate}</h1>
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
            
            {render_platform_card()}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_platform_card():
    platform_items = [
        {"icon": "🛡️", "label": "SEGURIDAD PRIMERO", "desc": "Estrategia integral para seguridad urbana y control territorial."},
        {"icon": "📈", "label": "LIBERTAD ECONÓMICA", "desc": "Reducción de carga fiscal para estimular el crecimiento de PYMES."},
        {"icon": "👪", "label": "VALORES DE FAMILIA", "desc": "Protección de estructuras tradicionales y libertad educativa."}
    ]
    
    html_items = ""
    for item in platform_items:
        html_items += f'<p><strong>{item["icon"]} {item["label"]}:</strong> {item["desc"]}</p>'
        
    return f"""
    <div style="margin-top: 20px;">
        <h3 style="font-family: var(--font-heading); color: var(--accent-gold); border-bottom: 1px solid #334155;">RESUMEN DE PLATAFORMA</h3>
        <div style="margin-top: 10px; font-size: 0.9rem; color: var(--text-primary);">
            {html_items}
        </div>
    </div>
    """
