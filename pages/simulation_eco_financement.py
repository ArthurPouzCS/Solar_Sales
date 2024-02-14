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

def tarif(dic):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ressources','tarifs.xlsx')
    df = pd.read_excel(path)
    #dic['materiels'].append('FHE') #Par défaut askip

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
            economie_n_plus_un = st.number_input('Economies N+1 (€/mois)', value=int(dic['economie_par_mois_moyen']), step=1)
            montant_materiels_et_services = st.number_input('Montant matériel et services (€))', value=ttc, step=100)
        with col2:
            report_jours = st.number_input('Report (jours)', value=180, step=1)
            duree_initiale = st.number_input('Durée initiale (mois)', value=170, step=1)
        with col3:
            partenaire_financier = st.selectbox('Partenaire financier', ['FranFinance', 'Finance2', 'Finance3'], index=1)
            premiere_mensualite = st.number_input('Première mensualité (€)', value=358.59, step=1.0)
        
        st.subheader("Aides au projet  💰")
        st.markdown("<p style='font-weight:bold;font-size:110%'>Aides et économies</p>", unsafe_allow_html=True)
        
        economies_sur_6_mois = economie_n_plus_un * int(report_jours/30)

        dic['EDF'] = edf # ????
        dic['EDF'] = tva

        mispace()
        style_table([
            [f'Economies sur {int(report_jours/30)} mois', str(economies_sur_6_mois)+'€'],
            ['MaPrimeRénov', str(dic['MPR'])+'€'],
            ['Coup de Pouce', str(dic['CEE'])+'€'],
            ['EDF', str(dic['EDF'])+'€'],
            ['Récupération de la TVA', str(dic['TVA'])+'€'],
            ["Déduction crédit d'impôts", '???'],
            ['Total', str(economies_sur_6_mois+dic['MPR']+dic['CEE']+dic['EDF'])+'€'],
            ['Reste à éco-financer après déduction des aides', str(montant_materiels_et_services - (economies_sur_6_mois+dic['MPR']+dic['CEE']+dic['EDF']+dic['TVA']))+'€'],
                    ])

        st.subheader("Eco-financement  💲")
        col1, col2, col3 = st.columns(3)
        with col1:
            amortissement_mois = st.number_input('Amortissement (mois)', value=180, step=1)
        with col2:
            mensualites_choisies = st.number_input('Mensualités (€)', value=160, step=1)
        with col3:
            economies_moy_par_mois = st.number_input('Economies Moy/mois)', value=472, step=1)

        st.subheader("Prévision Financière  🔭")
        col1, col2 = st.columns(2)
        #with col1:
        #    st.markdown('Gains et économies mensuelles pendant éco-financement')
        #    st.markdown('Gains et économies annuelles pendant éco-financement')
        #with col2:
        #    st.markdown(str(311)+' €')
        #    st.markdown(str(311*12)+' €')
        gain_eco_mensuelles_pdt_eco_financement = 0
        gain_eco_annuelles_pdt_eco_financement = 0 * tab['nbr_mois']
        show_eco('',
        ('Gains et économies mensuelles pendant éco-financement', str(gain_eco_mensuelles_pdt_eco_financement), '€'), 
        ('Gains et économies annuelles pendant éco-financement', str(gain_eco_annuelles_pdt_eco_financement),'€')
        )

        col1, col2 = st.columns(2)
        with col1:

            prevision_annee_eco_financement = st.number_input('Prévisions en années :', value=30, step=1)
            gain_et_eco_prevision_eco_financement = 0

            fig, ax = plt.subplots()
            wedgeprops = {'edgecolor': 'grey', 'linewidth': 2, 'antialiased': True}
            colors = ['#6eb52f', "#e0e0ef", 'lightcoral']
            sizes = [i for i in range(prevision_annee_eco_financement)] ##changer calcul
            ax.bar(range(prevision_annee_eco_financement),sizes)
            ax.axis('on')  # Equal 
            fig.set_facecolor((1,1,1,0))  
            st.pyplot(fig)
            path_fig = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generation_pdf\\bar_chart.png')
            fig.set_facecolor("white")  
            fig.savefig(path_fig)
        with col2:
            space(4)
            st.markdown("Total des gains et économies sur "+ str(prevision_annee_eco_financement)+" ans")
            st.markdown(str(23432)+'€')
            
        
        

        


        


        
        
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
                dic['mensualites_choisies'] = mensualites_choisies
                dic['economies_moy_par_mois'] = economies_moy_par_mois     

                dic['gain_eco_mensuelles_pdt_eco_financement'] = gain_eco_mensuelles_pdt_eco_financement
                dic['gain_eco_annuelles_pdt_eco_financement'] = gain_eco_annuelles_pdt_eco_financement

                dic['prevision_annee_eco_financement'] = prevision_annee_eco_financement
                dic['gain_et_eco_prevision_eco_financement'] = gain_et_eco_prevision_eco_financement   
                
                st.session_state.data = dic
                update_or_insert_data(dic)         


            switch_page('simulation_generer_documents')

render_page_ecofinancement()