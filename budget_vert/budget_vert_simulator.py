import streamlit as st
from pathlib import Path

st.set_page_config(
    initial_sidebar_state="expanded",
)

# Chemin vers le logo
BASE_DIR = Path(__file__).resolve().parent
logo_path = BASE_DIR / "Logo_CdC_Aunis_sud.jpg"

# Affichage du logo
st.logo(logo_path)

with st.sidebar:
    st.caption("Contact : s.labedens@aunis-sud.fr")
    st.caption("v1.0")

# Navigation
pg = st.navigation([
    st.Page("pages/axe1.py", title="🌏 Axe 1 - Atténuation Climat"),
    st.Page("pages/axe6.py", title="🦜 Axe 6 - Biodiversité"),
])
pg.run()
