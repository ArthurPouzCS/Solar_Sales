import streamlit as st
import time
import re
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
import os


def render_page_book():
    st.set_page_config(
    page_title="Saisir vos Données - Book",
    page_icon="📖", layout="wide", initial_sidebar_state="collapsed"
)
    afficher_frise_chronologique(5)

    with stylable_container(key="book_style", css_styles=my_style_container()):
        with st.container():
            st.subheader("Book  📖")
            #styled_button()
            #background('maison_energie.jpg', 'center right')
            
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'book_compressed.pdf')
            with stylable_container(key="book_style1", css_styles=
            f"""
            [data-testid="stMarkdownContainer"]>p{{
                color:{colors(0)};
                margin-bottom : 0;
            }}
            """):
                if st.button("Retour à l'accueil", key='retour1'):
                    switch_page("Accueil")

            with stylable_container(key="book_style1", css_styles=
            f"""
            [data-testid="stMarkdownContainer"]>p{{
                color:{colors(0)};
                margin-bottom : 0;
            }}
            """):
                if st.button('Suivant', key='suivant1'):
                    switch_page('simulation_selection_materiels')

            with stylable_container(key="book_style", css_styles="""
            .e1nzilvr5 > p{
                font-size: 20px;
            }
            """):
                with st.expander("📖 Voir le Book"):
                    with st.spinner('Chargement du Book...'):
                        displayPDF(path, 700,400)
           

            
        
    #### 

render_page_book()