import streamlit as st

st.set_page_config(
#    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.caption("v1.0")

pg = st.navigation([
    st.Page("pages/axe1.py", title="🌏 Axe 1 - Atténuation Climat"),
    st.Page("pages/axe6.py", title="🦜 Axe 6 - Biodiversité"),
])
pg.run()