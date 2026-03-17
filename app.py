"""
ENTE - Contrôle Qualité ULTRA PRO v2.1 (Persistance des imports)
✨ Correction: Les fichiers importés sont conservés en session_state
   → Plus besoin de réimporter quand on change de module

RUN:
pip install streamlit pandas numpy plotly pyreadstat openpyxl
streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pyreadstat
from datetime import datetime
from PIL import Image as PILImage
import warnings, os

warnings.filterwarnings("ignore")

# Favicon
_favicon = None
_logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "favicon.png")
if os.path.exists(_logo_path):
    _favicon = PILImage.open(_logo_path)

# Logo en base64 pour header + sidebar
import base64 as _b64
_logo_b64 = ""
_logo_full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ente_logo.png")
if os.path.exists(_logo_full_path):
    with open(_logo_full_path, "rb") as _f:
        _logo_b64 = _b64.b64encode(_f.read()).decode()

# =============================================================================
# CONFIG
# =============================================================================
st.set_page_config(
    page_title="ENTE - Contrôle Qualité",
    page_icon=_favicon or "📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# SESSION STATE — Persistance des fichiers importés
# =============================================================================
if "df_menage" not in st.session_state:
    st.session_state.df_menage = None
if "df_emploi" not in st.session_state:
    st.session_state.df_emploi = None
if "menage_filename" not in st.session_state:
    st.session_state.menage_filename = None
if "emploi_filename" not in st.session_state:
    st.session_state.emploi_filename = None
if "active_module" not in st.session_state:
    st.session_state.active_module = "exhaustivite"

# =============================================================================
# CSS PROFESSIONNEL — THÈME INSTITUTIONNEL MARINE / OR
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');

:root {
  --primary:       #0d2f5e;
  --primary-mid:   #1a4a8a;
  --primary-light: #2563b0;
  --accent:        #e9a800;
  --accent-light:  #fbbf24;
  --success:       #059669;
  --warning:       #d97706;
  --danger:        #dc2626;
  --info:          #0284c7;
  --text:          #111827;
  --muted:         #6b7280;
  --border:        #e5e7eb;
  --bg:            #f4f6fb;
  --card:          #ffffff;
  --shadow-sm:     0 1px 3px rgba(13,47,94,0.08), 0 1px 2px rgba(13,47,94,0.05);
  --shadow:        0 4px 12px rgba(13,47,94,0.10), 0 2px 4px rgba(13,47,94,0.06);
  --shadow-lg:     0 12px 28px rgba(13,47,94,0.14), 0 4px 8px rgba(13,47,94,0.08);
  --radius:        10px;
  --radius-sm:     6px;
  --transition:    all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

*, *::before, *::after {
  font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  box-sizing: border-box;
}

/* ---- PAGE BG ---- */
.main {
  background: var(--bg);
}
.block-container {
  padding-top: 1.5rem !important;
  padding-bottom: 2rem !important;
}

/* ---- ANIMATIONS ---- */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}
.main > div { animation: fadeUp 0.45s ease-out both; }

/* ---- HEADER ---- */
.header {
  background: var(--primary);
  padding: 1.75rem 2.5rem;
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  margin-bottom: 1.75rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  position: relative;
  overflow: hidden;
}
.header::before {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 320px; height: 100%;
  background: linear-gradient(135deg, transparent 40%, rgba(233,168,0,0.12) 100%);
  pointer-events: none;
}
.header::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0;
  width: 100%; height: 3px;
  background: linear-gradient(90deg, var(--accent) 0%, var(--accent-light) 60%, transparent 100%);
}
.header-text { flex: 1; }
.header h1 {
  color: white;
  margin: 0 0 0.25rem;
  font-family: 'Syne', sans-serif;
  font-size: 1.9rem;
  font-weight: 800;
  letter-spacing: -0.5px;
  line-height: 1.2;
}
.header p {
  color: rgba(255,255,255,0.75);
  margin: 0;
  font-size: 0.9rem;
  font-weight: 500;
  letter-spacing: 0.2px;
}
.header-badge {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 20px;
  padding: 0.35rem 0.9rem;
  color: var(--accent-light);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  white-space: nowrap;
}

/* ---- METRIC CARDS ---- */
[data-testid="stMetric"] {
  background: var(--card);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  border-top: 3px solid var(--primary-light);
  box-shadow: var(--shadow-sm);
  padding: 1.25rem 1.5rem !important;
  transition: var(--transition);
}
[data-testid="stMetric"]:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow);
  border-top-color: var(--accent);
}
[data-testid="stMetricValue"] {
  font-family: 'Syne', sans-serif !important;
  font-size: 2rem !important;
  font-weight: 800 !important;
  color: var(--primary) !important;
  letter-spacing: -0.5px;
}
[data-testid="stMetricLabel"] {
  font-size: 0.75rem !important;
  font-weight: 600 !important;
  color: var(--muted) !important;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #FAF6F0 0%, #F3EDE4 100%) !important;
  box-shadow: 4px 0 20px rgba(13,47,94,0.10);
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stCaption {
  color: #4a4540 !important;
  font-size: 0.85rem !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  color: #1A1816 !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  letter-spacing: -0.3px;
}
[data-testid="stSidebar"] strong {
  color: var(--primary) !important;
  font-size: 0.72rem !important;
  text-transform: uppercase;
  letter-spacing: 1px;
}
[data-testid="stSidebar"] hr {
  border-color: rgba(0,0,0,0.1) !important;
  margin: 0.75rem 0 !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
  background: rgba(255,255,255,0.6) !important;
  border: 1.5px dashed rgba(13,47,94,0.25) !important;
  border-radius: var(--radius-sm) !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
  border-color: var(--primary-light) !important;
  background: rgba(255,255,255,0.85) !important;
}
[data-testid="stSidebar"] [data-testid="stCheckbox"] label {
  color: #2D2B28 !important;
}
[data-testid="stSidebar"] .stSuccess {
  background: rgba(5,150,105,0.1) !important;
  border: 1px solid rgba(5,150,105,0.3) !important;
  border-radius: var(--radius-sm) !important;
  color: #065f46 !important;
  font-size: 0.82rem !important;
}

/* ---- SIDEBAR NAV BUTTONS ---- */
[data-testid="stSidebar"] [data-testid="stButton"] button {
  border-radius: var(--radius-sm) !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  padding: 12px 14px !important;
  line-height: 1.3 !important;
  text-align: left !important;
  margin-bottom: 3px !important;
  transition: var(--transition) !important;
  letter-spacing: 0.1px;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="secondary"] {
  background: rgba(255,255,255,0.65) !important;
  color: #4a4540 !important;
  border: 1px solid rgba(0,0,0,0.08) !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="secondary"]:hover {
  background: rgba(255,255,255,0.95) !important;
  border-color: var(--primary-light) !important;
  color: var(--primary) !important;
  transform: translateX(3px) !important;
  box-shadow: 0 3px 10px rgba(13,47,94,0.12) !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"] {
  background: var(--primary) !important;
  color: white !important;
  border: none !important;
  box-shadow: 0 3px 10px rgba(13,47,94,0.25) !important;
  font-weight: 700 !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="primary"]:hover {
  background: var(--primary-mid) !important;
  transform: translateX(3px) !important;
}

/* ---- TABS ---- */
.stTabs [data-baseweb="tab-list"] {
  gap: 4px;
  padding: 4px;
  border-radius: var(--radius);
  background: var(--card);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}
.stTabs [data-baseweb="tab"] {
  height: 44px;
  padding: 0 1.25rem;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 0.88rem;
  transition: var(--transition);
  color: var(--muted);
}
.stTabs [data-baseweb="tab"]:hover {
  background: rgba(13,47,94,0.06);
  color: var(--primary);
}
.stTabs [aria-selected="true"] {
  background: var(--primary) !important;
  color: white !important;
  box-shadow: var(--shadow-sm);
}

/* ---- MAIN BUTTONS ---- */
.stButton > button {
  background: var(--primary);
  color: white;
  border: none;
  padding: 0.65rem 1.75rem;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 0.9rem;
  transition: var(--transition);
  box-shadow: var(--shadow-sm);
  letter-spacing: 0.2px;
}
.stButton > button:hover {
  background: var(--primary-mid);
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}
.stButton > button:active {
  transform: translateY(0);
}

/* ---- DATAFRAME ---- */
.dataframe {
  border-radius: var(--radius) !important;
  overflow: hidden !important;
  box-shadow: var(--shadow-sm) !important;
  border: 1px solid var(--border) !important;
  font-size: 0.88rem !important;
}
.dataframe thead tr {
  background: var(--primary) !important;
}
.dataframe thead th {
  color: white !important;
  font-weight: 700 !important;
  padding: 0.85rem 1rem !important;
  text-transform: uppercase;
  font-size: 0.75rem !important;
  letter-spacing: 0.7px;
  border: none !important;
}
.dataframe tbody tr {
  transition: var(--transition);
  border-bottom: 1px solid var(--border) !important;
}
.dataframe tbody tr:hover {
  background-color: rgba(13,47,94,0.04) !important;
}
.dataframe tbody td {
  padding: 0.7rem 1rem !important;
  border: none !important;
  font-size: 0.87rem !important;
}

/* ---- CHARTS ---- */
.js-plotly-plot {
  border-radius: var(--radius);
  box-shadow: none;
  overflow: hidden;
  background: transparent;
  border: none;
}

/* ---- FILE UPLOADER (main area) ---- */
[data-testid="stFileUploader"] {
  background: white;
  border-radius: var(--radius);
  padding: 1.25rem;
  border: 1.5px dashed rgba(13,47,94,0.25);
  transition: var(--transition);
  box-shadow: var(--shadow-sm);
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--accent);
  background: rgba(233,168,0,0.02);
}

/* ---- ALERTS ---- */
.stSuccess {
  border-radius: var(--radius-sm) !important;
  border-left: 4px solid var(--success) !important;
  padding: 0.8rem 1rem !important;
  font-weight: 500 !important;
}
.stInfo {
  border-radius: var(--radius-sm) !important;
  border-left: 4px solid var(--info) !important;
  padding: 0.8rem 1rem !important;
  font-weight: 500 !important;
}
.stWarning {
  border-radius: var(--radius-sm) !important;
  border-left: 4px solid var(--warning) !important;
  padding: 0.8rem 1rem !important;
  font-weight: 500 !important;
}
.stError {
  border-radius: var(--radius-sm) !important;
  border-left: 4px solid var(--danger) !important;
  padding: 0.8rem 1rem !important;
  font-weight: 500 !important;
}

/* ---- EXPANDER ---- */
.streamlit-expanderHeader {
  background: white !important;
  border-radius: var(--radius-sm) !important;
  font-weight: 600 !important;
  border: 1px solid var(--border) !important;
  color: var(--primary) !important;
}
[data-testid="stExpander"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  box-shadow: var(--shadow-sm) !important;
}

/* ---- SELECT & MULTISELECT ---- */
[data-baseweb="select"] > div {
  border-radius: var(--radius-sm) !important;
  border-color: var(--border) !important;
}
[data-baseweb="select"] > div:focus-within {
  border-color: var(--primary-light) !important;
  box-shadow: 0 0 0 3px rgba(13,47,94,0.1) !important;
}

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #f1f3f7; border-radius: 8px; }
::-webkit-scrollbar-thumb {
  background: rgba(13,47,94,0.3);
  border-radius: 8px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--primary-light);
}

/* ---- TEXT INPUT (search) ---- */
[data-testid="stTextInput"] input {
  border-radius: var(--radius-sm) !important;
  border-color: var(--border) !important;
  font-size: 0.88rem !important;
}
[data-testid="stTextInput"] input:focus {
  border-color: var(--primary-light) !important;
  box-shadow: 0 0 0 3px rgba(13,47,94,0.1) !important;
}

/* ---- HEADINGS in main ---- */
h3, h4 { color: var(--primary) !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; }
hr { border-color: var(--border) !important; margin: 1.25rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# LABELS ET DICTIONNAIRES
# =============================================================================
LABELS_EQUIPES = {
    100: "Sidi Mohamed Boune",
    200: "Oumar Biye Salime",
    300: "Ahmed talib ahmed sidi",
    400: "Mohamed Vadhel Seydou Camara",
    500: "El moustapha Aboubecrine el Hafedh",
    600: "Mahmoud Abderrahime Dia",
    700: "Mohamed Yeslem Elkebir",
    800: "Mohamed Vadel Mohamed El Mouktar Elella",
    900: "Mamadou Ousmane Ba",
    1000: "Mohamed Salem Ahmed  Bezeid Mokhtareiny"
}

LABELS_ENQUETEURS = {
    100: "Sidi Mohamed Boune",
    101: "El Hassen Mohamed Yeslem Boubekar",
    102: "Taleb Sedigh Cheikh Mohamdy Jeddou",
    103: "Brahim Mohamed Mbarek",
    200: "Oumar Biye Salime",
    201: "Mohamedou saleck limam",
    202: "El Bou Mouhamed El Mokhtar Ameirine",
    203: "Sidi Dedd Salim Ahmed Mbadi",
    300: "Ahmed talib ahmed sidi",
    301: "Elhassen Oumar Ba",
    302: "Limame Malick mohamed Boushab",
    303: "Aly Abdel kader",
    400: "Mohamed Vadhel Seydou Camara",
    401: "Bocar souleymane sy",
    402: "Brahim Mohamed Mahmoud Sidi Haiballa",
    403: "Amadou Abdoulaye Ba",
    500: "El moustapha Aboubecrine el Hafedh",
    501: "Kemal Mohamed Abdellahi Bouje",
    502: "Ahmed Banné Messoud",
    503: "Mouhamadou Alassane ba",
    600: "Mahmoud Abderrahime Dia",
    601: "Mohamed El Moctar El Yass",
    602: "Ahmed Aboubecrine El Atighe",
    603: "Abou kalidou N'Gaide",
    700: "Mohamed Yeslem Elkebir",
    701: "Mohamed Lemine Deddaha",
    702: "Mohamed El Gewth",
    703: "Sid El Moctar Sidi Mahamoud Ahmed Sidi",
    800: "Mohamed Vadel Mohamed El Mouktar Elella",
    801: "Dah Belkheir Bewbe",
    802: "Ibrahime Boubou Dia",
    803: "Abdellahi Mohamed Taleb Ahmed",
    900: "Mamadou Ousmane Ba",
    901: "Mohamed lemine Mohemed oumar",
    902: "Sid Ahmed El Hacen Bilal loubek",
    903: "Amadou Adama Ly",
    1000: "Mohamed Salem Ahmed Bezeid Mokhtareiny",
    1001: "Imam cheikh ahmed baba cheikh",
    1002: "Sidi Mohamed Mohamed Sidi Aly",
    1003: "Demba Abdoul Ba"
}

def get_label_equipe(code):
    return LABELS_EQUIPES.get(int(code), f"Équipe {code}")

def get_label_enqueteur(code):
    return LABELS_ENQUETEURS.get(int(code), f"Enquêteur {code}")

# =============================================================================
# FONCTION DE RECHERCHE ET FILTRAGE POUR TABLEAUX
# =============================================================================
def display_searchable_dataframe(df, key_suffix="", height=450):
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Rechercher dans le tableau",
            key=f"search_{key_suffix}",
            placeholder="Tapez pour rechercher..."
        )
    
    with col2:
        rows_per_page = st.selectbox(
            "Lignes par page",
            options=[10, 25, 50, 100, "Tout"],
            index=1,
            key=f"rows_{key_suffix}"
        )
    
    with col3:
        if st.button("🔄 Réinitialiser", key=f"reset_{key_suffix}"):
            st.rerun()
    
    df_filtered = df.copy()
    if search_term:
        mask = df_filtered.astype(str).apply(
            lambda row: row.str.contains(search_term, case=False, na=False).any(), 
            axis=1
        )
        df_filtered = df_filtered[mask]
    
    total_rows = len(df_filtered)
    
    if rows_per_page == "Tout":
        df_display = df_filtered
        st.caption(f"📊 Affichage de **{total_rows}** résultats")
    else:
        rows_per_page = int(rows_per_page)
        total_pages = max(1, (total_rows + rows_per_page - 1) // rows_per_page)
        
        col_page1, col_page2, col_page3 = st.columns([1, 2, 1])
        with col_page2:
            page = st.number_input(
                f"Page (sur {total_pages})",
                min_value=1,
                max_value=total_pages,
                value=1,
                key=f"page_{key_suffix}"
            )
        
        start_idx = (page - 1) * rows_per_page
        end_idx = min(start_idx + rows_per_page, total_rows)
        df_display = df_filtered.iloc[start_idx:end_idx]
        
        st.caption(f"📊 Affichage de **{start_idx + 1}** à **{end_idx}** sur **{total_rows}** résultats")
    
    return df_display

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================
def load_spss_data(uploaded_file):
    try:
        df, meta = pyreadstat.read_sav(uploaded_file)
        df = df.replace({None: np.nan})
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement SPSS: {e}")
        return None

def apply_filters(df: pd.DataFrame, filtrer_i9r: bool) -> pd.DataFrame:
    if df is None:
        return None
    x = df.copy()
    if filtrer_i9r and "I9R" in x.columns:
        x = x[x["I9R"] == 1]
    return x

def create_strate(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    conditions = [
        (df["I1W"].between(13, 15)),
        ((df["I1W"] == 8) & (df["I1MI"] == 1)),
        ((df["I1W"] == 11) & (df["I1MI"] == 1)),
        (~df["I1W"].isin([8, 11, 13, 14, 15]) & (df["I1MI"] == 1)),
        (df["I1W"].isin([4, 5, 6, 10]) & (df["I1MI"] == 2)),
        (df["I1W"].isin([7, 9]) & (df["I1MI"] == 2)),
        (df["I1W"].isin([1, 2, 3, 8, 11, 12]) & (df["I1MI"] == 2)),
        (df["I1"] >= 2503900),
    ]
    choices = [1, 2, 3, 4, 5, 6, 7, 8]
    df["strate"] = np.select(conditions, choices, default=np.nan)
    strate_labels = {
        1: "Nouakchott", 2: "Nouadhibou", 3: "Zoueiratt", 4: "Autre urbain",
        5: "Fleuve", 6: "Oasis", 7: "Autre rural", 8: "Réfugiés",
    }
    df["strate_label"] = df["strate"].map(strate_labels).fillna("Non définie")
    return df

def create_wilaya_label(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    wilaya_mapping = {
        1: "Hodh Chargui", 2: "Hodh Gharbi", 3: "Assaba", 4: "Gorgol",
        5: "Brakna", 6: "Trarza", 7: "Adrar", 8: "Dakhlet Nouadhibou",
        9: "Tagant", 10: "Guidimakha", 11: "Tiris Zemmour", 12: "Inchiri",
        13: "Nouakchott Ouest", 14: "Nouakchott Nord", 15: "Nouakchott Sud",
    }
    df["wilaya_label"] = df["I1W"].map(wilaya_mapping).fillna("Non définie")
    return df

def safe_mean(s: pd.Series) -> float:
    try:
        return float(pd.to_numeric(s, errors="coerce").mean())
    except Exception:
        return 0.0

def calculate_employment_indicators(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()

    needed_cols = {
        "EA1": np.nan, "EA21": 0, "EA22": 0, "EA23": 0, "EA24": 0, "EA25": 0,
        "EA26": 0, "EA27": 0, "EA28": 0, "EA29": 0, "EA210": 0,
        "EA3": np.nan, "EA4": np.nan, "EA5A": np.nan, "EA5B": np.nan,
        "EA6A": np.nan, "EA6B": np.nan, "EA6C": np.nan, "EA6D": np.nan,
        "AP10B": np.nan, "R1": np.nan, "R3A": np.nan
    }
    for col, default_val in needed_cols.items():
        if col not in x.columns:
            x[col] = default_val

    x["Occupe"] = np.nan
    x.loc[x["EA1"] == 1, "Occupe"] = 1

    mask_ea2 = (
        (x["EA21"] == 1) | (x["EA22"] == 1) | (x["EA23"] == 1) | (x["EA24"] == 1) |
        (x["EA25"] == 1) | (x["EA26"] == 1) | (x["EA27"] == 1) | (x["EA28"] == 1) |
        (x["EA29"] == 1) | (x["EA210"] == 1)
    )
    x.loc[(x["EA1"] == 2) & mask_ea2, "Occupe"] = 1
    x.loc[(x["EA3"] == 1) & (x["EA4"] >= 1) & (x["EA4"] <= 5), "Occupe"] = 1
    x.loc[(x["EA3"] == 1) & (x["EA4"].isin([0, 7, 8, 9])) & (x["EA5A"] == 1), "Occupe"] = 1
    x.loc[(x["EA3"] == 1) & (x["EA4"] == 6) & (x["EA5B"] == 1), "Occupe"] = 1

    x["Chomage"] = np.nan
    x.loc[
        (x["Occupe"].isna()) &
        ((x["EA6A"] == 1) | (x["EA6B"] == 1)) &
        (x["EA6D"].isin([1, 2])),
        "Chomage"
    ] = 1
    x.loc[
        (x["EA6C"] > 3) & (x["EA6C"] <= 7) &
        (x["EA6D"].isin([1, 2])),
        "Chomage"
    ] = 1

    x["ME"] = np.nan
    x.loc[(x["Occupe"] == 1) | (x["Chomage"] == 1), "ME"] = 1

    x["HME"] = np.nan
    x.loc[x["ME"].isna(), "HME"] = 1

    x["s_emploi"] = np.nan
    x.loc[
        (x["Occupe"] == 1) &
        (pd.to_numeric(x["AP10B"], errors="coerce") < 40) &
        ((x["R1"] == 1) | (x["R3A"] == 1)),
        "s_emploi"
    ] = 1

    x["mp"] = np.nan
    x.loc[((x["EA6A"] == 1) | (x["EA6B"] == 1)) & (x["EA6D"].isin([3, 4])), "mp"] = 1
    x.loc[(x["EA6A"] == 2) & (x["EA6B"] == 2) & (x["EA6D"].isin([1, 2])), "mp"] = 1

    x["agetravail"] = np.nan
    age_col = "HX5" if "HX5" in x.columns else ("AGE" if "AGE" in x.columns else None)
    if age_col is not None:
        age_num = pd.to_numeric(x[age_col], errors="coerce")
        x.loc[(age_num >= 14) & (age_num <= 64), "agetravail"] = 1

    for col in ["r_emploi", "t_chomage", "t_part", "t_semploi", "t_mp", "t_hme"]:
        x[col] = np.nan

    x.loc[x["agetravail"] == 1, "r_emploi"] = x.loc[x["agetravail"] == 1, "Occupe"].fillna(0) * 100
    x.loc[x["agetravail"] == 1, "r_emploi"] = x.loc[x["agetravail"] == 1, "r_emploi"].fillna(0)

    x["t_chomage"] = np.nan
    mask_me = (x["agetravail"] == 1) & (x["ME"] == 1)
    x.loc[mask_me, "t_chomage"] = x.loc[mask_me, "Chomage"].fillna(0) * 100
    x.loc[mask_me, "t_chomage"] = x.loc[mask_me, "t_chomage"].fillna(0)

    x.loc[x["agetravail"] == 1, "t_part"] = x.loc[x["agetravail"] == 1, "ME"].fillna(0) * 100
    x.loc[x["agetravail"] == 1, "t_part"] = x.loc[x["agetravail"] == 1, "t_part"].fillna(0)

    mask_occ = (x["agetravail"] == 1) & (x["Occupe"] == 1)
    x.loc[mask_occ, "t_semploi"] = x.loc[mask_occ, "s_emploi"].fillna(0) * 100
    x.loc[mask_occ, "t_semploi"] = x.loc[mask_occ, "t_semploi"].fillna(0)

    x.loc[x["agetravail"] == 1, "t_mp"] = x.loc[x["agetravail"] == 1, "mp"].fillna(0) * 100
    x.loc[x["agetravail"] == 1, "t_mp"] = x.loc[x["agetravail"] == 1, "t_mp"].fillna(0)

    x.loc[x["agetravail"] == 1, "t_hme"] = x.loc[x["agetravail"] == 1, "HME"].fillna(0) * 100
    x.loc[x["agetravail"] == 1, "t_hme"] = x.loc[x["agetravail"] == 1, "t_hme"].fillna(0)

    x["statut"] = np.select(
        [x["Occupe"] == 1, x["Chomage"] == 1, x["HME"] == 1],
        ["Occupé", "Au chômage", "Hors main d'oeuvre"],
        default="Non déterminé"
    )
    return x

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    if _logo_b64:
        st.markdown(f'<img src="data:image/png;base64,{_logo_b64}" style="height:50px; border-radius:6px; background:rgba(255,255,255,0.85); padding:4px; margin-bottom:0.5rem;">', unsafe_allow_html=True)
    st.markdown("### ENTE - Contrôle Qualité")
    st.markdown("**ANSADE -- Mauritanie**")
    st.markdown("---")

    st.markdown("**Module d'analyse**")

    MODULES = {
        "exhaustivite": {"label": "Exhaustivité", "icon": "📋", "color": "#3b82f6"},
        "emploi": {"label": "Emploi", "icon": "💼", "color": "#10b981"},
        "consolide": {"label": "Vue Consolidée", "icon": "📊", "color": "#8b5cf6"},
    }

    for key, m in MODULES.items():
        is_active = st.session_state.active_module == key
        if st.button(
            f"{m['icon']}  {m['label']}",
            key=f"nav_{key}",
            width='stretch',
            type="primary" if is_active else "secondary"
        ):
            st.session_state.active_module = key
            st.rerun()

    module = {
        "exhaustivite": "📋 Exhaustivité",
        "emploi": "💼 Emploi",
        "consolide": "📊 Vue Consolidée",
    }[st.session_state.active_module]

    st.markdown("---")

    st.markdown("**📂 Bases de données**")

    if st.session_state.df_menage is not None:
        st.success(f"✅ Ménage : **{st.session_state.menage_filename}**")
        if st.button("🗑️ Supprimer base ménage", key="del_menage"):
            st.session_state.df_menage = None
            st.session_state.menage_filename = None
            st.rerun()
    else:
        uploaded_menage = st.file_uploader("Base Ménage (.sav)", type=["sav"], key="menage")
        if uploaded_menage is not None:
            with st.spinner("⏳ Chargement ménage..."):
                df_loaded = load_spss_data(uploaded_menage)
            if df_loaded is not None:
                st.session_state.df_menage = df_loaded
                st.session_state.menage_filename = uploaded_menage.name
                st.rerun()

    if st.session_state.df_emploi is not None:
        st.success(f"✅ Emploi : **{st.session_state.emploi_filename}**")
        if st.button("🗑️ Supprimer base emploi", key="del_emploi"):
            st.session_state.df_emploi = None
            st.session_state.emploi_filename = None
            st.rerun()
    else:
        uploaded_emploi = st.file_uploader("Base Emploi (.sav)", type=["sav"], key="emploi")
        if uploaded_emploi is not None:
            with st.spinner("⏳ Chargement emploi..."):
                df_loaded = load_spss_data(uploaded_emploi)
            if df_loaded is not None:
                st.session_state.df_emploi = df_loaded
                st.session_state.emploi_filename = uploaded_emploi.name
                st.rerun()

    st.markdown("---")
    st.markdown("**⚙️ Filtres**")
    filtrer_i9r = st.checkbox("✅ I9R=1", value=True)

# =============================================================================
# HEADER
# =============================================================================
st.markdown(f"""
<div class="header">
  {'<img src="data:image/png;base64,' + _logo_b64 + '" style="height:56px; border-radius:6px; background:rgba(255,255,255,0.9); padding:5px; flex-shrink:0;">' if _logo_b64 else '<div style="width:48px;height:48px;background:rgba(255,255,255,0.15);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0;">📊</div>'}
  <div class="header-text">
    <h1>ENTE — Contrôle Qualité</h1>
    <p>Enquête Nationale Trimestrielle sur l'Emploi · ANSADE Mauritanie</p>
  </div>
  <div class="header-badge">ENTE 2026</div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# MODULE 1: EXHAUSTIVITÉ
