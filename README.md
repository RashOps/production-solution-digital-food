# Food Characteristics Retriever

## Description

Ce projet est une application Python qui permet de récupérer les caractéristiques nutritionnelles des aliments (calories, protéines, glucides, lipides) en scrapant le site web infocalories.fr. Il offre deux interfaces : une application web interactive utilisant Streamlit et un script en ligne de commande.

## Fonctionnalités

- Recherche d'aliments par nom
- Récupération automatique des données nutritionnelles
- Interface web intuitive avec Streamlit (avec sidebar, historique et graphiques)
- Visualisation graphique des nutriments (barres)
- Export des données en CSV directement depuis l'interface
- Script CLI pour utilisation en ligne de commande
- Sauvegarde des données en CSV
- Tests unitaires

## Bibliothèques utilisées

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![Requests](https://img.shields.io/badge/Requests-2.0+-green.svg)](https://requests.readthedocs.io/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.0+-orange.svg)](https://www.crummy.com/software/BeautifulSoup/)
[![Pandas](https://img.shields.io/badge/Pandas-1.0+-blue.svg)](https://pandas.pydata.org/)

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone <url-du-repo>
   cd tp-food
   ```

2. Créez un environnement virtuel :
   ```bash
   python -m venv .venv
   ```

3. Activez l'environnement virtuel :
   - Sur Windows :
     ```bash
     .venv\Scripts\activate
     ```
   - Sur macOS/Linux :
     ```bash
     source .venv/bin/activate
     ```

4. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Interface Web (Streamlit)

Lancez l'application web :
```bash
streamlit run main.py
```

Ouvrez votre navigateur à l'adresse indiquée (généralement http://localhost:8501). L'interface offre :
- Une recherche d'aliments avec validation d'entrée
- Affichage des métriques nutritionnelles
- Graphique en barres pour la répartition des nutriments
- Historique des recherches dans la sidebar
- Export des données en CSV
- Indicateur visuel pour les aliments gras/non gras

### Script en Ligne de Commande

Utilisez le script CLI :
```bash
python get_food.py -f "nom_de_l_aliment"
```

Par exemple :
```bash
python get_food.py -f pomme
```

Les données seront affichées dans la console et sauvegardées dans `food.csv`.

## Déploiement

L'application est déployée en ligne et accessible via Streamlit Cloud :

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_on_white.svg)](https://projet-solution-digital-food.streamlit.app/)

## Structure du Projet

- `main.py` : Application Streamlit
- `food.py` : Classe Food avec logique de récupération des données
- `food_index.py` : Index des aliments pour la recherche
- `get_food.py` : Script CLI
- `test_food.py` : Tests unitaires
- `scraping_lab.py` : Laboratoire de scraping
- `food.csv` : Données des aliments

## Tests

Lancez les tests :
```bash
python -m unittest test_food.py
```