import psycopg2
import bcrypt
import streamlit as st
from cryptography.fernet import Fernet
import binascii

def execute_query(query, params=None, fetch=False):
       
    try:
        from credentials import MDP
        password = MDP
        connection = psycopg2.connect(
            user="postgres",
            password=password,
            host="localhost",
            port="5432",
            database="postgres",
            client_encoding="utf-8"
        )
    except:
        url_connexion = "postgres://rptrtffu:qJ9HUKXAgBrlwrJVtDU34C5W8Xu0hk85@dumbo.db.elephantsql.com/rptrtffu"
        connection = psycopg2.connect(url_connexion)


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

def update_password(mail, password):
    hashed_password = hash_password(password)

    query = f"UPDATE user_credentials SET mdp = '{hashed_password}' WHERE mail = '{mail}';"
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
    annee_isolation_comble VARCHAR(30),
    isolation_mur VARCHAR(30),
    annee_isolation_mur VARCHAR(30),
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
    dpe VARCHAR(10),
    puissance_kva INT,
    fournisseur VARCHAR(50),
    compteur VARCHAR(30),
    abonnement VARCHAR(50),
    montant_facture INT,
    connaissance_facture_elec VARCHAR(30),
    conso_kwh INT,
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
    apport INT,
    reste_a_eco_financer INT,
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
    data_dict.pop('id', None)
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


def create_table_params(): # On l'appelle dans authentification
    ##### Des paramètres pour tout le monde
    query = """
    CREATE TABLE IF NOT EXISTS params_table (
        id SERIAL PRIMARY KEY,
        prix_kwh FLOAT,
        prix_kwh_revendu_part FLOAT,
        prix_kwh_revendu_pro_0_3 FLOAT,
        prix_kwh_revendu_pro_3_9 FLOAT,
        prix_kwh_revendu_pro_9_36 FLOAT,
        prix_kwh_revendu_pro_36_100 FLOAT,
        rendement_paneaux FLOAT,
        heures_ensoleillement INT,
        coef_meteorologique FLOAT,
        coef_performance FLOAT,
        perte_systeme FLOAT,
        nbr_mois INT,
        surface_panneau FLOAT,
        tx_pac_air_air_qd_tt_elec FLOAT,
        tx_pac_air_eau_qd_tt_elec FLOAT,
        tx_pack_led_qd_tt_elec FLOAT,
        tx_pack_led_qd_tt_nn_elec FLOAT,
        tx_pac_air_air_qd_gaz_fioul FLOAT,
        tx_pac_air_eau_qd_gaz_fioul FLOAT,
        tx_ballon_thermo_qd_gaz_fioul_elec_ballon_sur_elec FLOAT,
        tx_pac_air_air_qd_gaz_fioul_ballon_sur_elec FLOAT,
        tx_pac_air_eau_qd_gaz_fioul_elec_ballon_sur_elec FLOAT,
        tx_ballon_thermo_qd_gaz_fioul_elec_ballon_sur_gaz FLOAT,
        tx_pac_air_air_qd_gaz_fioul_elec_ballon_sur_gaz FLOAT,
        tx_pac_air_eau_qd_gaz_fioul_elec_ballon_sur_gaz FLOAT,
        tx_domotique FLOAT,
        tx_micro_onduleur FLOAT,
        tx_batterie_stockage FLOAT,
        tx_vehicule_elec FLOAT,
        tx_masque_solaire FLOAT,
        conso_pac_air_air INT,
        conso_pac_air_eau INT,
        conso_ballon_thermo INT
        );
        """
    execute_query(query)

    # On initialise la table
    query = "SELECT prix_kwh FROM params_table"
    il_y_a_qqchose_dedans = execute_query(query, fetch=True)
    if not(il_y_a_qqchose_dedans):
        default_data_dict = {
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
        columns = ', '.join(default_data_dict.keys())
        placeholders = ', '.join(['%s' for _ in default_data_dict])
        insert_query = f"INSERT INTO params_table ({columns}) VALUES ({placeholders})"
        execute_query(insert_query, tuple(default_data_dict.values()))

def retrieve_data_params(column):
    query = f"SELECT {column} FROM params_table;" 
    result = execute_query(query, fetch=True)
    if result:
        result = result[0][0]
    return result
    

def update_or_insert_params_data(data_dict):
        create_table_params()
        data_dict = clean_dict(data_dict)
        data_dict.pop('id', None)
        # Vérification si l'email existe déjà dans la table
        #email = data_dict.get('email', None)
        
        query = "SELECT prix_kwh FROM params_table"
        existing_entry = execute_query(query, fetch=True)
        # Si l'entrée existe, mise à jour des données
        if existing_entry:
            update_query = "UPDATE params_table SET "
            update_query += ', '.join([f"{key} = %s" for key in data_dict.keys()])
            update_data = list(data_dict.values())
            execute_query(update_query, tuple(update_data))