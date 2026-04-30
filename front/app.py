"""Point d'entrée Streamlit : gère login/register, puis affiche le dashboard."""
import streamlit as st
from style import inject_css, EMERALD
import api_client as api

st.set_page_config(
    page_title="TerraSafe — Analyse de terrain",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()

# Init session
if 'token' not in st.session_state:
    st.session_state.token = None
    st.session_state.user = None


def page_auth():
    """Page de connexion / inscription élégante."""
    col2, col3 = st.columns([1, 1.2], gap="large")
    
    with col2:
        st.markdown(f"""
            <div class="auth-left">
                <h1>TerrainRisk</h1>
                <p class="subtitle">
                    ANALYSE INTELLIGENTE DE TERRAIN
                </p>
                <p class="description">
                    Evaluez en quelques secondes le risque d'un terrain pour la construction.
                    Modèles de regression, classification et projection 10 ans.
                </p>
                <ul class="features">
                    <li>15 Caractéristiques géotechniques analysées</li>
                    <li>5 techniques de machine learning utilisées simultanément</li>
                    <li>Rapport PDF détaillé généré automatiquement</li>
                    <li>Prédictions de risque à 1, 5 et 10 ans</li>
                </ul>
            </div>
                    
    """, unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="ts-auth-card">', unsafe_allow_html=True)
        st.markdown(f"<h2 style='margin-top:2; text-align:center'>Connexion</h2>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔑 Connexion", "✨ Créer un compte"])

        with tab1:
            st.markdown("&nbsp;")  # Petit espace pour aligner avec le formulaire d'inscription
            email = st.text_input("Adresse email", key="li_email", placeholder="vous@exemple.com")
            pwd = st.text_input("Mot de passe", type="password", key="li_pwd", placeholder="••••••••")
            if st.button("Se connecter →", use_container_width=True, key="btn_login"):
                if not email or not pwd:
                    st.warning("⚠️ Veuillez remplir tous les champs.")
                else:
                    try:
                        res = api.login(email, pwd)
                        if 'token' in res:
                            st.session_state.token = res['token']
                            st.session_state.user = res['user']
                            st.success(res.get('message', '✅ Connexion réussie ! Redirection...'))
                            st.rerun()
                        else:
                            st.error(res.get('error', '❌ Identifiants invalides'))
                    except Exception as e:
                        st.error(f"❌ Une erreur est survenue lors de la connexion: {e}")
                    return

        with tab2:
            st.markdown("&nbsp;")  # Petit espace pour aligner avec le formulaire de connexion
            name = st.text_input("Nom complet", key="ri_name", placeholder="Jean Dupont")
            email2 = st.text_input("Email", key="ri_email", placeholder="vous@exemple.com")
            pwd2 = st.text_input("Mot de passe (min 6 car.)", type="password", key="ri_pwd", placeholder="••••••••")
            if st.button("Créer mon compte", use_container_width=True, key="btn_reg"):
                if not name or not email2 or not pwd2:
                    st.warning("⚠️ Veuillez remplir tous les champs.")
                try:
                    res = api.register(email2, pwd2, name)
                    if 'token' in res:
                        st.session_state.token = res['token']
                        st.session_state.user = res['user']
                        st.success("✅ Inscription réussie ! Redirection...")
                        st.rerun()
                    else:
                        st.error(res.get('error', '❌ Une erreur est survenue lors de l\'inscription'))
                except Exception as e:
                    st.error("❌ Une erreur est survenue lors de l'inscription.")
            return
                
        st.markdown('</div>', unsafe_allow_html=True)


def dashboard():
    """Dashboard d'accueil après connexion."""
    user = st.session_state.user

    # Sidebar utilisateur
    with st.sidebar:
        st.markdown(f"### 👤 {user['name']}")
        st.caption(user['email'])
        st.divider()
        st.markdown("**Navigation** : utilisez le menu à gauche pour accéder aux pages.")
        st.divider()
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()

    # Hero
    st.markdown(f"""
    <div class="ts-hero">
      <h1>Bienvenue, {user['name'].split()[0]} 👋</h1>
      <p>TerrainRisk analyse jusqu'à 15 variables géotechniques, hydrologiques et urbanistiques
      pour évaluer le risque réel d'un terrain. Démarrez par une nouvelle analyse.</p>
    </div>
    """, unsafe_allow_html=True)

    # Cartes intro
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="ts-card">
        <h3>📝 Nouvelle analyse</h3>
        <p>Renseignez les caractéristiques d'un terrain et obtenez instantanément un
        verdict de risque, des graphiques et un rapport PDF.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="ts-card">
        <h3>📊 5 techniques ML</h3>
        <p>Régression simple/multiple, ACP, classification supervisée (Random Forest)
        et clustering K-Means — toutes utilisées simultanément.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="ts-card">
        <h3>📜 Historique</h3>
        <p>Toutes vos analyses sont sauvegardées dans MongoDB. Comparez l'évolution
        de plusieurs terrains au fil du temps.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("## À propos du projet", unsafe_allow_html=True)
    st.markdown("""
        **TerrainRisk** aide à déterminer si un terrain est **adéquat** pour une construction.
        L'application combine des données géotechniques (type de sol, pente, portance,
        humidité...)
        et environnementales (sismicité, inondation, érosion, climat) pour calculer un
        **score de risque entre 0 et 1** puis un **verdict clair** :
        
        - **Adéquat** — le terrain peut accueillir une construction avec les précautions standard.
        - **À surveiller** — des études complémentaires ou renforcements sont recommandés.
        - **Non adéquat** — risque élevé, déconseillé sans intervention lourde.
    """, unsafe_allow_html=True)
    colA, colB = st.columns(2)
    with colA:
        st.markdown("### ■ Les 5 techniques intégrées", unsafe_allow_html=True)
        st.markdown("""
            1. **Régression linéaire simple** — pente → risque
            2. **Régression linéaire multiple** — toutes les features → score
            3. **PCA** — réduction en 2D pour visualiser
            4. **Classification supervisée** — RandomForest + SVM
            5. **Classification non supervisée** — KMeans + DBSCAN
        """, unsafe_allow_html=True)
    with colB:
        st.markdown("### ■ Comment démarrer ?", unsafe_allow_html=True)
        st.markdown("""
            1. Va dans Analyse Terrain
            2. Saisis ou importe les caractéristiques
            3. Consulte Techniques ML pour chaque méthode
            4. Projette 10 ans d'évolution dans Prédictions
            5. Télécharge ton Rapport PDF
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="ts-info">
            <span>👉</span> 
            Sélectionnez une page dans le menu de gauche pour commencer.
        </div>
    """, unsafe_allow_html=True)
    


# --- Routeur ---
if st.session_state.token is None:
    page_auth()
else:
    dashboard()