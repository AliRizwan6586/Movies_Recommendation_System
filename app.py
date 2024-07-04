import streamlit as st
import pandas as pd
import pickle
import lzma
import requests

# Load the compressed similarity file
def decompress_pickle(file):
    with lzma.open(file, 'rb') as f:
        data = pickle.load(f)
    return data

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=fe1435d34e78c06da317be9d681b05e0&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = decompress_pickle('similarity2.pkl.xz')

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title("Movie Recommender System")

selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    for col, title, poster in zip([col1, col2, col3, col4, col5], recommendations, posters):
        with col:
            st.markdown(f"<h6 class='movie-title'>{title}</h6>", unsafe_allow_html=True)
            st.image(poster, use_column_width=True)

# Custom CSS to adjust text and image size and alignment
st.markdown(
    """
    <style>
    .stImage img {
        width: 100% !important;
        height: auto !important;
        object-fit: contain;
    }
    .movie-title {
        font-size: 14px;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

