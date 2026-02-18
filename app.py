import streamlit as st
import pickle
import requests
from concurrent.futures import ThreadPoolExecutor

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

* { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: #0d0d0d;
    background-image:
        radial-gradient(ellipse at 10% 50%, rgba(229, 9, 20, 0.07) 0%, transparent 60%),
        radial-gradient(ellipse at 90% 20%, rgba(229, 9, 20, 0.05) 0%, transparent 50%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1400px; }

.hero {
    text-align: center;
    padding: 2rem 0 1rem 0;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    letter-spacing: 4px;
    background: linear-gradient(135deg, #ffffff 40%, #e50914);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.hero-sub {
    color: #6b7280;
    font-size: 1rem;
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.stats-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.stat-box {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
}
.stat-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: #e50914;
    letter-spacing: 2px;
}
.stat-label {
    color: #6b7280;
    font-size: 0.72rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 0.2rem;
}

.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1.5px solid rgba(229, 9, 20, 0.4) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 1rem !important;
}
.stSelectbox label {
    color: #9ca3af !important;
    font-size: 0.8rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #e50914, #b00710) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.8rem !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.3rem !important;
    letter-spacing: 3px !important;
    transition: all 0.3s ease !important;
    margin-top: 0.5rem !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(229, 9, 20, 0.5) !important;
}

.movie-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    overflow: hidden;
    transition: all 0.3s ease;
}
.movie-card:hover {
    border-color: rgba(229, 9, 20, 0.6);
    transform: translateY(-6px);
    box-shadow: 0 15px 40px rgba(229, 9, 20, 0.25);
}
.movie-title-card {
    padding: 0.7rem 0.5rem;
    text-align: center;
    color: #e5e7eb;
    font-size: 0.82rem;
    font-weight: 500;
    line-height: 1.3;
}
.no-poster {
    background: rgba(255,255,255,0.04);
    height: 280px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #374151;
    font-size: 3.5rem;
}
.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 3px;
    color: #ffffff;
    margin: 2rem 0 0.3rem 0;
    border-left: 4px solid #e50914;
    padding-left: 1rem;
}
.red-line {
    height: 1px;
    background: linear-gradient(to right, #e50914, transparent);
    margin: 1.5rem 0;
}
.divider {
    height: 1px;
    background: rgba(255,255,255,0.06);
    margin: 0.5rem 0 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ─── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_data():
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

OMDB_KEY = "f3cdb96b"

# ─── Fetch Poster using OMDB ───────────────────────────────────────────────────
@st.cache_data(ttl=86400)
def fetch_poster(title):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_KEY}"
        res = requests.get(url, timeout=8)
        data = res.json()
        poster = data.get('Poster')
        if poster and poster != 'N/A':
            return poster
    except:
        pass
    return None


# ─── Recommend Function ────────────────────────────────────────────────────────
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )
    top5 = []
    for i in distances[1:6]:
        title = movies.iloc[i[0]].title
        top5.append({'title': title})

    # Fetch all 5 posters in parallel
    def get_poster(m):
        m['poster'] = fetch_poster(m['title'])
        return m

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(get_poster, top5))

    return results


# ─── UI ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">🎬 CineMatch</div>
    <div class="hero-sub">Discover your next favorite film</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-number">1494</div>
        <div class="stat-label">Movies Available</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">NLP</div>
        <div class="stat-label">Powered By</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">5</div>
        <div class="stat-label">Recommendations</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">OMDB</div>
        <div class="stat-label">Poster Source</div>
    </div>
</div>
<div class="red-line"></div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    selected_movie = st.selectbox(
        "SELECT A MOVIE YOU LIKE",
        movies['title'].values
    )
    btn = st.button("🎯 FIND SIMILAR MOVIES")

st.markdown('<div class="red-line"></div>', unsafe_allow_html=True)

if btn:
    st.markdown('<div class="section-title">RECOMMENDED FOR YOU</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    with st.spinner("🎬 Loading recommendations..."):
        results = recommend(selected_movie)

    cols = st.columns(5)
    for i, movie in enumerate(results):
        with cols[i]:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            if movie['poster']:
                st.image(movie['poster'], use_container_width=True)
            else:
                st.markdown('<div class="no-poster">🎬</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="movie-title-card">{movie["title"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div style="text-align:center;color:#2d2d2d;font-size:0.78rem;">Built with ❤️ · Streamlit · OMDB API · Scikit-learn</div>', unsafe_allow_html=True)
