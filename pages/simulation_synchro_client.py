import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
from api_functions import *
import pandas as pd
import time
import os
from streamlit_extras.stylable_container import stylable_container
from db_functions import *

def show_text(label, info):
    st.markdown(f"""
    <style>
        .label_text {{
            font-weight: bold;
            font-size : 20px;
            color: {colors(3)};
        }}

        .info_text {{
            color : {colors(3)};
            margin-left : 10px;
            font-size:18px;
        }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div>
        <div class="label_text">{label}</div>
        <div class="info_text">{info}</div>
    </div>
    """, unsafe_allow_html=True)

def style_button_synchro():
        st.markdown("""
        <style>
            div.stButton {
                text-align: left; /* Centrer le contenu du conteneur */
            }

            div.stButton > button:first-child {
                margin-top: 14px;
                padding-right : -4px;
                width: 220px;
                height: 50px;
                display: inline;
                margin-left: 20px; 
                backround-color: rgba(102, 0, 204, 0.8);
            }

            div.stButton > button:hover {
                background-color: rgba(102, 0, 204, 1);
                border: solid white 1px;
            }
        </style>
        
        """, unsafe_allow_html=True)

def render_page_synchro():
    
    st.set_page_config(
    page_title="Simuler votre Projet - Synchronisation",
    page_icon="🔄", layout="wide", initial_sidebar_state="collapsed")
    
    no_sidebar()
    #style_button_synchro()
    styled_button()
    css()
    #background('eolienne_rouge.jpg', 'bottom center')
    if 'data' in st.session_state:
        dic = st.session_state.data
        prenom, nom = dic['prenom'], dic['nom']
        mail = dic['email']
    #path_file_csv = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),'df_to_save'),'zoho_file.csv')
    #df = pd.read_csv(path_file_csv)
    #mail = df.mail.iloc[0]
    #l = (str(mail).split('@')[0]).split('.')
    #prenom, nom = l[0].capitalize(), l[1].capitalize()

    connecte_boolean = False
    if test_connexion_internet():
        connexion = 'Connecté 👌'
        access_token_from_refresh()
        connecte_boolean = True
    else:
        connexion = 'Non connecté au réseau ❌'

    if 'token' in st.session_state:
        access_token = st.session_state.token
        statut = 'Valide 👍'
    else:
        statut = 'Non Valide 👎'

    with stylable_container(
            key='adresse_container',
            css_styles = css_from_function(cadre=True)
            ):    
        with stylable_container(key="infos_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Informations clients et session  🧔")
                col1, col2 = st.columns(2)
                with col1:
                    show_text('Nom/Prénom', nom+'/'+prenom)
                    show_text('Email', mail)
                with col2:
                    show_text('Etat de la connexion', connexion)
                    show_text('Etat de la session', statut)
                space(1)
        with stylable_container(key="synchro_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Type de synchronisation  🔄")
                client_deja_cree = st.radio("Le client "+ dic['prenom'] +' '+dic['nom'] +" est-il déjà crée", ['Oui', 'Non'], index=1)

        mispace()
        with stylable_container(key="materiel_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Procédure de mise à jour client  ✅")
                c1, c2 = st.columns(2)
                if client_deja_cree == 'Oui':
                    with c1:
                        st.subheader("1/ Prénom / Nom du client")
                        a,b = st.columns(2)
                        with a:
                            prenom = st.text_input("Prénom du client")
                        with b:
                            nom = st.text_input("Nom du client")
                        if connecte_boolean:
                            email_selectionne = get_user_info_by_nom_prenom(access_token, nom, prenom)
                        else:
                            email_selectionne = None
                    with c2:
                        st.subheader("2/ Mise à jour du client")
                        space(1)
                        if email_selectionne!=None:
                            st.success(email_selectionne)
                            if st.button("Mettre à jour"):
                                
                                dic['nom'], dic['prenom'], dic['email'] = [nom], [prenom],  [email_selectionne]
                                response = create_contact(access_token, dic)
                else:
                    st.subheader("2/ Création du client") 
                    a, b = st.columns(2)
                    with a:
                        c,d = st.columns(2)
                        with c:
                            show_text('Nom / Prénom du client', dic['nom'] + ' / ' + dic['prenom'])
                            show_text('Mail du client', dic['email'])
                        with d:
                            
                            if st.button('Envoyer les données'):
                                response = create_contact(access_token, dic)
                                time.sleep(1)
                        

   
        x,y,z = st.columns(3)
        with z:   
            if st.button("Suivant"):
                switch_page('Accueil')

render_page_synchro()