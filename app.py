import streamlit as st
import pandas as pd
import pickle
import lzma

# Load the compressed similarity file
def decompress_pickle(file):
    with lzma.open(file, 'rb') as f:
        data = pickle.load(f)
    return data

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = decompress_pickle('similarity2.pkl.xz')

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

st.title("Movie Recommender System")

selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for i in recommendations:
        st.write(i)
