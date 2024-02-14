import matplotlib.pyplot as plt
import os
import pandas as pd
from datetime import datetime
import streamlit as st
import sys

path_functions = os.path.dirname(os.path.dirname(__file__)) # dir de SolarSales
sys.path.insert(0,path_functions)
from db_functions import *

def rapport_string_html(dic):


    current_path = os.path.dirname(__file__)
    
    nom, prenom = dic['nom'].upper(), dic['prenom'].upper()
    date = datetime.now().strftime("%d-%m-%Y")

    mail_sales = st.session_state.mail
    nom_sales = retrieve_data('user_credentials', mail_sales, 'nom')
    prenom_sales = retrieve_data('user_credentials', mail_sales, 'prenom')
    

    #df = pd.read_csv('./../df_to_save/zoho_file.csv')
    #nom_sales, prenom_sales = df['nom'].iloc[0],df['prenom'].iloc[0]
    #mail_sales = df['mail'].iloc[0]



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
                    width: 90%;
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
                    display: flex;
                    align-items: center;
                    margin-top: -130px;
                    margin-left: 20%;
                    width: 60%;
                    height: 100vh;
                }

                .image_energie {
                    flex: 1;
                    max-width: 40%;
                    height: auto;
                }

                .texte_energie_avant {
                    flex: 1;
                    background-color: orange;
                    padding: 10px 20px;
                    max-width: 80px;
                    margin-right: 10px;
                    border-radius: 5px;
                    transform: translateY(0px);
                    text-align: center;
                }
                .texte_energie_apres {
                    flex: 1;
                    background-color: greenyellow;
                    padding: 10px 20px;
                    max-width: 80px;
                    border-radius: 5px;
                    transform: translateY(-40px);
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
                    <div class="box_accueil" style="text-align: right;margin-left: 450px; margin-top:-100px">
                        <div>{nom_sales}</div>
                        <div>{prenom_sales}</div>
                        <div>{mail_sales}</div>
                    </div>
                </div>
                <span class="span_accueil"></span>
            </div>
            <div style="margin-top: 200px;text-align: center;">
                <img src="C:/Users/arthu/OneDrive/Documents 3A CS/Projet dev/streamlit-app/SolarSales/generation_pdf/logo_centre_energie.JPG" class="logo_accueil">
            </div>
            <div style="margin-top: 130px; margin-bottom:100px">
                <section style="text-align: center;">
                    <h2 style="margin: auto;">Rapport Financier</h2>
                    <h3 style="margin: auto;">Simulation réalisée le {date}</h3>
                </section>
            </div>
            
            
<div style="margin-top: 50px; margin-right: 6%; text-align: center;">
    <table style="border-collapse: collapse; width: 800px; margin: 0 auto; background-color:white">
        <tr>
            <td colspan="3" class="info_accueil" style="text-align: center;">
                <img src="C:/Users/arthu/OneDrive/Documents 3A CS/Projet dev/streamlit-app/SolarSales/generation_pdf/icon_location.png" alt="Département">
            </td>
            <td colspan="3" class="info_accueil" style="text-align: center;">
                <img src="C:/Users/arthu/OneDrive/Documents 3A CS/Projet dev/streamlit-app/SolarSales/generation_pdf/icon_calendar.png" alt="Année de construction">
            </td>
            <td colspan="3" class="info_accueil" style="text-align: center;">
                <img src="C:/Users/arthu/OneDrive/Documents 3A CS/Projet dev/streamlit-app/SolarSales/generation_pdf/icon_home.png" alt="Surface habitable">
            </td>
        </tr>
        <tr>
            <td colspan="3" style="font-weight: bold; text-align: center;">Département</td>
            <td colspan="3" style="font-weight: bold; width: 80px; text-align: center;">Année de construction</td>
            <td colspan="3" style="font-weight: bold; width: 80px; text-align: center;">Surface habitable</td>
        </tr>
        <tr>
            <td colspan="3" style="text-align: center;">{dic['departement'][0]}</td>
            <td colspan="3" style="text-align: center;">{dic['annee_construction']}</td>
            <td colspan="3" style="text-align: center;">{dic['surface']} m²</td>
        </tr>
    </table>
</div>




            <div style="margin-top: 350px; margin-bottom:50px;  text-align:center;">
                <section style="margin:auto;">
                    <p style="text-align: center; margin-left: 80px; color: royalblue; font-size: 15px;">
                        Ce rapport vous est fourni à titre indicatif et n'engage ni son auteur ni l'éditeur du logiciel qui a servi à le réaliser.
                    </p>
                </section>
            </div>



            <header style="margin-top:100px; text-align:center">
                <span>
                    <img style="margin-left:5px; margin-top:-10px; height:36px; width:auto;" src="C:/Users/arthu/OneDrive/Documents 3A CS/Projet dev/streamlit-app/SolarSales/generation_pdf/logo_centre_energie.JPG" alt="Votre Logo">
                    <h1 style="margin-top:-35px; margin-right:5px; width:750px; font-size:26px">Nos conseils pour vous accompagner dans vos projets</h1>
                </span>
                
            </header>

            <section>
        
        <img src="C:/Users/arthu/OneDrive/Documents 3A CS/Projet dev/streamlit-app/SolarSales/generation_pdf/image.jpg" alt="Votre Photo">
        <h2>1. Économies et mensualités</h2>
        <h1>A. FINANCEMENT</h1>
        <table>
            <tr>
                <th>Économies N+1<div class="corps">{dic['economie_n_plus_un']} €/mois</div></th>
                <th>Report<div class="corps">{dic['report_jours']} jours</div></th>
                <th>Montant matériels et services<div class="corps">{dic['montant_materiels_et_services']} €</div></th>
            </tr>
            <tr>
                <th>1ère mensualité<div class="corps">{dic['premiere_mensualite']} €</div></th>
                <th>Durée initiale<div class="corps">{dic['duree_initiale']} mois</div></th>
                <th>Partenaire financier<div class="corps">{dic['partenaire_financier']}</div></th>
            </tr>
        </table>
        <h2>2. Aides au projet</h2>
        <h3>Cumul de toutes les aides pour financer votre projet</h3>
        <table>
            <tr>
                <th>Économies sur 6 mois<div class="corps">{dic['economies_sur_6_mois']} €</div></th>
                <th>Ma prime rénov<div class="corps">{dic['MPR']} €</div></th>
                <th>Prime coup de pouce (CEE)<div class="corps">{dic['CEE']} €</div></th>
                <th>EDF<div class="corps">{dic['EDF']} €</div></th>
                <th>Récupération TVA<div class="corps">{dic['TVA']} €</div></th>
            </tr>
            <tr>
                <th>Déduction crédit d'impôts<div class="corps">??? €</div></th>
                <th>Apport personnel<div class="corps">??? €</div></th>
                <th>Total<div class="corps">??? €</div></th>
                <th>Reste à éco-financer<div class="corps">???? €</div></th>
            </tr>
        </table>
        <h2>3. Éco-financement</h2>        
        <h3>Simulation de votre projet pour financer grâce aux économies d'énergies</h3>
        <table>
            <tr>
                <th>Amortissement<div class="corps">{dic['amortissement_mois']} mois</div></th>
                <th>Mensualités<div class="corps">{dic['mensualites_choisies']} €</div></th>
                <th>Économies Moy/mois<div class="corps">{dic['economies_moy_par_mois']} €/mois</div></th>
            </tr>
        </table>     
        <h2 style="margin-top:300px">4. Prévision financière</h2>
        <h3>Simulation de votre projet pour financer grâce aux économies d'énergies</h3>
        <table>
            <tr>
                <th>Gains et économies mensuelles pendant éco-financement<div class="corps">{dic['gain_eco_mensuelles_pdt_eco_financement']} €</div></th>
                <th>Gains et économies annuelles pendant éco-financement<div class="corps">{dic['gain_eco_annuelles_pdt_eco_financement']} €</div></th>
                <th>Prévisions sur<div class="corps">{dic['prevision_annee_eco_financement']} ans</div></th>
                <th>Total gains et économies sur 30 ans<div class="corps">{dic['gain_et_eco_prevision_eco_financement']} €</div></th>
            </tr>
        </table>        

        <img style="max-width:90%; height:auto" alt="barchart" src="{os.path.join(current_path,'bar_chart.png')}">

    </section>

    </body>
    </html>

    """


    string = string_css + string_html
    return string