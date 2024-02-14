import streamlit as st
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import folium
import requests

def get_location_options(address):
    geolocator = Nominatim(user_agent="geo_search")
    locations = geolocator.geocode(address, exactly_one=False, limit=5, country_codes='FR')
    return [location.address for location in locations] if locations else []

def get_coordinates_from_address(address):
    response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={address}")
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    return None

def get_insee_from_coordinates(latitude, longitude):
    response = requests.get(f"https://api-adresse.data.gouv.fr/reverse/?lat={latitude}&lon={longitude}")
    if response.status_code == 200:
        data = response.json()
        if data and 'features' in data and data['features']:
            return data['features'][0]['properties']['citycode']
    return None

def get_all_parcelles_commune(insee_code):
    all_parcelles = []
    page = 1
    limit = 500  # Nombre de parcelles à récupérer par page

    while True:
        url = f"https://apicarto.ign.fr/api/cadastre/parcelle?code_insee={insee_code}&_limit={limit}&_start={(page - 1) * limit}"
        response = requests.get(url)

        if response.status_code == 200:
            parcelles = response.json()
            if parcelles['features']:
                all_parcelles.extend(parcelles['features'])
                page += 1
            else:
                break
        else:
            break

    return {"type": "FeatureCollection", "features": all_parcelles}

def display_map(parcelles, latitude, longitude):
    mymap = folium.Map(location=[latitude, longitude], zoom_start=30)

    for parcelle in parcelles['features']:
        folium.GeoJson(
            parcelle,
            name=f"Parcelle {parcelle['properties']['numero']}",
            tooltip=f"Parcelle {parcelle['properties']['numero']} - Contenance: {parcelle['properties']['contenance']} m²",
            style_function=lambda x: {'fillColor': 'orange', 'color': 'black'},
            overlay=True,  # Ajout de la couche à la carte
        ).add_to(mymap)

    folium_static(mymap, height=200, width=300)

def map_api():
    # Barre de recherche d'adresse
    adresse = st.text_input("Rechercher une adresse:")
    selected_address = st.selectbox("Choisissez une adresse:", get_location_options(adresse), index=0)
    
    # Bouton Rechercher pour déclencher l'appel API
    if st.button("Rechercher"):
        # Obtenez les coordonnées de l'adresse sélectionnée
        with st.spinner("Recherche en cours..."):
            coordinates = get_coordinates_from_address(selected_address)

            if coordinates:
                latitude, longitude = coordinates

                # Obtenez le code INSEE correspondant aux coordonnées
                insee_code = get_insee_from_coordinates(latitude, longitude)

                if insee_code:
                    # Utilisez le code INSEE pour obtenir toutes les parcelles de la commune
                    all_parcelles = get_all_parcelles_commune(insee_code)

                    if all_parcelles:
                        # Affichez toutes les parcelles sur la carte
                        display_map(all_parcelles, latitude, longitude)
