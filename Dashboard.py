import streamlit as st  # For user interface design
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

st.title("Sentiment Analysis Dashboard of Tweets USA Airline")
st.sidebar.title("Sentiment Analysis of Tweets USA Airline")

st.markdown("This application is a streamlit dashboard to analyze the sentiment of tweets about USA Airlines")
st.sidebar.markdown("This application is a streamlit dashboard to analyze the sentiment of tweets about USA Airlines")


@st.cache(persist=True)
def load():
    data = pd.read_csv("Tweets.csv")
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data


df = load()

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio("Sentiment", ("positive", "neutral", "negative"))
st.sidebar.markdown(df.query("airline_sentiment == @random_tweet")[["text"]].sample(n=1).iat[0, 0])

# For Interactive bar chart
st.sidebar.subheader("Number of Tweet per Sentiment")
select = st.sidebar.selectbox("Visualization type", ['Histogram', 'Pie chart'], key='1')
sentiment_count = df['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if st.sidebar.checkbox("View", True):
    st.markdown("### Number of Tweets per Sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x="Sentiment", y="Tweets", color="Tweets", height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values="Tweets", names="Sentiment")
        st.plotly_chart(fig)

# For Interactive Map
st.sidebar.subheader("Where and when are Users Tweeting from")
hour = st.sidebar.number_input("Hour of day", min_value=0, max_value=23)
modified_data = df[df['tweet_created'].dt.hour == hour]
if st.sidebar.checkbox("Show", True, key='1'):
    st.markdown("### Tweets Location based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1) % 24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Breakdown Airline Tweet by sentiment")
choice = st.sidebar.multiselect("Choose Airline", ("US Airways", "United", "American", "Southwest", "Delta", "Virgin America"), key="0")

if len(choice) > 0:
    choice_data = df[df.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x="airline", y="airline_sentiment", histfunc="count", color="airline_sentiment",
    facet_col="airline_sentiment", labels={"airline_sentiment": "tweets"}, height=600, width=800)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio("Display word cloud for what sentiment?", ("positive", "neutral", "negative"))

if st.sidebar.checkbox("View", True, key="3"):
    st.header("Word Cloud for %s sentiment" % word_sentiment)
    word_df = df[df["airline_sentiment"] == word_sentiment]
    words = " ".join(word_df["text"])
    processed_words = " ".join([word for word in words.split() if "http" not in word and not word.startswith("@") and word != "RT"])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white", height=640, width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()

st.set_option('deprecation.showPyplotGlobalUse', False)
