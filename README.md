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
- Un dossier contenant des scripts utilisés dans l'ensemble du projet, avec des sous-dossiers selon la tache réalisée:
    * preprocessor: Preprocessing avec Spark (+ Pipeline dans global_processor)
    * scraper: Fonctions de webscraping + projet Scrapy( plus adapté pour notre projet)
    * viz: Fonctions pour faire des graphes pour l'analyse exploratoire
- Un dossier comportant les notebooks: numérotés dans l'ordre d'exécution (webscraping => processing => eda)
- Une application Streamlit pour exposer les résultats de l'analyse
- Les artefacts ML pour l'app/prédiction

Normalement les notebooks sont complets, sinon les scripts des fonctions associées sont plutôt bien faits pour comprendre les actions réalisées (en anglais)


Dans un premier temps, nous effectuons une partie tournée "exploration des données" tandis que dans un second temps nous souhaitons privilégier la capacité de déploiement de ce projet.

### EDA
- Utilisation de techniques de web scraping pour récupérer les données tel que Selenium, BS4. Finalement, le package Scrapy sera choisi pour sa modularité et pour sa résilience aux problèmes de connexion.
-	Emploi de PySpark pour nettoyer les données et faire du feature engineering: traitement des types, de la géolocalisation des restaurants, mais surtout processing du texte issu des commentaires.
-	Nous réalisons une EDA (Exploratory Data Analysis) orientée NLP en analysant principalement les commentaires des utilisateurs (scores de polarité, analyse de sentiments, topic modelling éventuellement)

### Dev (en cours)
-	Nous adaptons les codes pour être orientés développement et créons une pipeline ETL Airflow qui interagit avec une base SQL.
-	Nous proposons le même type de contenu pour l'analyse précédente.
-	Nous généralisons notre approche à d'autres villes.

## Installation
Pour utiliser ce projet, vous devez clone ce repository en local et installer les requirements. Pour éviter tout problème de versions, nous vous conseillons de créer un environnement virtuel:
```
git clone https://github.com/luciegaba/sentiment-analysis-tripadvisor
conda create -n tripadvisor python=3.9
conda install pip # Si ce n'est pas le cas
pip install -r requirements.txt
```
Pour le notebook de processing vous avez deux alternatives: 
- Lancer depuis googlecolab ou en local en veillant à installer les élements suivants:
conda install pyspark


### Data

- Extraction des données: depuis le notebook webscraping ou en lançant la CL:
```
cd "scripts/scraper/scrapy_tripadvisor_scraper/tripadvisor_scraper"
scrapy crawl restaurants_urls_scraper
scrapy crawl reviews_scraper
```
Les données seront situées dans le dossier data à la racine du projet.

- Nettoyage des données: depuis le notebook processing () ou bien lancer dans Python (en étant à la racine du projet):
``` python
from scripts.preprocessor.global_processor import ProcessingPipeline
ProcessingPipeline("data/fetch_data.json").run_pipeline()

```
### Notebooks
-	Pour les notebooks, il vous suffit de les exécuter simplement. 
-	Il faudra vous assurer d'avoir le fichier fetch_data.json et clean_data.json pour que les notebooks de processing et d'eda fonctionnent (respectivement).

### Dev
Bientôt disponible. Le but était de faire un projet sur Aiflow en le connectant à une base SQL. Les prémices de ce travail sont disponibles dans dev mais n'ont pas pu été achevé!

### App

L'application a été déployée à l'adresse: https://luciegaba-sentiment-analysis-tripadvisor-appmain-njj9d8.streamlit.app/
En voici quelques previews:
![alt tag](https://github.com/luciegaba/sentiment-analysis-tripadvisor/blob/project_submission_french/visuals/Capture%20d%E2%80%99%C3%A9cran%202023-01-29%20%C3%A0%2017.03.38.png)

![alt tag](https://github.com/luciegaba/sentiment-analysis-tripadvisor/blob/project_submission_french/visuals/Capture%20d%E2%80%99%C3%A9cran%202023-01-29%20%C3%A0%2017.04.00.png)
Si vous souhaitez la déployer en local:
Il faut se positionner à la racine du projet et lancer:
```
streamlit run main/app.py
```

## Contact
* [Lucie Gabagnou👸](https://github.com/luciegaba) - Lucie.Gabagnou@etu.univ-paris1.fr
* [Yanis Rehoune👨‍🎓](https://github.com/Yanisreh) - Yanis.Rehoune@etu.univ-paris1.fr
