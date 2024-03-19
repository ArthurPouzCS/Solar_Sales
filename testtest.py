import streamlit as st
import folium as fl
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import requests
import json
from geopy.distance import geodesic
from streamlit_folium import folium_static

def get_pos(lat, lng):
    return lat, lng

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

def get_parcelles(latitude, longitude):
    url = "https://apicarto.ign.fr/api/cadastre/parcelle"
    
    geometry_point = create_square_polygon(latitude, longitude)

    params = {"geom": json.dumps(geometry_point)}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        parcelles = response.json()
        return parcelles
    else:
        return None

def display_satellite_map_with_parcelles(latitude, longitude, parcelles):
    mymap = fl.Map(location=[latitude, longitude], zoom_start=35, tiles="Stamen Terrain", control_scale=True, attr="Map data © Stamen Terrain")

    fl.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", name="Satellite", attr="Esri", overlay=True).add_to(mymap)

    if parcelles:
        for feature in parcelles["features"]:
            geometry = feature["geometry"]
            properties = feature["properties"]
            numero_parcelle = properties["numero"]
            fl.GeoJson(
                feature,
                name=f"Parcelle {numero_parcelle}",
                style_function=lambda feature: {
                    'fillColor': 'white',
                    'color': 'black',
                    'weight': 2
                },
                popup=fl.Popup(f"Parcelle : {numero_parcelle}"),
            ).add_to(mymap)

    def on_my_click(e):
        global parcelle_selectionnee
        if 'feature' in e:
            properties = e['feature']['properties']
            numero_parcelle = properties.get("numero", None)
            if numero_parcelle is not None:
                parcelle_selectionnee = numero_parcelle
                print(f"Parcelle sélectionnée : {parcelle_selectionnee}")

    folium_static(mymap, height=300, width=500)

def map_api():
    adresse = st.text_input("Rechercher une adresse:")

    location_options = get_location_options(adresse)
    location_options = [ ''.join([loc.split(',')[:][i] for i in [0,1,3,7]]) for loc in location_options]
    selected_address = st.selectbox("Choisissez une adresse:", location_options, index=0)

    coordinates = get_coordinates_from_address(selected_address)
    parcelles = None

    if coordinates:
        latitude, longitude = coordinates
        response = requests.get(f"https://api-adresse.data.gouv.fr/reverse/?lat={latitude}&lon={longitude}")
        if response.status_code == 200:
            data = response.json()
            try:
                insee_code = data['features'][0]['properties']['citycode']
                parcelles = get_parcelles(latitude, longitude)
            except:
                parcelles = {}

        display_satellite_map_with_parcelles(latitude, longitude, parcelles)

def main():
    st.title("Application combinée avec Streamlit et Folium")
    m = fl.Map()
    m.add_child(fl.LatLngPopup())
    map = st_folium(m, height=350, width=700)
    data = None

    if map.get("last_clicked"):
        data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])

    if data is not None:
        st.write(data) 
        print(data)

    map_api()

if __name__ == "__main__":
    main()
