import streamlit as st

#import pyodide_http # https://github.com/whitphx/stlite/blob/main/packages/desktop/README.md
#pyodide_http.patch_all()

from streamlit_extras.switch_page_button import switch_page
from functions import *
import base64
import pandas as pd
import os
from api_functions import *
from streamlit_extras.stylable_container import stylable_container
from db_functions import *


def get_token():
    #return None
    #chemin_fichier = os.path.join(os.path.join(os.path.dirname(__file__),'df_to_save'),'zoho_file.csv')
    #df = pd.read_csv(chemin_fichier)
    mail = st.session_state.mail
    refresh_token = retrieve_data('user_credentials', mail, 'refresh_token')
    if refresh_token:
        access_token_from_refresh()
    else:
        access_token_by_user()
    #if 'refresh_token' in df.columns:
    #    access_token_from_refresh()
    #else:
    #    access_token_by_user()
    if 'token' in st.session_state:
        st.success('Connecté à Zoho')

def show_title(text):
    st.markdown(f"""
        <style>
            .info-box-container {{
                background-color: {colors(0)};
                padding: 5px 10px;
                margin: 0px 5px 20px 5px;
                border-radius: 8px;
                width :  100%;
            }}

            .title {{
                font-size : 400%;
                font-weight : bold;
                margin-left : 33%;
            }}
        </style>
        """, unsafe_allow_html=True)

    content = f'<div class="info-box-container"><span class="title">{text}</span></div>'
    st.markdown(content, unsafe_allow_html=True)

