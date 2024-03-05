import streamlit as st
from pv_gis_function import get_solar_estimation, get_coordinates_from_address
from functions import displayPDF, dont_forget_past_audit
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container

import os
import sys
path_generer_pdf_py = os.path.join(os.getcwd(), 'generation_pdf')
sys.path.insert(0,path_generer_pdf_py)
from generer_pdf_app import generer_pvgis

past_audit, last = dont_forget_past_audit()

adresse = "425 Route de Soucieu 69440 Saint Laurent d'Agny"

lat, lon = get_coordinates_from_address(adresse)
system_loss = 0.08 
peak_power = 1.0 
if lat is not None and lon is not None:
    solar_data = get_solar_estimation(lat, lon, peak_power, system_loss)


#st.write(solar_data)
path = generer_pvgis(solar_data)
abs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'generation_pdf',path)

with stylable_container(key='titre_center', css_styles="""
[data-testid="stButton"] {
    text-align:right;
    height: 50px;
}
[data-testid="baseButton-secondary"]{
    width:120px;
    height:60px;
}
"""):
    if st.button("Accueil"):
        switch_page('Accueil')

displayPDF(abs_path, 400, 400)



