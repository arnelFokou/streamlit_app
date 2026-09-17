"""Point d'entrée de l'application multipage."""

import streamlit as st

st.set_page_config(
    page_title="Dashboard taxis NYC",
    page_icon="🚕",
    layout="wide",
)

pages = [
    st.Page("pages/1_Tendance_horaire.py", title="Tendance horaire", icon="📈"),
    st.Page("pages/2_Prix_par_periode.py", title="Prix par période", icon="📊"),
]

st.navigation(pages).run()
