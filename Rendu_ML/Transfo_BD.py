"""
Librairie contenant les fonctions permettant de nettoyer les données brutes.

- Par manque de temps il reste des tests à faire
"""

import itertools
import pandas as pd
import base64
import re
import numpy as np

def __produit_df_test():
    df = pd.read_csv('Test_nettoyage.csv')
    return df

def suppression_annonces_redondantes(df: pd.DataFrame) -> pd.DataFrame:
    """Enleve les lignes en doubles."""
    df=df.drop_duplicates()
    # Il existe des annonces postées deux fois à des dates différentes qui sont donc les mêmes mais n'ont
    # pas le même lien
    df=df.drop_duplicates(subset=['Prix','Description'])
    return df
def _verifie_suppression_annonces_redondantes() -> bool:
	"""Vérifie la fonction précédente"""
	entree = __produit_df_test()
	resultat = suppression_annonces_redondantes(entree)
	if (resultat.duplicated()==False).all:
		return True
	elif (resultat.duplicated(subset=['Prix','Description'])==False).all:
		return False
	else:
		return True

def transfo_data(df: pd.DataFrame) -> pd.DataFrame:
    """Rajoute les données à rajouter et supprime les données inutiles"""       
    df['Nb_pieces']=df.Nb_pieces_Surface_m2.str.extract(r'ces\n(\d*)|\nSur')
    df['Surface_m2']=df.Nb_pieces_Surface_m2.str.extract(r'icie\n(\d*)')
    df['Adresse'] = df.Adresse.str.extract(r'Lieu\n(.*)\nPub')
    df.replace(to_replace=r'^$', value=None, regex=True)
    return df 


def ajout_colonnes(df: pd.DataFrame) -> pd.DataFrame:
    """Recherche et ajout des informations suivantes (par regex)"""
    df['Meuble']=df.Description.str.extract(r'.*(meuble|meublé).*', flags=re.IGNORECASE)
    df['Meuble'] = df['Meuble'].fillna(0)
    df['Condition']=df.Description.str.extract(r'.*(neuf|neuve|nouveau|nouvel).*', flags=re.IGNORECASE)
    df['Condition'] = df['Condition'].fillna(0)
    df['Piscine']=df.Description.str.extract(r'.(piscine).', flags=re.IGNORECASE)
    df['Piscine'] = df['Piscine'].fillna(0)
    return df
def _verifie_ajout_colonnes() -> bool:
    """Vérifie la fonction précédente"""
    ...

def numerise_les_colonnes(df: pd.DataFrame) -> pd.DataFrame:
    """Convertit les colonnes en numérique"""
    def filtre(col_a_numeriser):
        if col_a_numeriser!=0:
            return 1
        else:
            return 0
        
    resultat = df.copy()
    resultat.Condition = resultat.Condition.apply(filtre)
    resultat.Meuble = resultat.Meuble.apply(filtre)
    resultat.Piscine= resultat.Piscine.apply(filtre)
    return resultat
def _verifie_numerise_les_colonnes() -> bool:
    """Vérifie la fonction précédente"""
    ...


def transfo_ML(df):
    """Supprime les colonnes inutiles"""
    df=df.drop(['Title','Links','Description','Nb_pieces_Surface_m2','Pays','Ville','Nature_annonce','Currency'], axis=1)
    return df
def _verifie_transfo_ML() -> bool:
	"""Vérifie la fonction précédente"""
	entree = __produit_df_test()
	resultat = transfo_ML(entree)
	liste_de_colonnes_a_ne_pas_avoir=['Title','Links','Description','Nb_pieces_Surface_m2','Pays','Ville','Nature_annonce','Currency']
	liste_noms_colonnes=list(resultat)
	for nom_a_ne_pas_avoir in liste_de_colonnes_a_ne_pas_avoir:
		for nom in liste_noms_colonnes:
			if nom_a_ne_pas_avoir==nom:
				return False
			else:
				return True
	

