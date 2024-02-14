import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
import plotly.express as px
import matplotlib.pyplot as plt
from dpe_function import *
from api_functions import *
from streamlit_extras.stylable_container import stylable_container
from db_functions import *

def render_page_comparaison():
    
    st.set_page_config(
    page_title="Simuler votre Projet - Comparaison",
    page_icon="👁‍🗨", layout="wide", initial_sidebar_state="collapsed"
)
    no_sidebar()
    background('reno.jpg', 'center right')

    styled_button()
    css()

    if 'data' in st.session_state:
        dic = st.session_state.data
        #st.json(dic)
    else :
        dic = {'adresse_postale': ["425 Route de Soucieu 69440 Saint Laurent d'Agny"], 'departement': ['01 - Ain'], 'parcelles': ['342'], 'pente_toit': [None], 'altitude': [None], 'masque_solaire': ['Oui'], 'orientation_toit': [None], 'type_personne': ['Particulier'], 'nom': [''], 'email': [''], 'prenom': [''], 'type_projet': ['Résidence Secondaire'], 'nbr_niveaux': [None], 'vitrage': [None], 'combles': [None], 'etat_charpente': [None], 'annee_construction': [1960], 'type_charpente': [None], 'isolation_comble': ['Non'], 'isolation_mur': ['Non'], 'nbr_personne': [1], 'temperature': [18], 'hauteur_ss_plafond': [2.0], 'surface': [50], 'surface_chauffer': [50], 'equipement_pv_passe': ['Oui'], 'puissance_deja_installee': [0.0], 'etude_solaire_passe': ['Oui'], 'dpe_passe': 
        ['Oui'], 'dpe': [None], 'puissance_kva': [None], 'fournisseur': [None], 'compteur': ['Monophasé'], 'abonnement': [None], 'montant_facture': [2000], 'connaissance_facture_elec': ['Non'], 'chauffage_electrique': [None], 'gaz_fioul': [['Gaz', 'Fioul']], 'gaz_facture':[1300], 'fioul_facture':[300], 'fioul_litre':[2000],'type_chaudiere': [None], 'type_materiel': [None], 'age_chaudiere': [5], 'chaudiere_electrique': ['Non'], 'autre_systeme_chauffage': [[]], 'hauteur_ecs': [None], 'ballon_eau_chaude_electrique': [None], 'climatisation': [None], 'plaque_cuisson': [None], 'lave_vaisselle': [None], 'seche_linge': [None], 'systeme_vmc': [None], 'type_four': [None], 'lave_linge': [None], 'voiture_electrique': [None], 'piscine_chauffee': [None], 'frigidaire': [[]], 'congelateur': [[]], 'habitude_conso': [None], 'ressources_annuelles': [20000], 'interesse': [[]], 'id': [0], 'nvl_conso_elec_kwh_ameliore_materiels_sans_pv':[1000], 'nvl_facture_elec_ameliore_materiels_sans_pv':[230],'nvl_facture_gaz':[50], 'nvl_facture_fioul_autre':[0], 'prod_total_annee':[8000], 'economies_annnuelles_pv_autoconso':[2160], 'gains_annnuelles_pv_surplus':[190] }
    

    tab = valeur_tabulees()
    prix_kwh = tab['prix_kwh']
    adresse = dic['adresse_postale'][0]
    try:
        facture_elec = dic['montant_facture'][0]
    except:
        facture_elec = dic['montant_facture']
    
    facture_gaz, facture_fioul = 0, 0
    try:
        if 'Gaz' in dic['gaz_fioul'][0]:
            facture_gaz = dic['gaz_facture'][0]
        if 'Fioul' in dic['gaz_fioul'][0]:
            facture_fioul = dic['fioul_facture'][0]
    except:
        if 'Gaz' in dic['gaz_fioul']:
            facture_gaz = dic['gaz_facture']
        if 'Fioul' in dic['gaz_fioul']:
            facture_fioul = dic['fioul_facture']

    facture_gaz_fioul = facture_gaz + facture_fioul
    facture_total = facture_elec + facture_gaz_fioul
    kwh_elec = facture_elec/prix_kwh
    
    if test_connexion_internet():
        result = obtenir_dpe_par_adresse(adresse)
    else:
        result = None
    
    if result == None:
        classe_dpe = 'D'
        classe_dpe_ges = 'D'
        nbr_ges = 30
        nbr_energie = 200
    else:
        classe_dpe = result['classe_consommation_energie']
        classe_dpe_ges = result['classe_estimation_ges']
        nbr_ges = result['estimation_ges']
        nbr_energie = result['consommation_energie']

    commentaires_batiment = {'A':'Bâtiment très performant !', 'B':'Bâtiment performant', 'C':'Bâtiment plutôt performant', 'D':'Bâtiment assez performant', 'E':'Bâtiment assez peu performant', 'F':'Bâtiment peu performant', 'G':'Bâtiment très peu performant'}
    commentaires_performance = {'A':'Très bonne performance énergétique','B':'Bonne performance énergétique','C':'Assez bonne performance énergétique','D':'Performance énergétique moyenne','E':'Performance énergétique moyenne','F':'Mauvaise performance énergétique','G':'Très mauvaise performance énergétique'}
    commentaires_ges = {'A':'Votre bâtiment émet très faiblement','B':'Votre bâtiment émet faiblement','C':'Votre bâtiment émet assez peu','D':'Votre bâtiment émet moyennement','E':'Votre bâtiment émet moyennement','F':'Votre bâtiment émet beaucoup','G':'Votre bâtiment émet vraiment beaucoup'}
    commentaire_batiment, commentaire_performance, commentaire_ges = commentaires_batiment[classe_dpe], commentaires_performance[classe_dpe], commentaires_ges[classe_dpe_ges]

    nvl_conso_elec = dic['nvl_conso_elec_kwh_ameliore_materiels_sans_pv']
    nvl_facture_elec, nvl_facture_gaz, nvl_facture_fioul_autre = dic['nvl_facture_elec_ameliore_materiels_sans_pv'], dic['nvl_facture_gaz'], dic['nvl_facture_fioul_autre']
    nvl_facture_total = nvl_facture_elec+nvl_facture_gaz+nvl_facture_fioul_autre
    
    prod_total_annee = dic['prod_total_annee']
    economies_annnuelles_pv_autoconso = dic['economies_annnuelles_pv_autoconso']
    gains_annnuelles_pv_surplus = dic['gains_annnuelles_pv_surplus']
    economies_tout_confondu = (facture_total-nvl_facture_total) + economies_annnuelles_pv_autoconso + gains_annnuelles_pv_surplus

    ratio_perf_matos_elec = nvl_conso_elec/kwh_elec
    nv_dpe, nv_ges = nbr_energie*ratio_perf_matos_elec, nbr_ges*ratio_perf_matos_elec
    
    etiquettes_dpe = {50:'A', 90:'B', 150:'C', 230:'D', 330:'E', 450:'F'}
    etiquettes_ges = {5:'A', 10:'B', 20:'C', 35:'D', 55:'E', 80:'F'}
    nv_dpe_lettre, nv_ges_lettre = 'G', 'G'
    for nbr in reversed(etiquettes_dpe.keys()):
        if nv_dpe<=nbr:
            nv_dpe_lettre = etiquettes_dpe[nbr]
    for nbr in reversed(etiquettes_ges.keys()):
        if nv_ges<=nbr:
            nv_ges_lettre = etiquettes_ges[nbr]
    nv_commentaire_batiment, nv_commentaire_performance, nv_commentaire_ges = commentaires_batiment[nv_dpe_lettre], commentaires_performance[nv_dpe_lettre], commentaires_ges[nv_ges_lettre]

    this_css_style = css_from_function()
    list(this_css_style).append("""
            .st-ij {color:#39e839;}
            """)
    with stylable_container(
            key='adresse_container',
            css_styles = this_css_style
            ):
        col1, col2 = st.columns(2)
        with col1:
            st.header("Avant rénovation  ⏪")
            tab1, tab2, tab3 = st.tabs(['Résumé', 'Energie', 'GES'])
            with tab1:
                show('',('Consommation électrique',"{:,}".format(int(kwh_elec)).replace(",", " "), 'kwH'))
                show('',('Facture électrique actuelle',"{:,}".format(int(facture_elec)).replace(",", " "), '€'))
                show('',('Facture gaz/fioul actuelle',"{:,}".format(int(facture_gaz_fioul)).replace(",", " "), '€'))
                show('',('Total des dépenses énergies',"{:,}".format(int(facture_total)).replace(",", " "), '€'))
            with tab2:
                show('',('Etiquette énergétique',classe_dpe, ''))
                show('',('Consommation énergétique', round(nbr_energie), 'kWh/m².an'))
                show('',(commentaire_batiment, '', ''))
                show('',(commentaire_performance, '', ''))
            with tab3:
                show('',('Classe GES',classe_dpe_ges, ''))
                show('',('Emission GES',nbr_ges, 'kCO2/m².an'))
                show('',(commentaire_ges,'', ''))
        with col2:
            st.header("Après rénovation  ⏩")
            tab1, tab2, tab3 = st.tabs(['Résumé', 'Energie', 'GES'])
            with tab1:
                show('',('Votre nouvelle consommation électrique',"{:,}".format(int(nvl_conso_elec)).replace(",", " "), 'kwH'))
                show('',('Nouvelle facture électricité gaz/fioul',"{:,}".format(int(nvl_facture_total)).replace(",", " "), '€'))
                show('',('Production solaire',"{:,}".format(int(prod_total_annee)).replace(",", " "), 'kwH'))
                show('',('Economies autoconso',"{:,}".format(int(economies_annnuelles_pv_autoconso)).replace(",", " "), '€'))
                show('',('Revente de surplus',"{:,}".format(int(gains_annnuelles_pv_surplus)).replace(",", " "), '€'))
                show('',('Total économies + gains',"{:,}".format(int(economies_tout_confondu)).replace(",", " "), '€/an'))
            with tab2:
                show('',('Etiquette énergétique',nv_dpe_lettre, ''))
                show('',('Consommation énergétique', round(nv_dpe), 'kWh/m².an'))
                show('',(nv_commentaire_batiment, '', ''))
                show('',(nv_commentaire_performance, '', ''))
            with tab3:
                show('',('Classe GES',nv_ges_lettre, ''))
                show('',('Emission GES',round(nv_ges), 'kCO2/m².an'))
                show('',(nv_commentaire_ges,'', ''))



        
        if st.button("Suivant"):
            if 'data' in st.session_state:
                dic = st.session_state.data
                dic['classe_dpe'] = classe_dpe
                dic['classe_dpe_ges'] = classe_dpe_ges
                dic['nbr_ges'] = nbr_ges
                dic['nbr_energie'] = nbr_energie
                
                dic['nv_ges_lettre'] = nv_ges_lettre
                dic['nv_ges'] = nv_ges
                dic['nv_dpe_lettre'] = nv_dpe_lettre
                dic['nv_dpe'] = nv_dpe


                st.session_state.data = dic
                update_or_insert_data(dic)
                
            switch_page('simulation_eco_financement')

render_page_comparaison()