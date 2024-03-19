import streamlit as st
from datetime import datetime
import pandas as pd
import sys
import os
path_functions = os.path.dirname(os.path.dirname(__file__)) # dir de SolarSales
sys.path.insert(0,path_functions)
from db_functions import *

def pac_string_html(dic):
    
    nom, prenom = dic['nom'].upper(), dic['prenom'].upper()
    date = datetime.now().strftime("%d-%m-%Y")

    mail_sales = st.session_state.mail
    nom_sales = retrieve_data('user_credentials', mail_sales, 'nom')
    prenom_sales = retrieve_data('user_credentials', mail_sales, 'prenom')

    string_css = """
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Votre Projet</title>
            <style>
                .body_accueil {
                    display: flex;
                    justify-content: space-between; 
                    gap: 20px; 
                }

                .container_accueil {
                    display: flex;
                }

                .box_accueil {
                    color: royalblue;
                    flex: 1; /* Fait occuper tout l'espace disponible à l'intérieur du conteneur */
                    padding: 10px; /* Marge intérieure pour l'esthétique */
                }

                .span_accueil {
                    width: 0; /* Fait occuper aucun espace horizontal */
                    height: 100%; /* Occupe toute la hauteur disponible */
                }

                .logo_accueil {
                    max-width: 300px;
                    max-height: 150px;
                    margin: auto;
                }

                .info_accueil{
                    background-color:white;
                    margin: 10px, 30px;
                    text-align: left;
                    align-items: left;
                    color: royalblue;
                    font-size: 15px;
                }


                body {
                    font-family: 'Lato', sans-serif;
                    font-weight: 300;
                    margin: 0;
                    padding: 0;
                }

                header {
                    background-color: white;
                    padding: 20px;
                    text-align: justify;
                    margin-bottom: 10px;
                }

                header img {
                    max-width: 100px;
                    max-height: 100px;
                    float:left;
                    margin-left: 10px;
                }

                .logo_droite {
                    background-color: grey;
                    max-width: 200px;
                    max-height: 200px;
                    float:right;
                    margin-right: 20%;
                    margin-top: -140px;
                }

                div span {
                    margin-top: 20px;
                    width: 80%;
                }
                span img {
                    max-width: 100px;
                    max-height: 50px;
                    float:left;
                    margin-right: 160px;
                    margin-left: 200px;
                }

                span p {
                    text-align: center;
                    float: center;
                }

                header h1 {
                    margin: 0;
                    color:royalblue;
                    float:right;
                    margin-right: 25%;
                    }

                section {
                    text-align: center;
                    padding: 20px;
                    color:darkblue;
                }

                section h1 {
                    background-color: royalblue;
                    border-radius: 5px;
                    color: white;
                    padding: 3px 30px 3px 20px;
                    width: fit-content;
                    font-size: 26px;
                    font-weight:lighter;
                }

                section h2 {
                    color: royalblue;
                    padding: 3px 30px 3px 20px;
                    width: fit-content;
                    font-size: 20px;
                    font-weight:lighter;
                    text-decoration: underline;
                }

                section h3 {
                    color: royalblue;
                    padding: 3px 30px;
                    width: fit-content;
                    font-size: 20px;
                    font-weight: lighter;
                }

                section img {
                    width: 70%;
                    height: 300px;
                }

                section p {
                    text-align: left;
                    width:80%;
                    margin: 20px 30px;
                }

                section li {
                    text-align: left;
                    margin-left: 50px;
                }

                section p span {
                    text-decoration: underline;
                }

                h2 {
                    text-align: center;
                }

                table {
                    width: 80%;
                    border-collapse: collapse;
                    margin: 0 auto; 
                    background-color: #f8f8f8;
                    color: black;
                }

                th {
                    border: 4px solid white;
                    padding: 10px;
                    text-align: center;
                    font-size: 18px;
                }

                th {
                    font-weight: bold;
                }

                .corps {
                    font-weight: lighter;
                    margin-top: 5px;
                    font-size: 15px;
                }
                .logo_energie{
                    background-color: grey;
                    float: center;
                    width:20%;
                }
                .conteneur_energie {
                    align-items: center;
                    margin-top: -130px;
                    margin-left: 20%;
                    width: 60%;
                    height: 100vh;
                }

                .image_energie {
                    
                    max-width: 40%;
                    height: auto;
                }

                .texte_energie_avant {
                    margin-top : -200px;
                    margin-right : -200px;
                    background-color: orange;
                    padding: 10px 20px;
                    max-width: 80px;
                    border-radius: 5px;
                    text-align: center;
                }
                .texte_energie_apres {
                    
                    background-color: greenyellow;
                    padding: 10px 20px;
                    max-width: 80px;
                    border-radius: 5px;
                    text-align: center;
                }
            </style>
        """

    string_html = f"""
        </head>
        <body>

            <div class="body_accueil">
                <div class="container_accueil" style="margin-left: 0px;">
                    <div class="box_accueil">
                        <div>{nom}</div>
                        <div>{prenom}</div>
                        <div>{dic['adresse_postale']}</div>
                        <div>{dic['email']}</div>
                        <div>Parcelle {dic['parcelles']}</div>
                    </div>
                    <div class="box_accueil" style="text-align: right;margin-left: 240px; margin-top:0px">
                        <div>{nom_sales}</div>
                        <div>{prenom_sales}</div>
                        <div>{mail_sales}</div>
                    </div>
                </div>
            </div>
            <div style="margin-top: 200px;text-align: center;">
                <img src="{os.path.join(os.path.dirname(__file__),'logo_centre_energie.JPG')}" class="logo_accueil">
            </div>
            <div style="margin-top: 130px; margin-bottom:100px">
                <section style="text-align: center;">
                    <h2 style="margin: auto;">Dimensionnement Pompe à Chaleur</h2>
                    <h3 style="margin: auto;">Simulation réalisée le 06/12/2023</h3>
                    <div style="margin-top:200px; text-align:center;">
                        <p style="margin-left:30%">Note de dimensionnement à destination du professionnel</p>
                    </div>
                </section>
            </div>
            <div>
                <section>
                    <table>
                        <tr>
                            <th>Altitude<div class="corps">{dic['altitude']}</div></th>
                            <th>Température extérieure de base<div class="corps">{dic['temperature_min_ext']}°C</div></th>
                            <th>Température de confort<div class="corps">{dic['temperature']}°C</div></th>
                        </tr>
                        <tr>
                            <th>Surface chauffée<div class="corps">{dic['surface_chauffer']}m²</div></th>
                            <th>Hauteur sous plafond<div class="corps">{dic['hauteur_ss_plafond']}m</div></th>
                            <th>Besoins bruts<div class="corps">{dic['puissance_pac']}kWh</div></th>
                        </tr>
                    </table>
                </section>
            </div>
        </body>
    </html>

    """

    return string_css+string_html