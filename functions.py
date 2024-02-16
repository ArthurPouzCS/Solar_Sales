import streamlit as st
import pandas as pd
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from calcul_aides import dic_aides_type_menage, subventionsMPR, translateMPR, subCEE, translateCEE
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
#from pdf2image import convert_from_path
import os
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
#from streamlit_pdf_viewer import pdf_viewer


def no_sidebar():
    no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
    """
    st.markdown(no_sidebar_style, unsafe_allow_html=True)

       
def custom_success(message):
    st.markdown(f'<p style="color: green; font-size: 14px;">{message}</p>', unsafe_allow_html=True)

def custom_warning(message):
    st.markdown(f'<p style="color: orange; font-size: 14px;">{message}</p>', unsafe_allow_html=True)

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def send_email(expediteur, destinataire, cc, objet, corps):
    
    df = pd.read_csv('./df_to_save/zoho_file.csv')
    mail_smtp = df.mail_smtp.iloc[0]
    mdp_smtp = df.mdp_smtp.iloc[0]

    # Configurer les informations du serveur SMTP pour Outlook
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587  # Utilisez le port 587 pour TLS (ou 25 pour non chiffré, mais 587 est recommandé)
    smtp_username = mail_smtp  # Remplacez par votre adresse e-mail Outlook
    smtp_password = mdp_smtp  # Remplacez par votre mot de passe Outlook -> ça marche  ! DIC_MDP[expediteur]

    # Configurer le message
    msg = MIMEMultipart()
    msg['From'] = expediteur
    msg['To'] = destinataire
    msg['Subject'] = subject

    # Ajouter le corps du message
    msg.attach(MIMEText(corps, 'plain'))

    # Établir la connexion avec le serveur SMTP
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Commencer la connexion TLS (si nécessaire)
        server.starttls()

        # Se connecter au serveur SMTP
        server.login(smtp_username, smtp_password)

        # Envoyer l'e-mail
        server.sendmail(msg['From'], msg['To'], msg.as_string())

def dic_to_df(dic):
    keys, values = list(dic.keys()), list(dic.values())
    for i in range(len(keys)):
        dic[keys[i]] = [values[i]]
    return pd.DataFrame(dic)

def space(rows):
    content = "<div>"
    for row in range(rows):
        content += "<br>"
    content += "</div>"
    st.markdown(content, unsafe_allow_html=True)

def mispace():
    st.markdown("<div style='margin-top : 10px></div>", unsafe_allow_html=True)

def show_past(label, *entries):
    st.markdown("""
        <style>
            .info-box-container {
                background-color: #f2f2f2;
                border: 1px solid #d4d4d4;
                padding: 5px 5%;
                margin: -10px 5px;
                border-radius: 8px;
            }

            .label {
                font-weight: bold;
                font-size : 110%;
                color: #003366;
            }

            .title {
                color : black;
                margin-left : 10px;
                font-size : 110%;
                font-weight : bold;
            }

            .value {
                color: black;
                margin-left : 20px;
                font-size: 110%;
            }

            .unit {
                
                color: rgb(12,0,150);
                margin-left : 5px;
            }
        </style>
        """, unsafe_allow_html=True)

    content = f'<div class="info-box-container"><span class="label">{label}</span>'

    for entry in entries:
        content += f'<div><span class="title">{entry[0]}</span><span class="value">{entry[1]}</span><span class="unit">{entry[2]}</span></div>'

    content += '</div>'
    st.markdown(content, unsafe_allow_html=True)

#anienne couleur_fond_show = #586e75

def show(label, *entries):
    st.markdown("""
        <style>
            .info-box-container {
                background-color: rgba(21, 67, 96, 0.9);
                border: 1px solid rgb(0,180,0);
                padding: 5px 5%;
                margin: -10px 5px;
                border-radius: 8px;
            }

            .label {
                font-weight: bold;
                font-size: 110%;
                color: rgb(240, 240, 240);
            }

            .entry {
                display: flex;
                justify-content: space-between;
                margin-top: 5px;
            }

            .title {
                color: rgb(220, 220, 220);
                font-size: 110%;
            }

            .value-unit {
                display: flex;
                flex-direction: row-reverse;
                font-size: 110%;
                margin-right:20px;
            }

            .value {
                color: rgb(220, 220, 220);
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

def show2_past(text):
    st.markdown("""
        <style>
            .info-box-container {
                background-color: #586e75;
                border: 1px solid rgb(0,180,0);
                padding: 5px 10px;
                margin: 0px 5px;
                border-radius: 8px;
                width :  90%;
            }

            .title {
                margin-left : 10px;
                text-align : centered;
            }
        </style>
        """, unsafe_allow_html=True)

    content = f'<div class="info-box-container"><span class="title">{text}</span></div>'
    st.markdown(content, unsafe_allow_html=True)

def show2(*entries):
    st.markdown("""
        <style>
            .info-box-container {
                background-color: rgba(21, 67, 96, 0.7);;
                border: 1px solid rgb(0,180,0);
                padding: 5px 5%;
                margin: -10px 5px;
                border-radius: 8px;
            }

            .entry {
                display: flex;
                justify-content: space-between;
                margin-top: 5px;
            }

            .title {
                color: rgb(220, 220, 220);
                font-size: 110%;
            }

            .value-unit {
                display: flex;
                flex-direction: row-reverse;
                font-size: 110%;
                margin-right:20px;
            }

            .value {
                color: rgb(220, 220, 220);
            }

          
        </style>
        """, unsafe_allow_html=True)

    content = f'<div class="info-box-container">'

    for entry in entries:
        content += f'<div class="entry"><span class="title">{entry[0]}</span><span class="value-unit"><span class="value">{entry[1]}</span></span></div>'

    content += '</div>'
    st.markdown(content, unsafe_allow_html=True)

def style_table(table_data):
    # Style CSS pour la table
    table_style = """
        <style>
            .styled-table {
                background-color:rgba(21, 67, 96, 0.7);
                color:white;
                margin: 0px;
                font-size: 16px;
                width: 100%;
                border-radius: 10px;
                overflow: hidden;
                border: 2px solid #000;
                transform: translateY(-30px);
            }

            .styled-table thead tr {
                background-color:#586e75;
                color: white;
                font-weight: bold;
                text-align: left;
            }

            .styled-table th,
            .styled-table td {
                
                padding: 12px 15px;
                border-bottom: 1px solid #ddd;
            }

            .styled-table tbody tr {
                transition: background-color 0.7s;
            }

            .styled-table tbody tr:hover {
                background-color: rgb(160, 160, 160);
            }
        </style>
    """

    # Construction du contenu HTML de la table
    table_content = "<table class='styled-table'>"

    for row in table_data:
        table_content += "<tr>"
        for col in row:
            table_content += f"<td>{col}</td>"
        table_content += "</tr>"

    table_content += "</table>"

    # Affichage du style et de la table avec st.markdown
    st.markdown(table_style, unsafe_allow_html=True)
    st.markdown(table_content, unsafe_allow_html=True)

def styled_button():
    st.markdown("""
    <style>
        div.stButton > button:first-child {
            margin-top : 30px;
            margin-right : 30px;
            width : 150px;
            height:60px;
            display : inline;
            float: right;
            border : solid lightgreen 1px;
        }
        div.stButton > button:hover {
            background-color : #f2f2f2;
            border : solid gray 1px;
            float: right;
        }
    </style>
    
    """, unsafe_allow_html=True)

def valeur_tabulees():
    constantes = {
        'prix_kwh':0.23, #prix_kwh_consomme_part
        'prix_kwh_revendu_part':0.10, #Fait

        'prix_kwh_revendu_pro_0_3':0.1735, #Fait
        'prix_kwh_revendu_pro_3_9':0.1474, #Fait
        'prix_kwh_revendu_pro_9_36':0.1382, #Fait
        'prix_kwh_revendu_pro_36_100':0.1202, #Fait


        'rendement_paneaux':0.14,
        'heures_ensoleillement':1180,
        #'puissance_restituée':10620, inutile
        'coef_meteorologique':0.8,
        'coef_performance':1.0,
        'perte_systeme':0.14,
        'nbr_mois':10,
        "surface_panneau":2.4,

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
    return constantes

def type_menage_fct(salaire, nbr_personnes, depart):
    depart = int(depart.split(' - ')[0]) #on récup le numéro du batiment
    ile_de_france = [75, 77, 78, 91, 92, 93, 94, 95]
    if depart in ile_de_france:
        list = dic_aides_type_menage['tableauRevenus_ile_de_france']
    else :
        list = dic_aides_type_menage['tableauRevenus_hors_ile_de_france']
    if nbr_personnes>5:
        pers_sup = nbr_personnes-5
        ########### à revoir !!!
        print((salaire - list[4]['menagesAuxRevenusModestes'])/pers_sup)
        if (salaire - list[4]['menagesAuxRevenusTresModestes'])/pers_sup < list[5]['menagesAuxRevenusTresModestes']:
                type = 'menagesAuxRevenusTresModestes'
        if (salaire - list[4]['menagesAuxRevenusModestes'])/pers_sup < list[5]['menagesAuxRevenusModestes']:
                type = 'menagesAuxRevenusModestes'
        if (salaire - list[4]['menagesAuxRevenusIntermediaires'])/pers_sup < list[5]['menagesAuxRevenusIntermediaires']:
                type = 'menagesAuxRevenusIntermediaires'
        if (salaire - list[4]['menagesAuxRevenusIntermediaires'])/pers_sup > list[5]['menagesAuxRevenusIntermediaires']:
                type = 'menagesAuxRevenusSuperieurs'
    else:
        i=nbr_personnes - 1
        if salaire < list[i]['menagesAuxRevenusTresModestes']:
            type = 'menagesAuxRevenusTresModestes'
        elif salaire < list[i]['menagesAuxRevenusModestes']:
            type = 'menagesAuxRevenusModestes'
        elif salaire < list[i]['menagesAuxRevenusIntermediaires']:
            type = 'menagesAuxRevenusIntermediaires'
        elif salaire >= list[i]['menagesAuxRevenusIntermediaires']:
                type = 'menagesAuxRevenusSuperieurs'
    
    nom_to_nbr = {'menagesAuxRevenusTresModestes':0, 'menagesAuxRevenusModestes':1, 'menagesAuxRevenusIntermediaires':2, 'menagesAuxRevenusSuperieurs':3}
    type_nbr = nom_to_nbr[type]
    return type_nbr

def aidesMPR(type_menage, list_materiel):
    s = 0
    for materiel in list_materiel:
        if materiel in translateMPR:
            nom = materiel
            materiel = translateMPR[nom]
            sub = subventionsMPR[materiel][type_menage]
            s+=sub
    return s

def departements():
    departements_france = [
    "01 - Ain",
    "02 - Aisne",
    "03 - Allier",
    "04 - Alpes-de-Haute-Provence",
    "05 - Hautes-Alpes",
    "06 - Alpes-Maritimes",
    "07 - Ardèche",
    "08 - Ardennes",
    "09 - Ariège",
    "10 - Aube",
    "11 - Aude",
    "12 - Aveyron",
    "13 - Bouches-du-Rhône",
    "14 - Calvados",
    "15 - Cantal",
    "16 - Charente",
    "17 - Charente-Maritime",
    "18 - Cher",
    "19 - Corrèze",
    "21 - Côte-d'Or",
    "22 - Côtes-d'Armor",
    "23 - Creuse",
    "24 - Dordogne",
    "25 - Doubs",
    "26 - Drôme",
    "27 - Eure",
    "28 - Eure-et-Loir",
    "29 - Finistère",
    "2A - Corse-du-Sud",
    "2B - Haute-Corse",
    "30 - Gard",
    "31 - Haute-Garonne",
    "32 - Gers",
    "33 - Gironde",
    "34 - Hérault",
    "35 - Ille-et-Vilaine",
    "36 - Indre",
    "37 - Indre-et-Loire",
    "38 - Isère",
    "39 - Jura",
    "40 - Landes",
    "41 - Loir-et-Cher",
    "42 - Loire",
    "43 - Haute-Loire",
    "44 - Loire-Atlantique",
    "45 - Loiret",
    "46 - Lot",
    "47 - Lot-et-Garonne",
    "48 - Lozère",
    "49 - Maine-et-Loire",
    "50 - Manche",
    "51 - Marne",
    "52 - Haute-Marne",
    "53 - Mayenne",
    "54 - Meurthe-et-Moselle",
    "55 - Meuse",
    "56 - Morbihan",
    "57 - Moselle",
    "58 - Nièvre",
    "59 - Nord",
    "60 - Oise",
    "61 - Orne",
    "62 - Pas-de-Calais",
    "63 - Puy-de-Dôme",
    "64 - Pyrénées-Atlantiques",
    "65 - Hautes-Pyrénées",
    "66 - Pyrénées-Orientales",
    "67 - Bas-Rhin",
    "68 - Haut-Rhin",
    "69 - Rhône",
    "70 - Haute-Saône",
    "71 - Saône-et-Loire",
    "72 - Sarthe",
    "73 - Savoie",
    "74 - Haute-Savoie",
    "75 - Paris",
    "76 - Seine-Maritime",
    "77 - Seine-et-Marne",
    "78 - Yvelines",
    "79 - Deux-Sèvres",
    "80 - Somme",
    "81 - Tarn",
    "82 - Tarn-et-Garonne",
    "83 - Var",
    "84 - Vaucluse",
    "85 - Vendée",
    "86 - Vienne",
    "87 - Haute-Vienne",
    "88 - Vosges",
    "89 - Yonne",
    "90 - Territoire de Belfort",
    "91 - Essonne",
    "92 - Hauts-de-Seine",
    "93 - Seine-Saint-Denis",
    "94 - Val-de-Marne",
    "95 - Val-d'Oise",
    "971 - Guadeloupe",
    "972 - Martinique",
    "973 - Guyane",
    "974 - La Réunion",
    "976 - Mayotte"
    ]
    return departements_france

def aidesCEE(type_menage, list_materiel):
    s=0
    menage_nom = ['menage_modeste_ou_tres_modeste','menage_modeste_ou_tres_modeste', 'menage_autre', 'menage_autre'][type_menage]
    sub = subCEE[menage_nom]
    for matos in list_materiel:
        if matos in translateCEE:
            nom_matos = translateCEE[matos]
            s+=sub[nom_matos]
    return s

def aidesEDF(puissance_panneaux):
    if puissance_panneaux<3:
        coef = 370              #370 €/kWc
    elif puissance_panneaux<9:
        coef = 280
    elif puissance_panneaux<36:
        coef = 200
    else:
        coef = 100
    return coef*puissance_panneaux

def displayPDF_basse_resol(pdf_path, width, height):
    with open(pdf_path, "rb") as pdf_file:
        file_stream = pdf_file.read()  
        doc = fitz.open(stream=file_stream, filetype='pdf')
        image_list = []
        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)
            pix = page.get_pixmap(dpi=300)  # scale up the image resolution
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            image_list.append(img)
    
    st.image(image_list, width=width, use_column_width=True)

def css():
    style = """
    <style>
        h1, h2, h3, h4, h5, h6 {
            font-size: 36px;
        }

    </style>

    """
    #ne fonctionne pas sur les labels jsp pk
    # Appliquer le style global
    #st.markdown(style, unsafe_allow_html=True)

def css_from_function(cadre=False):
    if cadre:
        css = ["""
                .block-container, .st-emotion-cache-z5fcl4, .ea3mdgi2 {
                    background-color: rgba(100,100,100,0.7);
                    border: 1px solid rgb(0,180,0);
                    }

                [data-testid="stMarkdownContainer"] > p {
                    font-size : 18px;
                    font-weight : bold;
                    }
                
                .st-emotion-cache-q8sbsg > p {
                    font-size : 18px;
                    font-weight : bold;
                }
                .st-emotion-cache-jnd7a1 p {
                    font-size : 18px;
                    font-weight : bold;
                }
                """]
    else:
        css = ["""
                [data-testid="stMarkdownContainer"] > p {
                    font-size : 18px;
                    font-weight : bold;
                    }
                
                .st-emotion-cache-q8sbsg > p {
                    font-size : 18px;
                    font-weight : bold;
                }
                .st-emotion-cache-jnd7a1 p {
                    font-size : 18px;
                    font-weight : bold;
                }
                """]
    return css

def convert_pdf_to_images(pdf_path, poppler_path):
    print(os.environ["PATH"])
    os.environ["PATH"] += os.pathsep + poppler_path
    print(os.environ["PATH"])
    images = convert_from_path(pdf_path, dpi=75)
    return images

def displayPDF_poppler(pdf_path, width, height):
    
    poppler_path = os.path.join(os.path.dirname(__file__),'poppler','poppler-23.11.0', 'Library', 'bin')
    
    images = convert_pdf_to_images(pdf_path, poppler_path)
    
    for i, img in enumerate(images):
        st.image(img, use_column_width=False, width=width)


def displayPDF(file, width, height):
    displayPDF_basse_resol(file, width, height)
    #displayPDF_pdf_viewer(file, width)
    #displayPDF_poppler(file, width, height)
    ## en dessous ça marche
    #with open(file, "rb") as pdf_file:
        #pdf_data = pdf_file.read()
        #base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
        #iframe_code = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={width} height={height} type="application/pdf" style="margin: auto; display: block; margin-bottom:50px"></iframe>'
        #st.markdown(str(iframe_code), unsafe_allow_html=True)
    

def background(img_path, position):

    def get_img_as_base64(path):
        with open(path, 'rb') as f:
            img = f.read()
        return base64.b64encode(img).decode()

    path_fin = os.path.join('ressources',img_path)
    path = os.path.join(os.path.dirname(__file__), path_fin)
    path_rel = os.path.relpath(path, os.getcwd())

    img = get_img_as_base64(path_rel)
    img_css = f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
            background-image: url("data:image/png;base64,{img}");
            background-position : {position};
            opacity : 0.8;
            background-repeat: no-repeat;
            background-size: cover;
            background-attachement : local;
            }}
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
            }}
        [data-testid= "stNotification"] {{
            background-color: rgba(33, 195, 84, 0.8);
            color : white;
            margin-top : 0px;
            margin-bottom : -20px;
        }}
        </style>
    """
    st.markdown(img_css, unsafe_allow_html=True)


def afficher_frise_chronologique_outdated(partie_actuelle):
    # -> peut etre faire columns avec switch button
    l = ['Etude Solaire', 'Habitat 1', 'Habitat 2', 'Habitat 3', 'Book']
    html_code = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                .timeline {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    background-color: rgb(20,150,70,0.8);
                    padding: 2px 15px 2px 15px;
                    border-radius: 20px;
                    position: relative;
                    top: -60px;
                }}

                .partie {{
                    flex: 1;
                    text-align: center;
                    padding: 0px;
                    transition: background-color 0.3s;
                    border-radius: 10px;
                }}

                .partie.actuelle {{
                    background-color: rgb(0,0,100,0.7);
                    color: #fff;
                }}
            </style>
        </head>
        <body>
            <div class="timeline">
                {"".join(f'<div class="partie {"actuelle" if i + 1 == int(partie_actuelle) else ""}">{l[i]}</div>' for i in range(5))}
            </div>
        </body>
        </html>
    """
    st.markdown(html_code, unsafe_allow_html=True)

