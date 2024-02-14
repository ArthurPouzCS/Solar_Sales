import streamlit as st
import requests
from geopy.geocoders import Nominatim
import os
import sys
from functions import *
import matplotlib.pyplot as plt


# Function to make API request and get solar production estimation
def get_solar_estimation(lat, lon, peak_power, system_loss):

    # PVGIS API endpoint
    API_ENDPOINT = "https://re.jrc.ec.europa.eu/api/PVcalc"
    
    params = {
        "lat": lat,
        "lon": lon,
        "peakpower": peak_power,
        "loss": system_loss,
        'outputformat':'json',
    }

    try:
        response = requests.get(API_ENDPOINT, params=params)
        response.raise_for_status()  # Check for errors

        # Assume the API response is in JSON format
        solar_data = response.json()
        return solar_data
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        st.error(f"Response content: {response.content.decode('utf-8')}")
        return None


# Function to get latitude and longitude from address using geopy
def get_coordinates_from_address(address):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        st.error("Unable to retrieve coordinates from the provided address.")
        return None, None

# Streamlit app
def calcul_pvgis(adresse, conso_annuelle_elec):
    
    lat, lon = get_coordinates_from_address(adresse)
    system_loss = 0.08 #dire 14% sur l'affichage
    peak_power = 1.0 #unitaire pour les calculs ################   IMPORTANT   #######################################

    if lat is not None and lon is not None:
        solar_data = get_solar_estimation(lat, lon, peak_power, system_loss)

        if solar_data:
            st.success("Données d'estimation solaire PVGIS récupérées avec succès.")

            lat, long, alti = solar_data['inputs']['location']['latitude'], solar_data['inputs']['location']['longitude'], solar_data['inputs']['location']['elevation']
            
            prod_an = solar_data['outputs']['totals']['fixed']['E_y']

            list = solar_data['outputs']['monthly']['fixed']
            nom_des_mois = ['Jan', 'Fev', 'Mars', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc']
            list_mois, list_mprod = [], []
            for prod in list:
                month = nom_des_mois[prod['month']-1]
                mprod = prod['E_m']
                list_mois.append(month)
                list_mprod.append(mprod)

            categories, puissances_produites = list_mois, list_mprod
            
            #on fait l'hypothèse qu'ils consomment uniformément sur l'année -> faux mais bon à voir
            conso_mois = conso_annuelle_elec/12
            pw_installee_unitaire_final = 6 #si jamais ne satsifait pas condition
            for pw_installee_unitaire in range(1,30):
                delta_conso = [(pw_installee_unitaire*val) - conso_mois for val in puissances_produites]
                pos = [val if val>=0 else 0 for val in delta_conso ]
                neg = [val if val<0 else 0 for val in delta_conso ]
                surplus = sum(pos)
                surplus_prct = surplus/(pw_installee_unitaire*prod_an)
                achete_sur_marche_pr_conso = sum(neg)
                achete_sur_marche_pr_conso_prct = achete_sur_marche_pr_conso/(pw_installee_unitaire*prod_an)
                if surplus_prct<0.25 and surplus_prct>0.18:
                    pw_installee_unitaire_final = pw_installee_unitaire

            delta_conso = [(pw_installee_unitaire_final*val) - conso_mois for val in puissances_produites]
            pos = [val if val>=0 else 0 for val in delta_conso ]
            surplus_final = sum(pos)
            surplus_prct_final = surplus_final/(pw_installee_unitaire_final*prod_an)
            independance_prct = max(0, 1-surplus_prct_final)
            return pw_installee_unitaire_final, independance_prct, surplus_prct_final, prod_an, puissances_produites

            