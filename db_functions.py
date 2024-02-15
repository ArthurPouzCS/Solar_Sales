import psycopg2
import bcrypt
import streamlit as st
from cryptography.fernet import Fernet
import binascii

def execute_query(query, params=None, fetch=False):
    url_connexion = "postgres://rptrtffu:qJ9HUKXAgBrlwrJVtDU34C5W8Xu0hk85@dumbo.db.elephantsql.com/rptrtffu"
    connection = psycopg2.connect(url_connexion)
        #user="postgres",
        #password="*****",
        #host="localhost",
        #port="5432",
        #database="postgres",
        #client_encoding="utf-8"
    #)

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
    finally:
        if connection:
            connection.close()

def create_table_user_credentials():
    ##### Rjouter les Not null
    query = """
    CREATE TABLE IF NOT EXISTS user_credentials (
        id SERIAL PRIMARY KEY,
        mail VARCHAR(100) UNIQUE NOT NULL,
        mdp VARCHAR(100) NOT NULL,
        nom VARCHAR(100),
        prenom VARCHAR(100),
        client_id VARCHAR(200),
        secret_id VARCHAR(512),
        mail_smtp VARCHAR(200),
        mdp_smtp VARCHAR(512),
        refresh_token VARCHAR(200)
    );
    """
    execute_query(query)

def drop_table(name):
    query = f"DROP TABLE IF EXISTS {name};"
    execute_query(query)

def retrieve_data(table, email, column):
    query = f"SELECT {column} FROM {table} WHERE mail='{email}';" 
    result = execute_query(query, fetch=True)
    if result:
        result = result[0][0]
    return result

def delete_data(name):
    query = f"DELETE FROM example_table WHERE name = '{name}';"
    execute_query(query)

def hash_password(password):
    # Générer un sel aléatoire 
    #salt = bcrypt.gensalt()
    salt = b'$2b$12$Hrykmqp0muwxKcnOflJFke'
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password.decode('utf-8')

def save_password(mail, password):
    hashed_password = hash_password(password)

    query = f"INSERT INTO user_credentials (mail, mdp) VALUES ('{mail}', '{hashed_password}');"
    execute_query(query)

def check_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_table_data(): # les multiselect ne sont pas enregistrés comme des [] d'ou la conversion en str dégueu
    query = """
    CREATE TABLE IF NOT EXISTS data_table (
    id SERIAL PRIMARY KEY,
    mail_sales VARCHAR(50),
    adresse_postale VARCHAR(255),
    departement VARCHAR(30),
    parcelles VARCHAR(10),
    pente_toit VARCHAR(50),
    altitude VARCHAR(50),
    masque_solaire VARCHAR(30),
    orientation_toit VARCHAR(30),
    type_personne VARCHAR(30),
    nom VARCHAR(50),
    email VARCHAR(50),
    prenom VARCHAR(50),
    type_projet VARCHAR(50),
    nbr_niveaux VARCHAR(30),
    vitrage VARCHAR(50),
    combles VARCHAR(50),
    couverture VARCHAR(50),
    etat_charpente VARCHAR(30),
    annee_construction INT,
    type_charpente VARCHAR(30),
    isolation_comble VARCHAR(30),
    isolation_mur VARCHAR(30),
    nbr_personne INT,
    temperature INT,
    hauteur_ss_plafond INT,
    surface INT,
    surface_chauffer INT,
    volume INT,
    temperature_min_ext INT,
    coef_isolation FLOAT,
    delta_t INT,
    puissance_pac FLOAT,
    equipement_pv_passe VARCHAR(30),
    etude_solaire_passe VARCHAR(30),
    dpe_passe VARCHAR(30),
    puissance_kva INT,
    fournisseur VARCHAR(50),
    compteur VARCHAR(30),
    abonnement VARCHAR(50),
    montant_facture INT,
    connaissance_facture_elec VARCHAR(30),
    chauffage_electrique VARCHAR(50),
    gaz_fioul VARCHAR(50),
    gaz_facture INT,
    fioul_facture INT,
    fioul_litre INT,
    type_chaudiere VARCHAR(30),
    type_materiel VARCHAR(50),
    age_chaudiere INT,
    chaudiere_electrique VARCHAR(30),
    autre_systeme_chauffage VARCHAR(50),
    facture_autre_syst_chauffage INT,
    hauteur_ecs VARCHAR(30),
    ballon_eau_chaude_electrique VARCHAR(30),
    climatisation VARCHAR(30),
    capacite_ballon INT,
    plaque_cuisson VARCHAR(50),
    lave_vaisselle VARCHAR(30),
    seche_linge VARCHAR(30),
    systeme_vmc VARCHAR(30),
    type_four VARCHAR(30),
    lave_linge VARCHAR(30),
    voiture_electrique VARCHAR(30),
    piscine_chauffee VARCHAR(30),
    frigidaire VARCHAR(50),
    congelateur VARCHAR(50),
    type_ampoule VARCHAR(50),
    habitude_conso VARCHAR(50),
    ressources_annuelles INT,
    interesse VARCHAR(50),
    nvl_conso_elec_kwh_ameliore_materiels_sans_pv INT,
    nvl_facture_elec_ameliore_materiels_sans_pv INT,
    nvl_facture_gaz INT,
    nvl_facture_fioul_autre INT,
    prod_total_annee FLOAT,
    economies_annnuelles_pv_autoconso FLOAT,
    gains_annnuelles_pv_surplus FLOAT,
    materiels VARCHAR(255)[],
    puissance_panneaux INT,
    pv_unitaire VARCHAR(30),
    nbr_panneaux INT,
    surface_panneaux FLOAT,
    h_soleil INT,
    p_restit FLOAT,
    coef_meteo FLOAT,
    coef_perf FLOAT,
    perte FLOAT,
    rdt_panneaux FLOAT,
    prix_achete FLOAT,
    prix_revendu FLOAT,
    gain_et_eco_elec_par_an FLOAT,
    eco_gaz_fioul_autres INT,
    indexation INT,
    annnees_prevision INT,
    economie_total FLOAT,
    economie_par_an_moyen FLOAT,
    economie_par_mois_moyen FLOAT,
    MPR INT,
    CEE INT,
    EDF INT,
    TVA INT,
    credit INT,
    total_aides INT,
    ancienne_conso_elec FLOAT,
    ancienne_facture_elec INT,
    classe_dpe VARCHAR(10),
    classe_dpe_ges VARCHAR(10),
    nbr_ges FLOAT,
    nbr_energie FLOAT,
    nv_ges_lettre VARCHAR(5),
    nv_ges FLOAT,
    nv_dpe_lettre VARCHAR(5),
    nv_dpe FLOAT,
    economie_n_plus_un INT,
    montant_materiels_et_services INT,
    report_jours INT,
    duree_initiale INT,
    partenaire_financier VARCHAR(50),
    premiere_mensualite FLOAT,
    economies_sur_6_mois VARCHAR(50),
    amortissement_mois INT,
    mensualites_choisies INT,
    economies_moy_par_mois INT,
    gain_eco_mensuelles_pdt_eco_financement INT,
    gain_eco_annuelles_pdt_eco_financement INT,
    prevision_annee_eco_financement INT,
    gain_et_eco_prevision_eco_financement INT,
    puissance_deja_installee INT,
    audit_path VARCHAR(255),
    rapport_path VARCHAR(255)
    );
    """
    execute_query(query)

