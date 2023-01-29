import os
import pandas as pd
import sys
import pickle
sys.path.append("./")
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import plotly.express as px

from text_components import (
    about_app_speech,
    foreword_analysis_speech,
    explanation_ratings_speech,
    explanation_wordclouds_speech,
    sentiment_analysis_speech,
    polarity_speech,
    polarity_interpretation_speech,
)
from scripts.ml.features import reviews_cleaner, polarity
from scripts.ml.model import predict,vectorizer_by_tfidf
from st_utils import (
    interactive_map,
    display_wordclouds,
    create_filters,
    filter_data,
    prepare_features_for_analysis,
)
from scripts.viz.graph import (
    plot_wordcloud,
    plot_top_ngrams,
    generate_wordcloud,
    histogram_plot,
    plot_sentiment_ratings,
    plot_model_performance,
)
from scripts.utils import get_data, save_plots_png


def user_mapping_part(dataframe, options):
    """
    Corresponds to First Tab: Map with filters
    """
    st.title("Dining in Paris?")
    st.markdown(
        "With this map, you will get the best adresses depending on users opinion!"
    )
    st.info("Selection filters to find the optimal restaurant for you!")
    selected_options = create_filters(options)
    selection_data = filter_data(dataframe, selected_options)
    try:
        map = interactive_map(
            selection_data,
            "longitude",
            "latitude",
            "glyphicon-cutlery",
            "white",
            "glyphicon",
            '<a href="{url}"target="_blank">{name}</a>',
        )
        folium_static(map)
        st.dataframe(
            selection_data[
                [
                    "name",
                    "ranking",
                    "average_note",
                    "location",
                    "reviews",
                    "number_reviews",
                ]
            ]
        )
    except (ValueError, KeyError):
        st.info("No restaurant matches your criteria")




def sentiment_analysis(data, project_path):
    """
    Corresponds to Second Tab: Sentiment Analysis
    """
    sentiment_analysis_speech()
    sentiment_data = reviews_cleaner(data)
    polarity(sentiment_data)
    with st.expander("Polarity score"):
        polarity_speech()
        sentiment_plot = plot_sentiment_ratings(sentiment_data)
        st.plotly_chart(sentiment_plot)
        polarity_interpretation_speech()
    with st.expander("Supervised Model"):
        vectorizer = st.radio("How to vectorize?", ("tfidf", "doc2vec"))
        with open(f"{project_path}/artefacts/results_{vectorizer}.pkl", "rb") as f:
            results = pickle.load(f)
        st.plotly_chart(plot_model_performance(results))

        with open(f"{project_path}/artefacts/svm.pkl", "rb") as f:
            model = pickle.load(f)
        with open(f"{project_path}/artefacts/tfidf.pkl", "rb") as f:
            tfidf = pickle.load(f)
        st.dataframe(sentiment_data["clean_reviews"])
        preds=predict(model,tfidf,sentiment_data)
        st.dataframe(preds)
        st.dataframe(pd.concat([sentiment_data["clean_reviews","ratings"],preds],axis=1))
        st.balloons()


def analysis_part(data, st, options, project_path):
    """
    Corresponds to Third Tab: Methods + Global Analysis
    """
    clean_corpus, cook_data = prepare_features_for_analysis(data)
    cooktype = options["filter_type"]
    foreword_analysis_speech()
    st.header("How do users think about Parisian restaurants?")
    explanation_ratings_speech()
    with st.expander("Cuisine Types"):
        cook_data = cook_data.query("cuisine in @cooktype")
        st.plotly_chart(
            histogram_plot(
                x=cook_data["average_note"],
                color=cook_data["cuisine"],
                title="Ratings distribution depending on cuisine type",
            )
        )
        st.caption("Ratings distribution depending on cuisine type")
        st.info("You can double-tap one style to see it")

    with st.expander("Locations"):
        map_cooktype = px.scatter_mapbox(
            data,
            lat="latitude",
            lon="longitude",
            text="name",
            color="average_note",
            zoom=10,
        ).update_layout(mapbox_style="carto-darkmatter")
        st.plotly_chart(map_cooktype)
        st.caption("Map of restaurants and their ratings")

    with st.expander("Comments"):
        subtab1, subtab2, subtab3 = st.tabs(
            ["Trigrams", "Global Wordcloud", "Wordcloud per rating note"]
        )
        with subtab1:
            st.plotly_chart(plot_top_ngrams(clean_corpus, 20, (3, 3)))
            st.caption(
                "Representative trigrams(sequence of three consecutive words) for all reviews"
            )
        with subtab2:
            st.caption("Wordcloud of most representative words in reviews")
            wc = generate_wordcloud(
                " ".join([elem for elem in clean_corpus]),
                background_image="TripAdvisor.jpg",
                background_color="black",
            )
            wc_fig, wc_ax = plot_wordcloud(wc, title="Wordcloud for reviews")
            save_plots_png(
                wc_fig,
                f"wordcloud.png",
                filepath=project_path + "/visuals/wordcloud/",
                repo=None,
            )
            image = Image.open(project_path + "/visuals/wordcloud/wordcloud.png")
            st.image(image)
        with subtab3:
            display_wordclouds(
                data,
                project_path,
                "average_note",
                list(set(data["average_note"].values.tolist())),
            )
            explanation_wordclouds_speech()
        st.markdown(
            "With the below elements, we concluded that textual analysis over reviews could potentially help to explain better the 'real value' of restaurants. Whereas the analysis over locations and over cuisine types is limited, we can provide an indepth-analysis of customer's tastes."
        )


def main_page():
    options = {
        "filter_type": [
            "Française",
            "Européenne",
            "Végétariens bienvenus",
            "Asiatique",
            "Italienne",
            "Bar",
            "Japonaise",
            "Pizza",
            "Méditerranéenne",
            "Café",
        ],
        "filter_price": ["€", "€€-€€€", "€€€€"],
        "hashtags": [
            " ",
            "atypique",
            "quartier",
            "métro",
            "silence",
            "cosy",
            "veggie",
            "rapide",
            "vin",
        ],
    }

    path = os.getcwd()
    st.set_page_config(
        page_title="TripAdvisor",
        page_icon=Image.open(path + "/visuals/TRIP-2af5b8e6.png"),
        initial_sidebar_state="expanded",
        menu_items={
            "About": """
                Contributions:
                - Lucie Gabagnou
                - Yanis Rehoune
                
                """
        },
    )
    data = get_data(path)
    about_app_speech()
    tab_map, tab_sentiment, tab_analysis = st.tabs(
        ["TripAdvisorMap", "Sentiment Analysis", "Methodology and Global Analysis"]
    )
    with tab_map:
        map_data = data.copy()
        user_mapping_part(map_data, options)
    with tab_sentiment:
        sentiment_analysis(data, path)
    with tab_analysis:
        analysis_part(data, st, options, project_path=path)


if __name__ == "__main__":
    main_page()
