import os
import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from scripts.ml.model import tfifdf_df
from scripts.utils import save_plots_png


def histogram_plot(x=None, y=None, color=None, title="Histogram"):
    """
    This function creates a histogram plot of the data provided.

    Parameters:
    x (None): The column in the dataframe to be plotted on the x-axis
    y (None): The second column in the dataframe to be used as y-axis
    color (None):  The column in the dataframe to be used as the color grouping
    title (str): title for fig
    Returns:
    plotly histogram plot object
    """
    try:
        histogram = px.histogram(
            x=x,
            y=y,
            color=color,
            title=title,
            color_discrete_sequence=px.colors.qualitative.G10,
        )
    except:
        histogram = px.histogram(
            x=x, y=y, title=title, color_discrete_sequence=px.colors.qualitative.G10
        )
    return histogram


def generate_wordcloud(
    text: StopIteration,
    max_words=200,
    background_image=None,
    background_color="white",
    width=800,
    height=400,
    stopwords=[
        "bien",
        "qualite",
        "bon",
        "plat",
        "sympa",
        "restaurer",
        "service",
        "accueil",
    ],
    colormap="Spectral",
):
    """
    Generate a wordcloud from the provided text

    Parameters:
    text: The text from which the wordcloud is to be generated.
    max_words: The maximum number of words to be displayed in the wordcloud (default: 200).
    background_image: The name of the image file to be used as background for the wordcloud (default: None).
    background_color: The background color of the wordcloud (default: 'white').
    width: The width of the generated wordcloud (default: 800).
    height: The height of the generated wordcloud (default: 400).
    stopwords: A list of words to be ignored while generating the wordcloud (default: ["bien","qualite","bon","plat","sympa","restaurer","service","accueil"]).
    colormap: The colormap used to color the wordcloud.

    Returns:
    wordcloud (WordCloud object): The generated wordcloud.
    """
    if background_image:
        mask = np.array(Image.open(os.getcwd() + "/visuals/" + background_image))
    else:
        mask = None
    wordcloud = WordCloud(
        width=width,
        height=height,
        background_color=background_color,
        max_words=max_words,
        collocations=False,
        mask=mask,
        stopwords=stopwords,
        colormap=colormap,
    )
    wordcloud.generate(text)
    return wordcloud


def plot_wordcloud(wordcloud, title="Nuage de mots", with_title=True):
    """
    Plots the given wordcloud.
    Parameters:
    - wordcloud: the wordcloud object
    - title: title of the plot
    Returns:
    - fig: the figure object
    - ax: the axis object
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(wordcloud, interpolation="bilinear")
    plt.imshow(wordcloud)
    if with_title:
        plt.title(title)
    return fig, ax


def wordclouds_by_theme(
    data, theme_col, theme_list, filepath=None, savefig=True, with_title=False
) -> None:
    """
    This function takes in a dataframe, a column name for the theme, a list of themes to be visualized.
    For each theme in the theme_list, it creates a wordcloud visualization using the top words from the tf-idf dataframe for that theme.
    It saves the wordcloud visualizations as .png files in the specified repository.
    Parameters:
    data (dataframe): The dataframe containing the text data to be analyzed
    theme_col (str): The column name for the theme
    theme_list (list): A list of themes to be visualized
    filepath (str): Filepath for save files
    savefig (boolean) : If True => Save image
    """
    text_by_thematic = data.groupby(theme_col)["clean_reviews"].apply(
        lambda x: " ".join([str(elem) for elem in x])
    )
    tfidf_df = tfifdf_df(text_by_thematic)
    for theme in theme_list:
        theme_topwords = [
            elem
            for elem in tfidf_df.sort_values(
                by=theme, axis=1, ascending=False
            ).columns.tolist()
        ]
        theme_text = " ".join(theme_topwords)
        wordcloud = generate_wordcloud(theme_text, background_color="black")
        wc_fig, wc_ax = plot_wordcloud(
            wordcloud, title=f"Wordcloud for {theme}", with_title=with_title
        )
        if savefig == True:
            save_plots_png(
                wc_fig, f"wordcloud_{theme}.png", filepath=filepath, repo=None
            )


def extract_ngrams(text, n_range=(2, 2)):
    """
    Extract the n-grams from a given text and return a list of tuples containing the n-gram and its frequency.
    Parameters:
    - text: the text to extract the n-grams from
    - n_range: a tuple specifying the range of n-grams to extract, e.g. (2,2) for bigrams, (1,3) for unigrams, bigrams, and trigrams

    Returns:
    - a list of tuples containing the n-gram and its frequency, sorted by descending frequency
    """

    vectorizer = CountVectorizer(ngram_range=n_range)
    ngrams = vectorizer.fit_transform(text)
    ngram_counts = ngrams.sum(axis=0)
    ngram_freq = [
        (ngram, ngram_counts[0, idx]) for ngram, idx in vectorizer.vocabulary_.items()
    ]
    ngram_freq = sorted(ngram_freq, key=lambda x: x[1], reverse=True)
    return ngram_freq


def plot_top_ngrams(text, n, n_range=(2, 2)):
    """
    Plot the top n n-grams by frequency from a given text.
    Parameters:
    - text: the text to extract the n-grams from
    - n: the number of top n-grams to plot
    - n_range: a tuple specifying the range of n-grams to extract, e.g. (2,2) for bigrams, (1,3) for unigrams, bigrams, and trigrams

    Returns:
    - a Plotly bar chart of the top n n-grams by frequency
    """

    common_ngrams = extract_ngrams(text, n_range)[:n]
    df = pd.DataFrame(common_ngrams, columns=["ngram", "count"])
    fig = px.bar(
        df, x="ngram", y="count", color_discrete_sequence=px.colors.qualitative.G10
    )
    fig.update_layout(
        title_text=f"Top {n} N-grams by frequency", template="plotly_white"
    )
    fig.update_xaxes(tickangle=45)
    return fig


def map_plot_cat(
    data: pd.DataFrame,
    lat_column: str,
    lon_column: str,
    zoom: int,
    text_column: str,
    color_column: str,
):
    """
    Plots a scatter map using the provided data, latitude and longitude columns, zoom level, text column and color column.
    Parameters:
    data: The data to be plotted
    lat_column: The name of the column containing the latitude values
    lon_column: The name of the column containing the longitude values
    zoom: The zoom level of the map (values between 0-20)
    text_column: The name of the column containing the text to be displayed on hover
    color_column: The name of the column containing the categorical values to be used for color coding the dots

    Returns:
    plotly.graph_objs._figure.Figure: The generated map plot
    """
    fig = px.scatter_mapbox(
        data,
        lat=lat_column,
        lon=lon_column,
        zoom=zoom,
        text=text_column,
        color=color_column,
        color_discrete_map=px.colors.qualitative.G10,
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


def plot_sentiment_ratings(data):
    """
    This function takes in a dataframe and plots the relationship between the polarity scores and the ratings.
    The dataframe should have columns named 'polarity' and 'ratings'.
    """
    fig = px.scatter(
        data,
        x="polarity",
        y="ratings",
        title="Relation between polarity scores and ratings",
        labels={"polarity": "Polarity score", "ratings": "Notation"},
    )
    return fig


def plot_model_performance(results: dict):
    """
    This fonction returns from a dict containing results from sentiment analysis (accuracy, confusion matrix), some plots
    """
    df = pd.DataFrame(results).T
    fig = px.bar(x=df.index, y=df["accuracy"], title="Model Accuracy")
    return fig
