import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
import os
import sys
from streamlit_extras.stylable_container import stylable_container
from db_functions import *

path_pdf = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generation_pdf')
sys.path.insert(0,path_pdf)
from generer_pdf_app import generer_pac_pdf


def render_page_note_dimensionnement():
    
    st.set_page_config(
    page_title="Simuler votre Projet - Note de dimensionnement",
    page_icon="📑", layout="wide", initial_sidebar_state="collapsed")
    past_audit, last = dont_forget_past_audit()
    no_sidebar()
    styled_button()
    css()
    #background('eoliennes.jpg', 'center center')

    if 'data' in st.session_state:
        dic = st.session_state.data
    else:
        st.error('Veuillez saisir vos données pour accéder à cette page')
    if 'PAC air-air Quadri' in dic['materiels'] or 'PAC air-eau' in dic['materiels']:
        note_a_faire = True
    else:
        note_a_faire = False

    with stylable_container(
            key='adresse_container',
            css_styles = css_from_function()
            ):    
        if note_a_faire:
            pac_path = generer_pac_pdf(dic)
            path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generation_pdf'), pac_path)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader('Note de dimensionnement à consulter 📋')
                space(1)
                displayPDF(path, 500, 500)
            with col2:
                space(3)
                with stylable_container(key="materiel_style", css_styles=my_style_container()):
                    with st.container():
                        show('Note de dimensionnement pour la pompe à chaleur. ',('Liste les informations utiles pour la sélection de la PAC.','',''))          
                        
                        space(2)
                        if st.button("Envoyer par mail"):
                            a,b = st.columns(2)
                            with a:
                                expediteur = st.text_input('Expéditeur', value='arthur.pouzargue@outlook.fr')
                                destinataire = st.text_input('Destinataire', value='arthur.pouzargue@outlook.fr')
                            with b:
                                cc = st.text_input('CC', value='arthur.pouzargue@outlook.fr')
                                objet = st.text_input('Objet', value='Rapport Financier')
                            ##pj = piece jointe !!
                            corps = st.text_area('', value=f"""
                            Bonjour,

                            Nous avons le plaisir de .............

                            L'utilisateur reconnaît expressément:
                            
                            Qu'il souhaite prendre un rendez-vous avec un conseiller à domicile, afin d'obtenir un devis détaillé, que cette demande de rendez-vous ne fait pas suite à une sollicitation téléphonique mais à une premier rendez vous au cours duquel un audit énergétique a été réalisé, que ses données personnelles sont traitées conformément aux dispositions légales applicables, comme précisé dans la "Politique de protection des données". 
                            
                            Bonne réception,
                            
                            Cordialement
                            """, height=300)
                            if st.button("Envoyer"):
                                mail(expediteur, destinataire, cc, objet, corps) #attention à mettre le mail comme il fait et mettre le mdp dans les réglages
                            

                            
                        
                        with open(path, "rb") as pdf_file:
                                pdf_data = pdf_file.read()
                        st.download_button(
                            label="Télécharger",
                            data = pdf_data,
                            file_name='note_dimensionnement_PAC.pdf',
                            key='button'
                        )           
                    
        else:
            show("", ('Pas de note de dimensionnement à générer. Vous pouvez passer à la suite 😉', '', ''))       
            space(1) 



        with stylable_container(key="adresse_style", css_styles="""
        .st-emotion-cache-kjgucs{
            color:white;
        }
        """):
            if st.button("Suivant"):
                switch_page('simulation_synchro_client')

render_page_note_dimensionnement()