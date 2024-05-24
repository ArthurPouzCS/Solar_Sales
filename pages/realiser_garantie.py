import streamlit as st
from pv_gis_function import get_solar_estimation, get_coordinates_from_address
from functions import displayPDF, dont_forget_past_audit, my_style_container, send_email, colors
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
import time

import os
import sys
path_generer_pdf_py = os.path.join(os.getcwd(), 'generation_pdf')
sys.path.insert(0,path_generer_pdf_py)
from generer_pdf_app import generer_pvgis

past_audit, last = dont_forget_past_audit()



if 'data' in st.session_state:
    if 'adresse_postale' in st.session_state.data:
        adresse = st.session_state.data['adresse_postale']
else : 
    adresse = None
    st.info('Veuillez renseigner une adresse pour obtenir une estimation de production solaire')

if adresse is not None:
    lat, lon = get_coordinates_from_address(adresse)
    system_loss = 0.08 
    peak_power = 1.0 
    if 'data' in st.session_state:
        if 'puissance_panneaux' in st.session_state.data:
            peak_power = st.session_state.data['puissance_panneaux']
    if lat is not None and lon is not None:
        solar_data = get_solar_estimation(lat, lon, peak_power, system_loss)

    path = generer_pvgis(solar_data)
    abs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'generation_pdf',path)

    with stylable_container(key='titre_center', css_styles=f"""
    [data-testid="stButton"] {{
        text-align:right;
        height: 50px;
    }}
    [data-testid="baseButton-secondary"]{{
        width:120px;
        height:60px;
    }}
    .st-emotion-cache-123r4br{{
        background-color: {colors(0)};
    }}
    """):
        if st.button("Accueil"):
            switch_page('Accueil')

        col1, col2 = st.columns(2)
        with col2:
            with stylable_container(key="adresse_style", css_styles=my_style_container()):
                with st.container():
                    #if st.button("Envoyer par mail"):
                    expediteur = st.text_input('Expéditeur', value='arthur.pouzargue@gmail.com')
                    destinataire = st.text_input('Destinataire', value='arthur.pouzargue@outlook.fr')
                    #cc = st.text_input('CC', value='arthur.pouzargue@outlook.fr')
                    cc = 'arthur.pouzargue@outlook.fr'
                    objet = st.text_input('Objet', value='Garantie de production photovoltaïque')
                    ##pj = piece jointe !!
                    corps = st.text_area('', value="""
                    Bonjour,

                    Veuillez recevoir en PJ l'estimation de production de vos panneaux photovoltaïques.
                    
                    Bonne réception,
                    
                    Cordialement
                    """, height=250)
                    
                    if st.button("Envoyer"):
                        #try:
                        send_email(expediteur, destinataire, cc, objet, corps, abs_path) #attention à mettre le mail comme il fait et mettre le mdp dans les réglages
                        time.sleep(2)
                        switch_page('Accueil')
        with col1:
            displayPDF(abs_path, 400, 400)

else:
    time.sleep(2)
    switch_page('Accueil')