# =============================================================================
if module == "📋 Exhaustivité":
    if st.session_state.df_menage is None:
        st.info("👆 Veuillez charger la base ménage dans la barre latérale")
    else:
        df = apply_filters(st.session_state.df_menage, filtrer_i9r)

        for c in ["I1", "I2", "I10"]:
            if c not in df.columns:
                st.error(f"❌ Colonne manquante: {c}")
                st.stop()

        with st.expander("🔍 Filtres Avancés", expanded=False):
            col1, col2, col3 = st.columns(3)

            with col1:
                if "I10" in df.columns:
                    equipes_dispo = sorted(pd.to_numeric(df["I10"], errors="coerce").dropna().unique())
                    equipes_labels = [f"{int(e)} - {get_label_equipe(e)}" for e in equipes_dispo]
                    selected_equipes = st.multiselect("Équipes", equipes_labels, default=equipes_labels)
                    if selected_equipes:
                        codes = [int(s.split(" - ")[0]) for s in selected_equipes]
                        df = df[df["I10"].isin(codes)]

            with col2:
                if "I1W" in df.columns:
                    df = create_wilaya_label(df)
                    wilayas_dispo = sorted(df["wilaya_label"].unique())
                    selected_wilayas = st.multiselect("Wilayas", wilayas_dispo, default=wilayas_dispo)
                    if selected_wilayas:
                        df = df[df["wilaya_label"].isin(selected_wilayas)]

            with col3:
                if all(c in df.columns for c in ["I1W", "I1MI"]):
                    df = create_strate(df)
                    strates_dispo = sorted(df["strate_label"].unique())
                    selected_strates = st.multiselect("Strates", strates_dispo, default=strates_dispo)
                    if selected_strates:
                        df = df[df["strate_label"].isin(selected_strates)]

        df["idmen"] = df["I1"].astype("Int64").astype(str) + "-" + df["I2"].astype("Int64").astype(str)
        df["nb_doublons"] = df.groupby("idmen")["idmen"].transform("count")
        doublons = df[df["nb_doublons"] > 1].copy()

        stats_grappes = df.groupby(["I1", "I10"]).agg(nb_menages=("I2", "count")).reset_index()
        stats_grappes["statut"] = np.where(stats_grappes["nb_menages"] >= 15, "✅ Complet", "⚠️ Incomplet")

        stats_equipes = df.groupby("I10").agg(nb_menages=("I2", "count"), nb_grappes=("I1", "nunique")).reset_index()

        if len(doublons) > 0:
            dbl_eq = doublons.groupby("I10")["idmen"].nunique().reset_index(name="nb_doublons")
            stats_equipes = stats_equipes.merge(dbl_eq, on="I10", how="left")
            stats_equipes["nb_doublons"] = stats_equipes["nb_doublons"].fillna(0).astype(int)
        else:
            stats_equipes["nb_doublons"] = 0

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("🏠 Ménages", f"{len(df):,}")
        with c2: st.metric("🗺️ Grappes", f"{df['I1'].nunique():,}")
        with c3: st.metric("👥 Équipes", f"{df['I10'].nunique():,}")
        with c4:
            nb_dbl = doublons["idmen"].nunique() if len(doublons) else 0
            st.metric("⚠️ Doublons", f"{nb_dbl:,}")

        st.markdown("---")

        tab1, tab2, tab3, tab4 = st.tabs(["📊 Vue d'Ensemble", "👥 Par Équipe", "🗺️ Par Grappe", "⚠️ Doublons"])

        with tab1:
            col1, col2 = st.columns(2)

            # ── Graphique 1 : Ménages par Équipe ──────────────────────────────
            with col1:
                st.markdown("### Ménages par Équipe")
                men_sorted = stats_equipes.sort_values("I10", ascending=True).copy()
                men_sorted["code_str"] = men_sorted["I10"].apply(lambda x: str(int(x)))
                fig = px.bar(
                    men_sorted, x="code_str", y="nb_menages",
                    color="nb_menages",
                    color_continuous_scale=[
                        [0.0,  "#cce4f6"],
                        [0.33, "#5aace3"],
                        [0.66, "#1a6db5"],
                        [1.0,  "#0a2d6e"],
                    ],
                    text="nb_menages"
                )
                fig.update_traces(
                    texttemplate='%{text:,}',
                    textposition='outside',
                    marker_line_width=0,
                )
                fig.update_layout(
                    height=420,
                    showlegend=False,
                    coloraxis_showscale=False,
                    xaxis_title="Équipe",
                    yaxis_title="Nombre de Ménages",
                    xaxis=dict(
                        tickfont=dict(size=12),
                        tickmode='array',
                        tickvals=men_sorted["code_str"].tolist(),
                        ticktext=men_sorted["code_str"].tolist(),
                        categoryorder='array',
                        categoryarray=men_sorted["code_str"].tolist(),
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=40, r=20, t=40, b=40),
                )
                fig.update_xaxes(showgrid=False, showline=False, zeroline=False)
                fig.update_yaxes(showgrid=False, showline=False, zeroline=False)
                st.plotly_chart(fig, width='stretch')

            # ── Graphique 2 : Grappes par Équipe ──────────────────────────────
            with col2:
                st.markdown("### Grappes par Équipe")
                gr_sorted = stats_equipes.sort_values("I10", ascending=True).copy()
                gr_sorted["code_str"] = gr_sorted["I10"].apply(lambda x: str(int(x)))
                fig = px.bar(
                    gr_sorted, x="code_str", y="nb_grappes",
                    color="nb_grappes",
                    color_continuous_scale=[
                        [0.0,  "#c8ecd7"],
                        [0.33, "#52b87a"],
                        [0.66, "#1a7d45"],
                        [1.0,  "#0a3d21"],
                    ],
                    text="nb_grappes"
                )
                fig.update_traces(
                    texttemplate='%{text:,}',
                    textposition='outside',
                    marker_line_width=0,
                )
                fig.update_layout(
                    height=420,
                    showlegend=False,
                    coloraxis_showscale=False,
                    xaxis_title="Équipe",
                    yaxis_title="Nombre de Grappes",
                    xaxis=dict(
                        tickfont=dict(size=12),
                        tickmode='array',
                        tickvals=gr_sorted["code_str"].tolist(),
                        ticktext=gr_sorted["code_str"].tolist(),
                        categoryorder='array',
                        categoryarray=gr_sorted["code_str"].tolist(),
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=40, r=20, t=40, b=40),
                )
                fig.update_xaxes(showgrid=False, showline=False, zeroline=False)
                fig.update_yaxes(showgrid=False, showline=False, zeroline=False)
                st.plotly_chart(fig, width='stretch')

            st.markdown("### Distribution des Ménages par Grappe")
            fig = px.histogram(stats_grappes, x="nb_menages", nbins=30,
                               color_discrete_sequence=["#667eea"])
            fig.add_vline(x=15, line_dash="dash", line_color="#ef4444", line_width=2,
                          annotation_text="Seuil: 15", annotation_position="top right")
            fig.update_layout(height=350, xaxis_title="Nombre de Ménages", yaxis_title="Fréquence", bargap=0.1)
            st.plotly_chart(fig, width='stretch')

        with tab2:
            st.markdown("### Récapitulatif par Équipe")
            display_equipes = stats_equipes.copy()
            display_equipes["Moy_menages"] = (display_equipes["nb_menages"] / display_equipes["nb_grappes"]).round(1)
            display_equipes["Nom"] = display_equipes["I10"].apply(lambda x: get_label_equipe(x))
            display_equipes = display_equipes.rename(columns={
                "I10": "Code", "nb_menages": "Ménages", "nb_grappes": "Grappes",
                "nb_doublons": "Doublons", "Moy_menages": "Moy/Grappe"
            })
            display_equipes["Code"] = display_equipes["Code"].apply(lambda x: f"{int(x)}" if pd.notna(x) else "")

            df_to_display = display_searchable_dataframe(
                display_equipes[["Code", "Nom", "Ménages", "Grappes", "Doublons", "Moy/Grappe"]],
                key_suffix="equipes_tab2"
            )
            st.dataframe(df_to_display, width='stretch', height=400)

            # ── Tableau ménages par enquêteur avec taux de contribution ──
            st.markdown("---")
            st.markdown("### 📋 Ménages réalisés par Enquêteur et contribution au sein de l'Équipe")

            if "I11" in df.columns:
                stats_enq = df.groupby(["I10", "I11"]).agg(
                    Ménages=("I2", "count")
                ).reset_index()

                total_equipe = stats_enq.groupby("I10")["Ménages"].transform("sum")
                stats_enq["% dans l'Équipe"] = (stats_enq["Ménages"] / total_equipe * 100).round(1)
                stats_enq["Nom Équipe"]    = stats_enq["I10"].apply(lambda x: get_label_equipe(x))
                stats_enq["Nom Enquêteur"] = stats_enq["I11"].apply(lambda x: get_label_enqueteur(x))
                stats_enq = stats_enq.sort_values(["I10", "I11"], ascending=True)

                display_enq = stats_enq.rename(columns={"I10": "Code Éq.", "I11": "Code Enq."})
                display_enq = display_enq[["Code Éq.", "Nom Équipe", "Code Enq.", "Nom Enquêteur", "Ménages", "% dans l'Équipe"]]

                df_enq_display = display_searchable_dataframe(display_enq, key_suffix="enq_menages_tab2", height=450)

                def style_contribution(row):
                    v = row["% dans l'Équipe"]
                    if v >= 40:
                        return ['background-color:#dbeafe; font-weight:600'] * len(row)
                    elif v <= 15:
                        return ['background-color:#fef3c7'] * len(row)
                    return [''] * len(row)

                st.dataframe(
                    df_enq_display.style.apply(style_contribution, axis=1).format({
                        "Code Éq.":  "{:.0f}",
                        "Code Enq.": "{:.0f}",
                        "Ménages":   "{:.0f}",
                        "% dans l'Équipe": "{:.1f}",
                    }),
                    width='stretch', height=450
                )

                csv_enq = display_enq.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Télécharger Ménages par Enquêteur (CSV)",
                    data=csv_enq,
                    file_name=f"menages_enqueteurs_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    key="dl_enq_menages"
                )
            else:
                st.info("ℹ️ Colonne I11 (enquêteur) absente de la base.")

        with tab3:
            nb_incomp = int((stats_grappes["nb_menages"] < 15).sum())
            nb_comp = int((stats_grappes["nb_menages"] >= 15).sum())
            taux = (nb_comp / len(stats_grappes) * 100) if len(stats_grappes) else 0

            a, b, c = st.columns(3)
            with a: st.metric("⚠️ Incomplètes", nb_incomp)
            with b: st.metric("✅ Complètes", nb_comp)
            with c: st.metric("📊 Taux", f"{taux:.1f}%")

            st.markdown("---")
            filtre = st.multiselect("Filtrer:", ["✅ Complet", "⚠️ Incomplet"], default=["⚠️ Incomplet"])
            df_grappes_filtered = stats_grappes[stats_grappes["statut"].isin(filtre)].copy()

            display_grappes = df_grappes_filtered.rename(columns={
                "I1": "Grappe", "I10": "Équipe", "nb_menages": "Nb Ménages", "statut": "Statut"
            })
            display_grappes["Grappe"] = display_grappes["Grappe"].apply(lambda x: f"{int(x)}" if pd.notna(x) else "")
            display_grappes["Équipe"] = display_grappes["Équipe"].apply(lambda x: f"{int(x)}" if pd.notna(x) else "")

            def color_status(val):
                if "Incomplet" in str(val) or "⚠️" in str(val):
                    return 'background-color: #fee2e2; color: #991b1b; font-weight: 600'
                if "Complet" in str(val) or "✅" in str(val):
                    return 'background-color: #d1fae5; color: #065f46; font-weight: 600'
                return ''

            df_to_display = display_searchable_dataframe(display_grappes, key_suffix="grappes_tab3", height=500)
            st.dataframe(df_to_display.style.applymap(color_status, subset=["Statut"]),
                         width='stretch', height=500)

        with tab4:
            if len(doublons) == 0:
                st.success("✅ Aucun doublon")
            else:
                st.warning(f"⚠️ {doublons['idmen'].nunique():,} doublons détectés")
                cols = [c for c in ["idmen", "I1", "I2", "I10", "I11", "nb_doublons"] if c in doublons.columns]
                display_doublons = doublons[cols].sort_values(["I1", "I2"])
                
                df_to_display = display_searchable_dataframe(display_doublons, key_suffix="doublons_tab4", height=500)
                st.dataframe(
                    df_to_display.style.format({
                        "I1": "{:.0f}", "I2": "{:.0f}", "I10": "{:.0f}", "I11": "{:.0f}", "nb_doublons": "{:.0f}"
                    }),
                    width='stretch',
                    height=500
                )

