import os 
import sys
import streamlit as st
from datetime import datetime
import pandas as pd

path_functions = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,path_functions)
from functions import valeur_tabulees
from db_functions import *

def audit_string_html(dic):
    lettre_avant, lettre_apres = dic['classe_dpe'], dic['nv_dpe_lettre']
    dic_etiquette_couleur = {'A':'#00A34B', 'B':'#00AF4C', 'C':'#ADD13D', 'D':'#E2E430', 'E':'#FDC41C' , 'F':'#F79344', 'G':'#EE3F3B'}
    couleur_avant, couleur_apres = dic_etiquette_couleur[lettre_avant], dic_etiquette_couleur[lettre_apres]
    dic_etiquette_hauteur = {'A':13, 'B':46, 'C':92, 'D':130, 'E':178 , 'F':215, 'G':253}
    hauteur_avant, hauteur_apres = dic_etiquette_hauteur[lettre_avant], dic_etiquette_hauteur[lettre_apres]
        
    nom, prenom = dic['nom'].upper(), dic['prenom'].upper()
    date = datetime.now().strftime("%d-%m-%Y")
    

    #df = pd.read_csv('./../df_to_save/zoho_file.csv')
    #nom_sales, prenom_sales = df['nom'].iloc[0],df['prenom'].iloc[0] 
    #mail_sales = df['mail'].iloc[0]

    mail_sales = st.session_state.mail
    nom_sales = retrieve_data('user_credentials', mail_sales, 'nom')
    prenom_sales = retrieve_data('user_credentials', mail_sales, 'prenom')
    
    
    tab = valeur_tabulees()

    valo_immo = dic['gain_et_eco_elec_par_an']/dic['ancienne_facture_elec'] * 10  # revoir calcul

    if dic['equipement_pv_passe']=='Non':
        dic['puissance_deja_installee'] = 0

    if dic['autre_systeme_chauffage']!=[]:
        chauffage_appoint = dic['autre_systeme_chauffage'][0][0]
        try:
            facture_autre_syst_chauffage = dic['facture_autre_syst_chauffage'][0]
        except:
            facture_autre_syst_chauffage = dic['facture_autre_syst_chauffage']
    else:
        chauffage_appoint = 'Non'
        facture_autre_syst_chauffage = 0

    
    if dic['equipement_pv_passe']!="Oui":
        dic['puissance_deja_installee']=0
    
    if dic['interesse']==[]:
        dic['interesse'] = "L'autoconsommation"

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
                    <div class="box_accueil" style="text-align: right;margin-left: 450px; margin-top:-100px">
                        <div>{nom_sales}</div>
                        <div>{prenom_sales}</div>
                        <div>{mail_sales}</div>
                    </div>
                </div>
                <span class="span_accueil"></span>
            </div>
            <div style="margin-top: 200px;text-align: center;">
                <img src="{os.path.join(os.path.dirname(__file__),'logo_centre_energie.JPG')}" class="logo_accueil">
            </div>
            <div style="margin-top: 130px; margin-bottom:100px">
                <section style="text-align: center;">
                    <h2 style="margin: auto;">Audit énergétique</h2>
                    <h3 style="margin: auto;">Simulation réalisée le 06/12/2023</h3>
                </section>
            </div>
            
            
