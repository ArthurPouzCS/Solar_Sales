import streamlit as st
import time
import re
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
import pandas as pd
import os
from streamlit_extras.stylable_container import stylable_container
from db_functions import *

def render_page_traitement_donnees():
    st.set_page_config(
    page_title="Saisir vos Données - Traitement des Données",
    page_icon="🔄", layout="wide", initial_sidebar_state="collapsed"
)
    no_sidebar()
    styled_button()
    css()

    #background('eolienne.jpg', 'center center')
    
    if 'data' in st.session_state : ## à regarder
        dic = st.session_state.data
        email = dic['email']
        
        #id = unique_id_from(email) ----> à faire
        id = 000000
        dic['id']=id

        df = dic_to_df(dic)
        path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'df_to_save'),'my_file.csv')
        df.to_csv(path)
        #sortir le csv et concat les anciens et le nouveau
        #st.dataframe(df)
        #st.json(dic)
    
    with stylable_container(
            key='load_container',
            css_styles = ["""
            [data-testid="stMarkdownContainer"] > p {
                font-size : 25px;
                font-weight : semi-bold;
                color : white;
                letter-spacing: 2px;
                font-family: 'Calibri', sans-serif; 
                }
            """]
            ):

        #with st.status("Récupération et traitement des données...", expanded=True) as status:
            #with st.spinner('En attente...'):

        time.sleep(0.5)
        st.write("Récupération des données Météo France...")
        time.sleep(0.5)
        st.write("Détection des ombrages grâce aux données NASA et IGN...")
        time.sleep(0.5)
        st.write("Dimensionnement de l'installation photovoltaïque...")
        time.sleep(0.5)
        st.write("Calcul de votre production électrique solaire...")
        time.sleep(0.5)
        st.write("Calcul de vos économies...")
        time.sleep(0.5)
        #status.update(label="Traitement terminé !", state="complete", expanded=False)
        
        switch_page("saisir_donnees_book")
        #### todoo

render_page_traitement_donnees()