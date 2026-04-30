import streamlit as st
from style import inject_css

st.set_page_config(page_title="Accueil", page_icon="🏠", layout="wide")
inject_css()

if not st.session_state.get('token'):
    st.warning("🔒 Connectez-vous depuis la page principale.")
    st.stop()

st.markdown("# 🏠 Accueil")
st.markdown(f"""
    <div class="ts-hero" style="padding:2rem 2.5rem; border-radius:22px; backgroud:linear-gradient(135deg, #1E2761 0%, #3B4CCA 100%);">
        <h1 style="color:white; margin:0;"> Bienvenue, {st.session_state.user['name']} </h1>
        <p style="font-size:1.1rem; opacity:.9; margin-top:.5rem;">
            Analyse intelligente de l'adéquation d'un terrain à la construction.
        </p>
        <p style="font-size:1rem; opacity:.9; margin-top:1rem;">
            prêt à analyser un terrain ?
        </p>
    </div>
""", unsafe_allow_html=True)

st.write("")

st.page_link("pages/2_📝_Nouvelle_Analyse.py", label="➡️ Lancer une nouvelle analyse", icon="📝")
