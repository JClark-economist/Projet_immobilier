"""
Librairie contenant les fonctions permettant de réaliser la partie construction des modèles et sélection.

- Par manque de temps il reste les tests à faire
"""

from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler, Normalizer, RobustScaler, StandardScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
import numpy as np
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import pickle 

def variables_X(df,colonne_a_numeriser,colonnes_deja_numeriques):
	"""Transforme les colonnes non numériques en colonnes numériques et sélectionne les colonnes utilisées pour construire les modèles (X)"""
	ct=ColumnTransformer([
			("Gestion Adresse", 
			Pipeline([
					("Numérisation", OneHotEncoder(sparse=False))
    
			]), 
			colonne_a_numeriser
			),
		(
			"Colonnes déja numériques",
			MinMaxScaler(),
			colonnes_deja_numeriques
		)
	])
	X=ct.fit_transform(df)
	print(X.shape)
	return X


def modeles_regression(param_lasso,param_ridge,param_elast1,param_elast2,nb_neighbors,n_estimators_RForest):
	"""Liste les modèles à utiliser pour l'entrainement, prend en entrée quelques hyperparamètres"""
	modeles= list()
	# Lasso
	for val_alpha in param_lasso:
		modeles.append(Lasso(alpha=val_alpha))
	# Ridge
	for val_alpha in param_ridge:
		modeles.append(Ridge(alpha=val_alpha))    
	# Elastic Network
	for val_alpha in param_elast1:
		for val_l1 in param_elast2:
			modeles.append(ElasticNet(alpha=val_alpha, l1_ratio=val_l1))    
	# KNRegressor
	for nb_voisins in nb_neighbors:
		modeles.append(KNeighborsRegressor(n_neighbors=nb_voisins))
	# SVR
	for val_epsilon in (10 ** n for n in range(-3, 1)):
		for val_C in (10 ** n for n in range(-3, 4)):
			modeles.append(SVR(epsilon=val_epsilon, C=val_C))    
	# Forêts aléatoires
	for nb_estimateurs in n_estimators_RForest:
		modeles.append(RandomForestRegressor(n_estimators=nb_estimateurs,n_jobs=4))
	return modeles


def modeles_sur_train(modeles,X_tr,y_tr,cross_validation,hors_presentation):
	"""Entraine les modèles sur les données train, avec cross validation. Retourne un dictionaire avec les scores de la cross validation par modèle"""
	if hors_presentation==True:# si on veut afficher les warnings dans le cadre de la préparation de la présentation
		resultats = dict()
		for modele in modeles:
			resultats[modele] = cross_val_score(modele, X_tr, y_tr, cv=cross_validation)	
		resultats_pour_tri= sorted([(scores.mean(),np.median(scores), scores.std(), repr(modele)) for modele, scores in resultats.items()], reverse=True)
		meilleurs_modeles=[]
		for moyenne, mediane, ecart_type, nom_modele in resultats_pour_tri:
			print(f"{nom_modele:45} {moyenne:4.3} {mediane:4.3} {ecart_type:6.5}")
		return resultats
	else:
		warnings.simplefilter("ignore")
		resultats = dict()
		for modele in modeles:
			resultats[modele] = cross_val_score(modele, X_tr, y_tr, cv=5)	
		resultats_pour_tri= sorted([(scores.mean(),np.median(scores), scores.std(), repr(modele)) for modele, scores in resultats.items()], reverse=True)
		meilleurs_modeles=[]
		for moyenne, mediane, ecart_type, nom_modele in resultats_pour_tri:
			print(f"{nom_modele:45} {moyenne:4.3} {mediane:4.3} {ecart_type:6.5}")
		return resultats
	
def visualisation_des_scores(scores,nombres_de_modeles_a_visualiser):
	"""Crée des boites à moustaches pour visualiser les résultats des cross validations sur les modèles selectionés classés dans l'ordre (du meilleur au pire)"""
	df=pd.DataFrame(scores)
	df=df.reindex(df.mean().sort_values(ascending=False).index, axis=1)
	df=df[df.columns[0:nombres_de_modeles_a_visualiser]]
	df=df.reindex(df.mean().sort_values(ascending=True).index, axis=1)
	df.boxplot(vert=False)

def score_meilleur_modele_sur_donnees_test(meilleur_modele,X_tr,y_tr,X_te,y_te):
	"""Renvoie le score du modèle selectioné lors de l'entrainement et du test"""
	scores_train=cross_val_score(meilleur_modele,X_tr,y_tr,cv=5)
	scores_train_mean=scores_train.mean()
	meilleur_modele.fit(X_tr, y_tr)
	print(f"Score test : {meilleur_modele.score(X_te, y_te):4.3}")
	print(f"Moyenne score train : {scores_train_mean:4.3}")

def sauvergarder_le_modele(nom_modele,modele_a_sauvegarder):
	"""Sauvergarde le modèle entrainé dans un fichier .pkl, pour une réutilisation sans avoir besoin de le ré entrainer"""
	pkl_filename = nom_modele+".pkl"
	with open(pkl_filename, 'wb') as file:
		pickle.dump(modele_a_sauvegarder, file)

def ouvrir_le_modele(nom_modele):
	"""Ouvrir le modèle séléctionné"""
	with open(nom_modele+".pkl", 'rb') as file:
		return pickle.load(file)