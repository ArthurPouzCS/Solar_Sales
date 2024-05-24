import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
from generation_pdf import *
import os
from streamlit_extras.stylable_container import stylable_container

def render_page_audit():
    
    st.set_page_config(
    page_title="Simuler votre Projet - Audit énergétique",
    page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

    past_audit, last = dont_forget_past_audit()
    if 'data' in st.session_state:
        path_pdf = st.session_state.data['audit_path']
        dic = st.session_state.data
    else :
        path_pdf = 'audit.pdf'
    no_sidebar()
    styled_button()
    css()
    #background('eolienne_champs.jpg', 'center center')
    
    with stylable_container(
            key='adresse_container',
            css_styles = css_from_function()
            ):    
        
        with stylable_container(key="materiel_style", css_styles=my_style_container()):
            with st.container():
                st.subheader('Audit énergétique à consulter  ⚡')
        col1, col2 = st.columns(2)
        
        with col1:
            real_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generation_pdf'),path_pdf)
            displayPDF_basse_resol(real_path, 500,500)
        with col2:
            show("", ('Audit réalisant une synthèse des éléments essentiels des données utilisateurs à la simulation énergétique.', '', ''))

            with stylable_container(key="adresse_style", css_styles=my_style_container()):
                with st.container():
                    #if st.button("Envoyer par mail"):
                    expediteur = st.text_input('Expéditeur', value='arthur.pouzargue@gmail.com')
                    destinataire = st.text_input('Destinataire', value='arthur.pouzargue@outlook.fr')
                    #cc = st.text_input('CC', value='arthur.pouzargue@outlook.fr')
                    cc = 'arthur.pouzargue@outlook.fr'
                    objet = st.text_input('Objet', value='Audit énergétique')
                    ##pj = piece jointe !!
                    corps = st.text_area('', value="""
                    Bonjour,

                    Veuillez recevoir en PJ votre audit énergétique.
                    
                    Bonne réception,
                    
                    Cordialement
                    """, height=250)
                    if st.button("Envoyer"):
                        #try:
                        send_email(expediteur, destinataire, cc, objet, corps, real_path) #attention à mettre le mail comme il fait et mettre le mdp dans les réglages
                
                if st.button("Suivant"):
                    switch_page('simulation_rapport_financier')
                if st.button("Accueil"):
                    switch_page('Accueil')
                        

render_page_audit()