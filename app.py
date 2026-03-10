import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYzcyMDQ4MDY3N2Y3ZWIwOWQzNDdjNjIxYTVjNjJjNSIsIm5iZiI6MTc3MzEzMTE0MS40MjksInN1YiI6IjY5YWZkNTg1MmM4N2QzMmU5YTBiMmY0NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.4mb4vEKCaSDVrNs-ElR1CGIOcSKyFF6jyKqwg4af22o"
    }

    response = requests.get(url.format(movie_id), headers=headers)
    if response.status_code != 200:
        # TMDB may return 404 or other errors for unknown IDs
        return "https://via.placeholder.com/500x750?text=No+Poster"

    data = response.json()
    poster_path = data.get('poster_path')
    if not poster_path:
        return "https://via.placeholder.com/500x750?text=No+Poster"

    return "https://image.tmdb.org/t/p/w500/" + poster_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie.title()].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_idx = i[0]
        movie_id = movies.iloc[movie_idx].id

        recommended_movies.append(movies.iloc[movie_idx].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", 'rb'))

st.title("Movie Recommendation System")

selected_movie = st.selectbox(
    'Search for a movie',
    movies['title'].values
)


if st.button('Recommend'):
    names, poster = recommend(selected_movie)

    cols = st.columns(5)
    for idx, (name, img_url) in enumerate(zip(names, poster)):
        col = cols[idx % 5]
        with col:
            st.image(img_url, width=160)
            st.caption(name)
