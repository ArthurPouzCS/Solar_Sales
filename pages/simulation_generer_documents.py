import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
import plotly.express as px
import matplotlib.pyplot as plt
import time
from streamlit_extras.stylable_container import stylable_container
from db_functions import *

import os
import sys
path_generer_pdf_py = os.path.join(os.getcwd(), 'generation_pdf')
sys.path.insert(0,path_generer_pdf_py)
from generer_pdf_app import generer_les_2_pdf


def render_page_generer_documents():
        
    st.set_page_config(
    page_title="Simuler votre Projet - Génerer les documents",
    page_icon="📄", layout="wide", initial_sidebar_state="collapsed")
    past_audit, last = dont_forget_past_audit()
    no_sidebar()
    
    if 'data' in st.session_state:
        dic = st.session_state.data
    else : 
        st.error("Veuillez d'abord simuler votre projet")


    styled_button()
    #css()
    background("eoliennes_montagnes.jpg", 'center center')
    #sst.subheader("Création des documents réglementaire  📄")
    
    space(1)
    css = ["""
                [data-testid="stMarkdownContainer"] > p {
                    font-size : 18px;
                    font-weight : bold;
                    color:white !important;
                    }
                
                .st-emotion-cache-q8sbsg > p {
                    font-size : 18px;
                    font-weight : bold;
                }
                .st-emotion-cache-jnd7a1 p {
                    font-size : 18px;
                    font-weight : bold;
                }
                """
                ]
    with stylable_container(
            key='adresse_container',
            css_styles = css
            ):    
        with st.spinner("Création des documents réglementaires ..."):
            eolienne_qui_tourne()
            audit_path, rapport_path = generer_les_2_pdf(dic)
            if 'data' in st.session_state:
                dic = st.session_state.data
                dic['audit_path'] = audit_path
                dic['rapport_path'] = rapport_path
                st.session_state.data = dic
        #st.balloons()
        #st.success('Documents générés !')
        #time.sleep(2)
        switch_page('simulation_audit')

render_page_generer_documents()