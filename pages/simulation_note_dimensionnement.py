import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
import os
import sys
from streamlit_extras.stylable_container import stylable_container
from db_functions import *

path_pdf = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generation_pdf')
sys.path.insert(0,path_pdf)
from generer_pdf_app import generer_pac_pdf


def render_page_note_dimensionnement():
    
    st.set_page_config(
    page_title="Simuler votre Projet - Note de dimensionnement",
    page_icon="📑", layout="wide", initial_sidebar_state="collapsed")
    no_sidebar()
    #styled_button()
    css()

    if 'data' in st.session_state:
        dic = st.session_state.data
    else:
        dic = {
                "adresse_postale": ["Rue Paul Signac les Mousseaux Le Raincy 93420"],
                "departement": ["93 - Seine-Saint-Denis"],
                "parcelles": ["55"],
                "pente_toit": ["Méditerranéen 10°"],
                "altitude": ["Entre 0 et 500m"],
                "masque_solaire": ["Oui"],
                "orientation_toit": ["Sud"],
                "type_personne": ["Particulier"],
                "nom": ["DUpont"],
                "email": ["dupon@ckhb.fr"],
                "prenom": ["Pierre"],
                "type_projet": ["Résidence Principale"],
                "nbr_niveaux": ["2 niveaux"],
                "vitrage": ["Simple Vitrage"],
                "combles": ["Tuile plate"],
                "etat_charpente": ["Bon Etat"],
                "annee_construction": [1960],
                "type_charpente": ["Bois"],
                "isolation_comble": ["Non"],
                "isolation_mur": ["Non"],
                "nbr_personne": [1],
                "temperature": [18],
                "hauteur_ss_plafond": [2],
                "surface": [50],
                "surface_chauffer": [50],
                "volume": [100],
                "temperature_min_ext": [-7],
                "coef_isolation": [1.8],
                "delta_t": [25],
                "puissance_pac": [4.5],
                "equipement_pv_passe": ["Non"],
                "etude_solaire_passe": ["Oui"],
                "dpe_passe": ["Non"],
                "puissance_kva": [3],
                "fournisseur": ["CDiscount Energy"],
                "compteur": ["Triphasé"],
                "abonnement": ["Base"],
                "montant_facture": [2000],
                "connaissance_facture_elec": ["Non"],
                "chauffage_electrique": ["Oui"],
                "gaz_fioul": [["Gaz", "Fioul"]],
                "gaz_facture": [500],
                "fioul_facture": [500],
                "fioul_litre": [2000],
                "type_chaudiere": ["Basse température"],
                "type_materiel": ["Radiateur seul"],
                "age_chaudiere": [5],
                "chaudiere_electrique": ["Non"],
                "autre_systeme_chauffage": [["Poêle à granulés (pellets)"]],
                "facture_autre_syst_chauffage": [400],
                "hauteur_ecs": ["Inférieur à 2m20"],
                "ballon_eau_chaude_electrique": ["Oui"],
                "climatisation": ["Non"],
                "capacite_ballon": [50],
                "plaque_cuisson": ["A induction"],
                "lave_vaisselle": ["Oui"],
                "seche_linge": ["Oui"],
                "systeme_vmc": ["Oui, simple flux"],
                "type_four": ["Non électrique"],
                "lave_linge": ["Oui"],
                "voiture_electrique": ["Oui"],
                "piscine_chauffee": ["Oui"],
                "frigidaire": [["Un simple", "Un américain"]],
                "congelateur": [["Congélateur coffre"]],
                "habitude_conso": ["Le matin et le soir"],
                "ressources_annuelles": [20000],
                "interesse": [["L'autoconsommation"]],
                "id": [0],
                "nvl_conso_elec_kwh_ameliore_materiels_sans_pv": 6947.826086956522,
                "nvl_facture_elec_ameliore_materiels_sans_pv": 1598.0000000000002,
                "nvl_facture_gaz": 250,
                "nvl_facture_fioul_autre": 450,
                "prod_total_annee": 7524.58,
                "economies_annnuelles_pv_autoconso": 2427.884628571429,
                "gains_annnuelles_pv_surplus": 234.32598757763972,
                "materiels": ["Ballon électrique", "Domotique", "PAC air-eau"],
                "puissance_panneaux": 7,
                "pv_unitaire": "500W",
                "nbr_panneaux": 14,
                "surface_panneaux": 33.6,
                "h_soleil": 1180,
                "p_restit": 7524.58,
                "coef_meteo": 0.8,
                "coef_perf": 1,
                "perte": 0.14,
                "rdt_panneaux": 0.14,
                "prix_achete": 0.23,
                "prix_revendu": 0.1,
                "gain_et_eco_elec_par_an": 3064.2106161490683,
                "eco_gaz_fioul_autres": 700,
                "indexation": 4,
                "annnees_prevision": 15,
                "economie_total": 32331.672218479904,
                "economie_par_an_moyen": 2155.444814565327,
                "economie_par_mois_moyen": 215.54448145653268,
                "MPR": 5000,
                "CEE": 4000,
                "EDF": 1960,
                "TVA": 0,
                "credit": 0,
                "total_aides": 10960,
                "ancienne_conso_elec": 8695.652173913044,
                "ancienne_facture_elec": 2000,
                "classe_dpe": "E",
                "classe_dpe_ges": "F",
                "nbr_ges": 56.76,
                "nbr_energie": 242.58,
                "nv_ges_lettre": "E",
                "nv_ges": 45.35124,
                "nv_dpe_lettre": "D",
                "nv_dpe": 193.82142,
                "economie_n_plus_un": 304,
                "montant_materiels_et_services": 35900,
                "report_jours": 180,
                "duree_initiale": 170,
                "partenaire_financier": "Finance2",
                "premiere_mensualite": 358.59,
                "economies_sur_6_mois": "???",
                "amortissement_mois": 180,
                "mensualites_choisies": 160,
                "economies_moy_par_mois": 472,
                "gain_eco_mensuelles_pdt_eco_financement": 0,
                "gain_eco_annuelles_pdt_eco_financement": 0,
                "prevision_annee_eco_financement": 30,
                "gain_et_eco_prevision_eco_financement": 0
                }

    if 'PAC air-air Quadri' in dic['materiels'] or 'PAC air-eau' in dic['materiels']:
        note_a_faire = True
    else:
        note_a_faire = False

    with stylable_container(
            key='adresse_container',
            css_styles = css_from_function()
            ):    
        if note_a_faire:
            pac_path = generer_pac_pdf(dic)
            path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generation_pdf'), pac_path)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader('Note de dimensionnement à consulter 📋')
                space(1)
                displayPDF(path, 500, 500)
            with col2:
                space(3)
                show('Note de dimensionnement pour la pompe à chaleur. ',('Liste les informations utiles pour la sélection de la PAC.','',''))          
                
                space(2)
                if st.button("Envoyer par mail"):
                    a,b = st.columns(2)
                    with a:
                        expediteur = st.text_input('Expéditeur', value='arthur.pouzargue@outlook.fr')
                        destinataire = st.text_input('Destinataire', value='arthur.pouzargue@outlook.fr')
                    with b:
                        cc = st.text_input('CC', value='arthur.pouzargue@outlook.fr')
                        objet = st.text_input('Objet', value='Rapport Financier')
                    ##pj = piece jointe !!
                    corps = st.text_area('', value=f"""
                    Bonjour,

                    Nous avons le plaisir de .............

                    L'utilisateur reconnaît expressément:
                    
                    Qu'il souhaite prendre un rendez-vous avec un conseiller à domicile, afin d'obtenir un devis détaillé, que cette demande de rendez-vous ne fait pas suite à une sollicitation téléphonique mais à une premier rendez vous au cours duquel un audit énergétique a été réalisé, que ses données personnelles sont traitées conformément aux dispositions légales applicables, comme précisé dans la "Politique de protection des données". 
                    
                    Bonne réception,
                    
                    Cordialement
                    """, height=300)
                    if st.button("Envoyer"):
                        mail(expediteur, destinataire, cc, objet, corps) #attention à mettre le mail comme il fait et mettre le mdp dans les réglages
                    

                    
                
                with open(path, "rb") as pdf_file:
                        pdf_data = pdf_file.read()
                st.download_button(
                    label="Télécharger",
                    data = pdf_data,
                    file_name='note_dimensionnement_PAC.pdf',
                    key='button'
                )           
                    
        else:
            show("", ('Pas de note de dimensionnement à générer. Vous pouvez passer à la suite 😉', '', ''))       
            space(1) 



        
        if st.button("Suivant"):
            switch_page('simulation_synchro_client')

render_page_note_dimensionnement()