def style_button():
        st.markdown(f"""
        <style>
            div.stButton > button:first-child {{
                width:250px;
                height:150px;
                margin : auto;
                margin-top : 5px;
                display:block;
                background-color : {colors(0)};
                color:white;
            }}
            div.stButton > button:hover {{
                background-color : {colors(0)};
                border : solid {colors(3)} 2px;
                color : white;
            }}
            .st-emotion-cache-1vm1bj5:focus:not(:active) {{
                background-color : {colors(1)};
                border : solid white 2px;
                color : white;
            }}

        </style>
        
        """, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    switch_page('authentification')



st.set_page_config(page_title="Accueil", page_icon="☀", layout="wide", initial_sidebar_state="collapsed")
no_sidebar()

css()
past_audit, last = dont_forget_past_audit()


show_title('FranceAudit ⚡')
# eolienne_qui_tourne()
#background('violet2.jpg', 'center right')
#backgroundColor(colors(5))

with stylable_container(
        key='adresse_container',
        css_styles = ["""
        .st-emotion-cache-x78sv8 p  {
            font-size:21px;
        }
        """]
        ):
    if True: #test_connexion_internet():
        chemin_fichier = os.path.join(os.path.join(os.path.dirname(__file__),'df_to_save'),'zoho_file.csv')
        client_id = retrieve_data('user_credentials', st.session_state.mail,'client_id')
        jamais_fait = (client_id == None)
        #jamais_fait = not(os.path.exists(chemin_fichier)) ## Avant
        if jamais_fait:
            with stylable_container(key='authentification', css_styles=f"""
            [data-testid="stNotification"]{{
                background-color:{colors(1)};
            }}
            """):
                st.info('Connectez vous à votre CRM Zoho')
            space(1)
            col1, col2 = st.columns(2)
            with col1:
                path_image = os.path.join(os.path.join(os.path.dirname(__file__), 'ressources'),'voltico_img.jpg')
                rel_path = os.path.relpath(path_image, os.getcwd())
                with stylable_container(
                    key='adresse_container',
                    css_styles = ["""
                    div[data-testid='stImage'] > img {
                        border-radius:10px;
                    }
                    """]
                    ):
                    st.image(rel_path, width=495)
            with col2:
                with stylable_container(key="materiel_style", css_styles=my_style_container()):
                    with st.container():
                        a,b = st.columns(2)
                        with a:
                            nom = st.text_input("Nom")
                            mail_smtp = st.text_input("Email pour envoi depuis l'application")
                            mail = st.text_input("Mail Zoho")
                            secret = st.text_input("Mot de passe API Zoho", type='password')
                        with b:
                            
                            prenom = st.text_input("Prénom")
                            space(1)
                            mdp_smtp = st.text_input("Mot de passe de votre adresse mail", type='password')
                            client = st.text_input("Client ID API Zoho")
                            space(1)
                        with st.expander('Comment trouver mes ID ?'):
                            st.info(r"Pour trouver vos ID, cliquez sur le bouton ci-dessus, connectez vous et cliquez sur Server-based Applications : Create Now, entrez FranceAudit dans Client Name, https://solar-sales-voltico-development.streamlit.app dans Homepage URL, et https://solar-sales-voltico-development.streamlit.app/ dans Authorized Redirect URIs")
                        with b:
                            with stylable_container(key="link_button_style2", css_styles=f"""
                            [data-testid="baseLinkButton-secondary"]{{
                                background-color : {colors(0)};
                            }}
                            """):
                                st.link_button("Pour trouver vos ID :","https://accounts.zoho.com/signin?servicename=AaaServer&serviceurl=%2Fdeveloperconsole")
                        with stylable_container(key="confirmation_style", css_styles=f"""
                            [data-testid="baseButton-secondary"]{{
                                background-color : {colors(0)};
                            }}
                            """):
                            confirmation_bouton = st.button('Confirmer')
                if confirmation_bouton:
                    #data = {
                    #    'mail': [mail],
                    #    'nom' : [nom],
                    #    'prenom' : [prenom],
                    #    'client_id': [client],
                    #    'secret_id': [secret],
                    #    'mail_smtp' : [mail_smtp],
                    #    'mdp_smtp' : [mdp_smtp]
                    #    }
                    #df = pd.DataFrame(data)
                    #path_zoho_csv = os.path.join(os.path.join(os.path.dirname(__file__),'df_to_save'),'zoho_file.csv')
                    #df.to_csv(path_zoho_csv, index=False)

                    insert_credential_data(mail, nom, prenom, client, secret, mail_smtp, mdp_smtp)

                    st.rerun()
                    get_token()
        else:
            get_token()

            style_button()

            cola, colb = st.columns(2)
            with cola:
                path_image = os.path.join(os.path.join(os.path.dirname(__file__), 'ressources'),'voltico_img.jpg')
                rel_path = os.path.relpath(path_image, os.getcwd())
                with stylable_container(
                    key='adresse_container',
                    css_styles = ["""
                    div[data-testid='stImage'] > img {
                        border-radius:10px;
                    }
                    """]
                    ):
                    st.image(rel_path, width=495)

            with colb:

                col1, col2 = st.columns(2)

                with col1:
                    if 'ancien_audit' in st.session_state :
                        if 'nom' in st.session_state.ancien_audit and 'prenom' in st.session_state.ancien_audit:
                            nom, prenom = st.session_state.ancien_audit['nom'], st.session_state.ancien_audit['prenom']
                            switch_to_simuler = st.button(f"Modifier les données de {prenom} {nom}")
                        else:
                            switch_to_simuler = st.button("Saisir vos données")
                    else:
                        switch_to_simuler = st.button("Saisir vos données")
                    if switch_to_simuler:
                        #st.toast("Bientôt disponible")
                        switch_page("saisir_donnees_etude_solaire")
                    
                    if 'ancien_audit' in st.session_state :
                        if 'nom' in st.session_state.ancien_audit and 'prenom' in st.session_state.ancien_audit:
                            nom, prenom = st.session_state.ancien_audit['nom'], st.session_state.ancien_audit['prenom']
                            switch_to_simuler = st.button(f"Réaliser la Garantie de {prenom} {nom}")
                        else:
                            if 'data' in st.session_state:
                                switch_to_simuler = st.button("Réaliser une Garantie")
                            else:
                                with stylable_container(key='bouton_simuler_rouge',css_styles=
                                """
                                .st-emotion-cache-1vm1bj5 {
                                    background-color : gray;
                                    pointer-events: none;
                                    }
                                """):
                                    switch_to_simuler = st.button("Réaliser une garantie")
                    else:
                        if 'data' in st.session_state:
                                switch_to_simuler = st.button("Réaliser une garantie")
                        else:
                            with stylable_container(key='bouton_simuler_rouge',css_styles=
                            """
                            .st-emotion-cache-123r4br {
                                background-color : gray;
                                pointer-events: none;
                                }
                            """):
                                switch_to_simuler = st.button("Réaliser une garantie")
                    if switch_to_simuler:
                        if 'data' in st.session_state:
                            switch_page("realiser_garantie")
                        else:
                            st.toast("Vous devez d'abord saisir des informations pour accéder à cet onglet")  

                    
                with col2:
                    if 'ancien_audit' in st.session_state :
                        if 'nom' in st.session_state.ancien_audit and 'prenom' in st.session_state.ancien_audit:
                            nom, prenom = st.session_state.ancien_audit['nom'], st.session_state.ancien_audit['prenom']
                            switch_to_simuler = st.button(f"Simuler le projet de {prenom} {nom}")
                        else:
                            if 'data' in st.session_state:
                                switch_to_simuler = st.button("Simuler votre projet")
                            else:
                                with stylable_container(key='bouton_simuler_rouge',css_styles=
                                """
                                .st-emotion-cache-1vm1bj5 {
                                    background-color : gray;
                                    pointer-events: none;
                                    }
                                """):
                                    switch_to_simuler = st.button("Simuler votre projet")
                    else:
                        if 'data' in st.session_state:
                                switch_to_simuler = st.button("Simuler votre projet")
                        else:
                            with stylable_container(key='bouton_simuler_rouge',css_styles=
                            """
                            .st-emotion-cache-1vm1bj5 {
                                background-color : gray;
                                pointer-events: none;
                                }
                            """):
                                switch_to_simuler = st.button("Simuler votre projet")
                    if switch_to_simuler:
                        if 'data' in st.session_state:
                            switch_page("simulation_selection_materiels")
                        else:
                            st.toast("Vous devez d'abord saisir des informations pour accéder à cet onglet")                            

                    if 'ancien_audit' in st.session_state :
                        if 'nom' in st.session_state.ancien_audit and 'prenom' in st.session_state.ancien_audit:
                            nom, prenom = st.session_state.ancien_audit['nom'], st.session_state.ancien_audit['prenom']
                            switch_to_simuler = st.button(f"Générer les documents de {prenom} {nom}")
                        else:
                            if 'data' in st.session_state:
                                switch_to_simuler = st.button("Générer vos documents")
                            else:
                                with stylable_container(key='bouton_simuler_rouge',css_styles=
                                """
                                .st-emotion-cache-1vm1bj5 {
                                    background-color : gray;
                                    pointer-events: none;
                                    }
                                """):
                                    switch_to_simuler = st.button("Générer vos documents")
                    else:
                        if 'data' in st.session_state:
                                switch_to_simuler = st.button("Générer vos documents")
                        else:
                            with stylable_container(key='bouton_simuler_rouge',css_styles=
                            """
                            .st-emotion-cache-1vm1bj5 {
                                background-color : gray;
                                pointer-events: none;
                                }
                            """):
                                switch_to_simuler = st.button("Générer vos documents")
                    
                    if switch_to_simuler:
                        if 'data' in st.session_state:
                            switch_page("generer_documents")
                        else:
                            st.toast("Vous devez d'abord saisir des informations pour accéder à cet onglet") 
                        
                
            with stylable_container(key='bouton_ancien_audit',
            css_styles = ["""
            div.stButton > button:first-child  {
                width : 80%;
                height : 30px;
                font-size : 25px;
                font-weight : semi-bold;
                letter-spacing: 2px;
                font-family: 'Calibri', sans-serif; 
                }
            """]):
                if st.button("Accéder à vos anciens audits"):
                    if 'ancien_audit' in st.session_state :
                        del st.session_state.ancien_audit
                        del st.session_state.data
                    switch_page("audit_anciens")

                if 'ancien_audit' in st.session_state :
                    if st.button("Procéder à un nouvel audit"):
                        del st.session_state.ancien_audit
                        del st.session_state.data
                        switch_page('Accueil')

            with stylable_container(key='bouton_reglages',
            css_styles = ["""
            div.stButton > button:first-child  {
                width : 40%;
                height : 20px;
                font-size : 25px;
                font-weight : semi-bold;
                font-family: 'Calibri', sans-serif; 
                text-align:center;
                position:relative;
                float:right;
                }
            """]):
                a,b = st.columns(2)
                with a:
                    if st.button("Réglages"):
                        switch_page("reglages")
                with b:
                    with stylable_container(key='bouton_annexe',
                    css_styles = ["""
                    div.stButton > button:first-child  {
                        width : 40%;
                        height : 20px;
                        font-size : 25px;
                        font-weight : semi-bold;
                        font-family: 'Calibri', sans-serif; 
                        text-align:center;
                        position:relative;
                        float:left;
                        }
                    """]):
                        if st.button("Documentation"):
                            switch_page("documentation")


            # if st.button('Configurations'):
            #     connected = True
            #     email = st.text_input('Mail du Compte SolarSales', value='ruben.chiche@gmail.com')
            #     if connected:
            #         st.success("Connecté avec le CRM")
            #     else:
            #         st.warning('Relancer connexion avec le CRM')

                #if 'data' in st.session_state:
                    #st.json(st.session_state.data)
    else:
        st.error("⛔ Pas de connexion Internet")

space(1)
with stylable_container(key='titre_center', css_styles="""
.st-emotion-cache-k7vsyb span {
    text-align:center;
    color:white;
}
.st-emotion-cache-1wncz92 p { text-align:center; }
.st-emotion-cache-1629p8f h1, .st-emotion-cache-1629p8f h2, .st-emotion-cache-1629p8f h3, .st-emotion-cache-1629p8f h4, .st-emotion-cache-1629p8f h5, .st-emotion-cache-1629p8f h6, .st-emotion-cache-1629p8f span {
    color:white;
}
"""):
    st.subheader('Par Voltico Developpement')

    #st.caption('_Developped_ by :blue[ArthurPouz] 🔥')



#[theme]

#primaryColor="royalblue"
#backgroundColor="white"
#secondaryBackgroundColor="#2ECC71"
#textColor="darkblue"
#accentColor="royalblue"
#font="sans serif"

#[theme]

#primaryColor="black"
#backgroundColor="#002b36"
#secondaryBackgroundColor="#586e75"
#textColor="#fafafa"
#font="sans serif"

