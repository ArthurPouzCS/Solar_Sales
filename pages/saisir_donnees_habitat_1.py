import streamlit as st
import time
import re
import base64
from geo_test3 import map_api
from streamlit_extras.switch_page_button import switch_page
from functions import *
from streamlit_extras.stylable_container import stylable_container
from db_functions import *

def render_page_habitat_1():
    
    st.set_page_config(
    page_title="Saisir vos Données - Habitat 1",
    page_icon="🏡", layout="wide", initial_sidebar_state="collapsed"
)

    past_audit, last = dont_forget_past_audit()
    no_sidebar()
    styled_button()
    css()
    background('mur.jpg', 'top right')
    afficher_frise_chronologique(2)

    if 'data' in st.session_state:
        dic = st.session_state.data
    else:
        dic = {}
        dic['departement']: [['01 - Ain']]

    try:
        num_departement = int(dic['departement'].split(' - ')[0])
    except:
        num_departement = 1

    
    with stylable_container(
            key='adresse_container',
            css_styles = css_from_function()
            ):
        with stylable_container(key="adresse_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Pour vous contacter  👨")
                col1, col2 = st.columns(2)
                with col1:
                    nom = st.text_input("Nom", value=last('nom', 'text_input'))
                    email = st.text_input("Email", value=last('email', 'text_input'))
                    if email:
                        if is_valid_email(email):
                            custom_success("Adresse e-mail valide : " + email)
                        else:
                            custom_warning("Adresse e-mail invalide")
                    else:
                        custom_warning("Veuillez saisir une adresse e-mail")
        
                with col2:
                    prenom = st.text_input("Prénom", value=last('prenom', 'text_input'))
                    options_type_projet = ["Résidence Principale", "Résidence Secondaire", "Votre Local d'Activité", "Autre"]
                    type_projet = st.selectbox("Votre projet concerne", options_type_projet, index=last('type_projet', 'selectbox', options_type_projet))
        
        with stylable_container(key="adresse_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Les caractéristiques de votre logement  📋")
                col1, col2 = st.columns(2)
                with col1:
                    nbr_niveaux = st.selectbox("Nombre de niveaux de votre maison (sol compris)", ["De plein-pied", "1 niveau", "2 niveaux", "3 niveaux ou +"], index=last('nbr_niveaux', 'selectbox', ["De plein-pied", "1 niveau", "2 niveaux", "3 niveaux ou +"]))
                    vitrage = st.selectbox("Vos fenêtres sont en", ["Simple Vitrage", "Double Vitrage", "Triple Vitrage"], index=last('vitrage', 'selectbox', ["Simple Vitrage", "Double Vitrage", "Triple Vitrage"]))
                    combles = st.selectbox("Vos combles sont", ["Aménagés", "Aménageables", "Perdus", "Sans Combles"], index=last('combles', 'selectbox', ["Aménagés", "Aménageables", "Perdus", "Sans Combles"]))
                    etat_charpente = st.selectbox("Etat de la charpente", ["Bon Etat", "Mauvais Etat"], index=last('etat_charpente', 'selectbox', ["Bon Etat", "Mauvais Etat"]))

                with col2:
                    annee_construction = st.number_input("Année de construction", min_value=1560, max_value=2030, value=last('annee_construction', 'number_input'), step=1)
                    couverture = st.selectbox("Votre couverture est en", ["Tuile plate", "Tuile canal","Tuile à emboîtement", "Tuile romane", "Tuile béton", "Zinc", "Pierre", "Ardoise", "Shingle", "Tôle ondulée"], index=last('couverture', 'selectbox', ["Tuile plate", "Tuile canal","Tuile à emboîtement", "Tuile romane", "Tuile béton", "Zinc", "Pierre", "Ardoise", "Shingle", "Tôle ondulée"]))
                    type_charpente = st.selectbox("Type de charpente", ["Bois", "Métallique", "Autres"], index=last('type_charpente', 'selectbox', ["Bois", "Métallique", "Autres"]))
                
                #Intervalles d'années pour le dimensionnement    
                # Les coefficients d’isolation (G): 
                # 0,4 : excellente isolation sans ponts thermique. RT2012/BBC 
                # 0.75 : pour les logements "RT2005" et réalisées entre 2007 et 2012 
                # 0.8 : pour les habitations "RT2000" et réalisées entre 2001 et 2006 
                # 0.95 : pour les maisons construites entre 1990 et 2000 
                # 1.15 : pour les maisons construites entre 1983 et 1989 
                # 1.4 : pour les maisons construites entre 1974 et 1982 
                # 1.8 : maison non isolée (murs, combles) et à menuiseries simples vitrage 
                coef_isolation_en_fct_annee = {1974:1.8, 1982:1.4, 1989:1.15, 2000:0.95, 2006:0.8, 2012:0.75, 3000:0.4}
                intervalle_annees_en_fct_annee = {1974:'Avant 1974', 1982:'1974 - 1982', 1989:'1983 - 1989', 2000:'1990 - 2000', 2006:'2001 - 2006', 2012:'2007 - 2012', 3000:'Après 2012'}
                coef_isolation = 1.15
                for annee in reversed(coef_isolation_en_fct_annee.keys()):
                    if annee_construction<=annee:
                        coef_isolation = coef_isolation_en_fct_annee[annee]
                        intervalle_annees = intervalle_annees_en_fct_annee[annee]

                temp_liste = [-10, -7, -8, -8, -10, -6, -6, -10, -5, -10, -5, -8, -5, -7, -8, -5, -5, -7, -8, -2, -10, -4, -8, -5, -12, -6, -7, -7, -4, -5, -5, -5, -5, -5, -4, -7, -7, -10, -10, -5, -7, -10, -8, -5, -7, -6, -5, -8, -7, -4, -10, -12, -7, -15, -12, -4, -15, -10, -9, -7, -7, -9, -8, -5, -5, -5, -15, -15, -10, -10, -10, -7, -10, -10, -5, -7, -7, -7, -7, -9, -5, -5, -5, -6, -5, -7, -8, -15, -10, -15, -7, -7, -7, -7, -7]
                num_depart_liste = list(range(1,96))
                dic_temp_min_en_fct_du_depart = {}
                for i in range(len(num_depart_liste)):
                    dic_temp_min_en_fct_du_depart[num_depart_liste[i]]=temp_liste[i]
                
                temperature_min_ext = dic_temp_min_en_fct_du_depart[num_departement]

        with stylable_container(key="adresse_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("L'entretien du bien  🔨")
                col1, col2 = st.columns(2)
                with col1:
                    isolation_comble = st.radio("Isolation des combles déjà effectuée ?", ["Oui", "Non"], index=1)
                    st.markdown("<sub>Intervalles d'années pour le dimensionnement PAC : "+intervalle_annees+"</sub>", unsafe_allow_html=True)
                    if isolation_comble=="Oui":
                        annee_isolation_comble = st.number_input("Année d'isolation des combles", min_value=2000, max_value=2030, step=1)
                with col2:
                    isolation_mur = st.radio("Isolation des murs déjà effectuée ?", ["Oui", "Non"], index=1)
                    st.markdown("<sub>Facteur d'isolation : "+ str(coef_isolation) +" \n Température de base extérieur:"+str(temperature_min_ext)+"</sub>", unsafe_allow_html=True) ################ aller chercher les informations depuis la loc
                    if isolation_mur=="Oui":
                        annee_isolation_mur = st.number_input("Année d'isolation des murs", min_value=2000, max_value=2030, step=1)
                
        with stylable_container(key="adresse_style", css_styles=my_style_container()):
            with st.container():
                st.subheader("Composition et surface de chauffe  🧱")
                col1, col2, col3 = st.columns(3)
                with col1:
                    nbr_personne = st.number_input("Nombre de personnes", min_value=1, max_value=20, step=1, value=int(last('nbr_personne', 'number_input')))
                with col2:
                    temperature = st.number_input("Température idéale", min_value=5, max_value=20, step=1, value=int(last('temperature', 'number_input'))) #, format="C") ### voir comment changer le format
                with col3:
                    hauteur_ss_plafond = st.number_input("Hauteur sous plafond", min_value=1.0, max_value=5.0,value=float(last('hauteur_ss_plafond',  'number_input')), step=0.1)
                
                col1, col2 = st.columns(2)
                with col1:
                    surface = st.number_input("Votre surface en m²", min_value=0, max_value=10000,value=int(last('surface', 'number_input')), step=10)
                with col2:
                    surface_chauffer = st.number_input("Votre surface à chauffer en m²", min_value=0, max_value=10000,value=int(last('surface_chauffer', 'number_input')), step=10)

                volume = surface_chauffer * hauteur_ss_plafond 
                delta_t = temperature - temperature_min_ext
                
                p = coef_isolation * volume * delta_t / 1000
                
                st.info("🔥 Dimensionnement de la Pompe à Chaleur potentielle : "+str(round(p,2))+"kwh")
                space(1)
                #"{:,}".format(int(kwh_elec)).replace(",", " ")
                
        
        if st.button('Suivant'):    
            if 'data' in st.session_state:
                dic = st.session_state.data
                
                dic['nom']=nom
                dic['email']=email
                dic['prenom']=prenom
                dic['type_projet']=type_projet
                dic['nbr_niveaux']=nbr_niveaux
                dic['vitrage']=vitrage
                dic['combles']=combles
                dic['etat_charpente']=etat_charpente
                dic['annee_construction']=annee_construction
                dic['couverture']=couverture ##### Attention anciennement comble égalament : doublon !!
                dic['type_charpente']=type_charpente
                dic['isolation_comble']=isolation_comble
                if isolation_comble=='Oui':
                    dic['annee_isolation_comble'] = annee_isolation_comble
                dic['isolation_mur']=isolation_mur
                if isolation_mur=='Oui':
                    dic['annee_isolation_mur']=annee_isolation_mur
                dic['nbr_personne']=nbr_personne
                dic['temperature']=temperature
                dic['hauteur_ss_plafond']=hauteur_ss_plafond
                dic['surface']=surface
                dic['surface_chauffer']=surface_chauffer

                dic['volume']=volume
                dic['temperature_min_ext']=temperature_min_ext
                dic['coef_isolation']=coef_isolation
                dic['delta_t']=delta_t
                dic['puissance_pac'] = p
                
                mail_sales = st.session_state.mail
                dic['mail_sales'] = mail_sales

                st.session_state.data = dic
                update_or_insert_data(dic)

            switch_page("saisir_donnees_habitat_2")
    
render_page_habitat_1()