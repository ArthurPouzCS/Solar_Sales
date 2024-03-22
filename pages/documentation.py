import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from functions import *
from streamlit_extras.stylable_container import stylable_container
import os
import sys
    
st.set_page_config(page_title="Documentation", page_icon="📄", layout="wide", initial_sidebar_state="collapsed")
no_sidebar()
css()
styled_button()
def remove_useless(chaine):
    caracteres_speciaux = ['_', '.pdf']
    for caractere in caracteres_speciaux:
        chaine = chaine.replace(caractere, '')
    chaine_sans_chiffres = ''.join(caractere for caractere in chaine if not caractere.isdigit())
    return chaine_sans_chiffres

with stylable_container(key='reglages_container', css_styles = my_style_container()):
    with st.container():
        st.subheader('Documents à consulter  📄')

        with stylable_container(key='accueil_container', css_styles = f"""
        [data-testid="baseButton-secondary"]{{
            position: relative;
            right:300px;
        }}
        """):
            if st.button('Accueil'):
                switch_page("Accueil")

        path_docs = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ressources','annexe_pdf')
        n = len(os.listdir(path_docs))
        for i,doc_name in enumerate(os.listdir(path_docs)):
            with stylable_container(key=f'doc_name_container', css_styles = f"""
                [data-testid="baseButton-secondary"]{{
                    background-color:{colors(0)};
                    margin: -10px 5px;
                    width: 50%;
                    height: 30px;
                    position: relative;
                    float:left;
                }}
            """):
                if st.button(remove_useless(doc_name)):
                    displayPDF(os.path.join(path_docs,doc_name), 500,300)




