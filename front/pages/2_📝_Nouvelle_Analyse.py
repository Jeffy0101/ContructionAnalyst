"""Formulaire de saisie + appel API + affichage résultat + bouton PDF."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from style import inject_css, badge, PLOTLY_COLORS, EMERALD
import api_client as api
from pdf_generator import generer_pdf

st.set_page_config(page_title="Nouvelle analyse", page_icon="📝", layout="wide")
inject_css()

if not st.session_state.get('token'):
    st.warning("🔒 Connectez-vous depuis la page principale.")
    st.stop()

st.markdown("# 📝 Nouvelle analyse de terrain")
st.caption("Renseignez les variables ci-dessous. Toutes sont obligatoires pour garantir la qualité de la prédiction.")

with st.form("form_terrain"):
    col1, col2 = st.columns(2)
    with col1:
        nom_terrain = st.text_input("Nom du terrain *", "Parcelle Yaoundé Nord")
    with col2:
        localisation = st.text_input("Localisation", "Yaoundé, Cameroun")

    st.markdown("### 🏔️ Géotechnique")
    g1, g2, g3 = st.columns(3)
    with g1:
        capacite_portante = st.slider("Capacité portante (kPa)", 50, 500, 200)
        pente = st.slider("Pente (%)", 0.0, 45.0, 8.0)
    with g2:
        zone_sismique = st.slider("Zone sismique (1-5)", 1, 5, 2)
        profondeur_nappe = st.slider("Profondeur nappe (m)", 0.0, 30.0, 8.0)
    with g3:
        type_sol_score = st.slider("Type sol (1=argile mou, 5=roche)", 1, 5, 3)

    st.markdown("### 💧 Hydrologie & climat")
    h1, h2, h3 = st.columns(3)
    with h1:
        pluviometrie_annuelle = st.slider("Pluviométrie (mm/an)", 300, 3000, 1400)
        distance_cours_eau = st.slider("Distance cours d'eau (m)", 0, 5000, 800)
    with h2:
        risque_inondation = st.slider("Risque inondation (0-10)", 0.0, 10.0, 3.0)
        qualite_drainage = st.slider("Qualité drainage (1-5)", 1, 5, 3)
    with h3:
        st.empty()

    st.markdown("### 🏙️ Environnement & urbanisme")
    u1, u2, u3 = st.columns(3)
    with u1:
        distance_route = st.slider("Distance route (m)", 0, 5000, 200)
        densite_urbaine = st.slider("Densité urbaine (hab/km²)", 0, 10000, 2500)
    with u2:
        distance_industrie = st.slider("Distance industrie (m)", 0, 10000, 1500)
        couverture_vegetale = st.slider("Couverture végétale (%)", 0, 100, 35)
    with u3:
        altitude = st.slider("Altitude (m)", 0, 3000, 700)
        exposition_vent = st.slider("Exposition vent (1-5)", 1, 5, 2)

    submit = st.form_submit_button("🔬 Analyser le terrain", use_container_width=True)

if submit:
    donnees = {
        'capacite_portante': capacite_portante, 'pente': pente,
        'zone_sismique': zone_sismique, 'profondeur_nappe': profondeur_nappe,
        'type_sol_score': type_sol_score,
        'pluviometrie_annuelle': pluviometrie_annuelle,
        'distance_cours_eau': distance_cours_eau,
        'risque_inondation': risque_inondation,
        'qualite_drainage': qualite_drainage,
        'distance_route': distance_route, 'densite_urbaine': densite_urbaine,
        'distance_industrie': distance_industrie,
        'couverture_vegetale': couverture_vegetale,
        'altitude': altitude, 'exposition_vent': exposition_vent,
    }

    with st.spinner("Analyse en cours..."):
        res = api.analyser(nom_terrain, localisation, donnees)

    if 'error' in res:
        st.error(res['error'])
        st.stop()

    st.success("✅ Analyse terminée")
    st.session_state.last_analyse = res
    st.session_state.last_donnees = donnees
    st.session_state.last_nom = nom_terrain
    st.session_state.last_loc = localisation

# Affichage résultats (persiste après rerun pour le bouton PDF)
if 'last_analyse' in st.session_state:
    res = st.session_state.last_analyse
    donnees = st.session_state.last_donnees

    st.divider()
    st.markdown("## 🎯 Résultats")

    # Métriques principales
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""<div class="ts-metric">
        <div class="label">Score de risque</div>
        <div class="value">{res['risque_score']:.1f}<span style="font-size:1rem; color:#475569;"> / 100</span></div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="ts-metric">
        <div class="label">Classification</div>
        <div class="value">{badge(res['classe'])}</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="ts-metric">
        <div class="label">Cluster (profil)</div>
        <div class="value">#{res['cluster'] + 1}</div>
        </div>""", unsafe_allow_html=True)

    # Verdict
    st.markdown(f"""<div class="ts-card" style="border-left:4px solid {EMERALD};">
    <h3 style="margin-top:0;">📋 Verdict</h3>
    <p style="font-size:1.05rem;">{res['verdict']}</p>
    </div>""", unsafe_allow_html=True)

    # Graphique 1 — Jauge de risque
    col_a, col_b = st.columns(2)
    with col_a:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=res['risque_score'],
            title={'text': "Score de risque"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': EMERALD},
                'steps': [
                    {'range': [0, 33], 'color': '#D1FAE5'},
                    {'range': [33, 66], 'color': '#FEF3C7'},
                    {'range': [66, 100], 'color': '#FEE2E2'},
                ],
            }
        ))
        fig.update_layout(height=300, margin=dict(t=40, b=0, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        # Probabilités
        probs = res['probabilites']
        fig2 = go.Figure(go.Bar(
            x=list(probs.values()), y=list(probs.keys()), orientation='h',
            marker_color=[EMERALD if k == res['classe'] else '#E5E7EB' for k in probs.keys()],
            text=[f"{v*100:.1f}%" for v in probs.values()], textposition='outside'
        ))
        fig2.update_layout(title="Probabilités par classe", height=300,
                            margin=dict(t=40, b=20, l=60, r=20),
                            xaxis=dict(range=[0, 1.1]))
        st.plotly_chart(fig2, use_container_width=True)

    # Importance variables
    imps = res['importances']
    imps_sorted = sorted(imps.items(), key=lambda x: x[1], reverse=True)[:10]
    fig3 = go.Figure(go.Bar(
        x=[v for _, v in imps_sorted],
        y=[k.replace('_', ' ') for k, _ in imps_sorted],
        orientation='h', marker_color=EMERALD
    ))
    fig3.update_layout(title="Top 10 variables les plus déterminantes (Random Forest)",
                       height=380, margin=dict(t=40, b=20, l=180, r=20),
                       yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig3, use_container_width=True)

    # Projection future
    proj = res['projection']
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=['Aujourd’hui', '+5 ans', '+10 ans'],
        y=[proj['actuel'], proj['risque_5ans'], proj['risque_10ans']],
        mode='lines+markers', line=dict(color=EMERALD, width=4),
        marker=dict(size=14), fill='tozeroy', fillcolor='rgba(16,185,129,0.15)'
    ))
    fig4.update_layout(title="🔮 Projection du risque (scénario tendanciel)",
                       height=320, margin=dict(t=50, b=20, l=40, r=20),
                       yaxis=dict(range=[0, 100], title="Score"))
    st.plotly_chart(fig4, use_container_width=True)

    # Bouton PDF
    st.divider()
    pdf_bytes = generer_pdf(
        res, st.session_state.last_nom, st.session_state.last_loc,
        st.session_state.user['name'], donnees
    )
    st.download_button(
        "📄 Télécharger le rapport PDF",
        data=pdf_bytes,
        file_name=f"rapport_{st.session_state.last_nom.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )   
