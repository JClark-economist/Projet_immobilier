"""
Librairie contenant les fonctions permettant de scraper les données sur deals.jumia.ci.

- Par manque de temps il reste les tests à faire
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from requests import get
import itertools
import pandas as pd
import base64
import time
import re

def get_links_jumia(start_page,start_url,pages):
    '''fonction utilisée pour récupérer les liens des annonces'''
    driver = webdriver.Chrome()
    liste_liens=[]
    for current_page in list(range(pages)):
        driver.get(start_url+str(start_page+current_page))# pour tourner les pages
        panel_annonce=driver.find_element_by_id("search-results")
        annonces = panel_annonce.find_elements_by_class_name("announcement-container")
        for annonce in annonces:
            liste_liens.append(annonce.find_element_by_css_selector('a').get_attribute('href'))
    driver.quit()
    liste_liens = list(set(liste_liens))
    return liste_liens 

def enregistrer_liste_liens(nom_du_fichier,liste_liens):
	"""fonction utiliser pour génerer un fichier texte avec les liens récupérés"""
	f = open(str(nom_du_fichier)+'.txt', 'w' )
	f.write(repr(liste_liens) )
	f.close()
	return "Fichier "+str(nom_du_fichier)+".txt enregistré."

def get_annonces_jumia_ventes_maisons(liste_liens):
    """Scraping des ventes de maisons (46 000 annonces)"""
    driver = webdriver.Chrome()
    data={}
    df=pd.DataFrame(columns=['Links','Title','Nature_annonce','Prix','Currency','Adresse','Ville','Pays','Nb_pieces_Surface_m2','Type_de_bien','Description'])
    for lien in liste_liens:
        driver.get(lien)# pour accéder à l'offre
        try:
            panel_annonce=driver.find_element_by_id("main-holder")# contenu de chaque annonce
        except:
            panel_annonce=None
        try:
            data['Title']=panel_annonce.find_element_by_class_name('heading-area').text
        except:
            data['Title']=None
        try:
            pieces_surface_descr=panel_annonce.find_element_by_class_name('post-content')
        except:
            pieces_surface_descr=None
        try:
            data['Description']=pieces_surface_descr.find_element_by_css_selector('div.post-text-content > p').text
        except:
            data['Description']=None
        try:
            data['Nb_pieces_Surface_m2']=pieces_surface_descr.find_element_by_class_name('new-attr-style').text
        except:
            data['Nb_pieces_Surface_m2']=None
        try:
            prix_adresse=panel_annonce.find_element_by_id('priceSection')
        except:
            prix_adresse=None
        try:
            prix_currency=prix_adresse.find_element_by_class_name('price')
        except:
            prix_currency=None
        try:
            data['Prix']=prix_adresse.find_element_by_css_selector('span > span:nth-child(1)').get_attribute('content')
        except:
            data['Prix']=None
        try:
            data['Currency']=prix_adresse.find_element_by_css_selector('span > span:nth-child(2)').get_attribute('content')
        except:
            data['Currency']=None
        data['Links']=lien
        data['Ville']='Abidjan'
        data['Pays']='Côte d\'Ivoire'
        data['Type_de_bien']='Maison'
        data['Nature_annonce']='Vente'
        try:
            data['Adresse']=prix_adresse.find_element_by_css_selector('div').text
        except:
            data['Adresse']=None
        df=df.append(data,ignore_index=True)
    driver.quit()
    return df 

def get_annonces_jumia_ventes_appart(liste_liens):
    """ scraping des ventes d'appartements (6 800 annonces) """
    driver = webdriver.Chrome()
    data={}
    df=pd.DataFrame(columns=['Links','Title','Nature_annonce','Prix','Currency','Adresse','Ville','Pays','Nb_pieces_Surface_m2','Type_de_bien','Description'])
    for lien in liste_liens:
        driver.get(lien)# pour accéder à l'offre
        try:
            panel_annonce=driver.find_element_by_id("main-holder")# contenu de chaque annonce
        except:
            panel_annonce=None
        try:
            data['Title']=panel_annonce.find_element_by_class_name('heading-area').text
        except:
            data['Title']=None
        try:
            pieces_surface_descr=panel_annonce.find_element_by_class_name('post-content')
        except:
            pieces_surface_descr=None
        try:
            data['Description']=pieces_surface_descr.find_element_by_css_selector('div.post-text-content > p').text
        except:
            data['Description']=None
        try:
            data['Nb_pieces_Surface_m2']=pieces_surface_descr.find_element_by_class_name('new-attr-style').text
        except:
            data['Nb_pieces_Surface_m2']=None
        try:
            prix_adresse=panel_annonce.find_element_by_id('priceSection')
        except:
            prix_adresse=None
        try:
            prix_currency=prix_adresse.find_element_by_class_name('price')
        except:
            prix_currency=None
        try:
            data['Prix']=prix_adresse.find_element_by_css_selector('span > span:nth-child(1)').get_attribute('content')
        except:
            data['Prix']=None
        try:
            data['Currency']=prix_adresse.find_element_by_css_selector('span > span:nth-child(2)').get_attribute('content')
        except:
            data['Currency']=None
        data['Links']=lien
        data['Ville']='Abidjan'
        data['Pays']='Côte d\'Ivoire'
        data['Type_de_bien']='Appartements'
        data['Nature_annonce']='Vente'
        try:
            data['Adresse']=prix_adresse.find_element_by_css_selector('div').text
        except:
            data['Adresse']=None
        df=df.append(data,ignore_index=True)
    driver.quit()
    return df 