def update_or_insert_data(data_dict):
    create_table_data()
    data_dict = clean_dict(data_dict)
    # Vérification si l'email existe déjà dans la table
    email = data_dict.get('email', None)
    if email:
        query = "SELECT adresse_postale FROM data_table WHERE email = %s"
        existing_entry = execute_query(query, (email,), fetch=True)
        # Si l'entrée existe, mise à jour des données
        if existing_entry:
            update_query = "UPDATE data_table SET "
            update_query += ', '.join([f"{key} = %s" for key in data_dict.keys()])
            update_query += " WHERE email = %s"
            update_data = list(data_dict.values()) + [email]
            execute_query(update_query, tuple(update_data))
        else:
            # Si l'entrée n'existe pas, insertion des nouvelles données
            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join(['%s' for _ in data_dict])
            insert_query = f"INSERT INTO data_table ({columns}) VALUES ({placeholders})"
            execute_query(insert_query, tuple(data_dict.values()))

def clean_dict(dict):
    clean = True
    for key, value in dict.items():
        if type(value)== type([]):
            if len(list(value))==1:
                dict[key] = value[0]
                clean = False
    if not(clean):
        dict = clean_dict(dict)
    return dict





    #if st.button('Inscription'):
    #    with st.form(key='inscription'):
    #        mail = st.text_input('Mail')
    #        password = st.text_input('Password', type='password')
    #        submit = st.form_submit_button("S'inscrire")

def mail_already_exist(mail):
    query = f"SELECT mail FROM user_credentials WHERE mail='{mail}';"
    result = execute_query(query, fetch=True)
    already = not(result == [])
    return already

clef = b'3xTl4p9b0S8etmDDFyo70j7fq3PXhdOugMqbLHkZsvE=' #"secrète"

def insert_credential_data(mail, nom, prenom, client, secret, mail_smtp, mdp_smtp):
    fernet = Fernet(clef)
    secret_encode = fernet.encrypt(secret.encode('utf-8'))
    mdp_smtp_encode = fernet.encrypt(mdp_smtp.encode('utf-8'))
    query = f"""
        UPDATE user_credentials
        SET nom='{nom}', prenom='{prenom}', client_id='{client}', secret_id=%s, mail_smtp='{mail_smtp}', mdp_smtp=%s
        WHERE mail='{mail}';
    """
    execute_query(query, (secret_encode, mdp_smtp_encode))

def retrieve_secrets(mail):
    query = f"SELECT client_id, secret_id, mail_smtp, mdp_smtp FROM user_credentials WHERE mail='{mail}';"
    result = execute_query(query, fetch=True)
    if result:
        fernet = Fernet(clef)     

        secret = fernet.decrypt(binascii.unhexlify(str(result[0][1])[2:])).decode('utf-8')
        mdp_smtp = fernet.decrypt(binascii.unhexlify(str(result[0][3])[2:])).decode('utf-8')
        
        client_id, secret_id, mail_smtp, mdp_smtp = result[0][0], secret, result[0][2], mdp_smtp
        result = client_id, secret_id, mail_smtp, mdp_smtp
    return result

def insert_refresh_token(mail, refresh_token):
    query = f"""
        UPDATE user_credentials
        SET refresh_token='{refresh_token}'
        WHERE mail='{mail}';
    """
    execute_query(query)

def get_refresh_token(mail):
    query = f"SELECT refresh_token FROM user_credentials WHERE mail='{mail}';"
    result = execute_query(query, fetch=True)
    if result:
        result = result[0][0]
    return result