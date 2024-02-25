import streamlit as st
import pdfkit
import os
import sys
from audit_html import * 
from rapport_financier_html import *
from pac_html import *
from pvgis_html import pvgis_html
import base64
    
def generer_un_pdf(dic, nom):
    cwdir = os.getcwd()
    file_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_dir)

    if nom == 'audit':
        output_pdf_path = 'audit.pdf'
        html_string = audit_string_html(dic)
    elif nom=='rapport_financier':
        output_pdf_path = 'rapport.pdf'
        html_string = rapport_string_html(dic)
    elif nom=='pvgis':
        output_pdf_path = 'pvgis.pdf'
        html_string = pvgis_html(dic)
    else:
        output_pdf_path = 'pac.pdf'
        html_string = pac_string_html(dic)

    if os.getcwd()[9:14]=='arthu':
        path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path)
    else:
        path = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),'wkhtmltopdf'),'bin'),'wkhtmltopdf.exe')
        config = pdfkit.configuration()

    pdf = pdfkit.from_string(html_string, output_path=False, configuration=config, options={"enable-local-file-access": ""})
    
    with open(output_pdf_path, "wb") as file:
        file.write(pdf)
    output_path = os.path.join(os.getcwd(),output_pdf_path)

    os.chdir(cwdir)
    return output_pdf_path

def generer_les_2_pdf(dic):
    audit_path = generer_un_pdf(dic,'audit')
    rapport_path = generer_un_pdf(dic,'rapport_financier')
    return audit_path, rapport_path

def generer_pac_pdf(dic):
    pac_path = generer_un_pdf(dic,'pac')
    return pac_path

def generer_pvgis(dic):
    pvgis_path = generer_un_pdf(dic,'pvgis')
    return pvgis_path


def test_pr_generer_le_pdf(nom):
    path_functions = os.path.dirname(os.path.dirname(__file__)) # dir de SolarSales
    sys.path.insert(0,path_functions)
    from functions import displayPDF_basse_resol

    dic={}
    audit_path = generer_un_pdf(dic,nom)
    displayPDF_basse_resol(audit_path, 500, 500)
