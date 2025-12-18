# CineMind: Hybrid & Mood-Based Movie Recommendation System
import streamlit as st
import pickle
import pandas as pd
import requests


# PAGE CONFIG
st.set_page_config(
    page_title="CineMind: Hybrid & Mood-Based Movie Recommendation System",
    layout="wide"
)


# NETFLIX DARK THEME CSS
st.markdown("""
<style>
.stApp { background-color:#0e1117; color:white; }
section[data-testid="stSidebar"] { background-color:#161a23; }

.stButton>button {
    background: linear-gradient(135deg,#e50914,#b00610);
    color:white;
    border-radius:12px;
    border:none;
    padding:10px 16px;
    font-weight:600;
    transition:0.3s;
}
.stButton>button:hover {
    transform:scale(1.05);
    box-shadow:0 0 15px rgba(229,9,20,0.6);
}

.movie-card {
    background:#1c1f2a;
    padding:12px;
    border-radius:18px;
    box-shadow:0 8px 18px rgba(0,0,0,0.6);
    transition:0.3s;
    text-align:center;
}
.movie-card:hover { transform:scale(1.08); }
.movie-title { margin-top:8px; font-size:14px; font-weight:600; }

/* Sidebar title */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #e50914 !important;
}

/* Sidebar content text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] span {
    color: #dcdcdc !important;
}
</style>
""", unsafe_allow_html=True)


# OMDB CONFIG
OMDB_API_KEY = "b75a476a"
FALLBACK_POSTER = "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"

@st.cache_data(show_spinner=False)
def fetch_movie_details_omdb(title):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}&plot=full"
        data = requests.get(url, timeout=5).json()
        if data.get("Response") == "True":
            return {
                "poster": data.get("Poster", FALLBACK_POSTER),
                "plot": data.get("Plot", "N/A"),
                "actors": data.get("Actors", "N/A"),
                "director": data.get("Director", "N/A"),
                "runtime": data.get("Runtime", "N/A"),
                "rating": data.get("imdbRating", "N/A")
            }
    except:
        pass
    return {
        "poster": FALLBACK_POSTER,
        "plot": "N/A",
        "actors": "N/A",
        "director": "N/A",
        "runtime": "N/A",
        "rating": "N/A"
    }


