# Web-scraping et Analyse de sentiments sur Trip Advisor 


## Table of Contents

* [Avant-propos](#avant-propos)
* [Contenu du projet](#contenu)
  * [EDA](#eda)
  * [Dev](#dev)
* [Installation](#installation)
  * [Data](#data)
  * [Notebooks (pour EDA)](#notebooks)
  * [Dev](#dev)
* [Contact](#contact)

<br>

## Avant-propos
Ce projet vise à extraire les données des restaurants de Paris sur Trip Advisor, à les nettoyer et réaliser une EDA (analyse exploratoire de données). Pour cela, nous utiliserons différents élements vus en cours tels que les méthodes de Web-scraping (Selenium, BS4), PySpark, etc... 

## Contenu
Ce projet comprend :
- Un dossier contenant des scripts utilisés dans la première partie (scripts), avec des sous-dossiers selon la tache réalisée:
    * preprocessor: Preprocessing avec Spark
    * scraper: Fonctions de webscraping + projet Scrapy( plus adapté pour notre projet)
    * viz: Fonctions pour faire des graphes pour l'analyse exploratoire
- Un dossier comportant les notebooks: numérotés dans l'ordre d'exécution (webscraping => processing => eda)
- Un projet Airflow
- Une application Streamlit pour exposer les résultats de l'analyse.

Dans un premier temps, nous effectuons une partie tournée exploration des données tandis que dans un second temps nous souhaitons privilégier la capacité de déploiement de ce projet.

### EDA
- Utilisation de techniques de web scraping pour récupérer les données tel que Selenium, BS4. Finalement, le package Scrapy sera choisi pour sa modularité et pour sa résilience aux problèmes de connexion.
-	Emploi de PySpark pour nettoyer les données et faire du feature engineering: traitement des types, de la géolocalisation des restaurants, mais surtout processing du texte issu des commentaires.
-	Nous réalisons une EDA (Exploratory Data Analysis) orientée NLP en analysant principalement les commentaires des utilisateurs (scores de polarité). Cette analyse sera étendue en système de recommandation par la suite.

### Dev
-	Nous adaptons les codes pour être orientés développement et créons une pipeline ETL Airflow qui interagit avec une base SQL.
-	Nous proposons le même type de contenu pour l'analyse précédente.
-	Nous généralisons notre approche à d'autres villes.

## Installation
Pour utiliser ce projet, vous devez clone ce repository en local et installer les requirements.
Pour le notebook de processing vous avez deux alternatives: 
- Lancer depuis googlecolab ou en local en veillant à installer les élements suivants:
conda..
python  3.9


### Data

- Extraction des données: depuis le notebook webscraping ou en lançant la CL:
```
cd "scripts/scraper/scrapy_tripadvisor_scraper/tripadvisor_scraper"
scrapy crawl restaurants_urls_scraper
scrapy crawl reviews_scraper
```
Les données seront situées dans le dossier data à la racine du projet.

- Nettoyage des données: depuis le notebook processing () ou bien lancer le script global_processor...
### Notebooks
-	Pour les notebooks, il vous suffit de les exécuter simplement. Remarque : le notebook qui concerne le preprocessing ne peut être exécuté exclusivement sur Google Colab pour l'instant (car utilisation de Pyspark).
-	Il faudra vous assurer d'avoir le fichier fetch_data.json et clean_data.json pour que les notebooks de processing et d'eda fonctionnent (respectivement).

### Dev
Bientôt disponible.


## Contact
* [Lucie Gabagnou👸](https://github.com/luciegaba) - Lucie.Gabagnou@etu.univ-paris1.fr
