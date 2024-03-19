import streamlit as st
import time
import re
import base64
from geo_test3 import map_api
from streamlit_extras.switch_page_button import switch_page
from functions import *
from map_api_functions import *
from api_functions import *
from streamlit_extras.stylable_container import stylable_container





def render_page_etude_solaire():
   
    st.set_page_config(
    page_title="Saisir vos Données - Etude Solaire",
    page_icon="☀", layout="wide", initial_sidebar_state="collapsed"
)
    past_audit, last = dont_forget_past_audit()
    no_sidebar()
    css()
    styled_button()    
    #background('maison_energie.jpg', 'bottom right')

    afficher_frise_chronologique(1)
    
    with stylable_container(
            key='adresse_container',
            css_styles = css_from_function()
            ):


        col1, col2 = st.columns(2)

        with col1:
            with stylable_container(key="adresse_style", css_styles=my_style_container()):
                with st.container():
                    if test_connexion_internet():
                        st.subheader("Saisir votre adresse  📭")
                        adresse = st.text_input("Rechercher une adresse:", value=last('adresse_postale', 'text_input'))
                        # Proposer des adresses en autocomplétion
                        
                        try:
                        location_options = get_location_options(adresse)
                        except:
                            location_options = []
                        
                        
                        #st.write(location_options[0])
                        sans_numero = [0,-2,2]
                        avec_numero = [0,1,-2,4]
                        if location_options != []:
                            depart_numero_retrieve = int(location_options[0].split(', ')[-2][:2])
                        else:
                            depart_numero_retrieve = 0
                        #st.markdown(depart_numero_retrieve)
                        location_options = [ ''.join([loc.split(',')[:][i] for i in (avec_numero if loc.split(',')[:][0].isdigit() else sans_numero)]) for loc in location_options]
                        selected_address = st.selectbox("Choisissez une adresse:", location_options, index=0)
                        with stylable_container(
                            key='carte',
                            css_styles = "div.stButton > button:first-child {  width:200px; background-color:white;, border:solid 1px black; height:10px; margin-right:35%}"
                            ):
                            load_map = st.button("Chercher sur la carte")
                        
                        if load_map:
                            # Obtenez les coordonnées de l'adresse sélectionnée
                            coordinates = get_coordinates_from_address(selected_address)

                            # Initialisez les parcelles à None
                            parcelles = None

                            # Affichez la carte dès le début
                            if coordinates:
                                latitude, longitude = coordinates

                                # Obtenez le code INSEE correspondant aux coordonnées
                                response = requests.get(f"https://api-adresse.data.gouv.fr/reverse/?lat={latitude}&lon={longitude}")
                                if response.status_code == 200:
                                    data = response.json()
                                    try:
                                        insee_code = data['features'][0]['properties']['citycode']
                                        parcelles = get_parcelles(latitude, longitude)
                                        
                                    except:
                                        parcelles = {}

                                # Affichez la carte satellite avec les parcelles
                                display_satellite_map_with_parcelles(latitude, longitude, parcelles)
                    else:
                        space(3)
                        st.error("⛔ Pas de connexion internet, vous connaissez votre numéro de parcel ?")
                        selected_address = ''
                        depart_numero_retrieve=0


        with col2:
            with stylable_container(key="location_style", css_styles=my_style_container()):
                with st.container():
                    st.subheader("Localisation et Parcelles  🏡")
                    if past_audit:
                        selected_address = last('adresse_postale', 'text_input')
                    adresse_postale = st.text_input("Votre adresse postale", selected_address)
                    options = departements()
                    if past_audit:
                        depart_numero_retrieve = last('departement', 'selectbox', options)
                    departement = st.selectbox("Sélectionnez votre département", options, index = depart_numero_retrieve)
                    parcelles = st.text_input("Vos parcelles", value=last('parcelles', 'text_input'))

        with stylable_container(key="adresse_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Toiture et Altitude  🗻")
                cola, colb = st.columns(2)
                with cola:
                    options_pente_toit = ["Plat 0°", "Méditerranéen 10°", "Semi-Méditerranéen 20°", "Classique 30°", "Alsacien/Breton 45°"]
                    pente_toit = st.selectbox("Veuillez préciser la pente du toit", options_pente_toit, index=last('pente_toit', 'selectbox', options_pente_toit))
                    options_altitude = ["Entre 0 et 500m", "Entre 500 et 1000m", "Plus de 1000m"]
                    altitude = st.selectbox("Veuillez préciser votre altitude", options_altitude, index=last('altitude', 'selectbox', options_altitude)) 
                    masque_solaire = st.radio("La toiture est-elle pourvue d'un masque solaire", ["Oui", "Non"], index=last('masque_solaire', 'radio', ['Oui', 'Non']))  
                    
                with colb:
                    options_orientation_toit = ["Nord", "Sud", "Est", "Ouest", "Nord-Est", "Nord-Ouest", "Sud-Est", "Sud-Ouest"]
                    orientation_toit = st.selectbox("Veuillez préciser l'orientation du toit", options_orientation_toit, index=last('orientation_toit', 'selectbox', options_orientation_toit))
                    options_type_personne = ["Particulier", "Professionnel", "Autre"]
                    type_personne = st.selectbox("Vous êtes :", options_type_personne, index=last('type_personne', 'selectbox', options_type_personne))
                
        submitted = st.button("Suivant")
        if submitted:
            dic = {
                "adresse_postale":adresse_postale, 
                "departement":departement, 
                "parcelles":parcelles, 
                "pente_toit":pente_toit, 
                "altitude":altitude, 
                "masque_solaire":masque_solaire, 
                "orientation_toit":orientation_toit, 
                "type_personne":type_personne
            }
            st.session_state.data = dic
            switch_page('saisir_donnees_habitat_1')

render_page_etude_solaire()