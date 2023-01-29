
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from scripts.ml.features import reviews_cleaner


def sentiments_label(value):
    if value == "1.0" or value == "2.0":
        value = "bad"
    elif value == "3.0" or value == "4.0":
        value = "average"
    elif value == "5.0":
        value = "excellent"
    else:
        value ="no_review"
    return value

def tfifdf_df(text):
    """
    This function takes in a single input, a text. It then applies the TfidfVectorizer to the text and returns a dataframe of the TF-IDF values of the text.
    Parameters:
    text: A string of text to be analyzed
    Returns:
    tfidf_df: A dataframe containing the TF-IDF values of the text, with columns being the words in the text and rows being the different text input.
    """
    tf=TfidfVectorizer()
    text_tf= tf.fit_transform(text)
    tfidf_df=pd.DataFrame(data=text_tf.toarray(),columns=tf.get_feature_names_out().tolist(),index=text.index)
    return tfidf_df


def prepare_for_ml(data:pd.DataFrame,vectorizer="tfidf"):
    """
    This function prepares the data for machine learning by splitting it into training and testing sets, and vectorizing the text data.
    It takes in a dataframe as input, and a string that indicates the type of vectorization to be used.
    The default vectorization method is tf-idf. The function returns the training and testing sets for both the features and the labels.
    """
    X=data["clean_reviews"]
    y=data["ratings"]
    y=y.apply(sentiments_label)
    y_cat=LabelEncoder().fit_transform(y)
    if vectorizer == "tfidf":
        X=vectorizer_by_tfidf(X)
    else: 
        X=vectorizer_by_doc2vec(X)
    X_train, X_test,y_train,y_test = train_test_split(
    X,y_cat, test_size=0.3, random_state=1)
    return  X_train,X_test, y_train,y_test


def vectorizer_by_tfidf(X:pd.Series):
    """
    This function vectorizes the input text data using the tf-idf method. It takes in a pandas series of text data as input and returns the vectorized representation of the data.
    """
    tf=TfidfVectorizer()
    X_tfidf= tf.fit_transform(X).toarray()
    return X_tfidf

def vectorizer_by_doc2vec(X:pd.Series):
    """
    This function vectorizes the input text data using the doc2vec method. It takes in a pandas series of text data as input and returns the vectorized representation of the data.
    """ 
    tagged_data = [TaggedDocument(words=review.split(), tags=[str(i)]) for i, review in enumerate(X)]
    model = Doc2Vec(tagged_data, vector_size=50, window=2, min_count=1, workers=4)
    review_vectors = [model.infer_vector(review.split()) for review in X]
    return review_vectors
    

def train_and_evaluate_models(X_train:pd.DataFrame,X_test:pd.DataFrame,y_train:pd.Series,y_test:pd.Series):
    """
    Train and evaluate multiple models on the provided data.
    Parameters:
    - X_train: features train set
    - X_test: features test set
    - Y_train: target train set
    - Y_test: target test set
    
    Returns:
    - plot of accuracies
    """

    models = {
        "KNN": KNeighborsClassifier(),
        "SVM": SVC(),
        "Random Forest": RandomForestClassifier(),
    }

    # Train and evaluate the models
    results = {}
    for model_name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results[model_name] = {
            "accuracy": model.score(X_test, y_test),
            "confusion_matrix": confusion_matrix(y_test, y_pred)
        }
    return results



def predict(model_fitted,vectorizer,data:pd.DataFrame):
    """
    Make predictions with a fitted model
    Inputs: model, data (dataframe containing clean_reviews)
    Returns: preds
    """
    X=data["clean_reviews"]
    print(X)
    X=vectorizer.transform(X).toarray()
    print(X.shape)
    preds=model_fitted.predict(X)

    return preds



