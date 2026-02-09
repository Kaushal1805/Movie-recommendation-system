import streamlit as st
import pickle
import pandas as pd

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered"
)

# ================= CUSTOM CSS =================
st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Title */
    h1 {
        text-align: center;
        color: #f9f9f9;
        font-size: 3rem;
    }

    /* Sub text */
    p {
        text-align: center;
        font-size: 1.1rem;
        color: #dddddd;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: #1e1e1e;
        color: white;
        border-radius: 10px;
    }

    /* Button */
    .stButton>button {
        background: linear-gradient(90deg, #ff512f, #dd2476);
        color: white;
        border: none;
        padding: 0.6em 1.5em;
        border-radius: 25px;
        font-size: 1rem;
        font-weight: bold;
        transition: 0.3s;
        display: block;
        margin: auto;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #dd2476, #ff512f);
    }

    /* Recommendation box */
    .recommend-box {
        background-color: rgba(255, 255, 255, 0.08);
        padding: 15px;
        border-radius: 15px;
        margin-top: 15px;
        font-size: 1.05rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        font-size: 0.85rem;
        color: #bbbbbb;
        margin-top: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= LOAD DATA =================
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ================= TITLE =================
st.title("🎬 Movie Recommendation System")
st.write(
    "Discover movies similar to your taste using Machine Learning & NLP 🍿"
)

st.markdown("<hr>", unsafe_allow_html=True)

# ================= METRIC =================
st.metric("🎥 Total Movies Available", len(movies))

st.markdown("<hr>", unsafe_allow_html=True)

# ================= SELECT MOVIE =================
selected_movie = st.selectbox(
    "🎯 Select a movie you like",
    movies['title'].values
)

# ================= RECOMMEND FUNCTION =================
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    return [movies.iloc[i[0]].title for i in movie_list]

# ================= BUTTON ACTION =================
if st.button("✨ Show Recommendations"):
    st.subheader("📌 Movies You May Also Like")

    recommendations = recommend(selected_movie)
    for i, movie in enumerate(recommendations, start=1):
        st.markdown(
            f"<div class='recommend-box'>{i}. 🎬 {movie}</div>",
            unsafe_allow_html=True
        )

# ================= FOOTER =================
st.markdown(
    "<div class='footer'>🚀 Built with Machine Learning (Cosine Similarity). "
    "Poster feature can be added later.</div>",
    unsafe_allow_html=True
)
