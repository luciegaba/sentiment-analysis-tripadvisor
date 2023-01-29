import pandas as pd
from textblob import TextBlob


def reviews_cleaner(data: pd.DataFrame) -> pd.DataFrame:
    """
    Get reviews exploded in several raws, as well as, ratings
    Parameters:
    df: Dataframe containing the 'clean_reviews' and 'ratings' columns
    Returns:
    data_with_reviews_splitted: Dataframe with exploded 'clean_reviews' and 'ratings' columns, and null values in 'clean_reviews' filled with empty string
    """
    data_ = data.copy()
    data_with_reviews_splitted = data_.explode("clean_reviews")
    data_with_ratings_splitted = data_.explode("ratings")
    data_with_reviews_splitted = pd.concat(
        [
            data_with_reviews_splitted.drop(columns="ratings"),
            data_with_ratings_splitted["ratings"],
        ],
        axis=1,
    )  # Contatenate two df with exploded columns
    data_with_reviews_splitted["clean_reviews"] = data_with_reviews_splitted[
        "clean_reviews"
    ].fillna("")
    return data_with_reviews_splitted


def polarity(data: pd.DataFrame) -> None:
    """
    This function takes in a dataframe (df) as an input and performs the following operations:
    Parameters:
    df: Dataframe containing 'clean_reviews' column
    Returns:
    df: Dataframe with an additional 'polarity' column
    """
    data["polarity"] = data["clean_reviews"].apply(
        lambda x: TextBlob(x).sentiment.polarity
    )
