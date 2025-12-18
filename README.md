# CineMind  A Hybrid & Mode-Based Movie Recommendation System  

CineMind is an intelligent and interactive movie recommendation system that suggests personalized movies based on *user mood, content similarity, popularity, and ratings*.  
The project combines *Content-Based Filtering* with a *Hybrid Recommendation approach* and provides a *Netflix-style user interface* for a smooth and engaging user experience.

---

## 🚀 Project Overview  

With thousands of movies available, choosing the right one becomes challenging.  
*CineMind* solves this problem by recommending movies using multiple strategies such as:

- 🎭 Mode-Based (Mood-Based) Recommendation  
- 🧠 Content Similarity  
- ⭐ Popularity & Trending Insights  
- 📈 Top-Rated Movies  
- 📌 Personalized Watchlist Feature  

The system focuses on *user-centric design* and *real-world recommendation logic*.

---

## 🧠 Recommendation Techniques Used  

### 1️⃣ Content-Based Filtering  
- Recommends movies similar to a selected movie  
- Uses features like *genres, overview, keywords, and metadata*  
- Similarity is computed using *vectorization and cosine similarity*

### 2️⃣ Hybrid Recommendation System  
- Combines:
  - Content-based similarity  
  - Popularity-based ranking  
  - Rating-based filtering  
- Produces *more accurate and balanced recommendations*

### 3️⃣ Mode-Based (Mood-Based) Recommendation  
- Allows users to select movies based on their mood, such as:
  - Happy 😊  
  - Sad 😢  
  - Action 🔥  
  - Romantic ❤  
  - Mind-Bending 🧠  
- Movies are filtered and recommended according to the selected mode

---

## ⭐ Key Features  

- 🎭 Mode-Based (Mood-Based) Movie Recommendation  
- 🧠 Content-Based Movie Similarity  
- 🔥 Trending Movies  
- ⭐ Top-Rated Movies  
- 📈 Popularity-Based Ranking  
- 📌 Personalized Watchlist (Save movies to watch later)  
- 🎨 Netflix-Style Dark UI  
- 🖼 Movie Poster Fetching using IMDb / OMDb API  
- ⚡ Fast and interactive UI using Streamlit  

---

## 📌 Watchlist Feature  

CineMind includes a *Watchlist feature* that allows users to save their favorite or planned-to-watch movies.  
This enhances user engagement by enabling:
- Saving movies for later viewing  
- Managing a personalized movie list  
- Improving the overall user experience  

---

## 📊 Dataset  

- *TMDB (The Movie Database) Dataset*  
- Contains:
  - Movie titles  
  - Genres  
  - Overview  
  - Ratings  
  - Popularity scores  

Movie posters are dynamically fetched using the *IMDb / OMDb API*.

---

## 🛠 Tech Stack  

- *Python*  
- *Pandas, NumPy* – Data preprocessing & analysis  
- *Scikit-learn* – Similarity & ML techniques  
- *Streamlit* – Web application & UI  
- *Pickle* – Model serialization  
- *TMDB Dataset*  
- *IMDb / OMDb API* – Poster fetching  

---

## 🎨 User Interface  

- Netflix-inspired clean and modern design  
- Dark theme for better visual experience  
- Interactive movie cards with:
  - Poster  
  - Movie title  
  - Rating  
- Smooth navigation and fast response  

---

## ▶ How to Run the Project  

```bash
git clone https://github.com/your-username/CineMind.git
cd CineMind
pip install -r requirements.txt
streamlit run app.py
