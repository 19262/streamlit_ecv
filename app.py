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
import warnings

warnings.filterwarnings("ignore")

# =============================================================================
# CONFIG
# =============================================================================
st.set_page_config(
    page_title="ENTE - Contrôle Qualité",
    page_icon="📊",
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

# =============================================================================
# CSS ULTRA PREMIUM OPTIMISÉ
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --primary: #667eea;
  --primary-dark: #5568d3;
  --secondary: #764ba2;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --info: #3b82f6;
  --text: #1f2937;
  --muted: #6b7280;
  --bg-light: #f9fafb;
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --radius: 12px;
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.main {
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  animation: fadeIn 0.5s ease-out;
}

.header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  padding: 2rem;
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  margin-bottom: 2rem;
  text-align: center;
}

.header h1 {
  color: white;
  margin: 0;
  font-size: 2.5rem;
  font-weight: 800;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.header p {
  color: rgba(255,255,255,0.95);
  margin: 0.5rem 0 0;
  font-size: 1rem;
  font-weight: 500;
}

[data-testid="stMetric"] {
  background: white;
  border-radius: var(--radius);
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: var(--shadow);
  padding: 1.5rem;
  transition: var(--transition);
}
[data-testid="stMetric"]:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}
[data-testid="stMetricValue"] {
  font-size: 2.2rem !important;
  font-weight: 800 !important;
  color: var(--primary) !important;
}
[data-testid="stMetricLabel"] {
  font-size: 0.9rem !important;
  font-weight: 600 !important;
  color: var(--muted) !important;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  box-shadow: var(--shadow-lg);
}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label {
  color: rgba(255,255,255,0.95) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  color: white !important;
  font-weight: 700 !important;
}

.stTabs [data-baseweb="tab-list"] {
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: var(--radius);
  background: white;
  box-shadow: var(--shadow);
}
.stTabs [data-baseweb="tab"] {
  height: 50px;
  padding: 0 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: var(--transition);
}
.stTabs [data-baseweb="tab"]:hover {
  background: rgba(102, 126, 234, 0.1);
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
  color: white !important;
  box-shadow: var(--shadow);
}

.stButton>button {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: var(--transition);
  box-shadow: var(--shadow);
}
.stButton>button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.dataframe {
  border-radius: var(--radius) !important;
  overflow: hidden !important;
  box-shadow: var(--shadow) !important;
  border: none !important;
  font-size: 0.9rem !important;
}
.dataframe thead tr {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
}
.dataframe thead th {
  color: white !important;
  font-weight: 700 !important;
  padding: 1rem !important;
  text-transform: uppercase;
  font-size: 0.8rem !important;
  letter-spacing: 0.5px;
  border: none !important;
}
.dataframe tbody tr {
  transition: var(--transition);
  border-bottom: 1px solid rgba(0,0,0,0.05) !important;
}
.dataframe tbody tr:hover {
  background-color: rgba(102, 126, 234, 0.05) !important;
}
.dataframe tbody td {
  padding: 0.75rem 1rem !important;
  border: none !important;
}

.js-plotly-plot {
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
  background: white;
}

[data-testid="stFileUploader"] {
  background: white;
  border-radius: var(--radius);
  padding: 1.5rem;
  border: 2px dashed rgba(102, 126, 234, 0.3);
  transition: var(--transition);
  box-shadow: var(--shadow);
}
[data-testid="stFileUploader"]:hover {
  border-color: rgba(102, 126, 234, 0.6);
  background: rgba(102, 126, 234, 0.02);
}

.stSuccess, .stInfo, .stWarning, .stError {
  border-radius: var(--radius) !important;
  padding: 1rem !important;
  box-shadow: var(--shadow) !important;
  font-weight: 600 !important;
}

.streamlit-expanderHeader {
  background: white;
  border-radius: var(--radius);
  font-weight: 600;
}

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary) 100%);
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# LABELS ET DICTIONNAIRES
# =============================================================================
LABELS_EQUIPES = {
    100: "Taleb Sedigh Cheikh Mohamdy Jeddou",
    200: "Sid El Moctar Sidi Mahamoud Ahmed Sidi",
    300: "El moustapha Aboubecrine el Hafedh",
    400: "Mahmoud Abderrahime Dia",
    500: "Sidi Mohamed Boune",
    600: "Amadou Adama Ly",
    700: "Ahmed Banné Messoud",
    800: "Mohamed Salem Ahmed Bezeid Mokhtareiny",
    900: "Mamadou Ousmane Ba",
    1000: "Mohamed Vadel Mohamed El Mouktar Elella"
}

