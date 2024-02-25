import streamlit as st
from datetime import datetime
import pandas as pd
import sys
import os
path_functions = os.path.dirname(os.path.dirname(__file__)) # dir de SolarSales
sys.path.insert(0,path_functions)
from db_functions import *

def pvgis_html(dic):
    
    nom, prenom = 'Beck', 'Martin' # à changer
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
            <li>Location [Lat/Lon]: 47.794, 2.472</li>
            <li>Horizon: Calculated</li>
            <li>Database used: PVGIS-SARAH2</li>
            <li>PV technology: Crystalline silicon</li>
            <li>PV installed [kWp]: 1</li>
            <li>System loss [%]: 14</li>
        </ul>
        
        <div class="blue-bg">Simulation outputs</div>
        <ul>
            <li>Slope angle [°]: 35</li>
            <li>Azimuth angle [°]: 0</li>
            <li>Yearly PV energy production [kWh]: 1187.45</li>
            <li>Yearly in-plane irradiation [kWh/m2]: 1504.58</li>
            <li>Year-to-year variability [kWh]: 53.41</li>
            <li>Changes in output due to:</li>
            <ul>
                <li>Angle of incidence [%]: -2.95</li>
                <li>Spectral effects [%]: 1.47</li>
                <li>Temperature and low irradiance [%]: -6.81</li>
                <li>Total loss [%]: -21.08</li>
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