def afficher_frise_chronologique(numero):
    l = ['Etude Solaire', 'Habitat 1', 'Habitat 2', 'Habitat 3', 'Book']
    p = ['saisir_donnees_etude_solaire', 'saisir_donnees_habitat_1', 'saisir_donnees_habitat_2', 'saisir_donnees_habitat_3', 'saisir_donnees_book']
    style_normal = """
            div.stButton > button:first-child {
                margin-top: -20px;
                margin-right: -15px;
                width: 119%;
                height : 15px;
                border-radius: 15px;
                border : 0px;
                display: inline;
                float: center;
                position: relative;
                top: -50px;
                background-color: rgb(0,150,49,1);
                color: white;
            }

            """
    style_now = """
            div.stButton > button:first-child {
                margin-top: -20px;
                margin-right: -15px;
                width: 119%;
                height : 15px;
                border-radius: 15px;
                border : 0px;
                display: inline;
                float: center;
                position: relative;
                top: -50px;
                background-color: rgb(150,200,100,1);
                color: white;
            }
            """

    for i,col in list(enumerate(st.columns(5))):
        if numero-1==i:
            style=style_now
        else:
            style=style_normal
        with col:
            with stylable_container(
            key=f'frise_{i}',
            css_styles = style
            ):
                if st.button(l[i]):
                    switch_page(p[i])


