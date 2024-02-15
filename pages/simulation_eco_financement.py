import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page
from functions import *
import plotly.express as px
import matplotlib.pyplot as plt
import os
from streamlit_extras.stylable_container import stylable_container
from db_functions import *
import pandas as pd
from matplotlib.ticker import FuncFormatter
import plotly.graph_objects as go

def tarif(dic):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ressources','tarifs.xlsx')
    df = pd.read_excel(path)

    if dic['pv_unitaire']=='375W':
        if 'Micro onduleurs' in dic['materiels'] or True: #and #passerelles??:
            df_clean = df.iloc[2:, 0:5].rename(columns=df.iloc[1:, 0:5].iloc[0])
            ligne = df_clean[df_clean['QTÉ']==dic['nbr_panneaux']]
            qte, puissance, ttc, edf, tva = ligne.iloc[0,0], ligne.iloc[0,1],ligne.iloc[0,2],ligne.iloc[0,3],ligne.iloc[0,4]
            if type(tva)==str:
                tva=0
            #puissance, ttc, edf, tva
   # elif dic['pv_unitaire']=='375W' and 'FHE' in dic['materiels']:
        df_clean = df.iloc[2:,[0,5,6]].rename(columns=df.iloc[1:,[0,5,6]].iloc[0])
        ligne = df_clean[df_clean['QTÉ']==dic['nbr_panneaux']]
        qte, ttc_fhe, tva_fhe = ligne.iloc[0,0],ligne.iloc[0,1],ligne.iloc[0,2]
        if type(tva_fhe)==str:
            tva_fhe=0
        #qte_fhe, ttc_fhe, tva_fhe

    elif dic['pv_unitaire']=='500W':
        if 'Micro onduleurs' in dic['materiels'] or True:
            df_clean = df.iloc[2:,8:13].rename(columns=df.iloc[1:,8:13].iloc[0])
            ligne = df_clean[df_clean['QTÉ']==dic['nbr_panneaux']]
            qte, puissance, ttc, edf, tva = ligne.iloc[0,0], ligne.iloc[0,1],ligne.iloc[0,2],ligne.iloc[0,3],ligne.iloc[0,4]
            if type(tva)==str:
                tva=0
            #puissance, ttc, edf, tva
    #elif dic['pv_unitaire']=='500W' and 'FHE' in dic['materiels']:
        df_clean = df.iloc[2:,[8,13,14]].rename(columns=df.iloc[1:,[13,14]].iloc[0])
        ligne = df_clean[df_clean['PV 500 WATTS SEULS']==dic['nbr_panneaux']] # c'est la colonne quantité juste on la voit pas
        qte, ttc_fhe, tva_fhe = ligne.iloc[0,0],ligne.iloc[0,1],ligne.iloc[0,2]
        if type(tva_fhe)==str:
            tva_fhe=0
        #qte, tva_fhe, ttc_fhe

    return qte, puissance, ttc, edf, tva, ttc_fhe, tva_fhe # en fait on n'utilise jamais les  x_fhe parce qu'ils sont déjà compris dans les autres


def showfinance(rows):
    st.markdown("""
        <style>
            .box{
                border-color : grey;
                border-radius : 5px;
                border : solid; 
                background-color : lightgrey;
               }
    
            .label{
                margin-left : 10px;
            }

            .montant{
                margin-left : 80%;
            }
        </style>
    """, unsafe_allow_html=True)

    content = f"<div class='box'>"

    for row in rows:
        label, montant = row[0], row[1]
        content += f"<div><span class='label'>{label}</span><span class='montant'>{montant} €</span></div>"

    content += "</div>"
    st.markdown(content, unsafe_allow_html=True)

def show_eco(label, *entries):
    st.markdown("""
        <style>
            .info-box-container {
                background-color: rgba(21, 67, 96, 0.7);
                border: 1px solid rgb(0,180,0);
                padding: 5px 5%;
                margin: -10px 5px;
                border-radius: 8px;
                width : 60%;
                transform: translateY(-25px); 
            }

            .label {
                font-weight: bold;
                font-size: 110%;
                color: white;
            }

            .entry {
                display: flex;
                justify-content: space-between;
                margin-top: 5px;
            }

            .title {
                margin-left:-20px;
                color: white;
                font-size: 110%;
            }

            .value-unit {
                display: flex;
                flex-direction: row-reverse;
                font-size: 110%;
                margin-right:20px;
            }

            .value {
                color: white;
            }

            .unit {
                color: white;
                margin-left: 5px;
            }à
        </style>
        """, unsafe_allow_html=True)

    content = f'<div class="info-box-container"><span class="label">{label}</span>'

    for entry in entries:
        content += f'<div class="entry"><span class="title">{entry[0]}</span><span class="value-unit"><span class="unit">{entry[2]}</span><span class="value">{entry[1]}</span></span></div>'

    content += '</div>'
    st.markdown(content, unsafe_allow_html=True)