def get_annonces_jumia_location_maisons(liste_liens):
    """Scraping des locations de maisons (56 000 annonces)"""
    driver = webdriver.Chrome()
    data={}
    df=pd.DataFrame(columns=['Links','Title','Nature_annonce','Prix','Currency','Adresse','Ville','Pays','Nb_pieces_Surface_m2','Type_de_bien','Description'])
    for lien in liste_liens:
        driver.get(lien)# pour accéder à l'offre
        try:
            panel_annonce=driver.find_element_by_id("main-holder")# contenu de chaque annonce
        except:
            panel_annonce=None
        try:
            data['Title']=panel_annonce.find_element_by_class_name('heading-area').text
        except:
            data['Title']=None
        try:
            pieces_surface_descr=panel_annonce.find_element_by_class_name('post-content')
        except:
            pieces_surface_descr=None
        try:
            data['Description']=pieces_surface_descr.find_element_by_css_selector('div.post-text-content > p').text
        except:
            data['Description']=None
        try:
            data['Nb_pieces_Surface_m2']=pieces_surface_descr.find_element_by_class_name('new-attr-style').text
        except:
            data['Nb_pieces_Surface_m2']=None
        try:
            prix_adresse=panel_annonce.find_element_by_id('priceSection')
        except:
            prix_adresse=None
        try:
            prix_currency=prix_adresse.find_element_by_class_name('price')
        except:
            prix_currency=None
        try:
            data['Prix']=prix_adresse.find_element_by_css_selector('span > span:nth-child(1)').get_attribute('content')
        except:
            data['Prix']=None
        try:
            data['Currency']=prix_adresse.find_element_by_css_selector('span > span:nth-child(2)').get_attribute('content')
        except:
            data['Currency']=None
        data['Links']=lien
        data['Ville']='Abidjan'
        data['Pays']='Côte d\'Ivoire'
        data['Type_de_bien']='Maison'
        data['Nature_annonce']='Location'
        try:
            data['Adresse']=prix_adresse.find_element_by_css_selector('div').text
        except:
            data['Adresse']=None
        df=df.append(data,ignore_index=True)
    driver.quit()
    return df 
	
def get_annonces_jumia_location_appartements(liste_liens):
    """scraping des locations d'appartements (58 000 annonces)"""
    driver = webdriver.Chrome()
    data={}
    df=pd.DataFrame(columns=['Links','Title','Nature_annonce','Prix','Currency','Adresse','Ville','Pays','Nb_pieces_Surface_m2','Type_de_bien','Description'])
    for lien in liste_liens:
        driver.get(lien)# pour accéder à l'offre
        try:
            panel_annonce=driver.find_element_by_id("main-holder")# contenu de chaque annonce
        except:
            panel_annonce=None
        try:
            data['Title']=panel_annonce.find_element_by_class_name('heading-area').text
        except:
            data['Title']=None
        try:
            pieces_surface_descr=panel_annonce.find_element_by_class_name('post-content')
        except:
            pieces_surface_descr=None
        try:
            data['Description']=pieces_surface_descr.find_element_by_css_selector('div.post-text-content > p').text
        except:
            data['Description']=None
        try:
            data['Nb_pieces_Surface_m2']=pieces_surface_descr.find_element_by_class_name('new-attr-style').text
        except:
            data['Nb_pieces_Surface_m2']=None
        try:
            prix_adresse=panel_annonce.find_element_by_id('priceSection')
        except:
            prix_adresse=None
        try:
            prix_currency=prix_adresse.find_element_by_class_name('price')
        except:
            prix_currency=None
        try:
            data['Prix']=prix_adresse.find_element_by_css_selector('span > span:nth-child(1)').get_attribute('content')
        except:
            data['Prix']=None
        try:
            data['Currency']=prix_adresse.find_element_by_css_selector('span > span:nth-child(2)').get_attribute('content')
        except:
            data['Currency']=None
        data['Links']=lien
        data['Ville']='Abidjan'
        data['Pays']='Côte d\'Ivoire'
        data['Type_de_bien']='Appartement'
        data['Nature_annonce']='Location'
        try:
            data['Adresse']=prix_adresse.find_element_by_css_selector('div').text
        except:
            data['Adresse']=None
        df=df.append(data,ignore_index=True)
    driver.quit()
    return df 	
