import streamlit as st
import time
import re
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
from streamlit_extras.stylable_container import stylable_container
from db_functions import *

def render_page_anciens_audit():
    
    st.set_page_config(
    page_title="Mes anciens audits",
    page_icon="📋", layout="wide", initial_sidebar_state="collapsed"
)
    no_sidebar()
    css()
    styled_button()
    background('reseau_elec.jpg', 'top center')


    def retrieve_anciens_audit(mail_sales):
        query = f"SELECT * FROM data_table WHERE mail_sales = '{mail_sales}'"
        query_columns = f"SELECT column_name FROM information_schema.columns WHERE table_name = 'data_table' ORDER BY ordinal_position;"
        
        result = execute_query(query_columns, fetch=True)
        from_db = {}
        for i in range(len(result)):
            from_db[result[i][0]] = i
        
        result = execute_query(query, fetch=True)

        return result, from_db

    def display_ancien_audit(audit, from_db):
        for i,key in enumerate(from_db.keys()):
            from_db[key]=audit[i]
        dic_audit = from_db

        adresse = dic_audit['adresse_postale']
        nom = dic_audit['nom']
        prenom = dic_audit['prenom']
        show(f"{prenom} {nom}", (f'{adresse}', '', ''))

        css = ["""
            [data-testid="stMarkdownContainer"] > p {
                font-size : 15px;
                font-weight : normal;
                font-family : 'Calibri', sans-serif;
                color : white;
            }
            
            div.stButton > button:first-child {
            margin-top: 3px;
            margin-right: 29%;
            width: 150px;
            height: 6px;
            display: inline;
            float: right;
            background-color: rgba(0,0,0,0);
            border: solid 1.1px rgba(0,0,0,0);
            }

            div.stButton > button:first-child : hover {
            background-color: rgba(0,0,0,0.3);
            border: solid 1.1px black;
            }
            div.stButton > button:first-child : active {
            background-color: rgba(0,0,0,0.3);
            border: solid 1.1px black;
            }

            """]

        with stylable_container(key='bouton_audits', 
        css_styles=css):
            if st.button('Voir le formulaire', key=f"audit_{dic_audit['id']}"):
                st.session_state.ancien_audit = dic_audit
                st.session_state.data = dic_audit
                if 'nouvel_audit' in st.session_state :
                    del st.session_state.nouvel_audit
                switch_page('Accueil')
            return None
    
    with stylable_container(
            key='adresse_container',
            css_styles = ["""
                [data-testid="stMarkdownContainer"] > p {
                    font-size : 18px;
                    font-weight : bold;
                    color : white;
                    }
                
                .st-emotion-cache-q8sbsg > p {
                    font-size : 18px;
                    font-weight : bold;
                    color : white;
                }
                .st-emotion-cache-jnd7a1 p {
                    font-size : 18px;
                    font-weight : bold;
                    color : white;
                }
                """]
            ):

        st.subheader('Mes anciens audits')
        mail_sales = st.session_state.mail
        liste_anciens_audit, from_db = retrieve_anciens_audit(mail_sales)

        cols = st.columns(3)
        for i,audit in enumerate(liste_anciens_audit):
            with cols[i%3]:
                display_ancien_audit(audit, from_db)


render_page_anciens_audit()