# LOAD DATA
movies = pickle.load(open("movies_df.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))


# SESSION STATE
if "page" not in st.session_state:
    st.session_state.page = "Recommend"
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []
if "recommended_movies" not in st.session_state:
    st.session_state.recommended_movies = []
if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None

if "mood_movies" not in st.session_state:
    st.session_state.mood_movies = pd.DataFrame()


# RECOMMEND FUNCTIONS
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movie_list]

def hybrid_recommend_app(movie_title, top_n=10):
    index = movies[movies["title"] == movie_title].index[0]
    content_scores = similarity[index]
    pop = (movies['popularity'] - movies['popularity'].min()) / (movies['popularity'].max() - movies['popularity'].min())
    vote = (movies['vote_average'] - movies['vote_average'].min()) / (movies['vote_average'].max() - movies['vote_average'].min())
    final_score = 0.6 * content_scores + 0.25 * vote + 0.15 * pop
    top_idx = final_score.argsort()[::-1][1:top_n+1]
    return [movies.iloc[i].title for i in top_idx]


# MOOD BASED RECOMMENDATION
MOOD_GENRE_MAP = {
    "Happy 😊": ["Comedy", "Animation", "Family"],
    "Sad 😢": ["Drama", "Romance"],
    "Action 🔥": ["Action", "Thriller"],
    "Romantic ❤": ["Romance"],
    "Mind-Bending 🧠": ["Sci-Fi", "Mystery"]
}

def recommend_by_mood(mood):
    genres = MOOD_GENRE_MAP[mood]

    filtered = movies[movies["genres"].apply(
        lambda g: any(genre in g for genre in genres)
    )]

    return filtered.sort_values(
        by=["vote_average", "popularity"],
        ascending=False
    ).head(10)


# MOVIE CARD
def movie_card(title, idx, add_watchlist=False):
    details = fetch_movie_details_omdb(title)

    st.markdown(f"""
    <div class="movie-card">
        <img src="{details['poster']}" width="100%" style="border-radius:14px;">
        <div class="movie-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "ℹ Details",
        key=f"details_{title}_{idx}_{st.session_state.page}"
    ):
        with st.expander("🎬 Movie Details", expanded=True):
            st.write("⭐ IMDb:", details["rating"])
            st.write("⏱ Runtime:", details["runtime"])
            st.write("🎥 Director:", details["director"])
            st.write("🎭 Cast:", details["actors"])
            st.write(details["plot"])

    if add_watchlist:
        if st.button(
            "❤ Watchlist",
            key=f"watch_{title}_{idx}_{st.session_state.page}"
        ):
            if title not in st.session_state.watchlist:
                st.session_state.watchlist.append(title)
                st.success("Added to Watchlist")


# GRID
def show_movie_grid(df, n=10):
    cols = st.columns(5)
    for i, row in enumerate(df.head(n).iterrows()):
        _, row = row
        with cols[i % 5]:
            movie_card(row["title"], i, True)


# HEADER & MENU
st.title("🎬 CineMind: Hybrid & Mood-Based Movie Recommendation System")
menu = ["Recommend", "Hybrid ", "Trending","Top Rated","Popular","Mood","Watchlist"]
menu_cols = st.columns(len(menu))
for col, name in zip(menu_cols, menu):
    with col:
        if st.button(name, key=f"menu_{name}"):
            st.session_state.page = name

st.divider()
choice = st.session_state.page


# PAGES
if choice == "Recommend":
    movie = st.selectbox("Select Movie", movies["title"].values)
    if st.button("Recommend Movies", key="btn_recommend"):
        st.session_state.recommended_movies = recommend(movie)

    cols = st.columns(5)
    for i, t in enumerate(st.session_state.recommended_movies):
        with cols[i % 5]:
            movie_card(t, i, True)


elif choice == "Hybrid ":
    movie = st.selectbox("Select Movie", movies["title"].values)
    if st.button("Hybrid Recommend", key="btn_hybrid"):
        st.session_state.recommended_movies = hybrid_recommend_app(movie)

    cols = st.columns(5)
    for i, t in enumerate(st.session_state.recommended_movies):
        with cols[i % 5]:
            movie_card(t, i, True)
elif choice == "Trending":
    show_movie_grid(movies.sort_values("popularity", ascending=False))

elif choice == "Top Rated":
    show_movie_grid(movies.sort_values("vote_average", ascending=False))

elif choice == "Popular":
    show_movie_grid(movies.sort_values("vote_count", ascending=False))

elif choice == "Mood":
    st.subheader("🎭 Choose Your Mood")

    cols = st.columns(len(MOOD_GENRE_MAP))

    for i, mood in enumerate(MOOD_GENRE_MAP.keys()):
        if cols[i].button(mood, key=f"mood_{mood}"):
            st.session_state.selected_mood = mood
            st.session_state.mood_movies = recommend_by_mood(mood)

    if st.session_state.selected_mood:
        st.markdown(
            f"### 🎬 Recommended Movies for {st.session_state.selected_mood}"
        )

    if not st.session_state.mood_movies.empty:
        cols_movies = st.columns(5)
        for i, row in enumerate(st.session_state.mood_movies.iterrows()):
            _, row = row
            with cols_movies[i % 5]:
                movie_card(row["title"], i, True)


elif choice == "Watchlist":
    if st.session_state.watchlist:
        cols = st.columns(5)
        for i, t in enumerate(st.session_state.watchlist):
            with cols[i % 5]:
                movie_card(t, i)

    else:
        st.info("Your watchlist is empty.")


# SIDEBAR
st.sidebar.title("🎬 About Project")
st.sidebar.write("""
• Netflix-style Dark UI  
• Content + Hybrid Recommendation  
• OMDb API Integration  
• Watchlist Feature  
• Mood Based Recommendation
""")

