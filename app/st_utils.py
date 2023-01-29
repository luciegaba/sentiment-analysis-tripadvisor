import folium
import os
import streamlit as st
from scripts.viz.graph import wordclouds_by_theme
from PIL import Image
from scripts.utils import flatten


def filter_data(data, options):
    """
    Filters a given dataframe based on user-specified options using a Streamlit selectbox, select_slider, and multiselect.
    The filtered data is sorted by descending average_note and only the top 20 rows are returned.

    Parameters:
    - data (dataframe): Data to be filtered
    - options (dict): A dictionary containing the options for the selectbox, select_slider, and multiselect.
                      keys: 'filter_type', 'filter_price', 'hashtags'
                      values: list of options for selectbox, list of options for select_slider, list of options for multiselect

    Returns:
    - filtered_data (dataframe): Filtered data based on user-specified options
    """

    filtered_data = data.copy()
    filtered_data = filtered_data[
        filtered_data["cuisine"].apply(lambda x: options["filter_type"] in x)
    ]
    filtered_data = filtered_data[
        filtered_data["price"].apply(lambda x: x[0] if len(x) > 0 else None)
        == options["filter_price"]
    ]
    filtered_data = filtered_data[
        filtered_data["reviews"]
        .apply(lambda x: " ".join(elem for elem in x))
        .apply(lambda x: any(hashtag in x for hashtag in options["hashtags"]))
    ]
    filtered_data = filtered_data.sort_values("average_note", ascending=False).head(20)
    return filtered_data


def prepare_features_for_analysis(raw_data):

    """
    Prepare the data for the analysis by flattening the cleaned reviews, splitting the cuisine modalities and dropping duplicate restaurants and filling any missing cuisine values with the mode.
    Parameters:
    - raw_data: The raw dataframe containing the reviews and restaurant information
    Returns:
    - Tuple containing the cleaned corpus and the processed dataframe with split cuisines and dropped duplicates
    """
    clean_corpus = flatten(raw_data["clean_reviews"].values.tolist())
    data_with_cook_modalities_splitted = raw_data.explode("cuisine")
    data_with_cook_modalities_splitted = data_with_cook_modalities_splitted.dropna(
        subset=["name", "average_note"]
    )
    data_with_cook_modalities_splitted = (
        data_with_cook_modalities_splitted.drop_duplicates(subset=["name"])
    )
    data_with_cook_modalities_splitted["cuisine"] = data_with_cook_modalities_splitted[
        "cuisine"
    ].fillna(data_with_cook_modalities_splitted["cuisine"].mode()[0])
    return clean_corpus, data_with_cook_modalities_splitted


def interactive_map(data, long_col, lat_col, icon, color, prefix, popup_msg):
    """
    Creates an interactive map using the Folium library, using the specified columns for longitude and latitude, marker icon, color, prefix, popup message and tile layer.
    :param data: The dataframe to use for the map markers
    :param long_col: The name of the column in the dataframe to use for longitude
    :param lat_col: The name of the column in the dataframe to use for latitude
    :param icon: The icon to use for the markers
    :param color: The color to use for the markers
    :param prefix: The prefix to use for the markers
    :param popup_msg: The message to use in the pop-up for each marker
    :param tile_layer: The tile layer to use for the map
    :return: An interactive map object
    """
    data[long_col] = data[long_col].fillna(data[long_col].mean())
    data[lat_col] = data[lat_col].fillna(data[lat_col].mean())

    m = folium.Map(
        location=[data[lat_col].mean(), data[long_col].mean()], zoom_start=10
    )
    for i in range(len(data)):
        folium.Marker(
            location=[data.iloc[i][lat_col], data.iloc[i][long_col]],
            popup=folium.Popup(popup_msg.format(**data.iloc[i])),
            icon=folium.Icon(color=color, icon_color="black", icon=icon, prefix=prefix),
        ).add_to(m)

    folium.TileLayer("cartodbdark_matter").add_to(m)
    return m


def display_wordclouds(data, project_path, theme_col, theme_list):
    """
    Creates wordclouds for each theme in the dataframe
    :param data: The dataframe to use for wordclouds
    :param project_path: the path of the project
    :param theme_col: The column in the dataframe that contains the themes
    :param theme_list: The list of themes to create wordclouds for
    """
    wordclouds_by_theme(
        data,
        theme_col=theme_col,
        theme_list=theme_list,
        filepath=project_path + "/visuals/wordcloud/",
    )
    wordclouds_images = [
        f for f in os.listdir(project_path + "/visuals/wordcloud") if f.endswith(".png")
    ]
    wordclouds_images.remove("wordcloud.png")
    for image_file in wordclouds_images:
        image = Image.open(project_path + "/visuals/wordcloud/" + image_file)
        st.image(image)
        st.caption(f"Wordclouds for {image_file.split('_')[1].replace('.png','')}")


def create_filters(options):
    """
    Create filters for the app:
    :param options: A dictionary containing the options for the filter type, filter price and hashtags
    :return: A dictionary containing the selected filter type, filter price, and hashtags
    """
    filter_type = st.selectbox(
        options=options["filter_type"], label="Choose a cuisine type"
    )
    filter_price = st.select_slider(
        options=options["filter_price"], label="What is your budget?"
    )
    hashtags = st.multiselect(
        label="Specific craving?",
        options=options["hashtags"],
        default=" ",
        format_func=lambda x: "# " + str(x),
    )
    return {
        "filter_type": filter_type,
        "filter_price": filter_price,
        "hashtags": hashtags,
    }
