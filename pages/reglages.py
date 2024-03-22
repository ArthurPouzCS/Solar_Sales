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
  
#dic = retrieve_data_params()
dic = {'param_ballon_thermo_tt_elec': 55, 'param_pac_air_air_tt_elec': 25, 'param_led_non_tt_elec': 10, 'param_ballon_thermo': 30}
if st.button('Accueil'):
    switch_page('Accueil')
with stylable_container(key='reglages_container', css_styles = my_style_container()):
    with st.container():
        tab2, tab3 = st.tabs(['Paramètres financiers', 'Changer mon mot de passe'])
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