def render_page_ecofinancement():
    
    st.set_page_config(
    page_title="Simuler votre Projet - Eco-Financement",
    page_icon="💰", layout="wide", initial_sidebar_state="collapsed")
    no_sidebar()
    background('argent.jpg', 'center center')

    if 'data' in st.session_state:
        dic = st.session_state.data
    else : 
        dic = {'CEE':0, 'MPR':0, 'EDF':0, 'TVA':0}

    qte, puissance, ttc, edf, tva, ttc_fhe, tva_fhe = tarif(dic)
    
    styled_button()
    css()
    tab = valeur_tabulees()

    with stylable_container(
            key='adresse_container',
            css_styles = css_from_function()
            ):
        st.subheader("Economies et mensualités  ⚡")
        col1, col2, col3 = st.columns(3)
        with col1:
            eco_n_plus_1 = dic['economies_annnuelles_pv_autoconso']/tab['nbr_mois']
            economie_n_plus_un = st.number_input('Economies N+1 (€/mois)', value=int(eco_n_plus_1), step=1)
            montant_materiels_et_services = st.number_input('Montant matériel et services (€))', value=ttc, step=100)
        with col2:
            report_jours = st.number_input('Report (jours)', value=180, step=1) # ne bouge pas 
            duree_initiale = st.number_input('Durée initiale (mois)', value=170, step=1) # dépend du partenaire financier
        with col3:
            partenaire_financier = st.selectbox('Partenaire financier', ['FranFinance', 'DomoFinance', 'Sofinco', 'Projexio', 'Paiement Comptant'], index=1)
            premiere_mensualite = st.number_input('Première mensualité (€)', value=358.59, step=1.0) ### A changer
        apport = st.number_input('Apport Personnel (€)', value=0, step=100)
        st.subheader("Aides au projet  💰")
        st.markdown("<p style='font-weight:bold;font-size:110%'>Aides et économies</p>", unsafe_allow_html=True)
        
        economies_sur_6_mois = economie_n_plus_un * int(report_jours/30)

        dic['EDF'] = edf
        dic['EDF'] = tva
        total_aides = economies_sur_6_mois+dic['MPR']+dic['CEE']+dic['EDF']+apport
        reste_a_eco_financer = montant_materiels_et_services - total_aides
        mispace()
        style_table([
            [f'Economies sur {int(report_jours/30)} mois', str(economies_sur_6_mois)+'€'],
            ['MaPrimeRénov', str(dic['MPR'])+'€'],
            ['Coup de Pouce', str(dic['CEE'])+'€'],
            ['EDF', str(dic['EDF'])+'€'],
            ['Récupération de la TVA', str(dic['TVA'])+'€'],
            ["Déduction crédit d'impôts", '0€'],
            ["Apport personnel", str(apport)+'€'],
            ['Total', str(total_aides)+'€'],
            ['Reste à éco-financer après déduction des aides', str(reste_a_eco_financer)+'€'],
                    ])

        st.subheader("Eco-financement  💲")
        col1, col2, col3 = st.columns(3)
        with col1:
            amortissement_mois = st.number_input('Amortissement (mois)', value=180, step=1)
        with col2:
            n, m, t = reste_a_eco_financer, amortissement_mois, 2.0 # taux d'intérêt à 2%
            t = t/12/100
            mensualites = (n*t*(1+t)**m)/((1+t)**m-1)
            mensualites_choisies = st.number_input('Mensualités (€)', value=mensualites, step=1.0)
        with col3:
            eco_mois_moy = dic['economie_par_mois_moyen']
            economies_moy_par_mois = st.number_input('Economies Moy/mois)', value=eco_mois_moy, step=1.0)

            nbr_annee_financement = amortissement_mois//12
            #gain_eco_mensuelles_pdt_eco_financement = economies_moy_par_mois - mensualites_choisies
            #gain_eco_annuelles_pdt_eco_financement = gain_eco_mensuelles_pdt_eco_financement * tab['nbr_mois']

            # economie réalisée par mois (calculés sur selection materiel avec la prédiction du prix de l'énergie) - mensualité choisie pendant remboursement (180 mois)
            # ensuite économie on enlèv pas les mensualités si on les a payées

        st.subheader("Prévision Financière  🔭")
        col1, col2 = st.columns(2)
        with col1:

            prevision_annee_eco_financement = st.number_input('Prévisions en années :', value=30, step=1) # pas eco financement en vrai mais bon juste prévision sur 30 ans

        

            fig, ax = plt.subplots()
            wedgeprops = {'edgecolor': 'grey', 'linewidth': 2, 'antialiased': True}
            colors = ['#6eb52f', "#e0e0ef", 'lightcoral']
            #sizes = [i for i in range(prevision_annee_eco_financement)] ##changer calcul
            index = dic['indexation']
            sizes = [economies_moy_par_mois*tab['nbr_mois']*(1+i)**(index/100) for i in range(prevision_annee_eco_financement)]
            sizes = [sizes[i]-mensualites_choisies*tab['nbr_mois'] if i<=nbr_annee_financement else sizes[i] for i in range(len(sizes))]
            ax.bar(range(prevision_annee_eco_financement),sizes)
            ax.set_ylim(-10, max(sizes) * 1.2)
            formatter = FuncFormatter(lambda x, _: f'{int(x)} €')
            ax.yaxis.set_major_formatter(formatter)
            ax.axis('on')  # Equal 
            fig.set_facecolor((1,1,1,0))              
            st.pyplot(fig)
            path_fig = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generation_pdf\\bar_chart.png')
            fig.set_facecolor((1,1,1,0))  
            fig.savefig(path_fig)

            gain_eco_mensuelles_pdt_eco_financement = economies_moy_par_mois - mensualites_choisies
            gain_eco_annuelles_pdt_eco_financement = gain_eco_mensuelles_pdt_eco_financement * tab['nbr_mois']

        with col2:
            space(3)
            with stylable_container(key='gains', css_styles = """
            .info-box-container{
                width:110%;
                padding: 30px 5px 30px 50px;
                margin-top : 60px;
                background-color: rgba(21, 67, 96, 0.9);
            }
            """):
                show_eco('',
                ('Gains et économies mensuelles pendant éco-financement', str(int(gain_eco_mensuelles_pdt_eco_financement)), '€'), 
                ('Gains et économies annuelles pendant éco-financement', str(int(gain_eco_annuelles_pdt_eco_financement)),'€'))
                gain_total = gain_eco_annuelles_pdt_eco_financement * nbr_annee_financement + (prevision_annee_eco_financement-nbr_annee_financement)*economies_moy_par_mois*tab['nbr_mois']
                show_eco('',
                ("Total des gains et économies sur "+ str(prevision_annee_eco_financement)+" ans", str(int(gain_total)), '€'), 
                )

                gain_et_eco_prevision_eco_financement = gain_eco_mensuelles_pdt_eco_financement
        
        

        


        


        
        
        if st.button("Suivant"):
            if 'data' in st.session_state:
                dic = st.session_state.data

                dic['economie_n_plus_un'] = economie_n_plus_un
                dic['montant_materiels_et_services'] = montant_materiels_et_services
                dic['report_jours'] = report_jours
                dic['duree_initiale'] = duree_initiale
                dic['partenaire_financier'] = partenaire_financier
                dic['premiere_mensualite'] = premiere_mensualite
                dic['economies_sur_6_mois'] = economies_sur_6_mois

                dic['amortissement_mois'] = amortissement_mois
                dic['mensualites_choisies'] = int(mensualites_choisies)
                dic['economies_moy_par_mois'] = int(economies_moy_par_mois)     

                dic['gain_eco_mensuelles_pdt_eco_financement'] = int(gain_eco_mensuelles_pdt_eco_financement)
                dic['gain_eco_annuelles_pdt_eco_financement'] = int(gain_eco_annuelles_pdt_eco_financement)

                dic['prevision_annee_eco_financement'] = prevision_annee_eco_financement
                dic['gain_et_eco_prevision_eco_financement'] = int(gain_et_eco_prevision_eco_financement)   
                
                st.session_state.data = dic
                update_or_insert_data(dic)         


            switch_page('simulation_generer_documents')

render_page_ecofinancement()