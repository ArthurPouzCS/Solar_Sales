import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from functions import *
from streamlit_extras.stylable_container import stylable_container
import time
from db_functions import *

def changer_mdp(last_password, new_password):
    if 'mail' in st.session_state:
        mail = st.session_state.mail
    else:
        st.error('Vous devez être connecté pour accéder à cette page')
        time.sleep(2)
        switch_page('Accueil')
    
    hashed_password = retrieve_data('user_credentials', mail, 'mdp')
    #st.write(hashed_password)
    if check_password(last_password, hashed_password):
        update_password(mail, new_password) #j'espère que ça n'entraine pas de bug -> faudra voir oklm
        st.success('Mot de passe changé')
    else:
        st.error('Ancien mot de passe incorrect')
    
    
st.set_page_config(page_title="Réglages", page_icon="⚙", layout="wide", initial_sidebar_state="collapsed")
no_sidebar()
css()
styled_button()

if 'mail' in st.session_state:
    mail = st.session_state.mail
    if 'admin' in mail or 'arthur.pouzargue@outlook.fr'==mail:
        admin_access = True
    else:
        admin_access = False

if st.button('Accueil'):
    switch_page('Accueil')
with stylable_container(key='reglages_container', css_styles = my_style_container()):
    with st.container():
        tab1, tab2, tab3 = st.tabs(['Paramètres généraux','Paramètres financiers', 'Changer mon mot de passe'])
        #with tab1:
        #    st.subheader('Paramètres généraux')
        #    a,b,c,d = st.columns(2)
        #    with a:
        #        param_ballon_thermo_tt_elec = st.number_input('Tx Ballon Thermo cas tout électrique (en %)', value=dic['param_ballon_thermo_tt_elec'], min_value=0, max_value=100, step=1)
        #    with b:
        #        param_pac_air_air_tt_elec = st.number_input('Tx Pac air-air Cas tout électrique (en %)', value=dic['param_pac_air_air_tt_elec'], min_value=0, max_value=100, step=1)
        #    with c:
        #        param_led_non_tt_elec = st.number_input('Tx pack led : Cas non tout électrique (en %)', value=dic['param_led_non_tt_elec'], min_value=0, max_value=100, step=1)
        #    with d:
        #        param_ballon_thermo = st.number_input('Tx ballon thermo : Cas gaz/fioul (en %)', value=dic['param_ballon_thermo'], min_value=0, max_value=100, step=1)
        with tab2:
            st.subheader('Réglages modifiables')
            nbr_mois = st.number_input('Calcul annuel sur X mois (en mois)', value=10, min_value=0, max_value=12, step=1)
            supplement_facture_total = st.number_input('Supplément sur facture totale (en €)', value=0, min_value=0, max_value=10000, step=1)
        with tab3:
            st.subheader('Changer mon mot de passe')
            last_password = st.text_input("Ancien mot de passe", type="password")
            new_password1 = st.text_input("Nouveau mot de passe", type="password")
            new_password2 = st.text_input("Confirmer le nouveau mot de passe", type="password")
            if new_password2!=None:
                if new_password1 != new_password2:
                    st.error("Les mots de passe ne correspondent pas")
                else:
                    st.success("Tout est bon !")
                    if st.button("Changer le mot de passe"):
                        changer_mdp(last_password, new_password1)
        with tab1:

            
            
            dic_tab = {
                'prix_kwh':0.23, #prix_kwh_consomme_part
                'prix_kwh_revendu_part':0.10, #Fait

                'prix_kwh_revendu_pro_0_3':0.13, #Fait
                'prix_kwh_revendu_pro_3_9':0.13, #Fait
                'prix_kwh_revendu_pro_9_36':0.078, #Fait
                'prix_kwh_revendu_pro_36_100':0.078, #Fait


                'rendement_paneaux':0.14,
                'heures_ensoleillement':1180,
                #'puissance_restituée':10620, inutile
                'coef_meteorologique':0.8,
                'coef_performance':1.0,
                'perte_systeme':0.14,
                'nbr_mois':10,
                "surface_panneau":2.4,

                # Pourcentage d'économie : si tu installes un ballon thermo quand tu n'as que de l'elec tu fais 25% d'économie sur ta facture par exemple
                # Si tu fais 30% d'éco avec le m1 et 20% avec le M2 tu fais 30% puis 20% donc = 1 - 0.7*0.8 = 44% d'économie !
                # Si M1 = 20%, M2=100% en théorie tu fais 100% d'économie donc 0 sur ta facture donc ta facture vaut (1-0.2)*(1-1)=0%=0€ ok
                # Si M1=20%, M2=0% tu ne fais que 20% en théorie donc ta facture vaut (1-0.2)*(1-0)*€=80% de € donc ok 
                #'tx_ballon_thermo_qd_tt_elec':0.25, #Fait # Outdated
                'tx_pac_air_air_qd_tt_elec':0.55, #Fait
                'tx_pac_air_eau_qd_tt_elec':0.25, #Fait
                'tx_pack_led_qd_tt_elec':0.09, #Fait
                'tx_pack_led_qd_tt_nn_elec':0.1, #Fait
                #'tx_ballon_thermo_qd_gaz_fioul':0.3, #Fait # Outdated
                'tx_pac_air_air_qd_gaz_fioul':0.7, #Fait
                'tx_pac_air_eau_qd_gaz_fioul':0.7, #Fait

                'tx_ballon_thermo_qd_gaz_fioul_elec_ballon_sur_elec':0.5, #Fait
                'tx_pac_air_air_qd_gaz_fioul_ballon_sur_elec':0, #Fait
                'tx_pac_air_eau_qd_gaz_fioul_elec_ballon_sur_elec':0, #Fait
                'tx_ballon_thermo_qd_gaz_fioul_elec_ballon_sur_gaz':0, #Fait
                'tx_pac_air_air_qd_gaz_fioul_elec_ballon_sur_gaz':1, #Fait
                'tx_pac_air_eau_qd_gaz_fioul_elec_ballon_sur_gaz':1, #Fait

                'tx_domotique':0, #Fait
                'tx_micro_onduleur':0, #Fait
                'tx_batterie_stockage':0, #Fait
                'tx_vehicule_elec':0, #Fait
                'tx_masque_solaire':0.002, #Fait

                'conso_pac_air_air':2600, #Fait
                'conso_pac_air_eau':2600, #Fait
                'conso_ballon_thermo':400, #Fait
            }
            try:
                for key in dic_tab.keys():
                    dic_tab[key] = retrieve_data_params(key)
            except:
                pass
            

            for key in dic_tab.keys():
                val = dic_tab[key]
                
                if admin_access:
                    new_val = st.number_input(key, value=val, min_value=val*0, max_value=val*1000)
                else:
                    new_val = st.number_input(key, value=val, min_value=val, max_value=val)
            
                dic_tab[key] = new_val

            if st.button('Mise à jour des réglages'):
                try :
                    update_or_insert_params_data(dic_tab)
                    st.success('Réglages modifiés avec succès 🎉')
                except:
                    st.error("Erreur lors de la mise à jour")