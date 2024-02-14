import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
import matplotlib.pyplot as plt
import base64

def generate_pdf_audit():

    def part(titre, caption, tab):
        space = Spacer(10,10)
        ss_titre = Paragraph(titre, styles['Heading3'])
        caption = Paragraph(caption, styles['Heading4'])
        tableau = generate_tableau(tab)
        return [space, ss_titre, caption, tableau]

    def page_couverture():

        adresse = Paragraph(f"5 Rue Paul Fignac 93420", styles['BodyText'])
        mail = Paragraph(f"test@mail.fr", styles['BodyText'])
        parcelle = Paragraph(f"Parcelle 53", styles['BodyText'])
        nom = Paragraph(f"CHICHE", styles['BodyText'])
        prenom = Paragraph(f"Ruben", styles['BodyText'])

        space = Spacer(10, 10)
        centre_energie =  Paragraph(f"☀ CENTRE ENERGIE", styles['Heading1'])
        titre = Paragraph(f"Audit énergétique", styles['Heading1'])
        ss_titre = Paragraph(f"Simulation réalisé le 03/12/2021", styles['Heading2'])

        departement = Paragraph(f"<b>Département</b>", styles['BodyText'])
        depart = Paragraph(f"93 - Seine-Saint-Denis", styles['BodyText'])

        annee = Paragraph(f"<b>Année de construction</b>", styles['BodyText'])
        ann = Paragraph(str(1993), styles['BodyText'])

        surface = Paragraph(f"<b>Surface habitable</b>", styles['BodyText'])
        surf = Paragraph(str(100)+'m²', styles['BodyText'])

        blabla = Paragraph("Cet audit vous est fourni à titre indicatif et n'engage ni son auteur ni l'éditeur de logiciel qui a servi à le réaliser. Seul un bureau d'étude énergétique habilité peut délivrer un étude énergétique réglementaire", styles['BodyText'])

        return [[[adresse, mail, parcelle],[nom, prenom]], centre_energie, space, titre, ss_titre, [[departement, depart], [annee, ann], [surface, surf]], blabla]

    def but_document():
        styles = getSampleStyleSheet()
        titre_but = Paragraph(f"Le but de ce document", styles['Heading3'])
        but_caption = Paragraph(f"Ce document vous permet de conserver les informations essentielles renseignées lors de l'étude effectué avec notre conseiller Centre énergie.", styles['BodyText'])
        but_list = Paragraph(f"""<div>Elle vous présente : 
        <ul>
        <li>Une synthèse des caractéristique de votre habitation.</li>
        <li>La simulation des gains et économies réalisés grâce au matériel préconisé.</li>
        <li>La simulation des aides financières auxquelles vous êtes éligible.</li>
        <li>Les avantages et caractéristiques du matériel préconisé.</li>
        <li>La simulation d'amortissement du matériel grâce aux économies réalisées.</li>
        </ul></div>""", styles['BodyText'])

        pvgis = Paragraph(f"Ce document est calculé sur la base des données PVGIS.", styles['BodyText'])
        simu = Paragraph(f"Toutes les simulations chiffrées présentes dans ce documents sont purement indicatives et basées sur les éléments que vous nous avez communiqués. La consommation énergétique d'une habitation étant dépendante de nombreux facteurs Centre énergie ne saurait voir sa responsabilité engagée dans l'hypothèseoù cette simulation ne correspondrait pas à la consommation réelle.", styles['BodyText'])
        avantage_reno = Paragraph(f"Avantage de la rénovation énergétique", styles['Heading3'])
        dimension = Paragraph(f"Votre projet de rénovation touche à la dimension énergétique de votre habitat.", styles['BodyText'])
        pvgis = Paragraph(f"Cela Vous apporte de nombreux avantages :", styles['BodyText'])
        img2 = Image('image2.jpg', width=pdf.width, height=0.3*pdf.height)
        logo = Image('image2.jpg', width=30, height=30)
        respect_env = Paragraph(f"De plus vous participez au respect de l'environnnement. Avec l'augmentation du prix de l'énergie, ne rien faire revient souvent plus cher", styles['BodyText'])

        return [titre_but, but_caption, but_list, pvgis, simu, avantage_reno, dimension, pvgis, img2, [logo, respect_env]]

    def generate_tableau(tab):
        bold_style = ParagraphStyle('BodyTextBold',parent=styles['BodyText'],fontName='Helvetica-Bold')
        
        table_data = [[[Paragraph(str(tab[i][j][0]), bold_style), Paragraph(str(tab[i][j][1]), styles['BodyText'])] for j in range(len(tab[0]))] for i in range(len(tab))]
        
        style = TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrer verticalement
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrer le texte
            ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Ajouter des lignes de grille
        ])

        tableau = Table(table_data, style=style)

        return tableau

    def caracteristique_habitat():

        # Titre
        subtitle_paragraph = Paragraph(f"<i>A. CARACTERISTIQUES HABITAT</i>", styles['Heading1'])

        # Image
        height_prct = 0.3
        image_path = 'image2.jpg'
        img = Image(image_path, width=pdf.width, height=height_prct*pdf.height)

        space = Spacer(10, 10)

        # Text
        titre_tableau = Paragraph(f"Les informations sur votre habitation, son budget et sa consommation", styles['Heading3'])

        # Tableau
        tab = [
            [('La pente du toît', 'Classique 30°'), ('Orientation du toît', 'Sud'), ('Vos fenêtres sont', 'Double vitrage'), ('Votre couverture','ardoisé')],
            [('Votre type de charpente', 'Bois'), ('Nombre de personne dans le logement', '1 Personne(s)'), ('Isolation des combles réalisée ?', 'Non'), ('Surface du logement',1600)],
            [('Surface de chauffe', str(100)+'m²'), ('Puissance de votre compteur', str(12)+'kVA'), ('Type de compteur', 'Monophasé'), ("Montant de votre facture d'électricité",str(1800)+'€')], 
            [('Votre consommation annuelle en kWh', str(8990)+'kWh'), ('Facture annuelle de gaz/fioul', str(1800)+'€'), ('Type de la chaudière', 'Ventouse'), ("Matériel chauffant utilisé",'Radiateur seul')], 
            [("Avez-vous un chauffage d'appoint ?", 'Non'), ('Montant de la facture', str(0)+'€'), ("Avez-vous un ballon d'eau chaude", 'Oui'), ("Capacité du ballon",str(200)+'L')],
            [("Hauteur sous plafond du local ballon", 'Inférieur à 2m20'), ('Puissance des panneaux solaire installés', str(0)+'Wc'), ("Votre type d'ampoule", 'Ampoule à incandescence + lampes à LED'), ("Ressources annuelles du foyer",str(29000)+'€')],
            [("Avez-vous bénéficié d'un crédit d'impôt ces  5 dernières années ?", 'Non'), ("Montant du crédit d'impôt", str(0)+'€'), ("Intéressé par", 'je ne sais pas encore'), ('','')], 
        ]
        tableau = generate_tableau(tab)

        return [subtitle_paragraph, space, img, space, titre_tableau, tableau]

    def selection_materiel():
        titre = Paragraph(f"B.SELECTION DE MATERIELS ET SERVICE", styles['Heading3'])
        img = Image('image2.jpg', width=pdf.width, height=0.3*pdf.height)

        ss_titre = Paragraph(f"1. Matériels et services", styles['Heading3'])
        souligne = Paragraph(f"Liste de matériels et services préconisé pour la rénovation", styles['BodyText'])
        content = "<div><ul>"
        for mat in ['Panneaux photovoltaïque', 'Compteur en monophasé', 'Micro onduleurs', 'Domotique', 'Ballon thermodynamique']:
            content += '<li>'+mat+'</li>'
        content += "</ul></div>"
        matos = Paragraph(content, styles['BodyText'])

        tab = [
            [("Heures d'ensoleillement", str(1190)+'h'), ("Puissance restituée", str(10620)+'kWh'), ("Coefficient météorologique", str(80)+'%')],
            [('Coefficient de performance', str(1.0)), ('Pertes du système', str(14)+'%'), ("Le coût du kWh", "Consommé : "+str(0.2308)+" €/kWh        Revendu : "+str(0.1339)+" €/kWh")]
        ]
        part_2 = part("2. Données techniques", "Les informations techniques", tab)
        
        tab = [
            [("Electricité", str(2243)+'€'), ("E.C.S/Chauffage", str(600)+'€')],
            [('Total Minimum / Mois', str(304)+'€'), ('Total Minimum N+1', str(3042)+'€')]
        ]
        part_3 = part("3. Les chiffres", "Gains et économies réalisés",tab)

        tab = [
            [("Economies sur l'indépendance", str(2300)+'€'), ("Economies du surplus", str(732)+'€')],
        ]
        part_4 = part("4. Transition énergétique", "Vous avez choisi l'autoconsommation", tab)

        # Pie Chart
        labels = ['Surplus', 'Indépendance']
        sizes = [20, 80]
        fig, ax = plt.subplots()
        wedgeprops = {'edgecolor': 'grey', 'linewidth': 2, 'antialiased': True}
        colors_pie = ['#6eb52f', "#e0e0ef", 'lightcoral']
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops=wedgeprops, colors=colors_pie)
        ax.axis('equal')  # Equal 
        chart_buffer = BytesIO()
        plt.savefig(chart_buffer, format='png')
        plt.close()
        chart_img = Image(chart_buffer, width=300, height=220)

        tab = [
            [("Indexation de", str(4)+'%/an'), ("Prévisions sur ", str(15)+'ans'), ("Total/Mois ", str(472)+'€'), ("Total/An ", str(4720)+'€'), ("Total des gains et économies sur 15 ans", str(79830)+'€')],
        ]
        part_5 = part("5. Prévisions", "Prévisions de l'évolution énergétique et de vos gains/économies", tab)

        tab = [
            [("Ma Prime Rénov", str(400)+'€'), ("Prime coup de pouce (CEE)", str(0)+'€'), ("Prime EDF", str(3420)+'€')],
            [("Récupération de la TVA", str(5536)+'€'), ("Déduciton des crédits d'impôts", str(0)+'€'), ('Total', str(8636)+'€')]
        ]
        part_6 = part("6. Les aides", "Les aides pour financer votre projet", tab)

        return [titre, img, ss_titre, souligne, matos, 
        part_2,  
        part_3,
        [[part_3], chart_img], 
        part_5, part_6
        ]

    def comparaison():
        # Titre
        subtitle_paragraph = Paragraph(f"<i>C. COMPARAISON</i>", styles['Heading1'])

        # Image
        height_prct = 0.3
        image_path = 'image2.jpg'
        img = Image(image_path, width=pdf.width, height=height_prct*pdf.height)

        space = Spacer(10, 10)

        diag = Paragraph(f"Diagnostic indicatif réalisé selon les dépenses énergétiques liées au chauffage et à l'eau chaude sanitaire. Ce diagnostic établit ci-dessous ne peut se substituer à un DPE réalisé par un bureau d'étude.", styles['BodyText'])

        tab = [
            [('Avant',''), ('Après', '')],
            [('Consommation électrique', str(8959)+'kWh'), ('Nouvelle consommation électrique', str(7453)+'kWh')],
            [('Facture électrique actuelle', str(1800)+'€'), ('Nouvelle facture électricité gaz/fioul', str(1290)+'€')],
            [('Facture gaz/fioul actuelle', str(1800)+'€'), ('', '')],
            [('Production solaire', str(0)+'kWh'), ('Nouvelle production solaire', str(10620)+'kWh')],
            [("Economies sur l'indépendance", str(0)+'€'), ("Nouvelle économies sur l'indépendance", str(2310)+'€')],
            [("Revente de surplus", str(0)+'€'), ("Nouvelle revente de surplus", str(730)+'€')],
            [("Total des dépenses d'énergies", str(3600)+'€/an'), ("Total économies + gains", str(3042)+'€/an')],
        ]
        part_1 = part("1. Résumé énergétique", "Comparaison de votre projet avant et après", tab)

        tab_2 = [
            [('',''), ('AVANT',''), ('APRES','')],
            [('Catégorie énergie', ''), ('', str('B52')), ('', str('A26'))],
            [('Catégorie climat', ''), ('', str('E8')), ('', str('A4'))],
            [('Valeur du bien immobilier', ''), ('', str(9)+'%'), ('', str(8)+'%')]
        ]
        part_2 = part("", "Comparaison sur la valeur immobilière", tab_2)

        return [subtitle_paragraph, img, space, diag, part_1, part_2]

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    items0 = page_couverture()
    items1 = but_document()
    items2 = caracteristique_habitat()
    items3 = selection_materiel()
    items4 = comparaison()

    items = items0+items1+items2+items3+items4
    data = [[item] for item in items]

    # Ajouter le tableau au PDF
    table_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    table = Table(data, colWidths=[pdf.width]) ###### ajuster qchose ici pour avoir plusieurs colonnes
    table.setStyle(table_style)

    # Construction finale du PDF
    pdf.build([table])

    buffer.seek(0)
    return buffer

def display_generated_audit():
    
    # Générer le PDF
    #if st.button("Générer le PDF"):
    pdf_buffer = generate_pdf_audit()

    pdf_data = pdf_buffer.read()
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display
    st.markdown(pdf_display, unsafe_allow_html=True)
