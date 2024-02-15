import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from pv_gis_function import *
import os 
from api_functions import *
from streamlit_extras.stylable_container import stylable_container
from db_functions import *

def render_page_selection_materiels():
    
    st.set_page_config(
    page_title="Simuler votre Projet - Sélection Matériels et Services",
    page_icon="🛠", layout="wide", initial_sidebar_state="collapsed"
    )
    no_sidebar()
    background('maison_panneaux.jpg', 'top center')
    st.markdown("""
    <style>
        div.stButton > button:first-child {
            margin-top : 30px;
            margin-right : 30px;
            width : 195px;
            height:55px;
            display : inline;
            float: right;
        }
        div.stButton > button:hover {
            background-color : #f2f2f2;
            border : solid gray 1px;
            float: right;
        }
    </style>
    """, unsafe_allow_html=True)
    css()

    global dic, tab
        
    if 'data' in st.session_state:
        dic = st.session_state.data
    else:
        st.write('Valeurs fictives')
        dic = {'adresse_postale': [["425 Route de Soucieu 69440 Saint Laurent d'Agny"]], 'departement': [['01 - Ain']], 'parcelles': [['342']], 'pente_toit': [[None]], 'altitude': [[None]], 'masque_solaire': [['Oui']], 'orientation_toit': [[None]], 'type_personne': [['Particulier']], 'nom': [['']], 'email': [['']], 'prenom': [['']], 'type_projet': [['Résidence Secondaire']], 'nbr_niveaux': [[None]], 'vitrage': [[None]], 'combles': [[None]], 'etat_charpente': [[None]], 'annee_construction': [[1960]], 'type_charpente': [[None]], 'isolation_comble': [['Non']], 'isolation_mur': [['Non']], 'nbr_personne': [[1]], 'temperature': [[18]], 'hauteur_ss_plafond': [[2.0]], 'surface': [[50]], 'surface_chauffer': [[50]], 'equipement_pv_passe': [['Oui']], 'puissance_deja_installee': [[0.0]], 'etude_solaire_passe': [['Oui']], 'dpe_passe': 
        [['Oui']], 'dpe': [[None]], 'puissance_kva': [[None]], 'fournisseur': [[None]], 'compteur': [['Monophasé']], 'abonnement': [[None]], 'montant_facture': [[2000]], 'connaissance_facture_elec': [['Non']], 'chauffage_electrique': [[None]], 'gaz_fioul': [[['Gaz', 'Fioul']]], 'gaz_facture':[[1300]], 'fioul_facture':[[300]], 'fioul_litre':[[2000]],'type_chaudiere': [[None]], 'type_materiel': [[None]], 'age_chaudiere': [[5]], 'chaudiere_electrique': [['Non']], 'autre_systeme_chauffage': [[[]]], 'hauteur_ecs': [[None]], 'ballon_eau_chaude_electrique': [[None]], 'climatisation': [[None]], 'plaque_cuisson': [[None]], 'lave_vaisselle': [[None]], 'seche_linge': [[None]], 'systeme_vmc': [[None]], 'type_four': [[None]], 'lave_linge': [[None]], 'voiture_electrique': [[None]], 'piscine_chauffee': [[None]], 'frigidaire': [[[]]], 'congelateur': [[[]]], 'habitude_conso': [[None]], 'ressources_annuelles': [[20000]], 'interesse': [[[]]], 'id': [0]}


    
    def val(label):
        if len(dic['adresse_postale'][0])>2: # pour vérifier si c'est une liste ou si ça renvoie juste la premiere lettre (ça bug le type == list)
            return dic[label][0]
        else:
            return dic[label]
        
    
    tab = valeur_tabulees()
    
    def amelioration(label, materiels):
        dic_amelioration_percent = {
        "FHE": 0,    
        "Micro onduleurs": tab['tx_micro_onduleur'],
        "Domotique": tab['tx_domotique'],
        "Passage en triphasé": 0,
        "Nettoyage et traitement": 0,
        "Batterie de stockage": tab['tx_batterie_stockage'],
        "Pergola solaire": tab['tx_masque_solaire'],
        "Borne de recharge véhicule électrique": tab['tx_vehicule_elec'],
        }
        if 'Ballon thermodynamique' in materiels :
            dic_amelioration_percent["Ballon thermodynamique"] = tab["tx_ballon_thermo_qd_gaz_fioul_elec_ballon_sur_gaz"]
            dic_amelioration_percent["PAC air-air Quadri"] = tab["tx_pac_air_air_qd_gaz_fioul_elec_ballon_sur_gaz"]
            dic_amelioration_percent["PAC air-eau"] = tab["tx_pac_air_eau_qd_gaz_fioul_elec_ballon_sur_gaz"]
            dic_amelioration_percent["Ballon électrique"] = tab["tx_ballon_thermo_qd_gaz_fioul_elec_ballon_sur_elec"]
        elif 'Ballon électrique' in materiels :
            dic_amelioration_percent["Ballon électrique"] = tab["tx_ballon_thermo_qd_gaz_fioul_elec_ballon_sur_elec"]
            dic_amelioration_percent["PAC air-air Quadri"] = tab["tx_pac_air_air_qd_gaz_fioul_ballon_sur_elec"]
            dic_amelioration_percent["PAC air-eau"] = tab["tx_pac_air_eau_qd_gaz_fioul_elec_ballon_sur_elec"]
            dic_amelioration_percent["Ballon thermodynamique"] = tab["tx_ballon_thermo_qd_gaz_fioul_elec_ballon_sur_gaz"]
        else:
            if 'Gaz' in val('gaz_fioul') or 'Fioul' in val('gaz_fioul'):
                # Cas Gaz/Fioul
                dic_amelioration_percent["PAC air-air Quadri"] = tab["tx_pac_air_air_qd_gaz_fioul"]
                dic_amelioration_percent["PAC air-eau"] = tab["tx_pac_air_eau_qd_gaz_fioul"]
                dic_amelioration_percent["Pack LED"] = tab["tx_pack_led_qd_tt_nn_elec"]
                #dic_amelioration_percent["Ballon(s)"] = tab["tx_ballon_thermo_qd_gaz_fioul"] 
                
                dic_amelioration_percent["Ballon électrique"] = tab["tx_ballon_thermo_qd_gaz_fioul_elec_ballon_sur_elec"]
                
            else:
                # Cas tout élec
                dic_amelioration_percent["PAC air-air Quadri"] = tab["tx_pac_air_air_qd_tt_elec"]
                dic_amelioration_percent["PAC air-eau"] = tab["tx_pac_air_eau_qd_tt_elec"]
                dic_amelioration_percent["Pack LED"] = tab["tx_pack_led_qd_tt_elec"]
                #dic_amelioration_percent["Ballon(s)"] = tab["tx_ballon_thermo_qd_tt_elec"]
            
            
        return 1-dic_amelioration_percent[label]

    #st.write(val('adresse_postale'), val('montant_facture'),tab['prix_kwh'])
    if test_connexion_internet():
        puissance_conseillee, independance, surplus, prod_pv_annnee_unit, l_prod_pv_mois_unit = calcul_pvgis(val('adresse_postale'), val('montant_facture')/tab['prix_kwh'])
    else:
        st.error("⛔ Pas de connexion internet, impossible de récupérer les données PVGIS 🌞")
        puissance_conseillee, independance, surplus, prod_pv_annnee_unit, l_prod_pv_mois_unit = 1,1,1,1,[1,1,1,1,1,1,1,1,1,1,1,1]
    cola, colb = st.columns(2)

    with stylable_container(
            key='adresse_container',
            css_styles = css_from_function()
            ):
        with colb:
            st.header("Matériels et Services 🔩")
            option_materiel = ['Micro onduleurs', 'FHE', 'Domotique', 'Ballon thermodynamique', 'Ballon électrique', 'PAC air-air Quadri', 'PAC air-eau', 'Pack LED', 'Passage en triphasé', 'Nettoyage et traitement', 'Pergola solaire', 'Batterie de stockage', 'Borne de recharge véhicule électrique']
            materiels = st.multiselect('',option_materiel)

            elec, gaz, fioul, autre = val('montant_facture'), 0, 0, 0
            
            if 'Fioul' in val('gaz_fioul'):
                fioul = val('fioul_facture')
            if 'Gaz' in val('gaz_fioul'):
                gaz = val('gaz_facture')
            if val('autre_systeme_chauffage') != []:
                autre = val('facture_autre_syst_chauffage')
            
            ############### Attention check les calculs pour les (1-Ri)^n ou Ri^n
            #st.write(elec, gaz, fioul, autre)
            total = elec+gaz+fioul+autre
            conso_init = round(total/tab['prix_kwh'], 1)
            r = 1
            for mat in materiels:
                r*=amelioration(mat, materiels)

            eco_an_elec = round(elec*(1-r))
            eco_an_gaz = round(gaz*(1-r))
            eco_an_autre = round((fioul+autre)*(1-r))
            eco_total_an = eco_an_elec + eco_an_gaz + eco_an_autre

            ################################## Revoir ça
            st.subheader('Les chiffres')
            show("Gains et économies", 
                    ('Electricité', eco_an_elec, "€"),
                    ("E.C.S", eco_an_gaz, "€"),
                    ("Chauffage", eco_an_autre, "€"),
                    ("Total Minimum N+1", eco_total_an, "€"),
                    ('Total Minimum/Mois', round(eco_total_an/tab['nbr_mois']), "€"))

        with cola:
            st.header("Votre Foyer  🏡")
            space(1)
            col1,col2 = st.columns(2)
            with col1:
                show("Département", ("", val('departement'), ""))
                show("Compteur / Puissance", ("", str(val('compteur'))+" / "+str(val('puissance_kva')), "kVA"))
                if val('equipement_pv_passe') == 'Oui':
                    show("Panneaux solaires installés", ("", val('puissance_deja_installee'), "Wc"))
                
            with col2:
        
                show("Total des dépenses", 
                    ('Electricité', elec, "€"),
                    ("Gaz", gaz, "€"),
                    ("Fioul", fioul, "€"),
                    ("Autre", autre, "€"),
                    ('Total', total, "€"))

                conso_elec = elec/tab['prix_kwh']
                ameliore = conso_elec #conso_init
                ameliore*=r ######################################################### NE FONCTIONNE PAS BIEN
                conso_additionnel = {
                    "PAC air-air Quadri":tab['conso_pac_air_air'],
                    "PAC air-eau":tab['conso_pac_air_eau'], 
                    "Ballon(s)":tab['conso_ballon_thermo']
                    }  
                for key in conso_additionnel.keys():
                    if key in materiels:
                        ameliore+=conso_additionnel[key]
                
                show("Consommation kWh",
                    ("Initial", "{:,}".format(int(conso_elec)).replace(",", " "), "kWh"),
                    ("Amélioré", "{:,}".format(int(ameliore)).replace(",", " "), "kWh"))
                    
        
        colx, coly = st.columns(2)

        with coly:
            space(3)
            st.subheader("Panneaux et revente  🌞")

            col1,col2 = st.columns(2)
            with col1:
                puissance_panneaux = st.number_input("Puissance des panneaux (kWc)", step=1, value=puissance_conseillee)
                st.markdown("<sub>Puissance conseillée "+str(puissance_conseillee)+" kWc hors pose sol</sub>", unsafe_allow_html=True)
                pv_unitaire = st.radio('Puissance unitaire du panneau', ['500W', '375W'])
                panneaux_sol = st.radio('Pose des panneaux au sol', ['Oui', 'Non'], index=1)
                nbr_panneaux = int(puissance_panneaux*1000/int(pv_unitaire.split('W')[0]))
                surface_panneaux = nbr_panneaux*tab["surface_panneau"]
            st.markdown("<sub>Quantité panneau et superficie : "+str(nbr_panneaux)+" panneaux ("+str(round(surface_panneaux,1))+"m²)</sub>", unsafe_allow_html=True)
            if val('compteur')=='Monophasé':
                st.markdown("<div style=color:red;font-size:12px><bold>Compteur en monophasé : Raccordement réseau plafonné à 6.0 kWc</bold></div>", unsafe_allow_html=True)
                if puissance_panneaux>=6:    
                    revente = 6 
                    injection_dir = puissance_panneaux-6
                else:
                    revente = puissance_panneaux
                    injection_dir = puissance_panneaux
            else:
                revente = puissance_panneaux
                injection_dir = puissance_panneaux

            st.markdown("<div><sub>* Votre installation : "+str(revente)+" kWc en revente partielle et "+str(injection_dir)+" kWc en injection directe.</sub></div>", unsafe_allow_html=True)

            coef_mult_choisi = puissance_panneaux
            #################################### A REFAIRE BIEEEN
            h_soleil = tab['heures_ensoleillement']
            p_restit = coef_mult_choisi*prod_pv_annnee_unit
            coef_meteo = tab['coef_meteorologique']
            coef_perf = tab['coef_performance']
            perte = tab['perte_systeme']
            rdt_panneaux = tab['rendement_paneaux']

            #energie_an_panneaux = puissance_panneaux*rdt_panneaux*h_soleil ## Outdated
            #surplus = (energie_an_panneaux-ameliore)/energie_an_panneaux ##Outdated
            conso_mois = (val('montant_facture')/tab['prix_kwh'])/12
            delta_conso = [(coef_mult_choisi*val) - conso_mois for val in l_prod_pv_mois_unit]
            pos = [val if val>=0 else 0 for val in delta_conso ]
            neg = [val if val<0 else 0 for val in delta_conso ]
            surplus = sum(pos) #en kwh attention
            surplus_prct = surplus/(coef_mult_choisi*prod_pv_annnee_unit)
            autoconso_prct = 1-surplus_prct
            surplus = surplus_prct*prod_pv_annnee_unit
            autoconso = autoconso_prct*prod_pv_annnee_unit
        
            with col2:    
                st.button("Favoriser revente")
                st.button("Modifier puissance")
            
            space(5)
            mispace()
            st.subheader('Données Techniques  📰')
            with st.container():
                show2(("Heures d'ensoleillement", "{:,}".format(int(h_soleil)).replace(",", " ")+' h'))
                show2(('Puissance restituée', "{:,}".format(int(p_restit)).replace(",", " ")+' kWh'))
                show2(('Coefficient Météorologique', str(coef_meteo)+'%'))
                show2(("Coefficient de performance", str(coef_perf)))
                show2(("Perte du système", str(perte)+'%'))
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div><br><div>', unsafe_allow_html=True)
                    mispace()
                    with stylable_container(
                    key='authenthif',
                    css_styles = """
                    div.stButton > button:first-child {
                        height:70px;
                        }
                    """
                    ):
                        st.button("Actualiser le coût du kwH")
                    
                with col2:
                    mispace()

                    prix_achete = st.number_input('Consommé (€/kWh)', value=tab['prix_kwh'], step=0.01)

                    prix_revendu = tab['prix_kwh_revendu_part']
                    if val('type_personne')=='Professionnel':
                        if puissance_panneaux <=3:
                            prix_revendu = tab['prix_kwh_revendu_pro_0_3']
                        elif puissance_panneaux <=9:
                            prix_revendu = tab['prix_kwh_revendu_pro_3_9']
                        elif puissance_panneaux <=36:
                            prix_revendu = tab['prix_kwh_revendu_pro_9_36']
                        else :
                            prix_revendu = tab['prix_kwh_revendu_pro_36_100']

                    prix_vendu = st.number_input('Revendu (€/kWh)', value=prix_revendu, step=0.01)
            
            space(3)
            mispace()
            with st.container():
                st.subheader('Vos aides  💰')
                st.markdown('<sub>Les aides auxquelles vous avez droit :</sub>', unsafe_allow_html=True)
                cola,colb = st.columns(2)
                
                avis_imposition = val('ressources_annuelles')
                nbr_personnes = val('nbr_personne')
                depart = val('departement')
                
                type_menage = type_menage_fct(avis_imposition, nbr_personnes, depart)
                MPR = aidesMPR(type_menage, materiels)
                CEE, EDF, TVA, credit = 0, 0, 0, 0
                if panneaux_sol == 'Non':
                    CEE = aidesCEE(type_menage, materiels)
                    EDF = aidesEDF(puissance_panneaux)
                    dic['pv_unitaire'] = pv_unitaire
                    dic['nbr_panneaux'] = nbr_panneaux
                    dic['materiels'] = materiels
                    qte, puissance, ttc, edf, tva, ttc_fhe, tva_fhe = tarif(dic)
                    TVA = tva
                    credit = 0
                
                if val('type_projet')=='Résidence Secondaire':
                    MPR = 0
                
                total_aides = MPR + CEE + EDF + TVA + credit
                ## Finiiiir aides !!

                style_table([
                    ['MaPrimeRénov',str(MPR)+'€'],
                    ['CEE',str(CEE)+'€'],
                    ['EDF', str(EDF)+'€'],
                    ['Récupération de la TVA',str(TVA)+'€'],
                    ["Déduction crédit d'impôts", str(credit)+'€'],
                    ['Total',str(total_aides)+'€']
                    ])


                st.markdown("<sub>Les aides CEE et MaPrimeRénov sont exclusivement disponible dans le cadre de l'installation d'un ballon thermodynamique et/ou d'une pompe à chaleur</sub>", unsafe_allow_html=True)
                st.markdown("<a href='wwww.example.com'>Consultez le document explicatif</a>", unsafe_allow_html=True)


                

        with colx:
            space(3)

            st.subheader("Transition Energétique  🌱")
            
            labels = ['Surplus', 'Indépendance']
            sizes = [round(surplus_prct*100,1), round(autoconso_prct*100,1)]
            
            fig, ax = plt.subplots()
            wedgeprops = {'edgecolor': 'white', 'linewidth': 1, 'antialiased': True}
            colors = ['#6eb52f', "#e0e0ef", 'lightcoral']
            pie = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops=wedgeprops, colors=colors)
            for label in pie[1]:
                label.set_color('darkblue')
            ax.axis('equal')  # Equal 
            fig.set_facecolor((1,1,1,0))  
            st.pyplot(fig)

            path_fig = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generation_pdf\\pie_chart.png')
            fig.set_facecolor("white")  
            fig.savefig(path_fig)
            
            facture_surplus = surplus*prix_vendu
            facture_autoconso = autoconso*prix_achete

            st.write('Indépendance mensuelle: '+str(round(facture_autoconso)) + ' €')
            st.write('Surplus mensuelle : '+str(round(facture_surplus))+' €')

            space(2)
            st.subheader('Prévisions  🔭')
            col1, col2 = st.columns(2)
            with col1:
                indexation = st.number_input('Indexation (en %/an)', value=4.0, step=0.2)
            with col2:
                annnees_prevision = st.number_input('Prévisions (en annéees)', value=15, step=1)

            #facture €/an = total
            
            fig, ax = plt.subplots()
            wedgeprops = {'edgecolor': 'grey', 'linewidth': 2, 'antialiased': True}
            colors = ['#6eb52f', "#e0e0ef", 'lightcoral']
            sizes = [elec*(1+i)**(indexation/100) for i in range(annnees_prevision)]
            ax.bar(range(annnees_prevision),sizes)
            ax.set_ylim(0, max(sizes) * 1.3)
            ax.axis('on')  # Equal 
            fig.set_facecolor((1,1,1,0))  
            st.pyplot(fig)

            st.markdown("<sub>Evolution de la facture énergétique mensuelle</sub>", unsafe_allow_html=True)
            
            st.subheader("Economies  🤑")
            economie_par_an = elec #*r  #Pas sur que ce soit la bonne chose
            economie_total = sum([economie_par_an*(1+i)**(indexation/100) for i in range(annnees_prevision)])
            economie_par_an_moyen = economie_total/annnees_prevision
            economie_par_mois_moyen = economie_par_an_moyen/tab['nbr_mois']

            show2(('Total/an', str(round(economie_par_an_moyen))+' €'))
            show2(('Total/mois', str(round(economie_par_mois_moyen))+' €'))
            show2(('Total des gains et économies sur '+ str(annnees_prevision) +' ans', str(round(economie_total))+' €'))
            space(3)
            mispace()
            st.info("""
            #### Avant de continuer n'oubliez pas 
            ###### Un projet bien défini c'est des économies garanties ⚡
            """)
            

        nvl_conso_elec_kwh_ameliore_materiels_sans_pv = ameliore            #La consommation d'élec en kwh après avoir ajouté le matos, pac, ballon, domotique
        nvl_facture_elec_ameliore_materiels_sans_pv = ameliore*prix_achete  #La facture de cette conso acheté à EDF
        nvl_facture_gaz = gaz - eco_an_gaz                                  # Nouvelle facture de gaz
        nvl_facture_fioul_autre = (autre + fioul) - eco_an_autre            # Nouvelle facture de fioul et autre
        prod_total_annee = prod_pv_annnee_unit*puissance_panneaux           #La production en kwh de l'installation PV choisie
        economies_annnuelles_pv_autoconso = facture_autoconso*12            # Les économies estimées grâce à ce qui est autoconsomé en PV (l'élec qu'on génère au lieu de l'acheter)
        gains_annnuelles_pv_surplus = facture_surplus*12                    # Les gains réalisés en vendant le surplus
        


        
        if st.button("Suivant"):
            if 'data' in st.session_state:
                dic = st.session_state.data
                
                dic['nvl_conso_elec_kwh_ameliore_materiels_sans_pv'] = nvl_conso_elec_kwh_ameliore_materiels_sans_pv
                dic['nvl_facture_elec_ameliore_materiels_sans_pv'] = nvl_facture_elec_ameliore_materiels_sans_pv
                dic['nvl_facture_gaz'] = nvl_facture_gaz
                dic['nvl_facture_fioul_autre'] = nvl_facture_fioul_autre
                dic['prod_total_annee'] = prod_total_annee

                dic['economies_annnuelles_pv_autoconso'] = economies_annnuelles_pv_autoconso
                dic['gains_annnuelles_pv_surplus'] = gains_annnuelles_pv_surplus

                dic['materiels'] = materiels
                dic['puissance_panneaux'] = puissance_panneaux
                dic['pv_unitaire'] = pv_unitaire
                dic['nbr_panneaux'] = nbr_panneaux
                dic['surface_panneaux'] = surface_panneaux

                dic['h_soleil'] = h_soleil
                dic['p_restit'] = p_restit
                dic['coef_meteo'] = coef_meteo
                dic['coef_perf'] = coef_perf
                dic['perte'] = perte
                dic['rdt_panneaux'] = rdt_panneaux
                dic['prix_achete'] = prix_achete
                dic['prix_revendu'] = prix_revendu

                ancienne_facture_elec = val('montant_facture')
                
                eco_elec_par_an = (ancienne_facture_elec - nvl_facture_elec_ameliore_materiels_sans_pv)
                gain_elec_par_an_pv = economies_annnuelles_pv_autoconso + gains_annnuelles_pv_surplus
                gain_et_eco_elec_par_an = eco_elec_par_an + gain_elec_par_an_pv
                dic['gain_et_eco_elec_par_an'] = gain_et_eco_elec_par_an

                eco_gaz_fioul_autres = (gaz+fioul+autre) - (nvl_facture_gaz + nvl_facture_fioul_autre)
                dic['eco_gaz_fioul_autres'] = eco_gaz_fioul_autres

                dic['indexation'] = indexation
                dic['annnees_prevision'] = annnees_prevision
                dic['economie_total'] = economie_total
                dic['economie_par_an_moyen'] = economie_par_an_moyen
                dic['economie_par_mois_moyen'] = economie_par_mois_moyen

                dic['MPR'] = MPR
                dic['CEE'] = CEE
                dic['EDF'] = EDF
                dic['TVA'] = TVA
                dic['credit'] = credit
                dic['total_aides'] = total_aides

                dic['ancienne_conso_elec'] = conso_elec
                dic['ancienne_facture_elec'] = ancienne_facture_elec

                st.session_state.data = dic
                update_or_insert_data(dic)

            switch_page('simulation_comparaison')

render_page_selection_materiels()