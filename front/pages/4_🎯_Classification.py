"""Visualisation classification supervisée."""
import streamlit as st
import pandas as pd
import plotly.express as px
from style import inject_css, PLOTLY_COLORS
import api_client as api

st.set_page_config(page_title="Classification", page_icon="🎯", layout="wide")
inject_css()

if not st.session_state.get('token'):
    st.warning("🔒 Connectez-vous."); st.stop()

st.markdown("# 🎯 Classification supervisée")
st.markdown('<p style="color: #4a5568; font-size: 1rem; opacity: 0.8;">Random Forest entraîné sur 3 classes : Faible / Moyen / Élevé.</p>', unsafe_allow_html=True)

data = api.dataset()
df = pd.DataFrame(data['sample'])
m = data['metrics']

st.markdown(f'<div class="ts-metric"><div class="label">Précision du modèle</div><div class="value">{m["accuracy_rf"]*100:.1f} %</div></div>', unsafe_allow_html=True)

st.markdown("### Distribution des classes")
counts = df['classe_risque'].value_counts().reset_index()
counts.columns = ['Classe', 'Nombre']
fig = px.bar(counts, x='Classe', y='Nombre', color='Classe',
             color_discrete_map={'Faible': '#10B981', 'Moyen': '#F59E0B', 'Élevé': '#DC2626'})
fig.update_layout(height=360, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Risque vs pente — coloré par classe")
fig2 = px.scatter(df, x='pente', y='risque', color='classe_risque',
                  color_discrete_map={'Faible': '#10B981', 'Moyen': '#F59E0B', 'Élevé': '#DC2626'},
                  opacity=0.7)
fig2.update_layout(height=440)
st.plotly_chart(fig2, use_container_width=True)
