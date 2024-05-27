import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=a62f740666df6cd0c9d0eb19fc9bbcda')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))

movies = pd.DataFrame(data=movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    num_columns = 5
    num_movies = len(names)
    num_rows = -(-num_movies // num_columns)  # Ceiling division

    for i in range(num_rows):
        cols = st.columns(num_columns)
        for j, col in enumerate(cols):
            movie_index = i * num_columns + j
            if movie_index < num_movies:
                col.text(names[movie_index])
                col.image(posters[movie_index])



