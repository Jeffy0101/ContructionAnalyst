"""Historique des analyses de l'utilisateur."""
import streamlit as st
import pandas as pd
from style import inject_css, badge
import api_client as api

st.set_page_config(page_title="Historique", page_icon="📜", layout="wide")
inject_css()

if not st.session_state.get('token'):
    st.warning("🔒 Connectez-vous."); st.stop()

st.markdown("# 📜 Historique des analyses")

res = api.historique()
analyses = res.get('analyses', [])

if not analyses:
    st.info("Aucune analyse pour l'instant. Créez-en une depuis la page Nouvelle Analyse.")
    st.stop()

for a in analyses:
    r = a['resultat']
    st.markdown(f"""<div class="ts-card">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <h3 style="margin:0;">{a['nom_terrain']}</h3>
          <p style="margin:4px 0; color:lightgreen;">{a.get('localisation','—')} · {a['date'][:10]}</p>
        </div>
        <div style="text-align:right;">
          <div style="font-size:1.8rem; font-weight:700;">{r['risque_score']:.1f}</div>
          {badge(r['classe'])}
        </div>
      </div>
    </div>""", unsafe_allow_html=True)
