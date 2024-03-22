import streamlit as st
import requests
import pandas as pd
import socket
import os
from db_functions import *
from streamlit_extras.stylable_container import stylable_container

def get_keys():
    path = os.path.join(os.path.join(os.path.dirname(__file__), 'df_to_save'),'zoho_file.csv')
    df = pd.read_csv(path)
    id = df.client_id.iloc[0]
    secret = df.secret_id.iloc[0]
    mail = df.mail.iloc[0]
    #redirect_uri = "http://localhost:8501/"
    redirect_uri = "https://solar-sales-voltico-development.streamlit.app/"
    return mail, id, secret, redirect_uri

def get_keys_from_bdd():
    mail = st.session_state.mail
    #query = f"SELECT * FROM user_credentials WHERE mail='{mail}';"
    #result = execute_query(query, fetch=True)
    #id = result[0][5]
    #secret = result[0][6]

    #redirect_uri = "http://localhost:8501/"
    redirect_uri = "https://solar-sales-voltico-development.streamlit.app/"
    id, secret, mail_smtp, mdp_smtp = retrieve_secrets(mail)
    return mail, id, secret, redirect_uri

def access_token_by_user():

    mail, id, secret, redirect_uri = get_keys_from_bdd() #get_keys()

    scope = "ZohoCRM.modules.ALL,ZohoCRM.settings.ALL,ZohoCRM.users.ALL,ZohoCRM.contacts.ALL,ZohoCRM.org.ALL" 
    #ZohoBooks.fullaccess.all"
    access_type = "offline"

    # URL d'autorisation
    authorization_url = "https://accounts.zoho.eu/oauth/v2/auth"
    authorization_params = {
        "scope": scope,
        "client_id": id,
        "response_type": "code",
        "access_type": access_type,
        "redirect_uri": redirect_uri,
    }

    url = st.experimental_get_query_params()
    if "code" in url:
        authorization_code = url["code"][0]
    else:           
        authorization_response = requests.get(authorization_url, params=authorization_params)
        url = authorization_response.url

        with stylable_container(key='lien_container',css_styles = ["""
        [data-testid="stMarkdownContainer"] > a  {
            font-color:lightblue;
        }
        [data-testid="stMarkdownContainer"] > p  {
            font-size: 16px;
            margin-left:17px;
        }
        """]):
            st.markdown(f"[Veuillez suivre le lien ci-dessous pour vous authentifier:]({url})")  
        # => renvoie le lien dans l'url de redirection en param
    
    if "code" in st.experimental_get_query_params():
        authorization_code = url["code"][0]
        token_url = "https://accounts.zoho.eu/oauth/v2/token"
        token_params = {
            "code": authorization_code,
            "client_id": id,
            "client_secret": secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
        token_response = requests.post(token_url, data=token_params)

        if "access_token" in token_response.json():
            access_token = token_response.json()["access_token"]
            refresh_token = token_response.json().get("refresh_token")
            
            mail = st.session_state.mail
            insert_refresh_token(mail, refresh_token)

            #df = pd.read_csv('./df_to_save/zoho_file.csv')
            #df['refresh_token'] = refresh_token
            #df.to_csv('./df_to_save/zoho_file.csv')
            st.session_state.token = access_token
            st.session_state.refresh = refresh_token
    
def access_token_from_refresh():

    if 'refresh' in st.session_state:
        refresh_token = st.session_state.refresh
    else:
        #path_zoho_csv = os.path.join(os.path.join(os.path.dirname(__file__),'df_to_save'),'zoho_file.csv')
        #df = pd.read_csv(path_zoho_csv)
        #refresh_token = df['refresh_token'].iloc[0]
        refresh_token = get_refresh_token(st.session_state.mail)

    
    mail, id, secret, redirect_uri = get_keys_from_bdd()
    token_url = "https://accounts.zoho.eu/oauth/v2/token"

    token_params = {
        "refresh_token": refresh_token,
        "client_id": id,
        "client_secret": secret,
        "redirect_uri": redirect_uri,
        "grant_type": "refresh_token",
    }

    # Envoyer la demande de rafraîchissement pour obtenir un nouvel access token
    token_response = requests.post(token_url, data=token_params)

    # Vérifier la réponse
    if token_response.status_code == 200:
        # Extraire et retourner le nouvel access token
        st.session_state.token = token_response.json().get("access_token")
    else:
        # Gérer les erreurs en fonction de la réponse
        print(f"Erreur lors du rafraîchissement du token : {token_response.text}")
        return None

def test_connexion_internet():
    try:
        # Tente de se connecter à un serveur Google (8.8.8.8) sur le port 53
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        print("Connexion Internet disponible.")
        return True
    except OSError:
        print("Pas de connexion Internet.")
        return False

## A check jsp encore si ça fonctionne bien
def get_user_info_by_email(access_token, email):
    # Endpoint pour récupérer la liste des utilisateurs
    endpoint = 'https://www.zohoapis.eu/crm/v2/Contacts/search?'
    headers = {
        "User-Agent": 'SolarSales/1.0',
        "Authorization": f"Bearer {access_token}",
    }
    #params = {"email":email}
    params2 = {"criteria":("Email:starts_with:"+email)}
    response = requests.get(endpoint, headers=headers, params=params2)
    if response.status_code == 200:
        options = []
        list = response.json().get('data')
        for x in list:
            options.append(x['Email'])
        email_selectionne = st.selectbox("Sélectionner le client :", options,  index=None)
    else:
        st.warning("Ce mail n'existe pas encore dans notre base de données")
        email_selectionne = None
    
    return email_selectionne

def get_user_info_by_nom_prenom(access_token, nom, prenom):
    # Endpoint pour récupérer la liste des utilisateurs
    endpoint = 'https://www.zohoapis.eu/crm/v2/Contacts/search?'
    headers = {
        "User-Agent": 'SolarSales/1.0',
        "Authorization": f"Bearer {access_token}",
    }
    #params = {"email":email}
    params2 = {"criteria":("First_Name:starts_with:"+prenom)or("Last_Name:starts_with:"+nom)}
    response = requests.get(endpoint, headers=headers, params=params2)
    if response.status_code == 200:
        options = []
        list = response.json().get('data')
        for x in list:
            options.append(x['Email'])
        email_selectionne = st.selectbox("Sélectionner le client :", options,  index=None)
    else:
        st.warning("Ce mail n'existe pas encore dans notre base de données")
        email_selectionne = None
    
    return email_selectionne
    
def create_contact(access_token, dic):
    # Endpoint pour créer un nouveau contact
    endpoint = "https://www.zohoapis.eu/crm/v2/Contacts/upsert"
    dic['adresse_postale'] = [["425 Route de Soucieu 69440 Saint Laurent d'Agny"]]
    dic['departement'] = [["69 - Rhône"]]
    dic['materiels'] = [[['PAC air-eau', 'Domotique']]]
    
    # Données du nouveau contact
    data = {
        "data": [
            {
                "First_Name": dic['prenom'][0],
                "Last_Name": dic['nom'][0],
                "Email": dic['email'][0],
                "Adresse de correspondance":dic['adresse_postale'][0], ##ne fonctionne que si le champ d'entrée est déjà présent sur le CRM -> pas grave juste faut le mettre
                "Code postale de correspondance":dic['departement'][0], #faut le mettre sous le bon format je crois
                "Description":dic['materiels'][0][0]
                
            }
        ]
    }

    headers = {
        "User-Agent": 'SolarSales/1.0',
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Envoie de la demande pour créer un nouveau contact
    response = requests.post(endpoint, headers=headers, json=data)

    #st.write(access_token, response.status_code, response.json())

    if response.status_code == 201 or response.status_code == 200:
        st.success("Données envoyées  🥳")
        return response.json()
    else:
        st.error("Erreur lors de la création du contact")
        #st.write(response.json())
        return None

    