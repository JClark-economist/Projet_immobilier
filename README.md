# Projet immobilier

Ce projet, réalisé dans le cadre du cours **Machine Learning** de Professeur Vincent Perrollaz en M2 Mécen, est mon premier projet de webscraping. Ce projet a pour but d'utiliser les techniques de webscraping acquises lors du cours en plus des techniques d'analyse statistique avancées.

## Objectifs

* Recenser le maximum d'offres postées sur les principaux sites immobiliers de la Côte d'Ivoire et du Sénégal à une date donnée (l'extraction pourra s'étaler sur quelques jours ou quelques semaines). Les données seront extraites par une technique de web-scraping utilisant Python ou une autre technologie adaptée. Les données devront contenir les informations suivantes : la surface, le lien Internet de l'annonce, l'adresse, la ville, la région, le prix, la surface (du logement, pas celle du terrain s'agissant des maisons), le nombre de pièces, le descriptif de l'annonce, la mention du caractère ancien ou neuf du logement qu'on pourra signaler par "N" ou "A", la nature du bien (maison, appartement...). Si des frais ou des taxes sont inclus et identifiables, ils devront idéalement être mentionnés.
* Récupérer le prix au mètre carré des biens locatifs et l'analyser et prédire les facteurs de variation de ce prix.

## Composition du repositoire

### La phase de scraping

La phase de scraping a été réalisée à l'aide de deux notebook et d'un dossier contenant des fichiers `.py` :

* `Scraping_senegal.ipynb` : contient le scraping réalisé sur les deux plus gros sites d'immobilier au Sénégal, **senegalcity.com** et **1000-annonces.sn**;
* `Scraping_cote_ivoire.ipynb` : contient le scraping réalisé sur le plus gros site d'immobilier en Côte d'ivoire, **jumia.ci**;
* `Essai_scrapy` : au vu de la lenteur de `selenium` (pour récupérer un total de 120 000 données), pour accélérer le processus j'ai tenté de commencer à utiliser `scrapy` avec `PostgreSQL` mais par manque de temps je n'ai pas pu le développer cette solution.

### La phase de nettoyage

* `Nettoyage_senegal.py` : contient les fonctions utilisées pour le nettoyage des deux bases de données pour le Sénégal;
* `Nettoyage_cote_ivoire.py` : contient les fonctions utilisées pour le nettoyage des quatres bases de données pour la Côte d'Ivoire.

### La phase d'analyse

* `Prix_locatif_immobilier.ipynb` : 