def conversion_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convertit les object en string et les colonnes Nb_pieces et Surface_m2 en numeric"""
    df['Nb_pieces'] = pd.to_numeric(df['Nb_pieces'])
    df['Surface_m2'] = pd.to_numeric(df['Surface_m2'])
    df=df.convert_dtypes()
    return df
def _verifie_conversion_types() -> bool:
    """Vérifie la fonction précédente"""
    entree = __produit_df_test()
    resultat = conversion_types(entree).dtypes.apply(type)
    en_theorie = pd.Series(
        index=["Prix","Adresse","Type_de_bien","Nb_pieces",	"Surface_m2","Meuble","Condition","Piscine","Titre_foncier"	,"Prix_m2"],
        data=[pd.Int64Dtype, pd.StringDtype, pd.Int64Dtype,  pd.Int64Dtype, pd.Int64Dtype, pd.Int64Dtype, pd.Int64Dtype,pd.Int64Dtype,pd.Int64Dtype,np.dtype]
    )
    return (resultat == en_theorie
    ).all()

def selection_m2(df: pd.DataFrame)->pd.DataFrame:
	"""Selectionne les lignes où l'information surface est disponible, calcule la colonne prix au mètre carré supprime la colonne prix"""
	df=df.dropna(axis=0, subset=["Surface_m2", "Nb_pieces", "Prix"])
	df=df[df.Surface_m2>10]
	df=df[df.Surface_m2<1000]
	df=df[df.Prix>10000]
	df['Prix_m2']=df['Prix']/df['Surface_m2']
	return df
def _verifie_selection_m2() -> bool:
	"""Vérifie la fonction précédente"""
	entree = __produit_df_test()
	resultat = selection_m2(entree)
	if (resultat.Surface_m2.value<=10).all:
		return False
	elif (resultat.Surface_m2.value>=1000).all:
		return False
	elif (pd.isna(resultat["Surface_m2", "Nb_pieces", "Prix"])==True).all:
		return False
	else:
		return True
	
	
def numerise_la_colonne_type_de_bien(df: pd.DataFrame) -> pd.DataFrame:
    """Convertit les colonnes en numérique"""
    def filtre(col_a_numeriser):
        if col_a_numeriser=='Maison':
            return 1
        else:
            return 0
        
    resultat = df.copy()
    resultat.Type_de_bien= resultat.Type_de_bien.apply(filtre)
    return resultat	
def _verifie_numerise_la_colonne_type_de_bien() -> bool:
    """Vérifie la fonction précédente"""
    ...


def ajout_colonnes_ventes(df: pd.DataFrame) -> pd.DataFrame:
    """Recherche et ajout des informations suivantes pour les ventes (par regex)"""
    df['Titre_foncier']=df.Description.str.extract(r'.*(titre foncier|titres foncier|titrefoncier|titresfoncier).*', flags=re.IGNORECASE)
    df['Titre_foncier'] = df['Titre_foncier'].fillna(0)
    return df
def _verifie_ajout_colonnes_ventes() -> bool:
    """Vérifie la fonction précédente"""
    ...

def numerise_les_colonnes_ventes(df: pd.DataFrame) -> pd.DataFrame:
    """Convertit les colonnes en numérique"""
    def filtre(col_a_numeriser):
        if col_a_numeriser!=0:
            return 1
        else:
            return 0
        
    resultat = df.copy()
    resultat.Titre_foncier = resultat.Titre_foncier.apply(filtre)
    return resultat
def _verifie_numerise_les_colonnes_ventes() -> bool:
    """Vérifie la fonction précédente"""
    ...


if __name__ == "__main__":
    assert _verifie_suppression_annonces_redondantes()
    assert _verifie_transfo_data()
    assert _verifie_ajout_colonnes()
    assert _verifie_numerise_les_colonnes()
    assert _verifie_numerise_les_colonnes_ventes()
    assert _verifie_transfo_ML()
    assert _verifie_conversion_types()
    assert _verifie_selection_m2()
    assert _verifie_numerise_la_colonne_type_de_bien()