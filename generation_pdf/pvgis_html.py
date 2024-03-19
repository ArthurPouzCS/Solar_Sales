import streamlit as st
from datetime import datetime
import pandas as pd
import sys
import os
path_functions = os.path.dirname(os.path.dirname(__file__)) # dir de SolarSales
sys.path.insert(0,path_functions)
from db_functions import *

def pvgis_html(dic):
    if 'data' in st.session_state:
        if 'nom' in st.session_state.data and 'prenom' in st.session_state.data :
            prenom, nom = st.session_state.data['prenom'], st.session_state.data['nom']
        
    date = datetime.now().strftime("%d-%m-%Y")

    mail_sales = st.session_state.mail
    nom_sales = retrieve_data('user_credentials', mail_sales, 'nom')
    prenom_sales = retrieve_data('user_credentials', mail_sales, 'prenom')

    string_css = """
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Garantie de production</title>
            <style>
                
                



                
        .titre{
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            margin-bottom: 20px;
            color:#3498db
        }

        .sous-titre{
            text-align: center;
            font-size: 15px;
            font-weight: semi-bold;
            margin-bottom: 20px;
            color:black;
        }

        body {
            font-family: 'calibri', 'Arial', 'sans-serif';
            margin: 20px;
            padding: 10px;
            background-color: white;
        }

        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
        }

        .column_text {
            flex : 2;
            width: 45%;
            height: 360px;
            padding: 10px 0px;
            box-sizing: border-box;
            margin-bottom: 20px;
            margin-left : 10%;
            margin-right : 0;
        }

        .column_horizon {
            flex : 1;
            width: 30%;
            padding: 10px 0px;
            box-sizing: border-box;
            margin-bottom: 20px;
            margin-left : 0;
            margin-right : 10%;
            text-align: center;
            position:absolute;
            top:221px;
            right:20px;
        }

        .column_bar {
            margin-top : 100px;
            width: 60%;
            height: 200px;
            padding: 0px;
            box-sizing: border-box;
            margin-bottom: 20px;
            position: absolute;
            left: 20%;
        }

        .blue-bg {
            background-color: #3498db;
            color: white;
            padding: 10px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .blue-bg-horizon {
            background-color: #3498db;
            color: white;
            padding: 10px;
            margin-bottom: -150px;
            font-weight: bold;
            position:relative;
            top:-104px;
        }
        .blue-bg-chart {
            background-color: #3498db;
            color: white;
            padding: 10px;
            margin-top:30px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .bar-chart {
            width: 600px; /* Ajustez la largeur selon vos besoins */
            height: 300px;
            max-width: 800px; 
            margin-left : -30px;
            display: block;
            position: relative;
            z-index: 4;
        }

        .horizon-image {
            width: 280px;
            height: auto;
            margin-top:90px;
        }
    
            </style>
        """

    string_html = f"""
        </head>
        <body>
        <div class="titre">Garantie de production</div>
        <div class="sous-titre">Réalisation le {date} pour {prenom} {nom}</div>
            <div class="container">
    <div class="column_text">
        <div class="blue-bg">Provided inputs</div>
        <ul>
            <li>Summary</li>
            <li>Location : {dic['inputs']['location']['latitude']}, {dic['inputs']['location']['longitude']}</li>
            <li>Horizon: Calculated</li>
            <li>Database used: {dic['inputs']['meteo_data']['radiation_db']}</li>
            <li>PV technology: {dic['inputs']['pv_module']['technology']}</li>
            <li>PV installed : {dic['inputs']['pv_module']['peak_power']} kWp</li>
            <li>System loss : {dic['inputs']['pv_module']['system_loss']*100} %</li>
        </ul>
        
        <div class="blue-bg">Simulation outputs</div>
        <ul>
            <li>Slope angle : {dic['inputs']['mounting_system']['fixed']['slope']['value']}°</li>
            <li>Azimuth angle : {dic['inputs']['mounting_system']['fixed']['azimuth']['value']}°</li>
            <li>Yearly PV energy production : {dic['outputs']['totals']['fixed']['E_y']} kWh</li>
            <li>Yearly in-plane irradiation : {dic['outputs']['totals']['fixed']['H(i)_y']} kWh/m²</li>
            <li>Year-to-year variability : {dic['outputs']['totals']['fixed']['SD_y']} kWh</li>
            <li>Changes in output due to:</li>
            <ul>
                <li>Angle of incidence : {dic['outputs']['totals']['fixed']['l_aoi']} %</li>
                <li>Spectral effects : {dic['outputs']['totals']['fixed']['l_spec']} %</li>
                <li>Temperature and low irradiance : {dic['outputs']['totals']['fixed']['l_tg']} %</li>
                <li>Total loss : {dic['outputs']['totals']['fixed']['l_total']} %</li>
            </ul>
        </ul>
    </div>
    
    <div class="column_horizon">
        <div class="blue-bg-horizon">Outline of horizon</div>
        <img class="horizon-image" src="{os.path.join(os.path.dirname(__file__),'horizon.png')}" alt="Horizon Outline">
    </div>
    
</div>
    <div class="column_bar">
        <div class="blue-bg-chart">Monthly energy output from fix-angle PV system</div>
        <img class="bar-chart" id="monthly-chart" src="{os.path.join(os.path.dirname(__file__),'bar_chart.png')}" alt="BarChart">
    </div>
<div class="container">
        </body>
    </html>

    """

    return string_css+string_html



def past_pvgis_html(dic):
    with open('./pvgis.html', 'r', encoding='utf-8') as fichier:
        contenu_html = fichier.read()

    string_css, string_html = contenu_html.split('<body>')[0], contenu_html.split('<body>')[1]
    
    for mot in ['bar_chart.png', 'horizon.png']:
        string_html = string_html.replace(mot, os.path.join(os.path.dirname(__file__),mot))


    return string_css + string_html