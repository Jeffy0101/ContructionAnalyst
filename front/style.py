"""Système de design : couleurs, CSS injecté dans toutes les pages."""
import streamlit as st

# Palette
EMERALD = "#10B981"
EMERALD_DARK = "#059669"
EMERALD_LIGHT = "#D1FAE5"
INK = "#0F172A"
SLATE = "#475569"
BG = "#F8FAFC"
CARD = "#415263"

PLOTLY_COLORS = ['#10B981', '#059669', '#34D399', '#6EE7B7', '#A7F3D0']


def inject_css():
    st.markdown(f"""
    
    <style>

    /* === GLOBAL === */
    html, body {{
        font-family: 'Inter',-apple-system, 'Segoe UI', Roboto, sans-serif;
        color: #0F172A;
        background: #F8FAFC;
    }}

    .stApp {{
        background: linear-gradient(180deg,#FFFFFF 0%, #F1F5F9 100%);
    }}
    /* === HEADER STREAMLIT === */
    header[data-testid="stHeader"] {{
        background: white !important;
    }}

    header[data-testid="stHeader"] * {{
        color: #0F172A !important;
    }}
                
    /* === FIX MARKDOWN VISIBILITY === */
    [data-testid="stMarkdownContainer"] {{
        color: #0F172A !important;
    }}

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] div {{
        color: #0F172A !important;
    }}

    /* bouton menu (≡) */
    button[kind="header"] {{
        color: #0F172A !important;
    }}

    h1 {{
        font-size: 2.8rem !important;
        font-weight: 800;
        color: #0F172A;
    }}
    h2 {{
        font-size: 2rem !important;
        font-weight: 700;
        color: #0F172A;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        letter-spacing: -0.01em;
    }}
    h3 {{
      font-size: 1.4rem !important;
      font-weight: 600;
      color: #1E293B;
      margin-top: 1rem;
      margin-bottom: 0.5rem;
      position: relative;
    }}
        h3::after {{
          content: "";
          display: block;
          width: 40px;
          height: 4px;
          background: #10B981;
          border-radius: 2px;
          margin-top: 6px;
        }}        
        
    
    /* === HERO === */
    .ts-hero {{
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        padding: 50px;
        border-radius: 24px;
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(16,185,129,0.3);
    }}

    /* === CARD === */
    .ts-card {{
        background: white;
        color: #0F172A;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        transition: 0.4s;
    }}

    .ts-card:hover {{
        transform: translateY(-8px);
    }}
    
    .ts-info{{
        background: #E1F5FE;
        color: #01579B;
        border-radius: 12px;
        padding: 16px 24px;
        display: flex;
        align-items: center;
        gap: 16px;
        font-weight: bold;
        font-size: 18px;
        border-left: 5px solid #01579b;
        margin-top: 30px;
    }}

    /* === INPUT === */
    .stTextInput input {{
        border-radius: 14px !important;
        padding: 14px !important;
        border: 1px solid #E2E8F0 !important;
    }}

    .stTextInput input:focus {{
        border-color: #10B981 !important;
        box-shadow: 0 0 0 4px rgba(16,185,129,0.2) !important;
    }}

    /* === BUTTON === */
    .stButton>button {{
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        border-radius: 12px;
        height: 48px;
        font-weight: 600;
        transition: 0.2s;
    }}

    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(16,185,129,0.4);
    }}

    /* === TEXT FIX === */
    body, p, span, div {{
        color: #0F172A !important;
    }}

    /* === SIDEBAR === */
    [data-testid="stSidebar"] {{
        background: white;
        border-right: 1px solid #E5E7EB;
    }}

    /* === HIDE STREAMLIT === */
    #MainMenu {{visibility:hidden;}}
    footer {{visibility:hidden;}}

    
   
    [data-testid="stPageLink"]{{
        background: #E1F5FE;
        color: #01579B;
        border-radius: 12px;
        padding: 16px 24px;
        display: flex;
        align-items: center;
        gap: 16px;
        font-weight: bold;
        font-size: 18px;
        border-left: 5px solid #01579b;
        margin-top: 30px; 
        transition: 0.3s;
    }}
    [data-testid="stPageLink"]:hover {{
        color: white !important;
        transform: scale(1.02);
        box-shadow: 0 10px 25px rgba(16,185,129,0.4);
    }}
    .[data-testid="stDownloadButton"] {{
        background-color: #E1F5FE;
        color: #01579B;
        border-radius: 12px;
        padding: 16px 24px;
        display: flex;
        gap: 16px;
        font-weight: bold;
        font-size: 18px;
        border-left: 5px solid #01579b;
        margin-top: 30px; 
        transition: 0.3s;
    }}
    .[data-testid="stDownloadButton"]:hover {{
        color: white !important;
        transform: scale(1.02);
        box-shadow: 0 10px 25px rgba(16,185,129,0.4);
    }}

    stCaption, stError, stSlider, label p{{
        color: #0F172A !important;
        caret-color: #10B981 !important;
        opacity: 1 !important;
        font-weight: 500 !important;

    }}
    
        /* === INPUTS BLANCS (LOGIN CLEAN) === */
    .stTextInput input,
    .stPasswordInput input,
    .stNumberInput input,
    .stTextArea textarea {{
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
    }}

    /* Focus (quand on clique dedans) */
    .stTextInput input:focus,
    .stPasswordInput input:focus,
    .stNumberInput input:focus {{
        border-color: #10B981 !important;
        box-shadow: 0 0 0 4px rgba(16,185,129,0.15) !important;
        outline: none !important;
    }}

    /* Placeholder */
    .stTextInput input::placeholder,
    .stPasswordInput input::placeholder {{
        color: #94A3B8 !important;
    }}

    /* Curseur */
    .stTextInput input,
    .stPasswordInput input {{
        caret-color: #10B981 !important;
    }}
    
    /* === AUTOFILL FIX (Chrome) === */
    input:-webkit-autofill,
    input:-webkit-autofill:focus {{
        -webkit-text-fill-color: #0F172A !important;
        -webkit-box-shadow: 0 0 0px 1000px #FFFFFF inset !important;
        transition: background-color 5000s ease-in-out 0s;
    }}
    
    .stPasswordInput button {{
      background: #F1F5F9 !important;
      color: #0F172A !important;
      border-radius: 0 12px 12px 0 !important;
    }}

    .auth-left h1 {{
        font-size: 7rem;
        color: #1E2761;
        text-align: center;
        background: linear-gradient(135deg, #10B981, #059669);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 20px 40px rgba(16,185,129,0.3));
        margin-bottom: 0.5rem; 
    }}

    .auth-left .subtitle {{
        text-align: center;
        font-weight: 700;
        letter-spacing: 0.1em;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        color: #10B981 !important;
        margin-bottom: 1rem;
    }}
    .subtitle {{
        position: relative;
    }}

    .subtitle::after {{
        content: "";
        display: block;
        width: 40px;
        height: 3px;
        background: #10B981;
        margin: 6px auto 0;
        border-radius: 2px;
    }}

    .auth-left .description {{
        color: #475569;
        font-size: 1.05rem;
        line-height: 1.6;
        margin-top: 1rem;
        color: #475569;
        max-width: 420px;
        margin: 0 auto;
    }}

    .auth-left .features {{
        color: #334155;
        margin-top: 1.5rem;
        line-height: 1.8;
        padding-left: 3rem;
    }}
    
    .auth-left .features li {{
        margin-bottom: 8px;
    }}

    .auth-left .features li:hover {{
        color: #10B981;
        transition: 0.2s;
    }}

    
    /* Cache le menu Streamlit par défaut */
      #MainMenu {{visibility:hidden;}}
      footer {{visibility:hidden;}}
    </style>
 """, unsafe_allow_html=True)


def badge(classe):
    cls = {'Faible': 'ts-badge-low', 'Moyen': 'ts-badge-mid', 'Élevé': 'ts-badge-high'}.get(classe, 'ts-badge-low')
    return f'<span class="ts-badge {cls}">{classe}</span>'
