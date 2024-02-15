import streamlit as st
from streamlit_extras import stylable_container
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Générer vos Documents",
    page_icon="📽", layout="wide", initial_sidebar_state="collapsed"
)

st.session_state.generation = True
switch_page()
st.write("# Générer vos Documents ! 👋")