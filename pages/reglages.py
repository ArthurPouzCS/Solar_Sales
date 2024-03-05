import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from functions import *
from streamlit_extras.stylable_container import stylable_container
 


st.set_page_config(page_title="Réglages", page_icon="⚙", layout="wide", initial_sidebar_state="collapsed")
no_sidebar()
css()
  

with stylable_container(key='reglages_container', css_styles = my_style_container()):
    with st.container():
        tab1, tab2, tab3 = st.tabs(['Paramètres généraux', 'Paramètres financiers', 'Paramètres techniques'])
        with tab1:
            st.subheader('Paramètres généraux')
            st.write('A venir')
        with tab2:
            st.subheader('Paramètres financiers')
            st.write('A venir')
        with tab3:
            st.subheader('Paramètres techniques')
            st.write('A venir')