# =============================================================================
# MODULE 2: EMPLOI
# =============================================================================
elif module == "💼 Emploi":
    if st.session_state.df_emploi is None:
        st.info("👆 Veuillez charger la base emploi dans la barre latérale")
    else:
        df = apply_filters(st.session_state.df_emploi, filtrer_i9r)

        for c in ["I1", "I2", "IND1", "I10"]:
            if c not in df.columns:
                st.error(f"❌ Colonne manquante: {c}")
                st.stop()

        if all(c in df.columns for c in ["I1W", "I1MI", "I1"]):
            df = create_strate(df)
            df = create_wilaya_label(df)

        with st.expander("🔍 Filtres Avancés", expanded=False):
            col1, col2, col3 = st.columns(3)

            with col1:
                if "I10" in df.columns:
                    equipes_dispo = sorted(pd.to_numeric(df["I10"], errors="coerce").dropna().unique())
                    equipes_labels = [f"{int(e)} - {get_label_equipe(e)}" for e in equipes_dispo]
                    selected_equipes = st.multiselect("Équipes", equipes_labels, default=equipes_labels)
                    if selected_equipes:
                        codes = [int(s.split(" - ")[0]) for s in selected_equipes]
                        df = df[df["I10"].isin(codes)]

            with col2:
                if "wilaya_label" in df.columns:
                    wilayas_dispo = sorted(df["wilaya_label"].unique())
                    selected_wilayas = st.multiselect("Wilayas", wilayas_dispo, default=wilayas_dispo)
                    if selected_wilayas:
                        df = df[df["wilaya_label"].isin(selected_wilayas)]

            with col3:
                if "strate_label" in df.columns:
                    strates_dispo = sorted(df["strate_label"].unique())
                    selected_strates = st.multiselect("Strates", strates_dispo, default=strates_dispo)
                    if selected_strates:
                        df = df[df["strate_label"].isin(selected_strates)]

        df = calculate_employment_indicators(df)
        df["idmen"] = df["I1"].astype("Int64").astype(str) + "-" + df["I2"].astype("Int64").astype(str)
        df["idind"] = df["idmen"] + "-" + df["IND1"].astype("Int64").astype(str)

        nb_ind = len(df)
        nb_occ = int(pd.to_numeric(df["Occupe"], errors="coerce").sum(skipna=True))
        nb_ch = int(pd.to_numeric(df["Chomage"], errors="coerce").sum(skipna=True))

        df_age = df[df["agetravail"] == 1].copy()
        t_part = safe_mean(df_age["t_part"]) if "t_part" in df_age.columns else 0
        r_emp = safe_mean(df_age["r_emploi"]) if "r_emploi" in df_age.columns else 0
        t_chom = safe_mean(df_age["t_chomage"]) if "t_chomage" in df_age.columns else 0

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("👥 Individus 14-64", f"{len(df_age):,}")
        with c2: st.metric("💼 Occupés", f"{nb_occ:,}")
        with c3: st.metric("📉 Chômeurs", f"{nb_ch:,}")
        with c4: st.metric("📊 Taux Chômage", f"{t_chom:.1f}%")

        st.markdown("---")

        tab1, tab2, tab3, tab4 = st.tabs(["📊 Indicateurs", "⏱️ Durées", "🏭 Branches", "📍 Géographie"])

        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("📈 Taux Participation", f"{t_part:.1f}%")
            with col2: st.metric("💼 Ratio Emploi", f"{r_emp:.1f}%")
            with col3: st.metric("📉 Taux Chômage", f"{t_chom:.1f}%")

            st.markdown("---")

            if "I10" in df_age.columns and len(df_age) > 0:
                st.markdown("### Indicateurs par Équipe")

                indic_equipe = df_age.groupby("I10").agg(
                    Effectif=("IND1", "count"),
                    t_part=("t_part", "mean"),
                    r_emploi=("r_emploi", "mean"),
                    t_chomage=("t_chomage", "mean")
                ).reset_index().sort_values("I10", ascending=True)
                indic_equipe["code_str"] = indic_equipe["I10"].apply(lambda x: str(int(x)))

                fig = go.Figure()
                fig.add_trace(go.Bar(name="Taux participation", x=indic_equipe["code_str"], y=indic_equipe["t_part"], marker_color="#667eea", marker_line_width=0))
                fig.add_trace(go.Bar(name="Ratio emploi", x=indic_equipe["code_str"], y=indic_equipe["r_emploi"], marker_color="#10b981", marker_line_width=0))
                fig.add_trace(go.Bar(name="Taux chômage", x=indic_equipe["code_str"], y=indic_equipe["t_chomage"], marker_color="#f59e0b", marker_line_width=0))

                fig.update_layout(
                    barmode="group", height=420,
                    xaxis_title="Équipe", yaxis_title="Taux (%)",
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=40, r=20, t=40, b=40),
                    xaxis=dict(
                        tickmode='array',
                        tickvals=indic_equipe["code_str"].tolist(),
                        ticktext=indic_equipe["code_str"].tolist(),
                        categoryorder='array',
                        categoryarray=indic_equipe["code_str"].tolist(),
                        tickfont=dict(size=12),
                        showgrid=False, showline=False, zeroline=False,
                    ),
                    yaxis=dict(showgrid=False, showline=False, zeroline=False),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, width='stretch')

                display_indic = indic_equipe.copy()
                display_indic["Nom"] = display_indic["I10"].apply(lambda x: get_label_equipe(x))
                display_indic = display_indic.rename(columns={
                    "I10": "Code",
                    "t_part": "Taux Part.",
                    "r_emploi": "Ratio Emploi",
                    "t_chomage": "Taux Chômage"
                })
                for col in ["Taux Part.", "Ratio Emploi", "Taux Chômage"]:
                    if col in display_indic.columns:
                        display_indic[col] = display_indic[col].round(1)

                df_to_display = display_searchable_dataframe(display_indic, key_suffix="indicateurs_tab1", height=400)
                st.dataframe(
                    df_to_display.style.format({
                        "Code": "{:.0f}",
                        "Effectif": "{:.0f}",
                        "Taux Part.": "{:.1f}",
                        "Ratio Emploi": "{:.1f}",
                        "Taux Chômage": "{:.1f}"
                    }),
                    width='stretch',
                    height=400
                )

            if "I11" in df_age.columns and len(df_age) > 0:
                st.markdown("---")
                st.markdown("### 🧑‍💼 Indicateurs par Enquêteur")

                indic_enqueteur = df_age.groupby(["I10", "I11"]).agg(
                    Effectif=("IND1", "count"),
                    t_part=("t_part", "mean"),
                    r_emploi=("r_emploi", "mean"),
                    t_chomage=("t_chomage", "mean"),
                ).reset_index().sort_values(["I10", "I11"])

                indic_enqueteur["Nom Équipe"] = indic_enqueteur["I10"].apply(lambda x: get_label_equipe(x))
                indic_enqueteur["Nom Enquêteur"] = indic_enqueteur["I11"].apply(lambda x: get_label_enqueteur(x))

                display_enq = indic_enqueteur.rename(columns={
                    "I10": "Code Éq.",
                    "I11": "Code Enq.",
                    "t_part": "Taux Part.",
                    "r_emploi": "Ratio Emploi",
                    "t_chomage": "Taux Chômage",
                })

                for col in ["Taux Part.", "Ratio Emploi", "Taux Chômage"]:
                    if col in display_enq.columns:
                        display_enq[col] = display_enq[col].round(1)

                cols_enq = [
                    "Code Éq.", "Nom Équipe", "Code Enq.", "Nom Enquêteur",
                    "Effectif", "Taux Part.", "Ratio Emploi", "Taux Chômage"
                ]
                cols_enq = [c for c in cols_enq if c in display_enq.columns]

                top20_enq = indic_enqueteur.sort_values("Effectif", ascending=False).head(20).copy()
                top20_enq["label"] = top20_enq.apply(
                    lambda x: f"Éq.{int(x['I10'])} - {get_label_enqueteur(x['I11']).split(' ')[0]} ({int(x['I11'])})", axis=1
                )

                fig = go.Figure()
                fig.add_trace(go.Bar(name="Taux Part.", x=top20_enq["label"], y=top20_enq["t_part"], marker_color="#667eea"))
                fig.add_trace(go.Bar(name="Ratio Emploi", x=top20_enq["label"], y=top20_enq["r_emploi"], marker_color="#10b981"))
                fig.add_trace(go.Bar(name="Taux Chômage", x=top20_enq["label"], y=top20_enq["t_chomage"], marker_color="#f59e0b"))
                fig.update_layout(
                    barmode="group", height=450,
                    xaxis_title="", yaxis_title="Taux (%)",
                    xaxis_tickangle=-45,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, width='stretch')

                df_enq_display = display_searchable_dataframe(
                    display_enq[cols_enq],
                    key_suffix="enqueteurs_indic_tab1",
                    height=450
                )

                def style_chomage_enq(row):
                    tc = row.get("Taux Chômage", 0)
                    if tc > 30:
                        return ['background-color: #fee2e2'] * len(row)
                    elif tc > 20:
                        return ['background-color: #fed7aa'] * len(row)
                    return [''] * len(row)

                styled_enq = df_enq_display.style.apply(style_chomage_enq, axis=1)

                fmt_enq = {
                    "Code Éq.": "{:.0f}", "Code Enq.": "{:.0f}",
                    "Effectif": "{:.0f}",
                    "Taux Part.": "{:.1f}", "Ratio Emploi": "{:.1f}",
                    "Taux Chômage": "{:.1f}"
                }
                fmt_enq = {k: v for k, v in fmt_enq.items() if k in cols_enq}

                st.dataframe(
                    styled_enq.format(fmt_enq),
                    width='stretch',
                    height=450
                )

                csv_enq = display_enq[cols_enq].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Télécharger Indicateurs par Enquêteur (CSV)",
                    data=csv_enq,
                    file_name=f"indicateurs_enqueteurs_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    key="dl_enqueteurs_indic"
                )

        with tab2:
            dur_men_moy, dur_ind_moy = 0.0, 0.0
            pct_men_rapide = pd.DataFrame()
            pct_emploi_rapide = pd.DataFrame()
            dur_men_data = pd.DataFrame()
            occ = pd.DataFrame()

            if all(c in df.columns for c in ["MENHH1", "MENMM1", "IND5H", "IND5M"]):
                df["dur_men_min"] = np.where(
                    df["MENHH1"].notna() & df["MENMM1"].notna() & df["IND5H"].notna() & df["IND5M"].notna(),
                    (df["IND5H"] * 60 + df["IND5M"]) - (df["MENHH1"] * 60 + df["MENMM1"]),
                    np.nan
                )

                dur_men_data = df[df["IND1"] == 1].copy()
                dur_men_moy = safe_mean(dur_men_data["dur_men_min"])

                if "I10" in df.columns and "I11" in df.columns and len(dur_men_data) > 0:
                    pct_men_rapide = dur_men_data.groupby(["I10", "I11"]).agg(
                        total_menages=("dur_men_min", "count"),
                        moins_10min=("dur_men_min", lambda x: (x < 10).sum()),
                        duree_moy=("dur_men_min", "mean"),
                    ).reset_index()

                    pct_men_rapide["pct_moins_10min"] = (
                        pct_men_rapide["moins_10min"] / pct_men_rapide["total_menages"] * 100
                    ).round(1)
                    pct_men_rapide["duree_moy"] = pct_men_rapide["duree_moy"].round(1)
                    pct_men_rapide = pct_men_rapide.sort_values("pct_moins_10min", ascending=False)

            if (df["Occupe"] == 1).any() and all(c in df.columns for c in ["IND5FH", "IND5FM", "IND5H", "IND5M"]):
                occ = df[df["Occupe"] == 1].copy()
                occ["dur_ind_min"] = np.where(
                    occ["IND5H"].notna() & occ["IND5M"].notna() & occ["IND5FH"].notna() & occ["IND5FM"].notna(),
                    (occ["IND5FH"] * 60 + occ["IND5FM"]) - (occ["IND5H"] * 60 + occ["IND5M"]),
                    np.nan
                )
                dur_ind_moy = safe_mean(occ["dur_ind_min"])

                if "I10" in occ.columns and "I11" in occ.columns and len(occ) > 0:
                    pct_emploi_rapide = occ.groupby(["I10", "I11"]).agg(
                        total_emplois=("dur_ind_min", "count"),
                        moins_5min=("dur_ind_min", lambda x: (x <= 5).sum()),
                        duree_moy=("dur_ind_min", "mean"),
                    ).reset_index()

                    pct_emploi_rapide["pct_moins_5min"] = (
                        pct_emploi_rapide["moins_5min"] / pct_emploi_rapide["total_emplois"] * 100
                    ).round(1)
                    pct_emploi_rapide["duree_moy"] = pct_emploi_rapide["duree_moy"].round(1)
                    pct_emploi_rapide = pct_emploi_rapide.sort_values("pct_moins_5min", ascending=False)

            col1, col2 = st.columns(2)
            with col1: st.metric("⏱️ Durée Moy. Ménage", f"{dur_men_moy:.1f} min")
            with col2: st.metric("👤 Durée Moy. Emploi", f"{dur_ind_moy:.1f} min")

            st.markdown("---")

            sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📊 Analyse Ménages", "💼 Analyse Emploi", "📈 Distributions"])

            with sub_tab1:
                if len(pct_men_rapide) > 0:
                    st.markdown("### 📊 Analyse Détaillée des Durées Ménages par Enquêteur")

                    total_moins_10 = pct_men_rapide["moins_10min"].sum()
                    total_menages = pct_men_rapide["total_menages"].sum()
                    pct_global = (total_moins_10 / total_menages * 100) if total_menages > 0 else 0

                    a, b, c = st.columns(3)
                    with a: st.metric("% Global < 10 min", f"{pct_global:.1f}%")
                    with b: st.metric("Nb Total Ménages", f"{total_menages:,}")
                    with c: st.metric("Nb Total < 10 min", f"{total_moins_10:,}")

                    st.markdown("---")

                    col1, col2 = st.columns(2)
                    with col1:
                        seuil_alert = st.slider("Seuil d'alerte (%)", 0, 100, 30, 5, key="seuil_men")
                    with col2:
                        show_all = st.checkbox("Afficher tous les enquêteurs", value=True, key="show_all_men")

                    display_men = pct_men_rapide.copy() if show_all else pct_men_rapide[pct_men_rapide["pct_moins_10min"] >= seuil_alert].copy()

                    display_men["Nom_Equipe"] = display_men["I10"].apply(lambda x: get_label_equipe(x))
                    display_men["Nom_Enqueteur"] = display_men["I11"].apply(lambda x: get_label_enqueteur(x))

                    display_men_final = display_men[[
                        "I10", "Nom_Equipe", "I11", "Nom_Enqueteur",
                        "total_menages", "moins_10min", "pct_moins_10min", "duree_moy"
                    ]].rename(columns={
                        "I10": "Code Équipe",
                        "Nom_Equipe": "Équipe",
                        "I11": "Code Enq.",
                        "Nom_Enqueteur": "Enquêteur",
                        "total_menages": "Total",
                        "moins_10min": "< 10 min",
                        "pct_moins_10min": "% < 10 min",
                        "duree_moy": "Moy."
                    })

                    def style_menage_row(row):
                        v = row["% < 10 min"]
                        if v > 50:
                            return ['background-color: #fee2e2; font-weight: 600'] * len(row)
                        elif v > 30:
                            return ['background-color: #fed7aa; font-weight: 600'] * len(row)
                        elif v > 15:
                            return ['background-color: #fef3c7'] * len(row)
                        elif v > 0:
                            return ['background-color: #d1fae5'] * len(row)
                        return [''] * len(row)

                    df_to_display = display_searchable_dataframe(display_men_final, key_suffix="menages_duree", height=420)
                    styled_df = df_to_display.style.apply(style_menage_row, axis=1)
                    st.dataframe(
                        styled_df.format({
                            "Code Équipe": "{:.0f}",
                            "Code Enq.": "{:.0f}",
                            "Total": "{:.0f}",
                            "< 10 min": "{:.0f}",
                            "% < 10 min": "{:.1f}",
                            "Moy.": "{:.1f}"
                        }),
                        width='stretch',
                        height=420
                    )

                    st.markdown("---")
                    st.markdown("### 📊 Enquêteurs avec % Questionnaire Ménages < 10 min")

                    chart_men = pct_men_rapide[pct_men_rapide["pct_moins_10min"] > 0].copy()
                    chart_men = chart_men.sort_values("pct_moins_10min", ascending=True)
                    chart_men["label"] = chart_men.apply(
                        lambda x: f"Équipe {int(x['I10'])} - Enq. {int(x['I11'])}", axis=1
                    )

                    fig = px.bar(
                        chart_men,
                        x="pct_moins_10min",
                        y="label",
                        orientation="h",
                        color="pct_moins_10min",
                        color_continuous_scale=["#10b981", "#fbbf24", "#f59e0b", "#ef4444"],
                        text="pct_moins_10min"
                    )
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', marker_line_width=0)
                    fig.update_layout(
                        height=min(500, max(300, len(chart_men) * 30 + 60)),
                        showlegend=False,
                        coloraxis_showscale=False,
                        xaxis_title="% Entretiens < 10 min",
                        yaxis_title="",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=10, r=60, t=20, b=40),
                        xaxis=dict(showgrid=False, showline=False, zeroline=False),
                        yaxis=dict(showgrid=False, showline=False, zeroline=False,
                                   tickfont=dict(size=11)),
                    )
                    fig.add_vline(x=30, line_dash="dash", line_color="#ef4444", line_width=2,
                                  annotation_text="Seuil: 30%", annotation_position="top right")
                    st.plotly_chart(fig, width='stretch')

                    st.markdown("---")
                    csv_men = display_men_final.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger Rapport Ménages (CSV)",
                        data=csv_men,
                        file_name=f"analyse_durees_menages_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("ℹ️ Données de durée ménage non disponibles")

            with sub_tab2:
                if len(pct_emploi_rapide) > 0:
                    st.markdown("### 💼 Analyse Détaillée des Durées Emploi par Enquêteur")

                    total_moins_5 = pct_emploi_rapide["moins_5min"].sum()
                    total_emplois = pct_emploi_rapide["total_emplois"].sum()
                    pct_global = (total_moins_5 / total_emplois * 100) if total_emplois > 0 else 0

                    a, b, c = st.columns(3)
                    with a: st.metric("% Global ≤ 5 min", f"{pct_global:.1f}%")
                    with b: st.metric("Nb Total Emplois", f"{total_emplois:,}")
                    with c: st.metric("Nb Total ≤ 5 min", f"{total_moins_5:,}")

                    st.markdown("---")

                    col1, col2 = st.columns(2)
                    with col1:
                        seuil_alert_emp = st.slider("Seuil d'alerte (%)", 0, 100, 30, 5, key="seuil_emp")
                    with col2:
                        show_all_emp = st.checkbox("Afficher tous les enquêteurs", value=True, key="show_all_emp")

                    display_emp = pct_emploi_rapide.copy() if show_all_emp else pct_emploi_rapide[pct_emploi_rapide["pct_moins_5min"] >= seuil_alert_emp].copy()

                    display_emp["Nom_Equipe"] = display_emp["I10"].apply(lambda x: get_label_equipe(x))
                    display_emp["Nom_Enqueteur"] = display_emp["I11"].apply(lambda x: get_label_enqueteur(x))

                    display_emp_final = display_emp[[
                        "I10", "Nom_Equipe", "I11", "Nom_Enqueteur",
                        "total_emplois", "moins_5min", "pct_moins_5min", "duree_moy"
                    ]].rename(columns={
                        "I10": "Code Équipe",
                        "Nom_Equipe": "Équipe",
                        "I11": "Code Enq.",
                        "Nom_Enqueteur": "Enquêteur",
                        "total_emplois": "Total",
                        "moins_5min": "≤ 5 min",
                        "pct_moins_5min": "% ≤ 5 min",
                        "duree_moy": "Moy."
                    })

                    def style_emploi_row(row):
                        v = row["% ≤ 5 min"]
                        if v > 50:
                            return ['background-color: #fee2e2; font-weight: 600'] * len(row)
                        elif v > 30:
                            return ['background-color: #fed7aa; font-weight: 600'] * len(row)
                        elif v > 15:
                            return ['background-color: #fef3c7'] * len(row)
                        elif v > 0:
                            return ['background-color: #d1fae5'] * len(row)
                        return [''] * len(row)

                    df_to_display = display_searchable_dataframe(display_emp_final, key_suffix="emploi_duree", height=420)
                    styled_df = df_to_display.style.apply(style_emploi_row, axis=1)
                    st.dataframe(
                        styled_df.format({
                            "Code Équipe": "{:.0f}",
                            "Code Enq.": "{:.0f}",
                            "Total": "{:.0f}",
                            "≤ 5 min": "{:.0f}",
                            "% ≤ 5 min": "{:.1f}",
                            "Moy.": "{:.1f}"
                        }),
                        width='stretch',
                        height=420
                    )

                    st.markdown("---")
                    st.markdown("### Enquêteurs avec % Individu en Emplois ≤ 5 min ")

                    chart_emp = pct_emploi_rapide[pct_emploi_rapide["pct_moins_5min"] > 0].copy()
                    chart_emp = chart_emp.sort_values("pct_moins_5min", ascending=True)
                    chart_emp["label"] = chart_emp.apply(
                        lambda x: f"Équipe {int(x['I10'])} - Enq. {int(x['I11'])}", axis=1
                    )

                    fig = px.bar(
                        chart_emp,
                        x="pct_moins_5min",
                        y="label",
                        orientation="h",
                        color="pct_moins_5min",
                        color_continuous_scale=["#10b981", "#fbbf24", "#f59e0b", "#ef4444"],
                        text="pct_moins_5min"
                    )
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', marker_line_width=0)
                    fig.update_layout(
                        height=min(500, max(300, len(chart_emp) * 30 + 60)),
                        showlegend=False,
                        coloraxis_showscale=False,
                        xaxis_title="% Entretiens ≤ 5 min",
                        yaxis_title="",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=10, r=60, t=20, b=40),
                        xaxis=dict(showgrid=False, showline=False, zeroline=False),
                        yaxis=dict(showgrid=False, showline=False, zeroline=False,
                                   tickfont=dict(size=11)),
                    )
                    fig.add_vline(x=30, line_dash="dash", line_color="#ef4444", line_width=2,
                                  annotation_text="Seuil: 30%", annotation_position="top right")
                    st.plotly_chart(fig, width='stretch')

                    st.markdown("---")
                    csv_emp = display_emp_final.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger Rapport Emploi (CSV)",
                        data=csv_emp,
                        file_name=f"analyse_durees_emploi_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("ℹ️ Données de durée emploi non disponibles")

            with sub_tab3:
                st.markdown("### 📈 Distributions des Durées d'Entretien")
                col1, col2 = st.columns(2)

                with col1:
                    if len(dur_men_data) > 0 and "dur_men_min" in dur_men_data.columns and dur_men_data["dur_men_min"].notna().any():
                        st.markdown("#### Distribution Durées Ménage")
                        dur_men_clean = dur_men_data[dur_men_data["dur_men_min"].notna()].copy()
                        fig = px.histogram(dur_men_clean, x="dur_men_min", nbins=40,
                                           color_discrete_sequence=["#667eea"], marginal="box")
                        fig.add_vline(x=10, line_dash="dash", line_color="#ef4444", line_width=2,
                                      annotation_text="< 10 min", annotation_position="top right")
                        fig.update_layout(height=350, xaxis_title="Durée (minutes)", yaxis_title="Fréquence", showlegend=False)
                        st.plotly_chart(fig, width='stretch')

                with col2:
                    if len(occ) > 0 and "dur_ind_min" in occ.columns and occ["dur_ind_min"].notna().any():
                        st.markdown("#### Distribution Durées Emploi")
                        occ_clean = occ[occ["dur_ind_min"].notna()].copy()
                        fig = px.histogram(occ_clean, x="dur_ind_min", nbins=40,
                                           color_discrete_sequence=["#10b981"], marginal="box")
                        fig.add_vline(x=5, line_dash="dash", line_color="#ef4444", line_width=2,
                                      annotation_text="≤ 5 min", annotation_position="top right")
                        fig.update_layout(height=350, xaxis_title="Durée (minutes)", yaxis_title="Fréquence", showlegend=False)
                        st.plotly_chart(fig, width='stretch')

        with tab3:
            if "AP2A" in df.columns or "AP2AC1" in df.columns:
                br = df[df["Occupe"] == 1].copy()
                nb_avec = len(br[br["AP2A"].notna() | br["AP2AC1"].notna()]) if all(c in br.columns for c in ["AP2A", "AP2AC1"]) else 0
                nb_sans = max(nb_occ - nb_avec, 0)
                taux = (nb_avec / nb_occ * 100) if nb_occ > 0 else 0

                a, b, c = st.columns(3)
                with a: st.metric("✅ Avec Branche", f"{nb_avec:,}")
                with b: st.metric("❌ Sans Branche", f"{nb_sans:,}")
                with c: st.metric("📊 Taux", f"{taux:.1f}%")

                if "AP2A" in br.columns and br["AP2A"].notna().any():
                    st.markdown("---")
                    st.markdown("### Top 15 Branches")
                    top = br["AP2A"].value_counts().head(15).reset_index()
                    top.columns = ["Branche", "Effectif"]
                    fig = px.bar(top, x="Effectif", y="Branche", orientation="h",
                                 color="Effectif", color_continuous_scale="Oranges")
                    fig.update_layout(height=500, showlegend=False, yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig, width='stretch')

                st.markdown("---")
                st.markdown("### 📋 Détail des Branches d'Activité par Individu")

                LABELS_AP2AC1 = {
                    "A01001": "Cultures de céréales", "A01002": "Culture de légumes frais",
                    "A01003": "Culture de fruits", "A01004": "Autres cultures",
                    "A01005": "Activités de soutien à la culture",
                    "A02001": "Élevage d'animaux sur pieds", "A02002": "Élevage de volailles",
                    "A02003": "Autres activités liées à l'élevage",
                    "A03000": "Sylviculture, Exploitation forestière et Cueillette",
                    "A04000": "Pêche, pisciculture et aquaculture",
                    "B05001": "Extraction de pétrole brut et de gaz naturel",
                    "B05002": "Extraction de minerais de fer",
                    "B05003": "Extraction d'autres minerais métalliques non ferreux",
                    "B05004": "Autres activités extractives",
                    "B05005": "Activités de soutien aux industries extractives",
                    "C06001": "Abattage, transformation et conservation des viandes",
                    "C06002": "Transformation, conservation de poissons",
                    "C06003": "Fabrication de produits laitiers et de glaces",
                    "C06004": "Travail des grains, Fabrication de produits amylacés",
                    "C06005": "Fabrication de produits alimentaires à base de céréales",
                    "C06006": "Fabrication de boissons",
                    "C06007": "Autres industries agroalimentaires",
                    "C07001": "Fabrication de textile et d'articles d'habillement",
                    "C07002": "Travail du cuir, fabrication de chaussures",
                    "C07003": "Fabrication d'articles en bois, liège et sparterie",
                    "C07004": "Fabrication de papiers, cartons",
                    "C07005": "Imprimerie et enregistrements sonores",
                    "C07006": "Raffinage pétrolier et cokéfaction",
                    "C07007": "Fabrication de produits chimiques, caoutchouc, plastique",
                    "C07008": "Fabrication de ciment, verre, matériaux de construction",
                    "C07009": "Métallurgie et fonderie, ouvrages en métaux",
                    "C07010": "Fabrication de machines, appareils électriques",
                    "C07011": "Autres activités manufacturières n.c.a.",
                    "C07012": "Réparation et installation de machines",
                    "D08000": "Production et distribution d'électricité et de gaz",
                    "E08001": "Captage, traitement et distribution d'eau",
                    "E08002": "Assainissement, traitement des déchets",
                    "F09001": "Construction de bâtiments",
                    "F09002": "Travaux de génie civil",
                    "F09003": "Activités spécialisées de construction",
                    "G10001": "Commerce",
                    "G10002": "Entretien et réparation de véhicules",
                    "H11001": "Transports ferroviaires", "H11002": "Transports routiers",
                    "H11003": "Autres transports terrestres",
                    "H11004": "Transports maritimes et fluviales",
                    "H11005": "Transports aériens",
                    "H11006": "Entreposages et auxiliaires de transport",
                    "H11007": "Activités de poste et de courrier",
                    "I11000": "Activités de restauration et d'hébergement",
                    "J11001": "Télécommunications",
                    "J11002": "Autres activités d'information et de communication",
                    "K12001": "Activités de banque centrale",
                    "K12002": "Activités financières",
                    "K12003": "Activités d'assurance",
                    "K12004": "Activités d'auxiliaires financiers et d'assurance",
                    "L13000": "Activités immobilières",
                    "M13000": "Activités spécialisées, scientifiques et techniques",
                    "N13000": "Activités de soutien et de bureau",
                    "O14001": "Administration générale, économique, sociale",
                    "O14002": "Sécurité sociale obligatoire",
                    "P15000": "Enseignement",
                    "Q16000": "Santé humaine et action sociale",
                    "R17000": "Activités artistiques, spectacle et récréatives",
                    "S17001": "Activités des organisations associatives",
                    "S17002": "Réparation d'ordinateurs et articles personnels",
                    "S17003": "Autres activités de service personnels n.c.a.",
                    "T17000": "Activités des ménages employeurs de personnel domestique",
                    "U19000": "Correction territoriale",
                }

                br_ap3 = br.copy()
                st.caption(f"🔎 Filtre : Occupé = 1 → **{len(br_ap3):,}** individus occupés")

                if len(br_ap3) > 0:
                    display_br = br_ap3.copy()

                    if "AP2AC1" in display_br.columns:
                        display_br["Libellé Branche"] = display_br["AP2AC1"].astype(str).map(LABELS_AP2AC1).fillna("—")

                    if "I10" in display_br.columns:
                        display_br["Nom Équipe"] = display_br["I10"].apply(lambda x: get_label_equipe(x) if pd.notna(x) else "")
                    if "I11" in display_br.columns:
                        display_br["Nom Enquêteur"] = display_br["I11"].apply(lambda x: get_label_enqueteur(x) if pd.notna(x) else "")

                    cols_br = []
                    for c in ["idmen", "idind", "I10", "Nom Équipe", "I11", "Nom Enquêteur", "AP2A", "AP2AC1", "Libellé Branche", "AP2AC"]:
                        if c in display_br.columns:
                            cols_br.append(c)

                    display_br_final = display_br[cols_br].rename(columns={
                        "idmen": "ID Ménage",
                        "idind": "ID Individu",
                        "I10": "Équipe",
                        "I11": "Enquêteur",
                        "AP2A": "Branche",
                        "AP2AC1": "Code Activité",
                        "AP2AC": "AP2AC",
                    })

                    df_br_display = display_searchable_dataframe(
                        display_br_final,
                        key_suffix="branches_detail",
                        height=500
                    )

                    fmt_br = {}
                    for c in ["Équipe", "Enquêteur"]:
                        if c in display_br_final.columns:
                            fmt_br[c] = "{:.0f}"

                    if fmt_br:
                        st.dataframe(df_br_display.style.format(fmt_br), width='stretch', height=500)
                    else:
                        st.dataframe(df_br_display, width='stretch', height=500)

                    csv_br = display_br_final.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger Détail Branches (CSV)",
                        data=csv_br,
                        file_name=f"detail_branches_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        key="dl_branches_detail"
                    )
                else:
                    st.info("ℹ️ Aucun individu occupé")

        with tab4:
            if "strate_label" in df.columns and len(df_age) > 0:
                st.markdown("### Indicateurs par Strate")
                indic_strate = df_age.groupby("strate_label").agg(
                    Effectif=("IND1", "count"),
                    t_part=("t_part", "mean"),
                    r_emploi=("r_emploi", "mean"),
                    t_chomage=("t_chomage", "mean")
                ).reset_index()

                long = indic_strate.melt(
                    id_vars=["strate_label"],
                    value_vars=["t_part", "r_emploi", "t_chomage"],
                    var_name="Indicateur",
                    value_name="Valeur"
                )

                fig = px.bar(long, x="strate_label", y="Valeur", color="Indicateur",
                             barmode="group",
                             color_discrete_map={"t_part": "#667eea", "r_emploi": "#10b981", "t_chomage": "#f59e0b"})
                fig.update_layout(height=400, xaxis_tickangle=-30, xaxis_title="Strate", yaxis_title="Taux (%)")
                st.plotly_chart(fig, width='stretch')

            if "wilaya_label" in df.columns and len(df_age) > 0:
                st.markdown("---")
                st.markdown("### Indicateurs par Wilaya")

                indic_wilaya = df_age.groupby("wilaya_label").agg(
                    Effectif=("IND1", "count"),
                    t_part=("t_part", "mean"),
                    r_emploi=("r_emploi", "mean"),
                    t_chomage=("t_chomage", "mean")
                ).reset_index().sort_values("Effectif", ascending=False)

                long_wilaya = indic_wilaya.melt(
                    id_vars=["wilaya_label"],
                    value_vars=["t_part", "r_emploi", "t_chomage"],
                    var_name="Indicateur",
                    value_name="Valeur"
                )

                fig = px.bar(
                    long_wilaya,
                    x="wilaya_label",
                    y="Valeur",
                    color="Indicateur",
                    barmode="group",
                    color_discrete_map={
                        "t_part": "#667eea",
                        "r_emploi": "#10b981",
                        "t_chomage": "#f59e0b"
                    }
                )
                fig.update_layout(
                    height=450,
                    xaxis_tickangle=-45,
                    xaxis_title="Wilaya",
                    yaxis_title="Taux (%)",
                    legend=dict(
                        title="Indicateur",
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                st.plotly_chart(fig, width='stretch')

                st.markdown("---")
                st.markdown("### 📋 Tableau Détaillé par Wilaya")

                display_wilaya = indic_wilaya.copy()
                display_wilaya = display_wilaya.rename(columns={
                    "wilaya_label": "Wilaya",
                    "t_part": "Taux Part.",
                    "r_emploi": "Ratio Emploi",
                    "t_chomage": "Taux Chômage"
                })

                for col in ["Taux Part.", "Ratio Emploi", "Taux Chômage"]:
                    if col in display_wilaya.columns:
                        display_wilaya[col] = display_wilaya[col].round(1)

                df_to_display = display_searchable_dataframe(
                    display_wilaya[["Wilaya", "Effectif", "Taux Part.", "Ratio Emploi", "Taux Chômage"]],
                    key_suffix="wilaya_geo",
                    height=400
                )

                st.dataframe(
                    df_to_display.style.format({
                        "Effectif": "{:.0f}",
                        "Taux Part.": "{:.1f}",
                        "Ratio Emploi": "{:.1f}",
                        "Taux Chômage": "{:.1f}"
                    }),
                    width='stretch',
                    height=400
                )

# =============================================================================
# MODULE 3: VUE CONSOLIDÉE
# =============================================================================
elif module == "📊 Vue Consolidée":
    if st.session_state.df_menage is None or st.session_state.df_emploi is None:
        missing = []
        if st.session_state.df_menage is None:
            missing.append("base ménage")
        if st.session_state.df_emploi is None:
            missing.append("base emploi")
        st.info(f"👆 Veuillez charger la **{' et la '.join(missing)}** dans la barre latérale")
    else:
        df_men = apply_filters(st.session_state.df_menage, filtrer_i9r)
        df_emp = apply_filters(st.session_state.df_emploi, filtrer_i9r)

        df_emp = calculate_employment_indicators(df_emp)
        df_age = df_emp[df_emp["agetravail"] == 1].copy()

        nb_menages = len(df_men)
        nb_grappes = df_men["I1"].nunique() if "I1" in df_men.columns else 0
        nb_individus = len(df_age)
        nb_occ = int(pd.to_numeric(df_emp["Occupe"], errors="coerce").sum(skipna=True))
        t_chom = safe_mean(df_age["t_chomage"]) if "t_chomage" in df_age.columns else 0

        st.markdown("### 📊 Vue d'Ensemble Consolidée")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.metric("🏠 Ménages", f"{nb_menages:,}")
        with c2: st.metric("🗺️ Grappes", f"{nb_grappes:,}")
        with c3: st.metric("👥 Individus 14-64", f"{nb_individus:,}")
        with c4: st.metric("💼 Occupés", f"{nb_occ:,}")
        with c5: st.metric("📊 Taux Chômage", f"{t_chom:.1f}%")

        st.markdown("---")

        tab1, tab2 = st.tabs(["📈 Progression Terrain", "💼 Indicateurs Emploi"])

        with tab1:
            st.markdown("### Progression de la Collecte par Équipe")

            if "I10" in df_men.columns:
                stats_equipes = df_men.groupby("I10").agg(
                    Ménages=("I2", "count"),
                    Grappes=("I1", "nunique")
                ).reset_index()

                stats_equipes["Nom"] = stats_equipes["I10"].apply(lambda x: get_label_equipe(x))
                stats_equipes = stats_equipes.rename(columns={"I10": "Code"})

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### Ménages Collectés")
                    men_cons = stats_equipes.sort_values("Code", ascending=True).copy()
                    men_cons["code_str"] = men_cons["Code"].apply(lambda x: str(int(x)))
                    fig = px.bar(
                        men_cons, x="code_str", y="Ménages",
                        color="Ménages",
                        color_continuous_scale=[
                            [0.0,  "#cce4f6"],
                            [0.33, "#5aace3"],
                            [0.66, "#1a6db5"],
                            [1.0,  "#0a2d6e"],
                        ],
                        text="Ménages"
                    )
                    fig.update_traces(texttemplate='%{text:,}', textposition='outside', marker_line_width=0)
                    fig.update_layout(
                        height=420,
                        showlegend=False,
                        coloraxis_showscale=False,
                        xaxis_title="Équipe",
                        yaxis_title="Nombre de Ménages",
                        xaxis=dict(
                            tickfont=dict(size=12),
                            tickmode='array',
                            tickvals=men_cons["code_str"].tolist(),
                            ticktext=men_cons["code_str"].tolist(),
                            categoryorder='array',
                            categoryarray=men_cons["code_str"].tolist(),
                        ),
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=40, r=20, t=40, b=40),
                    )
                    fig.update_xaxes(showgrid=False, showline=False, zeroline=False)
                    fig.update_yaxes(showgrid=False, showline=False, zeroline=False)
                    st.plotly_chart(fig, width='stretch')

                with col2:
                    st.markdown("#### Grappes Visitées")
                    gr_cons = stats_equipes.sort_values("Code", ascending=True).copy()
                    gr_cons["code_str"] = gr_cons["Code"].apply(lambda x: str(int(x)))
                    fig = px.bar(
                        gr_cons, x="code_str", y="Grappes",
                        color="Grappes",
                        color_continuous_scale=[
                            [0.0,  "#c8ecd7"],
                            [0.33, "#52b87a"],
                            [0.66, "#1a7d45"],
                            [1.0,  "#0a3d21"],
                        ],
                        text="Grappes"
                    )
                    fig.update_traces(texttemplate='%{text:,}', textposition='outside', marker_line_width=0)
                    fig.update_layout(
                        height=420,
                        showlegend=False,
                        coloraxis_showscale=False,
                        xaxis_title="Équipe",
                        yaxis_title="Nombre de Grappes",
                        xaxis=dict(
                            tickfont=dict(size=12),
                            tickmode='array',
                            tickvals=gr_cons["code_str"].tolist(),
                            ticktext=gr_cons["code_str"].tolist(),
                            categoryorder='array',
                            categoryarray=gr_cons["code_str"].tolist(),
                        ),
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=40, r=20, t=40, b=40),
                    )
                    fig.update_xaxes(showgrid=False, showline=False, zeroline=False)
                    fig.update_yaxes(showgrid=False, showline=False, zeroline=False)
                    st.plotly_chart(fig, width='stretch')

                st.markdown("---")
                st.markdown("### 📋 Récapitulatif Détaillé par Équipe")

                stats_equipes["Moy/Grappe"] = (stats_equipes["Ménages"] / stats_equipes["Grappes"]).round(1)

                df_to_display = display_searchable_dataframe(
                    stats_equipes[["Code", "Nom", "Ménages", "Grappes", "Moy/Grappe"]],
                    key_suffix="consolidé_equipes"
                )
                st.dataframe(df_to_display, width='stretch', height=400)

        with tab2:
            st.markdown("### Indicateurs d'Emploi Consolidés")

            if len(df_age) > 0:
                col1, col2, col3 = st.columns(3)

                t_part = safe_mean(df_age["t_part"]) if "t_part" in df_age.columns else 0
                r_emp = safe_mean(df_age["r_emploi"]) if "r_emploi" in df_age.columns else 0

                with col1:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=t_part,
                        number={'suffix': "%", 'font': {'size': 50, 'color': "#667eea"}},
                        title={'text': "Taux Participation", 'font': {'size': 18, 'color': "#1f2937"}},
                        gauge={
                            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#64748b"},
                            'bar': {'color': "#667eea", 'thickness': 0.75},
                            'bgcolor': "white",
                            'borderwidth': 2,
                            'bordercolor': "#e2e8f0"
                        },
                        domain={'x': [0, 1], 'y': [0, 1]}
                    ))
                    fig.update_layout(height=280, margin=dict(l=20, r=20, t=60, b=20),
                                      paper_bgcolor="rgba(0,0,0,0)", font={'family': "Inter"})
                    st.plotly_chart(fig, width='stretch')

                with col2:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=r_emp,
                        number={'suffix': "%", 'font': {'size': 50, 'color': "#10b981"}},
                        title={'text': "Ratio Emploi", 'font': {'size': 18, 'color': "#1f2937"}},
                        gauge={
                            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#64748b"},
                            'bar': {'color': "#10b981", 'thickness': 0.75},
                            'bgcolor': "white",
                            'borderwidth': 2,
                            'bordercolor': "#e2e8f0"
                        },
                        domain={'x': [0, 1], 'y': [0, 1]}
                    ))
                    fig.update_layout(height=280, margin=dict(l=20, r=20, t=60, b=20),
                                      paper_bgcolor="rgba(0,0,0,0)", font={'family': "Inter"})
                    st.plotly_chart(fig, width='stretch')

                with col3:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=t_chom,
                        number={'suffix': "%", 'font': {'size': 50, 'color': "#f59e0b"}},
                        title={'text': "Taux Chômage", 'font': {'size': 18, 'color': "#1f2937"}},
                        gauge={
                            'axis': {'range': [None, 50], 'tickwidth': 1, 'tickcolor': "#64748b"},
                            'bar': {'color': "#f59e0b", 'thickness': 0.75},
                            'bgcolor': "white",
                            'borderwidth': 2,
                            'bordercolor': "#e2e8f0"
                        },
                        domain={'x': [0, 1], 'y': [0, 1]}
                    ))
                    fig.update_layout(height=280, margin=dict(l=20, r=20, t=60, b=20),
                                      paper_bgcolor="rgba(0,0,0,0)", font={'family': "Inter"})
                    st.plotly_chart(fig, width='stretch')

                if "I10" in df_age.columns:
                    st.markdown("---")
                    st.markdown("### 📊 Indicateurs par Équipe")

                    indic_equipe = df_age.groupby("I10").agg(
                        Effectif=("IND1", "count"),
                        t_part=("t_part", "mean"),
                        r_emploi=("r_emploi", "mean"),
                        t_chomage=("t_chomage", "mean")
                    ).reset_index().sort_values("I10", ascending=True)
                    indic_equipe["code_str"] = indic_equipe["I10"].apply(lambda x: str(int(x)))

                    fig = go.Figure()
                    fig.add_trace(go.Bar(name="Taux Participation", x=indic_equipe["code_str"], y=indic_equipe["t_part"], marker_color="#667eea", marker_line_width=0))
                    fig.add_trace(go.Bar(name="Ratio Emploi", x=indic_equipe["code_str"], y=indic_equipe["r_emploi"], marker_color="#10b981", marker_line_width=0))
                    fig.add_trace(go.Bar(name="Taux Chômage", x=indic_equipe["code_str"], y=indic_equipe["t_chomage"], marker_color="#f59e0b", marker_line_width=0))

                    fig.update_layout(
                        barmode="group", height=420,
                        xaxis_title="Équipe", yaxis_title="Taux (%)",
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=40, r=20, t=40, b=40),
                        xaxis=dict(
                            tickmode='array',
                            tickvals=indic_equipe["code_str"].tolist(),
                            ticktext=indic_equipe["code_str"].tolist(),
                            categoryorder='array',
                            categoryarray=indic_equipe["code_str"].tolist(),
                            tickfont=dict(size=12),
                            showgrid=False, showline=False, zeroline=False,
                        ),
                        yaxis=dict(showgrid=False, showline=False, zeroline=False),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    st.plotly_chart(fig, width='stretch')

                    st.markdown("---")
                    display_indic = indic_equipe.copy()
                    display_indic["Nom"] = display_indic["I10"].apply(lambda x: get_label_equipe(x))
                    display_indic = display_indic.rename(columns={
                        "I10": "Code",
                        "t_part": "Taux Part.",
                        "r_emploi": "Ratio Emploi",
                        "t_chomage": "Taux Chômage"
                    })

                    for col in ["Taux Part.", "Ratio Emploi", "Taux Chômage"]:
                        if col in display_indic.columns:
                            display_indic[col] = display_indic[col].round(1)

                    df_to_display = display_searchable_dataframe(
                        display_indic[["Code", "Nom", "Effectif", "Taux Part.", "Ratio Emploi", "Taux Chômage"]],
                        key_suffix="consolidé_indicateurs"
                    )

                    st.dataframe(
                        df_to_display.style.format({
                            "Code": "{:.0f}",
                            "Effectif": "{:.0f}",
                            "Taux Part.": "{:.1f}",
                            "Ratio Emploi": "{:.1f}",
                            "Taux Chômage": "{:.1f}"
                        }),
                        width='stretch',
                        height=400
                    )

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
<div style="display:flex; align-items:center; justify-content:space-between; padding: 1.25rem 2rem;
            background: var(--primary, #0d2f5e); border-radius: 10px; color: white; gap: 1rem; flex-wrap: wrap;">
    <div>
        <div style="font-family:'Syne',sans-serif; font-weight:700; font-size:1rem; margin-bottom:3px;">Dashboard ENTE — Contrôle Qualité</div>
        <div style="color:rgba(255,255,255,0.6); font-size:0.8rem;">© 2026 ANSADE · Mauritanie · Développé avec Streamlit</div>
    </div>
    <div style="background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); border-radius:20px;
                padding:0.3rem 0.9rem; font-size:0.75rem; font-weight:600; letter-spacing:0.8px;
                color:rgba(255,255,255,0.8); text-transform:uppercase; white-space:nowrap;">
        ENTE 2026
    </div>
</div>
""", unsafe_allow_html=True)