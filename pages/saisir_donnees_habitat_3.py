import streamlit as st
import time
import re
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
from streamlit_extras.stylable_container import stylable_container
from db_functions import *


def render_page_habitat_3():
    st.set_page_config(
    page_title="Saisir vos données - Habitat 3",
    page_icon="🏡", layout="wide", initial_sidebar_state="collapsed"
)
    past_audit, last = dont_forget_past_audit()
    no_sidebar()
    styled_button()
    css()
    #background('plaque_cuisson.jpg', 'center center')

    afficher_frise_chronologique(4)
    
    with stylable_container(
            key='adresse_container',
            css_styles = css_from_function()
            ):

        with stylable_container(key="production_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Votre production d'eau chaude sanitaire et climatisation  💧")
                col1, col2 = st.columns(2)
                with col1:
                    hauteur_ecs = st.selectbox("Quelle hauteur sous plafond du système de production d'ECS", ["Inférieur à 2m20", "Supérieur à 2m20"], index=last('hauteur_ecs', 'selectbox', ["Inférieur à 2m20", "Supérieur à 2m20"]))
                    st.markdown(f'<p style="color: white; font-size: 14px;">ECS : Eau chaude sanitaire (ballon..)</p>', unsafe_allow_html=True)
                    ballon_eau_chaude_electrique = st.radio("Avez-vous un ballon d'eau chaude électrique ?", ["Oui", "Oui, un thermodynamique", "Non", "Non, j'ai un système d'eau chaude instantanée"], index=last('ballon_eau_chaude_electrique', 'radio', ["Oui", "Oui, un thermodynamique", "Non", "Non, j'ai un système d'eau chaude instantanée"] ))
                with col2:
                    climatisation = st.radio("Avez-vous une climatisation", ["Oui","Non"], index=last('climatisation', 'radio', ["Oui","Non"]))
                    if "Oui" == ballon_eau_chaude_electrique or "Oui, un thermodynamique"== ballon_eau_chaude_electrique:
                        capacite_ballon = st.selectbox("Quelle est la capacité de votre ballon (en L)", [50, 100, 150, 200, 250, 300, 350], index=last('capacite_ballon', 'selectbox', [50, 100, 150, 200, 250, 300, 350]))
                    #if ballon_eau_chaude_electrique == "Non, j'ai un système d'eau chaude instantanée":
                        #capacite_eau_chaude_elec = st.number_input("Quelle est sa capacité (en L)", value=last('capacite_eau_chaude_elec', 'number_input'), step=10)
        
        with stylable_container(key="materiel_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Votre matériel  🤖")
                col1, col2 = st.columns(2)
                with col1:
                    plaque_cuisson = st.selectbox("Dans votre cuisine, votre plaque de cuisson est :", ["Une plaque à gaz", "Non électrique", "En fonte", "Vitrocéramique", "A induction", "Aucune plaque"], index=last('plaque_cuisson', 'selectbox', ["Une plaque à gaz", "Non électrique", "En fonte", "Vitrocéramique", "A induction", "Aucune plaque"]))
                    lave_vaisselle = st.selectbox("Avez-vous un lave-vaisselle ?", ["Oui", "Non"], index=last('lave_vaisselle', 'selectbox', ["Oui", "Non"]))
                    seche_linge = st.selectbox("Avez-vous un sèche-linge ?", ["Oui", "Non"], index=last('seche_linge', 'selectbox', ["Oui", "Non"]))
                    systeme_vmc = st.selectbox("Avez-vous un systeme VMC ?", ["Oui, simple flux", "Oui, double flux", "Non"], index=last('systeme_vmc', 'selectbox', ["Oui, simple flux", "Oui, double flux", "Non"]))
                with col2:    
                    type_four = st.selectbox("Quel type de four possédez-vous :", ["Electrique", "Non électrique", "Aucun four"], index=last('type_four', 'selectbox', ["Electrique", "Non électrique", "Aucun four"]))
                    lave_linge = st.selectbox("Avez-vous un lave-linge ?", ["Oui", "Non"], index=last('lave_linge', 'selectbox', ["Oui", "Non"]))
                    
                    voiture_electrique = st.selectbox("Possédez-vous une voiture électrique ?", ["Oui", "Non"], index=last('voiture_electrique', 'selectbox', ["Oui", "Non"]))
                    piscine_chauffee = st.selectbox("Possédez-vous une piscine chauffée ?", ["Oui", "Non"], index=last('piscine_chauffee', 'selectbox', ["Oui", "Non"]))
                
                frigidaire = st.multiselect("Quel frigidaire avez-vous ? (Choix multiples)", ["Un simple", "Un combiné avec congélateur", "Un américain", "Je n'ai pas de frigidaire"], default=last('frigidaire', 'multiselect'))
                congelateur = st.multiselect("Quel congélateur avez-vous ? (Choix multiples)", ["Congélateur armoire", "Congélateur coffre", "Je n'ai pas de congélateur"], default=last('congelateur', 'multiselect'))
                type_ampoule = st.multiselect("Quelle(s) ampoule(s) utilisez-vous ? (Choix multipless)", ["Ampoule à incandescence", "Ampoule halogène", "Ampoule fluocompacte", "Lampe LED", "Ampoule basse consommation"], default=last('type_ampoule', 'multiselect'))   
                habitude_conso = st.selectbox("Quelles sont vos habitudes de consommation énergétique?", ["Le matin et le soir", "Le midi et le soir", "Le matin, midi et soir", "Le soir uniquement"], index=last('habitude_conso', 'selectbox', ["Le matin et le soir", "Le midi et le soir", "Le matin, midi et soir", "Le soir uniquement"]))
        
        with stylable_container(key="ressource_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Vos ressources et choix de consommation énergétique  💼")
                ressources_annuelles = st.number_input("Ressources annuelles : Inférieur à (€/an :", value=last('ressources_annuelles', 'number_input'), step=1000)
                interesse = st.multiselect("Vous êtes plutôt intéressé(e) par :", ["L'autoconsommation", "La vente totale", "Je ne sais pas encore"], default=last('interesse', 'multiselect'))


        #st.json(st.session_state.data)
        
        if st.button("Suivant"):
            
            if 'data' in st.session_state:
                dic = st.session_state.data

                dic['hauteur_ecs']=hauteur_ecs
                dic['ballon_eau_chaude_electrique']=ballon_eau_chaude_electrique
                dic['climatisation']=climatisation
                if "Oui" == ballon_eau_chaude_electrique or "Oui, un thermodynamique"== ballon_eau_chaude_electrique:
                    dic['capacite_ballon']=capacite_ballon

                dic['plaque_cuisson']=plaque_cuisson
                dic['lave_vaisselle']=lave_vaisselle
                dic['seche_linge']=seche_linge
                dic['systeme_vmc']=systeme_vmc
                dic['type_four']=type_four
                dic['lave_linge']=lave_linge
                dic['voiture_electrique']=voiture_electrique
                dic['piscine_chauffee']=piscine_chauffee
                dic['frigidaire']=frigidaire
                dic['congelateur']=congelateur
                dic['type_ampoule']=type_ampoule
                dic['habitude_conso']=habitude_conso
                dic['ressources_annuelles']=ressources_annuelles
                dic['interesse']=interesse
            

                st.session_state.data = dic
                update_or_insert_data(dic)

            switch_page('saisir_donnees_traitement_donnees')

        if st.button("Accueil"):
            switch_page('Accueil')

render_page_habitat_3()