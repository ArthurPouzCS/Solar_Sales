import streamlit as st
import time
import re
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
from streamlit_extras.stylable_container import stylable_container
from db_functions import *


def render_page_habitat_2():
    st.set_page_config(
    page_title="Saisir vos Données - Habitat 2",
    page_icon="🏡", layout="wide", initial_sidebar_state="collapsed"
)
    past_audit, last = dont_forget_past_audit()
    no_sidebar()
    styled_button()
    css()
    #background('electricite.jpg', 'center left')
    afficher_frise_chronologique(3)

    with stylable_container(
            key='adresse_container',
            css_styles = css_from_function()
            ):

        with stylable_container(key="adresse_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Diagnostique et Etudes  📊")
                col1, col2 = st.columns(2)
                with col1:
                    equipement_pv_passe = st.radio("Êtes-vous déjà équipé d'une installation photovoltaïque ?", ["Oui", "Non"], index=last('equipement_pv_passe', 'radio', ['Oui', 'Non']))
                    if equipement_pv_passe=="Oui":
                        puissance_deja_installee = st.number_input("Puissance déjà installée", last('puissance_deja_installee', 'number_input'))
                    etude_solaire_passe = st.radio("Avez-vous déjà effectué une étude solaire ?", ["Oui", "Non"], index=last('etude_solaire_passe', 'radio', ['Oui', 'Non']))
                with col2:
                    dpe_passe = st.radio("Avez-vous déjà effectué un DPE ?", ["Oui", "Non"], index=last('dpe_passe', 'radio', ['Oui', 'Non']))
                    if dpe_passe=="Oui":
                        dpe = st.selectbox("Quel était le DPE calculé ?", ["A", "B", "C", "D", "E", "F", "G"], index=last('dpe', 'selectbox', ["A", "B", "C", "D", "E", "F", "G"]))

        with stylable_container(key="adresse_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Caractéristiques électrique  💡")
                col1, col2 = st.columns(2)
                with col1:
                    puissance_kva = st.selectbox("Quelle est la puissance de votre compteur en kVA ?", [3,6,9,12,15,18,24,30,36],index=last('puissance_kva', 'selectbox', [3,6,9,12,15,18,24,30,36]))
                    fournisseur = st.selectbox("Quel est votre fournisseur d'électricité ?", ["TotalEnergies", "Alterna", "Barry", "Bulb", "Direct Energy", "CDiscount Energy", "Butagaz", "Leclerc Energies", "Elecocité", "Energem", "EDF", "ENGIE", "ENI", "Plum", "Proxelia", "Selia", "Sowee"], index=last('fournisseur', 'selectbox', ["TotalEnergies", "Alterna", "Barry", "Bulb", "Direct Energy", "CDiscount Energy", "Butagaz", "Leclerc Energies", "Elecocité", "Energem", "EDF", "ENGIE", "ENI", "Plum", "Proxelia", "Selia", "Sowee"]))
                with col2:
                    compteur = st.selectbox("D'ailleurs, ce compteur est ", ["Monophasé", "Triphasé", "Je ne sais pas"], index=last('compteur', 'selectbox', ["Monophasé", "Triphasé", "Je ne sais pas"]))
                    abonnement = st.selectbox("Quel est votre abonnement ?", ["Base", "Heures pleines / Heures creuses", "EJP", "Tempo"], index=last('abonnement', 'selectbox', ["Base", "Heures pleines / Heures creuses", "EJP", "Tempo"]))
        
        with stylable_container(key="adresse_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Votre consommation électrique  ⚡")
                col1, col2 = st.columns(2)
                with col1:
                    montant_facture = st.number_input("Quel est le montant de votre facture d'électricité annuelle (en €)", value=last('montant_facture', 'number_input'), step=100)
                with col2:
                    connaissance_facture_elec =  st.radio("Connaissez vous votre consommation annuelle d'électricité en kWh", ["Oui",  "Non"], index=last('connaissance_facture_elec', 'radio', ["Oui",  "Non"]))
                    if connaissance_facture_elec == "Oui":
                        conso_kwh = st.number_input("Consommation annuelle en kWh", value=last('conso_kwh','number_input'), step=1000)
        
        with stylable_container(key="adresse_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Votre chauffage  🔥")
                chauffage_electrique = st.selectbox("Avez-vous un chauffage électrique ?", ["Oui", "Oui mais c'est une pompe à chaleur air-air", "Oui mais c'est une pompe à chaleur air-air", "Oui mais c'est une pompe à chaleur air-eau", "Oui mais c'est une pompe à chaleur eau-eau", "Oui mais c'est une pompe à chaleur géothermique", "Non"], index=last('chauffage_electrique', 'selectbox', ["Oui", "Oui mais c'est une pompe à chaleur air-air", "Oui mais c'est une pompe à chaleur air-air", "Oui mais c'est une pompe à chaleur air-eau", "Oui mais c'est une pompe à chaleur eau-eau", "Oui mais c'est une pompe à chaleur géothermique", "Non"]))
                gaz_fioul = st.multiselect("Avez-vous un chauffage au gaz/fioul ? (Choix multiples)", ["Gaz", "Fioul", "Non"], default=last('gaz_fioul', 'multiselect'))
                n = len(gaz_fioul)
                if "Non" not in gaz_fioul:
                    col = [1,2]
                    col[0], col[1] = st.columns(2)
                    for i in range(n):
                        x = gaz_fioul[i]
                        with col[i]:
                            if "Gaz" == x:
                                gaz_facture = st.number_input("Facture annuelle du gaz (en €)", value=last('gaz_facture', 'number_input'), step=50)
                                #fioul_facture = None
                            elif "Fioul" == x:
                                a,b = st.columns(2)
                                with a:
                                    fioul_facture = st.number_input("Facture annuelle du fioul (en €)", value=last('fioul_facture', 'number_input'), step=50)
                                    #gaz_facture = None
                                with b:
                                    fioul_litre = st.number_input("Conso annuelle de fioul (en L)", value=last('fioul_litre', 'number_input'), step=50)
                col1, col2 = st.columns(2)
                with col1:
                    type_chaudiere = st.selectbox("Quel type de chaudière", ["Ventouse", "Basse température", "Condensation", "Autre"], index=last('type_chaudiere', 'selectbox', ["Ventouse", "Basse température", "Condensation", "Autre"]))
                with col2:
                    type_materiel = st.selectbox("Quel type de matériel", ["Radiateur seul", "Chauffage au sol seul", "Radiateurs et chauffage au sol"], index=last('type_materiel', 'selectbox', ["Radiateur seul", "Chauffage au sol seul", "Radiateurs et chauffage au sol"]))
                age_chaudiere = st.number_input("Age de la chaudière", min_value=0, value=last('age_chaudiere', 'number_input'), step=1)
                chaudiere_electrique = st.radio("Avez-vous une chaudière électrique ?", ["Oui", "Non"], index=last('chaudiere_electrique', 'radio', ["Oui", "Non"]))
                autre_systeme_chauffage = st.multiselect("Avez-vous un autre système de chauffage ? (Choix multiples)", ["Poêle à granulés (pellets)", "Poêle bûches", "Cheminée","Chaudière à bois", "Insert", "Autre", "Non"], default=last('autre_systeme_chauffage', 'multiselect'))
                if autre_systeme_chauffage != [] and 'Non' not in autre_systeme_chauffage :
                    facture_autre_syst_chauffage = st.number_input("Facture annuelle pour ce système (en €)", value=last('facture_autre_syst_chauffage','number_input'), step=50)

        
        if st.button("Suivant"):

            if 'data' in st.session_state:
                dic = st.session_state.data
                
                dic['equipement_pv_passe']=equipement_pv_passe
                if equipement_pv_passe=="Oui":
                    dic['puissance_deja_installee']=puissance_deja_installee
                dic['etude_solaire_passe']=etude_solaire_passe
                dic['dpe_passe']=dpe_passe
                if dpe_passe=="Oui":
                    dic['dpe']=dpe
                dic['puissance_kva']=puissance_kva
                dic['fournisseur']=fournisseur
                dic['compteur']=compteur
                dic['abonnement']=abonnement
                dic['montant_facture']=montant_facture
                dic['connaissance_facture_elec']=connaissance_facture_elec
                if connaissance_facture_elec == "Oui":
                    dic['conso_kwh']=conso_kwh
                dic['chauffage_electrique']=chauffage_electrique
                dic['gaz_fioul']=gaz_fioul

                dic['gaz_facture']=0
                dic['fioul_facture']=0
                if "Gaz" in gaz_fioul:
                    dic['gaz_facture']=gaz_facture
                if 'Fioul' in gaz_fioul:
                    dic['fioul_facture']=fioul_facture
                    dic['fioul_litre']=fioul_litre
                dic['type_chaudiere']=type_chaudiere
                dic['type_materiel']=type_materiel
                dic['age_chaudiere']=age_chaudiere
                dic['chaudiere_electrique']=chaudiere_electrique
                dic['autre_systeme_chauffage']=autre_systeme_chauffage
                #if autre_systeme_chauffage!=[] and autre_systeme_chauffage!=['Non']:
                try:
                    dic['facture_autre_syst_chauffage']=facture_autre_syst_chauffage
                except:
                    pass
                
                
                
                st.session_state.data = dic
                update_or_insert_data(dic)



            switch_page('saisir_donnees_habitat_3')

render_page_habitat_2()