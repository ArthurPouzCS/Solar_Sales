import requests
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def get_coordinates_from_address(address):
    st.write('Les données de localisation sont fournies par Nominatim, un service de géocodage fourni par OpenStreetMap (OSM), et sont soumises à la licence Open Database License (ODbL). © OpenStreetMap contributeurs.')
    headers = {
        'User-Agent': 'SolarSales/1.0'
    }
    response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={address}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    else:
        st.write(response.text)

    return None

def obtenir_dpe_par_adresse(adresse):
    # Étape 1: Obtenez les coordonnées géographiques (latitude, longitude) de l'adresse
    # Vous pouvez utiliser un service de géocodage en ligne ou une bibliothèque Python comme geopy
    # pour convertir l'adresse en coordonnées géographiques.

    # Exemple fictif (à remplacer par votre propre code)
    latitude, longitude = get_coordinates_from_address(adresse)
    #latitude, longitude = 48.858844, 2.294350

    # Étape 2: Utilisez les coordonnées dans une requête pour récupérer les données DPE
    url = 'https://data.ademe.fr/data-fair/api/v1/datasets/dpe-france/lines'
    
    # Paramètres de la requête
    params = {
        'bbox': f'{longitude-0.001},{latitude-0.001},{longitude+0.001},{latitude+0.001}',
        'size': 1,  # Vous pouvez ajuster la taille en fonction de vos besoins
        'select': '*',
        'q_mode': 'simple'
    }

    # Envoyer la requête
    #st.write(url, params)
    response = requests.get(url, params=params)
    #st.write(response.json())

    # Étape 3: Analysez la réponse pour obtenir les informations sur le DPE de la maison
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            dpe_info = data['results'][0]
            #with stylable_container(key='dpe_fonction', css_styles="""
            #.st-gm{
            #    color:rgba(33, 195, 84, 1);
            #}
            #"""):
                #st.success('Données DPE trouvées !')
            return dpe_info
        else:
            st.warning('Données DPE introuvables')
            return None
            print("Aucune information sur le DPE trouvée.")
    else:
        print(f"Erreur lors de la requête: {response.status_code}")