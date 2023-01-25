import spacy
import os
from unidecode import unidecode
import nltk
import re

os.system("python -m spacy download fr_core_news_md")
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nlp = spacy.load("fr_core_news_md")

def clean_text_sentiment_analysis(reviews, spacy_conf='fr_core_news_md'):
    """
    Cleans text for sentiment analysis by applying lowercasing, removing special characters and digits, stopwords, lemmatization and named entities removal.
    
    Parameters:
    reviews (list): List of text reviews
    spacy_conf (str): spaCy model to use for lemmatization and named entities removal. Default is 'fr_core_news_md'.
    
    Returns:
    list: List of cleaned text reviews list.
    """

    def extract_score(text: str) -> float:
        """
        Extracts the score from a given text, converts it to a float, and divides it by 10.
        If no score is found, returns None.
        The score as a float, divided by 10 
        """
        score = re.findall(r'bubble_(\d+)', text)
        if score:
            return int(score[0])/10
        else:
            return None


    nlp = spacy.load(spacy_conf)
    cleaned_reviews = []
    reviews_ratings = []
    for review in reviews:
        rating=extract_score(review)       
        text = review.lower()    # Convert all letters to lowercase
        text = unidecode(text)   # Remove accent characters
        stop_words = set(nltk.stopwords.words("french"))
        text = " ".join([word for word in text.split() if word not in stop_words])
        doc = nlp(text) # Lemmatize the text using spaCy
        text = ' '.join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_digit and not token.is_space and not token.is_bracket and not token.is_quote and not token.like_url and not token.like_email]) 
        for ent in doc.ents: # Remove named entities using spaCy: Names, Surnames, Places
            text = text.replace(ent.text, "")
        reviews_ratings.append([rating])
        cleaned_reviews.append([text]) # Append the cleaned text to the list
    return cleaned_reviews,reviews_ratings
