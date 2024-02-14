import streamlit as st
from functions import *
from db_functions import *
from streamlit_extras.switch_page_button import switch_page
from api_functions import *
from time import time

st.set_page_config(
    page_title="Simuler votre Projet - Synchronisation",
    page_icon="🔄", layout="wide", initial_sidebar_state="collapsed")

no_sidebar()
css()

#drop_table('user_credentials')
#drop_table('data_table')

create_table_user_credentials()
create_table_data()
background('pv_authentif.jpg', 'top right')

with stylable_container(
            key='authenthif',
            css_styles = """
            [data-testid="stVerticalBlockBorderWrapper"] {
                background-color: rgba(200,200,200, 0.8);
                padding: 10px 10px;
                border-radius: 8px;
                }
                
            """
            ):
    url = st.experimental_get_query_params()
    if "code" in url:
        st.success('Un dernier ptit effort 😉')
        mail = st.text_input('Mail')
        password = st.text_input('Password', type='password')
        submit = st.button("Se connecter")
        if submit:
            hashed_password = retrieve_data('user_credentials', mail, 'mdp')
            if check_password(password, hashed_password):
                st.success('Connexion réussie')
                st.session_state.mail = mail ### Primary key
                st.session_state.logged_in = True
                access_token_by_user()
                st.write(st.session_state)
                switch_page('Accueil')
            else:
                st.error('Mot de passe incorrect')
        
    else:

        if st.session_state.logged_in == False:
            connexion, inscription = st.tabs(['Connexion', 'Inscription'])
            with inscription:
                mail_inscription = st.text_input('Mail', key='inscription')
                already = mail_already_exist(mail_inscription)
                if already and mail_inscription != '':
                    st.error('Mail déjà utilisé')
                password_inscription = st.text_input('Password', type='password', key='mdp_inscription')
                if not already:
                    if st.button("S'inscrire") :
                        save_password(mail_inscription, password_inscription)
                        st.success('Inscription réussie')
                        st.session_state.mail = mail_inscription ### Primary key
                        st.session_state.logged_in = True
                        switch_page('Accueil')
            with connexion:
                mail = st.text_input('Mail')
                password = st.text_input('Password', type='password')
                if st.button("Se connecter"):
                    hashed_password = retrieve_data('user_credentials', mail, 'mdp')
                    if check_password(password, hashed_password):
                        st.success('Connexion réussie')
                        st.session_state.mail = mail ### Primary key
                        st.session_state.logged_in = True
                        switch_page('Accueil')
                    else:
                        st.error('Mot de passe incorrect')
    

                
