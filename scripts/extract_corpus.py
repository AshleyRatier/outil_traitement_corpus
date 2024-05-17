import pandas as pd
import requests
from bs4 import BeautifulSoup


# URL du site à scraper
url_base = 'https://www.imdb.com/title/tt1517268/reviews/?ref_=tt_ov_rt'


def classer_note(note):
    try:
        valeur_note = int(note)
        if valeur_note >= 5:
            return 'pos'
        else:
            return 'neg'
    except (ValueError, TypeError):
        return ' '
        
# Fonction pour récupérer les critiques
def recup_reviews(url):
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
    
reviews_data = recup_reviews(url_base)
reviews_df = pd.DataFrame(reviews_data)
reviews_df['label'] = reviews_df['note'].apply(classer_note)

# Sauvegarde dans un fichier CSV
reviews_df.to_csv('film_reviews.csv', index=False)

print('Sauvegarde effectuée')
