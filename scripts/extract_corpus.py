"""
Ce script permet de scrapper le web à partir d'un URL de film donné. Il récupère les critiques ainsi que les notes qui y sont associées. 
Il permet également de classer les notes au-dessus de 5 de manière positive et celles en dessous de 5 de manière négative. 
Ce script enregistrera les données dans un fichier CSV.
Ce script requiert l'installation de Pandas, Requests ainsi que de BeautifulSoup.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL du site à scraper
url_base = 'https://www.imdb.com/title/tt1517268/reviews/?ref_=tt_ov_rt'

def classer_note(note):
    """
    Classe une note en fonction de sa valeur.
    
    Parameters
    ----------
    note : str
        La note sous forme de chaîne de caractères.
    
    Returns
    -------
    str
        'pos' si la note est supérieure ou égale à 5, 'neg' si la note est inférieure à 5, et ' ' en cas d'erreur.
    """
    try:
        valeur_note = int(note)
        if valeur_note >= 5:
            return 'pos'
        else:
            return 'neg'
    except (ValueError, TypeError):
        return ' '

def recup_reviews(url):
    """
    Récupère les critiques et les notes associées à partir de l'URL donné.
    
    Parameters
    ----------
    url : str
        L'URL de la page à scraper.
    
    Returns
    -------
    list
        Une liste de dictionnaires contenant les critiques et les notes.
    """
    resultat = requests.get(url)
    soup = BeautifulSoup(resultat.text, 'html.parser')
    reviews = []
    review_blocks = soup.find_all('div', class_='review-container')
    
    for block in review_blocks:
        review = block.find('div', class_='text show-more__control').text
        try:
            note = block.find('span', class_='rating-other-user-rating').find('span').text
        except AttributeError:
            note = None
        
        reviews.append({'review': review, 'note': note})
    return reviews

# Récupérer les critiques
reviews_data = recup_reviews(url_base)

# Convertir en DataFrame
reviews_df = pd.DataFrame(reviews_data)

# Ajouter une colonne label en classant les notes
reviews_df['label'] = reviews_df['note'].apply(classer_note)

# Sauvegarder dans un fichier CSV
reviews_df.to_csv('film_reviews.csv', index=False)

print('Sauvegarde effectuée')