<div style="margin-top: 50px; margin-right: 6%; text-align: center;">
    <table style="border-collapse: collapse; width: 800px; margin: 0 auto; background-color:white">
        <tr>
            <td colspan="3" class="info_accueil" style="text-align: center;">
                <img src="{os.path.join(os.path.dirname(__file__),'icon_location.png')}" alt="Département">
            </td>
            <td colspan="3" class="info_accueil" style="text-align: center;">
                <img src="{os.path.join(os.path.dirname(__file__),'icon_calendar.png')}" alt="Année de construction">
            </td>
            <td colspan="3" class="info_accueil" style="text-align: center;">
                <img src="{os.path.join(os.path.dirname(__file__),'icon_home.png')}" alt="Surface habitable">
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
                        Cet audit vous est fourni à titre indicatif et n'engage ni son auteur ni l'éditeur du logiciel qui a servi à le réaliser. Seul un bureau d'étude énergétique habilité peut délivrer une étude énergétique réglementaire
                    </p>
                </section>
            </div>



            <header style="margin-top:100px; text-align:center">
                <span>
                    <img style="margin-left:60px; margin-top:-10px; width:fit-content" src="{os.path.join(os.path.dirname(__file__),'logo_centre_energie.JPG')}" alt="Votre Logo">
                    <h1 style="margin-top:-26px; margin-right:1800px">Vous accompagne dans vos projets</h1>
                </span>
                
            </header>

            <section>
                <img src="{os.path.join(os.path.dirname(__file__),'image.jpg')}" alt="Votre Photo">
                <h1>Le but de ce document</h1>
                <p>Ce document vous permet de conserver les informations essentielles renseignées lors de l’étude effectuée avec notre
                    conseiller Centre énergie.<br>
                    <span>Elle vous présente :</span>
                    <ul>
                        <li>Une synthèse des caractéristiques de votre habitation.</li>
                        <li>La simulation des gains et économies réalisés grâce au matériel préconisé.</li>
                        <li>Une simulation des aides financières auxquelles vous êtes éligibles.</li>
                        <li>Les avantages et caractéristiques du matériel préconisé.</li>
                        <li>La simulation d’amortissement du matériel grâce aux économies réalisées</li>
                    </ul>
                </p>
                <p>
                    Ce document est calculé sur la base des données PVGIS.<br>
                    Toutes les simulations chiffrées présentes dans ce document sont purement indicatives et basées sur les éléments que
                    vous nous avez communiqués. La consommation énergétique d’une habitation étant dépendante de nombreux
                    facteurs, Centre énergie ne saurait voir sa responsabilité engagée dans l’hypothèse où cette simulation ne
                    correspondrait pas à la consommation réelle
                </p>
                <h1>Avantages de la rénovation énergétique</h1>
                <p>Votre projet de rénovation touche à la dimension énérgétique de votre habitat.<br>
                    <span>Cela vous apporte de nombreux avantages :</span>
                </p>
                <img src="{os.path.join(os.path.dirname(__file__),'image.jpg')}" alt="Votre Photo">
                <div>
                    <span>
                        <img style="height:auto; margin:5px 15px 10px 30px" src="{os.path.join(os.path.dirname(__file__),'logo_centre_energie.JPG')}" alt="Votre Photo">
                        <p>
                            De plus, vous participez au respect de l'environnement.
                            Avec l'augmentation du prix de l'énergie, ne rien faire revient souvent
                            plus cher           
                        </p>
                    </span>
                </div>
            </section>
            <section>
                <h1>A. CARACTÉRISTIQUES HABITAT</h1>
                <img src="{os.path.join(os.path.dirname(__file__),'image.jpg')}" alt="Votre Photo">
                <h3>Les informations sur votre habitation son budget et sa consommation</h3>
            
                <table>
                    <tr>
                        <th>La pente du toit<div class="corps">{dic['pente_toit']}</div></th>
                        <th>Orientation du toit<div class="corps">{dic['orientation_toit']}</div></th>
                        <th>Vos fenêtres sont<div class="corps">{dic['vitrage']}</div></th>
                        <th>Votre couverture<div class="corps">{dic['combles']}</div></th>
                    </tr>
                    <tr>
                        <th>Votre type de charpente<div class="corps">{dic['type_charpente']}</div></th>
                        <th>Nombre de personnes dans le logement<div class="corps">{dic['nbr_personne']} Personne(s)</div></th>
                        <th>Isolation des combles réalisée ?<div class="corps">{dic['isolation_comble']}</div></th>
                        <th>Surface du logement<div class="corps">{dic['surface']} m²</div></th>
                    </tr>
                    <tr>
                        <th>Surface de chauffe<div class="corps">{dic['surface_chauffer']} m²</div></th>
                        <th>Puissance de votre compteur<div class="corps">{dic['puissance_kva']} kVA</div></th>
                        <th>Type de compteur<div class="corps">{dic['compteur']}</div></th>
                        <th>Montant de votre facture d'électricité<div class="corps">{dic['montant_facture']} €</div></th>
                    </tr>
                    <tr>
                        <th>Votre consommation annuelle en kWh<div class="corps">{round(dic['montant_facture']/tab['prix_kwh'])} kWh</div></th>
                        <th>Facture annuelle de gaz/fioul<div class="corps">{dic['gaz_facture']+dic['fioul_facture']} €</div></th>
                        <th>Type de la chaudière gaz/fioul<div class="corps">{dic['type_chaudiere']}</div></th>
                        <th>Matériel chauffant utilisé<div class="corps">{dic['type_materiel']}</div></th>
                    </tr>
                    <tr>
                        <th>Avez-vous un chauffage d'appoint ?<div class="corps">{chauffage_appoint}</div></th>
                        <th>Montant de la facture<div class="corps">{facture_autre_syst_chauffage} €</div></th>
                        <th>Avez-vous un ballon d'eau chaude ?<div class="corps">{dic['ballon_eau_chaude_electrique']}</div></th>
                        <th>Capacité du ballon<div class="corps">{dic['capacite_ballon']} Litre(s)</div></th>
                    </tr>
                    <tr>
                        <th>Hauteur s.plafond du local ballon<div class="corps">{dic['hauteur_ecs']}</div></th>
                        <th>Puis. des panneaux sol. installés<div class="corps">{dic['puissance_deja_installee']} kWc</div></th>
                        <th>Votre type d'ampoule<div class="corps">Les lampes à LED, L'ampoule à incandescence</div></th>
                        <th>Ressources annuelles du foyer<div class="corps">{dic['ressources_annuelles']} €</div></th>
                    </tr>
                    <tr>
                        <th>Avez-vous bénéficié d'un crédit d'impôt ces 5 dernières années ?<div class="corps">Non</div></th>
                        <th>Montant du crédit d'impôt<div class="corps">0 €</div></th>
                        <th>Intéressé par<div class="corps">{dic['interesse']}</div></th>
                    </tr>
                </table>
            </section>
            <section>
                <h1>B. SÉLECTION DE MATÉRIELS ET SERVICES</h1>
                <img src="{os.path.join(os.path.dirname(__file__),'image.jpg')}" alt="Votre Photo">
                <h2>1. Matériels et services</h2>
                <p>
                    <span>Liste de matériels et services préconisés pour la rénovation :</span>
                    <br>
                    <ul>
                        <li>Panneaux photovoltaïques : {dic['puissance_panneaux']} kWc {dic['nbr_panneaux']} panneaux de {dic['pv_unitaire']} ({dic['surface_panneaux']} m²)</li>
            """

    string_for_matos  = ""
    for matos in dic['materiels']:
        string_for_matos += f"""
                        <li>{matos}</li>
                        """
    string_suite = f"""
                        
                    </ul>
                </p>
                <h2>2. Données techniques</h2>
                <h3>Les informations techniques</h3>
                <table>
                    <tr>
                        <th>Heures d'ensoleillement<div class="corps">{dic['h_soleil']} h</div></th>
                        <th>Puissance restituée<div class="corps">{int(dic['p_restit'])} kWh</div></th>
                        <th>Coefficient météorologique<div class="corps">{100*dic['coef_meteo']} %</div></th>
                    </tr>
                    <tr>
                        <th>Coefficient de performance<div class="corps">{dic['coef_perf']}</div></th>
                        <th>Pertes du système<div class="corps">{round(100*dic['perte'])}%</div></th>
                        <th>Le coût du kWh<div class="corps">Consommé : {dic['prix_achete']} €/kWh<br>Revendu : {dic['prix_revendu']} €/kWh</div></th>
                    </tr>
                </table>
                <h2>3. Les chiffres</h2>
                <h3>Gains et économies réalisés</h3>
                <table>
                    <tr>
                        <th>Électricité<div class="corps">{int(dic['gain_et_eco_elec_par_an'])} €</div></th>
                        <th>E.C.S/Chauffage **<div class="corps">{dic['eco_gaz_fioul_autres']} €</div></th>
                    </tr>
                    <tr>
                        <th>Total Minimum / Mois<div class="corps">??? €</div></th>
                        <th>Total Minimum N+1<div class="corps">??? €</div></th>
                    </tr>
                </table>
                <h2 style="margin-top:300px; margin-bottom:70px">4. Transition énergétique</h2>
                <span>
                    <div style="width: 50%;">
                        <h3>Vous avez choisi l'autoconsommation</h3>
                        <table>
                            <tr>
                                <th>Économies sur l'indépendance<div class="corps">{int(dic['economies_annnuelles_pv_autoconso'])} €</div></th>
                                <th>Économies du surplus<div class="corps">{int(dic['gains_annnuelles_pv_surplus'])} €</div></th>
                            </tr>
                        </table>
                    </div>
                    <img class="logo_droite" src="{os.path.join(os.path.dirname(__file__),'pie_chart.png')}" style="max-width:45%; max-height:55%; position:absolute; right:-180px; top:5400px " alt="Pie Chart Logo">
                </span>
                <br>
                <br>
                <h2>5. Prévisions</h2>
                <h3>Prévision de l'évolution énergétique et vos gain/économies</h3>
                <table>
                    <tr>
                        <th>Indexation de<div class="corps">{dic['indexation']}% /an</div></th>
                        <th>Prévisions sur<div class="corps">{dic['annnees_prevision']} Ans</div></th>
                        <th>Total/mois<div class="corps">{int(dic['economie_par_mois_moyen'])} €</div></th>
                        <th>Total/an<div class="corps">{int(dic['economie_par_an_moyen'])} €</div></th>
                        <th>Total des gains et économies sur 15 ans<div class="corps">{int(dic['economie_total'])} €</div></th>
                    </tr>
                </table>
                <h2>6. Les aides</h2>
                <h3>Les aides pour financer votre projet</h3>
                <table>
                    <th>Ma prime rénov<div class="corps">{dic['mpr']} €</div></th>
                    <th>Prime coup de pouce (CEE)<div class="corps">{dic['cee']} €</div></th>
                    <th>Prime EDF<div class="corps">{dic['edf']} €</div></th>
                    <th>Récupération de la TVA<div class="corps">{dic['tva']} €</div></th>
                    <th>Déduction des crédits d'impôts<div class="corps">{dic['credit']} €</div></th>
                    <th>Total<div class="corps">{dic['total_aides']} €</div></th>
                </tr>
            </table>
            
            </section>
            <section>
                <h1>C.COMPARAISON</h1>
                <img src="{os.path.join(os.path.dirname(__file__),'image.jpg')}" alt="Votre Photo">
                <p>Diagnostic indicatif réalisé selon les dépenses énergétiques liées au chauffage et à l'eau chaude sanitaire. Ce diagnostic,
                    établit ci-dessous ne peut se substituer à un DPE réalisé par un bureau d'étude.
                </p>
                <h2 style="margin-top:300px">1. Résumé énergétique</h2>
                <h3>Comparaison de votre projet avant et après</h3>
                <table>
                    <tr>
                        <th><div class="corps">AVANT</div></th>
                        <th><div class="corps">APRES</div></th>
                    </tr>
                    <tr>
                        <th>Consommation électrique<div class="corps">{int(dic['ancienne_conso_elec'])} kWh</div></th>
                        <th>Nouvelle consommation électrique<div class="corps">{int(dic['nvl_conso_elec_kwh_ameliore_materiels_sans_pv'])} kWh</div></th>
                    </tr>
                    <tr>
                        <th>Facture électrique actuelle<div class="corps">{dic['ancienne_facture_elec']} €</div></th>
                        <th>Nouvelle facture électrique<div class="corps">{int(dic['nvl_facture_elec_ameliore_materiels_sans_pv'])} €</div></th>
                    </tr>
                    <tr>
                        <th>Production solaire<div class="corps">0 kWh</div></th>
                        <th>Nouvelle production solaire<div class="corps">{round(dic['prod_total_annee'])} kWh</div></th>
                    </tr>
                    <tr>
                        <th>Économies sur l'indépendance<div class="corps">0 €</div></th>
                        <th>Nouvelles économies sur l'indépendance<div class="corps">{int(dic['economies_annnuelles_pv_autoconso'])} €</div></th>
                    </tr>
                    <tr>
                        <th>Revente de surplus<div class="corps">0 €</div></th>
                        <th>Nouvelle revente de surplus<div class="corps">{round(dic['gains_annnuelles_pv_surplus'])} €</div></th>
                    </tr>
                    <tr>
                        <th>Total des dépenses énergies<div class="corps">{round(dic['nvl_facture_elec_ameliore_materiels_sans_pv'])}€/an</div></th>
                        <th>Total économies + gains<div class="corps">{round(dic['gain_et_eco_elec_par_an'])}€/an</div></th>
                    </tr>
                </table>
                <h3>Comparaison sur la valeur immobilière</h3>
                <table>
                    <tr>
                        <th><div class="corps"></div></th>
                        <th><div class="corps">AVANT</div></th>
                        <th><div class="corps">APRES</div></th>
                    </tr>
                    <tr>
                        <th>Catégorie énergie</th>
                        <th><div class="corps">{dic['classe_dpe']} ({int(dic['nbr_energie'])})</div></th>
                        <th><div class="corps">{dic['nv_dpe_lettre']} ({int(dic['nv_dpe'])})</div></th>
                    </tr>
                    <tr>
                        <th>Catégorie climat</th>
                        <th><div class="corps">{dic['classe_dpe_ges']} ({int(dic['nbr_ges'])})</div></th>
                        <th><div class="corps">{dic['nv_ges_lettre']} ({int(dic['nv_ges'])})</div></th>
                    </tr>
                    <tr>
                        <th>Valeur du bien immobilier</th>
                        <th><div class="corps">0 %</div></th>
                        <th><div class="corps">+ {int(valo_immo)} %</div></th>
                    </tr>
                </table>
            </section>
            <section>  
            
                <h3>Diagnostic</h3>
            </section style="margin-bottom:100px">
            <div style="display: flex; align-items: center;">
            <div style="margin-left: 150px; margin-top:50px; position: relative;">
                <img src="{os.path.join(os.path.dirname(__file__),'etiquette_energie.png')}" alt="Image Etiquette Energie" style="width: 300px; height: auto;">

                <div style="position: absolute; top: {hauteur_avant}px; right: 300px; background-color: {couleur_avant}; text-align: center; padding: 5px; width: 120px; border-radius:5px; font-size:20px">
                    Avant {int(dic['nbr_energie'])}
                </div>
                
                <div style="position: absolute; top: {hauteur_apres}px; right: 160px; background-color: {couleur_apres}; text-align: center; padding: 5px; width: 120px;border-radius:5px; font-size:20px">
                    Après {int(dic['nv_dpe'])}
                </div>
            </div>

        </body>
        </html>

        """
    string = string_css+string_html + string_for_matos + string_suite
    

    return string