"""ACP (réduction dimensionnalité) + K-Means (clustering non-supervisé)."""
import streamlit as st
import pandas as pd
import plotly.express as px
from style import inject_css, PLOTLY_COLORS
import api_client as api

st.set_page_config(page_title="ACP & Clustering", page_icon="🔬", layout="wide")
inject_css()

if not st.session_state.get('token'):
    st.warning("🔒 Connectez-vous."); st.stop()

st.markdown("# 🔬 ACP & Clustering K-Means")
st.markdown('<p style="color: #4a5568; font-size: 1rem; opacity: 0.8;">Réduction de dimension à 2 axes (ACP) + regroupement automatique en 3 clusters.</p>', unsafe_allow_html=True)

data = api.dataset()
df = pd.DataFrame(data['sample'])
m = data['metrics']

c1, c2 = st.columns(2)
with c1:
    st.markdown(f'<div class="ts-metric"><div class="label">Variance expliquée axe 1</div><div class="value">{m["pca_variance"][0]*100:.1f} %</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="ts-metric"><div class="label">Variance expliquée axe 2</div><div class="value">{m["pca_variance"][1]*100:.1f} %</div></div>', unsafe_allow_html=True)

st.markdown("### Projection ACP — colorée par cluster K-Means")
df['cluster_label'] = df['cluster'].map({0: 'Cluster 1', 1: 'Cluster 2', 2: 'Cluster 3'})
fig = px.scatter(df, x='pca1', y='pca2', color='cluster_label',
                 color_discrete_sequence=PLOTLY_COLORS,
                 hover_data=['risque', 'classe_risque'], opacity=0.7)
fig.update_layout(height=520)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Profil moyen de chaque cluster")
profile = df.groupby('cluster_label')[['risque', 'pente', 'capacite_portante', 'risque_inondation']].mean().round(2)
st.dataframe(profile, use_container_width=True)
