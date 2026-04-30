"""Visualisation des régressions linéaires (simple + multiple)."""
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from style import inject_css, EMERALD
import api_client as api

st.set_page_config(page_title="Régressions", page_icon="📊", layout="wide")
inject_css()

if not st.session_state.get('token'):
    st.warning("🔒 Connectez-vous."); st.stop()

st.markdown("# 📊 Régressions linéaires")
st.markdown('<p style="color: #4a5568; font-size: 1rem; opacity: 0.8;">Analyse des relations entre variables et risque (modèles entraînés sur 500 terrains)</p>', unsafe_allow_html=True)

data = api.dataset()
df = pd.DataFrame(data['sample'])
m = data['metrics']

c1, c2 = st.columns(2)
with c1:
    st.markdown(f'<div class="ts-metric"><div class="label">R² Régression simple</div><div class="value">{m["r2_simple"]:.3f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="ts-metric"><div class="label">R² Régression multiple</div><div class="value">{m["r2_multiple"]:.3f}</div></div>', unsafe_allow_html=True)

st.markdown("### 1️⃣ Régression simple : risque ~ pente")
fig = px.scatter(df, x='pente', y='risque', trendline='ols',
                 trendline_color_override=EMERALD,
                 color_discrete_sequence=[EMERALD],
                 opacity=0.5)
fig.update_layout(height=420, margin=dict(t=20, b=20))
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 2️⃣ Régression multiple — corrélations")
corr = df[[c for c in df.columns if c not in ['classe_risque','pca1','pca2','cluster']]].corr()
fig2 = px.imshow(corr, color_continuous_scale='RdYlGn_r', aspect='auto')
fig2.update_layout(height=600, margin=dict(t=20, b=20))
st.plotly_chart(fig2, use_container_width=True)
