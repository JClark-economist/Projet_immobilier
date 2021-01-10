# Projet immobilier

Ce projet, réalisé dans le cadre du cours **Machine Learning** de Professeur Vincent Perrollaz en M2 Mécen, est mon premier projet de webscraping. Ce projet a pour but d'utiliser les techniques de webscraping et d'application des algorithmes ML acquises lors du cours en plus des techniques d'analyse statistique avancées.

## Objectifs

* Recenser le maximum d'offres postées sur les principaux sites immobiliers de la Côte d'Ivoire et du Sénégal à une date donnée (l'extraction pourra s'étaler sur quelques jours ou quelques semaines). Les données seront extraites par une technique de web-scraping utilisant Python ou une autre technologie adaptée. Les données devront contenir les informations suivantes : la surface, le lien Internet de l'annonce, l'adresse, la ville, la région, le prix, la surface (du logement, pas celle du terrain s'agissant des maisons), le nombre de pièces, le descriptif de l'annonce, la mention du caractère ancien ou neuf du logement qu'on pourra signaler par "N" ou "A", la nature du bien (maison, appartement...). Si des frais ou des taxes sont inclus et identifiables, ils devront idéalement être mentionnés ;
* **Problématique :** Identifier les meilleurs investissements locatifs ;
* **Modélisation :** Utiliser un prédicteur de prix au mètre carré pour les biens locatifs et un autre prédicteur pour les achats. Pour un nouveau bien ayant des caractéristiques déterminées trouver le rendement en pourcentage à l'année.

## Composition du repositoire

### Rendu projet

Cette partie du repositoire contient la présentation finale et les modules qui ont servis d'une part à l'extraction et d'autre part au nettoyage des données utilisées. La présentation contient aussi la phase d'analyse et de construction, vérification et choix des modèles.

### La phase de scraping

La phase de scraping a été réalisée à l'aide de deux notebook et d'un dossier contenant des fichiers `.py` :

* `scraping_senegal.py` : contient le scraping réalisé sur les deux plus gros sites d'immobilier au Sénégal, **senegalcity.com**, **1000-annonces.sn** et **deals.jumia.sn** ;
* `scraping_ci.py` : contient le scraping réalisé sur le plus gros site d'immobilier en Côte d'ivoire, **deals.jumia.ci** ;
* `Essai_scrapy` : au vu de la lenteur de `selenium` (pour récupérer un total de 120 000 données), pour accélérer le processus j'ai tenté de commencer à utiliser `scrapy` avec `PostgreSQL` mais par manque de temps je n'ai pas pu développer cette solution.

### La phase de nettoyage

* `nettoyage_senegal.py` : contient les fonctions utilisées pour le nettoyage des deux bases de données pour le Sénégal ;
* `nettoyage_cote_ivoire.py` : contient les fonctions utilisées pour le nettoyage des quatres bases de données pour la Côte d'Ivoire.

