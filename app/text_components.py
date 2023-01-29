import streamlit as st


# MAIN PAGE
def about_app_speech():
    st.title("Trip Advisor 🍽️")
    st.markdown(
    """
<div style="text-align:center;">
  <h3>Discover Your Next Dining Destination with TripAdvisor 🏙️</h3>
  <p>With the help of TripAdvisor, we've analyzed thousands of user reviews to bring you the most comprehensive and accurate information about restaurants in Paris. Our sentiment analysis algorithm examines the emotions and opinions expressed in each review, giving you an in-depth understanding of what people are saying about the restaurant.</p>
  <p>Navigate through our interactive map to find your next dining destination. In addition to our sentiment analysis, we've also included information on our methodology and a detailed breakdown of the results, so you can see exactly how we arrived at our conclusions.</p>
  <p>Whether you're a local or a tourist, our app is the perfect tool for finding your next great meal in Paris. Try it out now and experience the future of restaurant discovery.</p>
</div>
    """,
    unsafe_allow_html=True,
    )


# TAB1


# TAB2
def sentiment_analysis_speech():
   st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; flex-direction: column;">
  <h3>Welcome to our Sentiment Analysis Tool</h3>
  <p>Get an insight into the opinions expressed in restaurant reviews on TripAdvisor! Our algorithm examines the language used in each review, assigning a polarity score to determine the sentiment expressed. After that, because polarity scores have limited interpretations, we do a sentiment analysis.<p>
</div>
    """, unsafe_allow_html=True,
    )

def polarity_speech():
    st.markdown(
        """
        <div style="text-align:center;">
        <p>In this analysis, we aim to understand if the sentiment score truly represents the user ratings. If we find that sentiment scores accurately reflect the reviews, then sentiment analysis would not be necessary. On the other hand, if this is not the case, the relationship between sentiment scores and ratings is ambiguous:</p>
        <p>- The ratings may not be representative enough of the comments: user reviews contain much more information and nuances than ratings can capture. Furthermore, people have different rating scales: one person who rates 4 may not have the same criteria as another person who rates 4 for the same restaurant! In this sense, for the same rating, sentiment scores can be very different!</p>
        </div>
        """, unsafe_allow_html=True
    )

def polarity_interpretation_speech():
    st.markdown(
        """
        <center>
Here, we see that the majority of ratings have sentiment scores centered around 0. This indicates that sentiment scores alone may not accurately reflect the ratings given by users. This could be due to various reasons such as users having different rating scales or the limited information that a sentiment score can capture compared to the detailed information expressed in a review. Only very positive reviews seem to be well transcribed, as they are distinguishable from the rest with a distinct distribution around 0.5. It's important to note that sentiment scores have limitations, as they do not take into account the specific context of the review or terms used. They are different from advanced methods like Doc2Vec and BERT-type embeddings which consider the context.
</center>
    """, unsafe_allow_html=True
    )


def model_interpretation_speech():
    st.markdown(
        """
        <p>Among the different models tested (whether on a text embedded by TFIDF or Doc2Vec), everything seems to indicate that the SVM is a relevant model with an accuracy of 0.7. In addition, the confusion matrices also reveal that the model classifies well. It's worth mentioning that the goal of this sentiment analysis was to accurately understand the emotions of the users, rather than simply providing a rating. What do you think?</p>
        """,
        unsafe_allow_html=True)
# TAB3
def foreword_analysis_speech():
    st.title("How we reach these results?")
    st.markdown(
        "<p>In order to better understand the needs of our users, we have collected TripAdvisor data on Parisian restaurants. To do this, we use web scraping technologies, which is an automated technique for extracting information from the web.</p>\
        <p>After collecting the data, we had to clean it. To do this, we use Big Data methods such as Spark, which allow us to efficiently process large volumes of data.</p>\
        <p>Now that our data is ready, we can begin our analysis...</p>\
        <br>\
        ",
        unsafe_allow_html=True,
    )


def explanation_ratings_speech():
    st.subheader("How ratings are made?")
    st.markdown(
        "<p> There are many reasons for differences in restaurant ratings. Among our answers, we have:<p>\
    <p>    - Type of food: Perhaps some types of food are relatively more appreciated by our users such as typical French cuisine<p>\
    <p>    - Location: regardless of the audience (international or local), some places are more famous for their cuisine. Typically, in areas such as Opéra, restaurants are numerous and mostly renowned. Is this remarkable?<p>\
    <p> In a way, some elements are more obvious such as the service, the reception, the quality of the food itself. So our analysis is very quickly turned to the comments to better understand the reasons that make the rating of restaurants.",
        unsafe_allow_html=True,
    )


def explanation_wordclouds_speech():
    st.markdown(
        "The general themes that can be inferred from the wordclouds are as follows: <p> \
                <p> - Wordcloud for ratings < 2: Words such as 'taste' and 'long' are prominent. <p> \
                <p> - Wordcloud for ratings 2.5, 3, 3.5 and 4: Words such as 'long', 'expensive', 'pizza' and 'sushi' are prominent. <p> \
                <p> - Wordcloud for ratings 4.5 and 5: Words such as 'dessert', 'wine' and 'excellent' are prominent.<p> \
               It's important to note that these wordclouds represent the average ratings and not individual ratings. People have different tastes and may not necessarily appreciate the same restaurant in the same way. Therefore, in the sentiment analysis section, we will focus only on the comments associated with the ratings, rather than the overall rating of the restaurant.",
        unsafe_allow_html=True,
    )
