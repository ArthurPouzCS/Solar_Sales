import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
import os
import sys
from streamlit_extras.stylable_container import stylable_container
from db_functions import *

def render_page_rapport_financier():
    
    st.set_page_config(
    page_title="Simuler votre Projet - Rapport Financier",
    page_icon="📰", layout="wide", initial_sidebar_state="collapsed")
    no_sidebar()

    if 'data' in st.session_state:
        path_pdf = st.session_state.data['rapport_path']
    else :
        path_pdf = 'rapport.pdf'

    styled_button()
    css()
    
    with stylable_container(
            key='adresse_container',
            css_styles = css_from_function()
            ):    
        st.subheader('Rapport Financier à consulter  📄')
        col1, col2 = st.columns(2)
        with col1:
            real_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),'generation_pdf'),path_pdf)
            displayPDF_basse_resol(real_path, 500,500)
            #displayPDF(real_path, 500,500)
        with col2:
            show('', ('Synthèse de la simulation financière.','',''))
            space(1)
            st.markdown("<div>Prendre un rendez-vous et recevoir son rapport financier.</div>", unsafe_allow_html=True)
            space(1)
            date_rdv = st.date_input('Date du RDV')
            heure_rdv = st.time_input("Heure du RDV")
            condition_accepte = st.radio("J'accepte les conditions", ['Oui'], index=0)
            if condition_accepte=='Oui':
                if st.button("Prendre un RDV"):
                    expediteur = st.text_input('Expéditeur', value='arthur.pouzargue@outlook.fr')
                    destinataire = st.text_input('Destinataire', value='arthur.pouzargue@outlook.fr')
                    cc = st.text_input('CC', value='arthur.pouzargue@outlook.fr')
                    objet = st.text_input('Objet', value='Rapport Financier')
                    ##pj = piece jointe !!
                    corps = st.text_area('', value=f"""
                    Bonjour,

                    Nous avons le plaisir de vous confirmer votre demande de RDV avec un de nos conseillers qui aura lieu le {date_rdv} à {heure_rdv}.

                    L'utilisateur reconnaît expressément:
                    Qu'il souhaite prendre un rendez-vous avec un conseiller à domicile, afin d'obtenir un devis détaillé, que cette demande de rendez-vous ne fait pas suite à une sollicitation téléphonique mais à une premier rendez vous au cours duquel un audit énergétique a été réalisé, que ses données personnelles sont traitées conformément aux dispositions légales applicables, comme précisé dans la "Politique de protection des données". 
                    
                    Bonne réception,
                    
                    Cordialement
                    """, height=500)
                    if st.button("Envoyer"):
                        mail(expediteur, destinataire, cc, objet, corps) #attention à mettre le mail comme il fait et mettre le mdp dans les réglages
                        
                


        



        
        if st.button("Suivant"):
            switch_page('simulation_note_dimensionnement')

render_page_rapport_financier()