def displayPDF_pdf_viewer(file, width):
    with open(file, "rb") as file:
        binary = file.read()
    pdf_viewer(
                input=binary,
                width=700
            )

def dont_forget_past_audit():
    default_dic = {
                'adresse_postale':'',
                'surface': 100,
                'temperature': 18, 
                'hauteur_ss_plafond': 2.5, 
                'surface_chauffer':100,
                'annee_construction':1990,
                'nbr_personne':2,
                'montant_facture':2000,
                'conso_kwh':10000,
                'gaz_facture':500,
                'fioul_facture':500,
                'fioul_litre':2000,
                'age_chaudiere':5,
                'facture_autre_syst_chauffage':400,
                'capacite_eau_chaude_elec':100,
                'ressources_annuelles':20000,
                }

    def last(key, my_type, options=None):
            if my_type in ["text_input", "number_input"]:
                return dic_ancien_audit[key]
            if my_type in ["radio", "selectbox"]:
                if key=='masque_solaire':
                    return 1
                try:
                    return options.index(dic_ancien_audit[key])
                except :
                    return 0
            if my_type in ["multiselect"]: ## on dirait que les multiselect sont enregistrés en {"value1", "value2"} -> dans db_functions il faut définir les multiselect en VARCHAR(50)[]!!
                if '","' in dic_ancien_audit[key]:
                    result = dic_ancien_audit[key].split('{"')[1]
                    result = result.split('"}')[0]
                    result =  result.split('","')
                    return result
                elif ',' in dic_ancien_audit[key]:
                    result = dic_ancien_audit[key].split('{')[1]
                    result = result.split('}')[0]
                    result =  result.split(',')
                    return result 
                else:
                    return dic_ancien_audit[key]

    def pas_last(key, my_type, options=None):
            if key in default_dic.keys():
                return default_dic[key]
            else:
                return None

    def current_last(key, my_type, options=None):
        ## Faire qqchose pour que le dic soit toujours le meme
        if key in dic_ancien_audit.keys():
            if my_type in ["text_input", "number_input"]:
                if type(dic_ancien_audit[key])==list:
                    return dic_ancien_audit[key][0]
                return dic_ancien_audit[key]
            if my_type in ["radio", "selectbox"]:
                if key=='masque_solaire':
                    return 1
                if type(dic_ancien_audit[key])==list:
                    try :
                        return options.index(dic_ancien_audit[key][0])
                    except:
                        return 0
                return options.index(dic_ancien_audit[key])
            if my_type in ["multiselect"]: ## on dirait que les multiselect sont enregistrés en {"value1", "value2"} -> dans db_functions il faut définir les multiselect en VARCHAR(50)[]!!
                if type(dic_ancien_audit[key][0])==list:
                    result = dic_ancien_audit[key][0]
                    return result
                if '","' in dic_ancien_audit[key]:
                    result = dic_ancien_audit[key].split('{"')[1]
                    result = result.split('"}')[0]
                    result =  result.split('","')
                    return result
                else:
                    return dic_ancien_audit[key]
        else:
            if key in default_dic.keys():
                return default_dic[key]
            else:
                return None


    if 'ancien_audit' in st.session_state and not('nouvel_audit' in st.session_state):
        dic_ancien_audit = st.session_state.ancien_audit
        st.subheader(f"Audit de {dic_ancien_audit['prenom']} {dic_ancien_audit['nom']}", divider='blue')
        past_audit = True

        return past_audit, last
        
    elif 'data' in st.session_state:
        past_audit = False
        dic_ancien_audit = st.session_state.data
        return past_audit, current_last

    else: 
        past_audit = False
        return past_audit, pas_last
        
def frame(): #pas encore utilisé
    stctnr =  stylable_container(
            key='authenthif',
            css_styles = """
            [data-testid="stVerticalBlockBorderWrapper"] {
                background-color: rgba(200,200,200, 0.8);
                padding: 10px 10px;
                border-radius: 8px;
                }
                
            """
            )
    return stctnr

def tarif(dic):
    path = os.path.join(os.path.dirname(__file__), 'ressources','tarifs.xlsx')
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