LABELS_ENQUETEURS = {
    100: "Taleb Sedigh Cheikh Mohamdy Jeddou",
    101: "El Hassen Mohamed Yeslem Boubekar",
    102: "Mohamed Yeslem Elkebir",
    103: "Amadou Abdoulaye Ba",
    200: "Sid El Moctar Sidi Mahamoud Ahmed Sidi",
    201: "Mohamedou saleck limam",
    202: "El Bou Mouhamed El Mokhtar Ameirine",
    203: "Aly Abdel kader",
    300: "El moustapha Aboubecrine el Hafedh",
    301: "Sidi Dedd Salim Ahmed Mbadi",
    302: "Ahmed Aboubecrine El Atighe",
    303: "Abdellahi Mohamed Taleb Ahmed",
    400: "Mahmoud Abderrahime Dia",
    401: "Ibrahime Boubou Dia",
    402: "Brahim Mohamed Mbarek",
    403: "Mohamed Vadhel Seydou Camara",
    500: "Sidi Mohamed Boune",
    501: "Kemal Mohamed Abdellahi Bouje",
    502: "Limame Malick mohamed Boushab",
    503: "Mouhamadou Alassane ba",
    600: "Amadou Adama Ly",
    601: "Sid Ahmed El Hacen Bilal loubek",
    602: "Abou kalidou N'Gaide",
    603: "Mohamed Lemine Deddaha",
    700: "Ahmed Banné Messoud",
    701: "Mohamed El Gewth",
    702: "Oumar Biye Salime",
    703: "Mohamed El Moctar El Yass",
    800: "Mohamed Salem Ahmed Bezeid Mokhtareiny",
    801: "Brahim Mohamed Mahmoud Sidi Haiballa",
    802: "Ahmed talib ahmed sidi",
    803: "Elhassen Oumar Ba",
    900: "Mamadou Ousmane Ba",
    901: "Sidi Mohamed Mohamed Sidi Aly",
    902: "Dah Belkheir Bewbe",
    903: "Bocar souleymane sy",
    1000: "Mohamed Vadel Mohamed El Mouktar Elella",
    1001: "Demba Abdoul Ba",
    1002: "Mohamed lemine Mohemed oumar",
    1003: "Imam cheikh ahmed baba cheikh"
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
    """Charge un fichier SPSS (sans cache car on stocke dans session_state)"""
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
# SIDEBAR — Import unique avec persistance session_state
# =============================================================================
with st.sidebar:
    st.markdown("### 📊 ENTE - Contrôle Qualité")
    st.markdown("**ANSADE -- Mauritanie**")
    st.markdown("---")

    module = st.radio(
        "**Module d'analyse**",
        ["📋 Exhaustivité", "💼 Emploi", "📊 Vue Consolidée"],
        help="Sélectionnez le module souhaité"
    )

    st.markdown("---")

    # ═══════════════════════════════════════════════════════════════════
    # IMPORTATION PERSISTANTE — Les deux uploaders sont TOUJOURS visibles
    # Les données sont stockées dans session_state une seule fois
    # ═══════════════════════════════════════════════════════════════════

    st.markdown("**📂 Bases de données**")

    # --- Base Ménage ---
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

    # --- Base Emploi ---
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
st.markdown("""
<div class="header">
  <h1>📊 ENTE - Contrôle Qualité</h1>
  <p>Enquête Nationale Trimesterielle sur l'Emploi - ENTE 2026</p>
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

            with col1:
                st.markdown("### Ménages par Équipe")
                top_menages = stats_equipes.sort_values("nb_menages", ascending=False).head(15)
                fig = px.bar(
                    top_menages, x="nb_menages", y="I10",
                    orientation='h', color="nb_menages",
                    color_continuous_scale="Blues", text="nb_menages"
                )
                fig.update_traces(texttemplate='%{text:,}', textposition='outside')
                fig.update_layout(height=400, showlegend=False,
                                  xaxis_title="Nombre de Ménages", yaxis_title="Équipe",
                                  yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("### Grappes par Équipe")
                top_grappes = stats_equipes.sort_values("nb_grappes", ascending=False).head(15)
                fig = px.bar(
                    top_grappes, x="nb_grappes", y="I10",
                    orientation='h', color="nb_grappes",
                    color_continuous_scale="Greens", text="nb_grappes"
                )
                fig.update_traces(texttemplate='%{text:,}', textposition='outside')
                fig.update_layout(height=400, showlegend=False,
                                  xaxis_title="Nombre de Grappes", yaxis_title="Équipe",
                                  yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Distribution des Ménages par Grappe")
            fig = px.histogram(stats_grappes, x="nb_menages", nbins=30,
                               color_discrete_sequence=["#667eea"])
            fig.add_vline(x=15, line_dash="dash", line_color="#ef4444", line_width=2,
                          annotation_text="Seuil: 15", annotation_position="top right")
            fig.update_layout(height=350, xaxis_title="Nombre de Ménages", yaxis_title="Fréquence", bargap=0.1)
            st.plotly_chart(fig, use_container_width=True)

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
            st.dataframe(df_to_display, use_container_width=True, height=450)

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
                         use_container_width=True, height=500)

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
                    use_container_width=True,
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
                ).reset_index().sort_values("Effectif", ascending=False)

                fig = go.Figure()
                fig.add_trace(go.Bar(name="Taux participation", x=indic_equipe["I10"], y=indic_equipe["t_part"], marker_color="#667eea"))
                fig.add_trace(go.Bar(name="Ratio emploi", x=indic_equipe["I10"], y=indic_equipe["r_emploi"], marker_color="#10b981"))
                fig.add_trace(go.Bar(name="Taux chômage", x=indic_equipe["I10"], y=indic_equipe["t_chomage"], marker_color="#f59e0b"))

                fig.update_layout(
                    barmode="group", height=400,
                    xaxis_title="Équipe", yaxis_title="Taux (%)",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)

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
                    use_container_width=True,
                    height=400
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
                        use_container_width=True,
                        height=420
                    )

                    st.markdown("---")
                    st.markdown("### 📊 Top 15 Enquêteurs - % Questionnaire Ménages < 10 min")

                    top15_men = pct_men_rapide.head(15).copy()
                    top15_men["label"] = top15_men.apply(
                        lambda x: f"Équipe {int(x['I10'])} - Enq. {int(x['I11'])}", axis=1
                    )

                    fig = px.bar(
                        top15_men,
                        x="pct_moins_10min",
                        y="label",
                        orientation="h",
                        color="pct_moins_10min",
                        color_continuous_scale=["#10b981", "#fbbf24", "#f59e0b", "#ef4444"],
                        text="pct_moins_10min"
                    )
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    fig.update_layout(
                        height=500, showlegend=False,
                        xaxis_title="% Entretiens < 10 min",
                        yaxis_title="",
                        yaxis={'categoryorder': 'total ascending'}
                    )
                    fig.add_vline(x=30, line_dash="dash", line_color="#ef4444", line_width=2,
                                  annotation_text="Seuil: 30%", annotation_position="top right")
                    st.plotly_chart(fig, use_container_width=True)

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
                        use_container_width=True,
                        height=420
                    )

                    st.markdown("---")
                    st.markdown("### Top 15 Enquêteurs - % Individu en Emplois ≤ 5 min")

                    top15_emp = pct_emploi_rapide.head(15).copy()
                    top15_emp["label"] = top15_emp.apply(
                        lambda x: f"Équipe {int(x['I10'])} - Enq. {int(x['I11'])}", axis=1
                    )

                    fig = px.bar(
                        top15_emp,
                        x="pct_moins_5min",
                        y="label",
                        orientation="h",
                        color="pct_moins_5min",
                        color_continuous_scale=["#10b981", "#fbbf24", "#f59e0b", "#ef4444"],
                        text="pct_moins_5min"
                    )
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    fig.update_layout(
                        height=500, showlegend=False,
                        xaxis_title="% Entretiens ≤ 5 min",
                        yaxis_title="",
                        yaxis={'categoryorder': 'total ascending'}
                    )
                    fig.add_vline(x=30, line_dash="dash", line_color="#ef4444", line_width=2,
                                  annotation_text="Seuil: 30%", annotation_position="top right")
                    st.plotly_chart(fig, use_container_width=True)

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
                        st.plotly_chart(fig, use_container_width=True)

                with col2:
                    if len(occ) > 0 and "dur_ind_min" in occ.columns and occ["dur_ind_min"].notna().any():
                        st.markdown("#### Distribution Durées Emploi")
                        occ_clean = occ[occ["dur_ind_min"].notna()].copy()
                        fig = px.histogram(occ_clean, x="dur_ind_min", nbins=40,
                                           color_discrete_sequence=["#10b981"], marginal="box")
                        fig.add_vline(x=5, line_dash="dash", line_color="#ef4444", line_width=2,
                                      annotation_text="≤ 5 min", annotation_position="top right")
                        fig.update_layout(height=350, xaxis_title="Durée (minutes)", yaxis_title="Fréquence", showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)

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
                    st.plotly_chart(fig, use_container_width=True)

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
                st.plotly_chart(fig, use_container_width=True)
            
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
                st.plotly_chart(fig, use_container_width=True)
                
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
                    use_container_width=True,
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
                    fig = px.bar(
                        stats_equipes.sort_values("Ménages", ascending=False).head(15),
                        x="Ménages",
                        y="Code",
                        orientation="h",
                        color="Ménages",
                        color_continuous_scale="Blues",
                        text="Ménages"
                    )
                    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
                    fig.update_layout(
                        height=450,
                        showlegend=False,
                        yaxis={'categoryorder': 'total ascending'},
                        xaxis_title="Nombre de Ménages",
                        yaxis_title="Équipe"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### Grappes Visitées")
                    fig = px.bar(
                        stats_equipes.sort_values("Grappes", ascending=False).head(15),
                        x="Grappes",
                        y="Code",
                        orientation="h",
                        color="Grappes",
                        color_continuous_scale="Greens",
                        text="Grappes"
                    )
                    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
                    fig.update_layout(
                        height=450,
                        showlegend=False,
                        yaxis={'categoryorder': 'total ascending'},
                        xaxis_title="Nombre de Grappes",
                        yaxis_title="Équipe"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                st.markdown("### 📋 Récapitulatif Détaillé par Équipe")
                
                stats_equipes["Moy/Grappe"] = (stats_equipes["Ménages"] / stats_equipes["Grappes"]).round(1)
                
                df_to_display = display_searchable_dataframe(
                    stats_equipes[["Code", "Nom", "Ménages", "Grappes", "Moy/Grappe"]],
                    key_suffix="consolidé_equipes"
                )
                st.dataframe(df_to_display, use_container_width=True, height=400)

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
                    fig.update_layout(
                        height=280,
                        margin=dict(l=20, r=20, t=60, b=20),
                        paper_bgcolor="rgba(0,0,0,0)",
                        font={'family': "Inter"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
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
                    fig.update_layout(
                        height=280,
                        margin=dict(l=20, r=20, t=60, b=20),
                        paper_bgcolor="rgba(0,0,0,0)",
                        font={'family': "Inter"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
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
                    fig.update_layout(
                        height=280,
                        margin=dict(l=20, r=20, t=60, b=20),
                        paper_bgcolor="rgba(0,0,0,0)",
                        font={'family': "Inter"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                if "I10" in df_age.columns:
                    st.markdown("---")
                    st.markdown("### 📊 Indicateurs par Équipe")
                    
                    indic_equipe = df_age.groupby("I10").agg(
                        Effectif=("IND1", "count"),
                        t_part=("t_part", "mean"),
                        r_emploi=("r_emploi", "mean"),
                        t_chomage=("t_chomage", "mean")
                    ).reset_index().sort_values("Effectif", ascending=False)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        name="Taux Participation",
                        x=indic_equipe["I10"],
                        y=indic_equipe["t_part"],
                        marker_color="#667eea"
                    ))
                    fig.add_trace(go.Bar(
                        name="Ratio Emploi",
                        x=indic_equipe["I10"],
                        y=indic_equipe["r_emploi"],
                        marker_color="#10b981"
                    ))
                    fig.add_trace(go.Bar(
                        name="Taux Chômage",
                        x=indic_equipe["I10"],
                        y=indic_equipe["t_chomage"],
                        marker_color="#f59e0b"
                    ))
                    
                    fig.update_layout(
                        barmode="group",
                        height=400,
                        xaxis_title="Équipe",
                        yaxis_title="Taux (%)",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
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
                        use_container_width=True,
                        height=400
                    )

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 12px; color: white;">
    <h3 style="margin: 0;">📊 Dashboard ENTE v2.1</h3>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">© 2026 ANSADE -- Mauritanie - Développé avec Streamlit</p>
</div>
""", unsafe_allow_html=True)