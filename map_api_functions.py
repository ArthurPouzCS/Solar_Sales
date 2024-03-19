import streamlit as st
#from js import pyodide
#await pyodide.loadPackage("ssl")
#import ssl

#import micropip
#await micropip.install('ssl')
import ssl

from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import folium
import requests
from geopy.distance import geodesic
import json

def create_square_polygon(latitude, longitude):
    # Coordonnées du point central
    center_point = (latitude, longitude)

    # Calculer les coordonnées des quatre coins du carré
    top_right = geodesic(kilometers=0.1).destination(center_point, 45)
    bottom_right = geodesic(kilometers=0.1).destination(center_point, 135)
    bottom_left = geodesic(kilometers=0.1).destination(center_point, -135)
    top_left = geodesic(kilometers=0.1).destination(center_point, -45)

    # Construire le polygone au format GeoJSON
    square_polygon = {
        "type": "Polygon",
        "coordinates": [[
            [top_right.longitude, top_right.latitude],
            [bottom_right.longitude, bottom_right.latitude],
            [bottom_left.longitude, bottom_left.latitude],
            [top_left.longitude, top_left.latitude],
            [top_right.longitude, top_right.latitude],  # Pour fermer le polygone
        ]]
    }

    return square_polygon

#@st.cache_data()
def get_location_options_past(address):
    geolocator = Nominatim(user_agent="geo_search")
    locations = geolocator.geocode(address, exactly_one=False, limit=5, country_codes='FR')
    return [location.address for location in locations] if locations else []

def get_location_options(address):
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 5,
        "countrycodes": "FR"
    }
    headers = {
        "User-Agent": 'SolarSales/1.0'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
    except requests.exceptions.RequestException as e:
        st.write("Erreur de connexion :", e)

    if response.status_code == 200:
        locations = response.json()
        return [location['display_name'] for location in locations] if locations else []
    else:
        # Gérer les erreurs de requête HTTP
        print("Erreur lors de la requête HTTP :", response.status_code)
        return []

#@st.cache_data()
def get_coordinates_from_address(address):
    response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={address}")
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    return None

#@st.cache_data()
def get_parcelles(latitude, longitude):
    url = "https://apicarto.ign.fr/api/cadastre/parcelle"
    
    #geometry_point = {"type": "Point","coordinates": [longitude, latitude]}
    geometry_point = create_square_polygon(latitude, longitude)

    params = {"geom":json.dumps(geometry_point)}
    response =  requests.get(url, params=params)
    
    if response.status_code == 200:
        parcelles = response.json()
        return parcelles
    else:
        return None

def display_satellite_map_with_parcelles(latitude, longitude, parcelles):
    mymap = folium.Map(location=[latitude, longitude], zoom_start=35, tiles="Stamen Terrain", control_scale=True, attr="Map data © Stamen Terrain")

    # Ajouter une couche satellite
    folium.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", name="Satellite", attr="Esri", overlay=True).add_to(mymap)

    # Ajouter les parcelles à la carte si elles sont disponibles
    if parcelles:
        
        # Ajoute la géométrie avec des popups dépendant de la position sur la carte
        for feature in parcelles["features"]:
            geometry = feature["geometry"]
            properties = feature["properties"]
            
            # Obtient le numéro de parcelle
            numero_parcelle = properties["numero"]
            
            # Ajoute la géométrie avec un popup contenant le numéro de parcelle
            folium.GeoJson(
                feature,
                name=f"Parcelle {numero_parcelle}",
                style_function=lambda feature: {
                    'fillColor': 'white',
                    'color': 'black',
                    'weight': 2
                },
                popup=folium.Popup(f"Parcelle : {numero_parcelle}"),
            ).add_to(mymap)

    def on_my_click(e):
        global parcelle_selectionnee
        # Extraire les informations de la parcelle cliquée
        if 'feature' in e:
            properties = e['feature']['properties']
            numero_parcelle = properties.get("numero", None)
            if numero_parcelle is not None:
                # Mettre à jour la variable externe
                parcelle_selectionnee = numero_parcelle
                print(f"Parcelle sélectionnée : {parcelle_selectionnee}")

    folium_static(mymap, height=300, width=500)


def map_api():
    adresse = st.text_input("Rechercher une adresse:")

    # Proposer des adresses en autocomplétion
    location_options = get_location_options(adresse)
    location_options = [ ''.join([loc.split(',')[:][i] for i in [0,1,3,7]]) for loc in location_options]
    selected_address = st.selectbox("Choisissez une adresse:", location_options, index=0)

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
        

