import streamlit as st
import pickle 
import pandas as pd
import requests

def fetch_poster(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data= response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

movies_dict= pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity= pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommendations')

def recommend(movie):
    movie_index= movies[movies['title']== movie].index[0]
    distances = similarity[movie_index]
    movie_list= sorted(list(enumerate(distances)),reverse= True, key= lambda x: x[1])[1:6]
    recommended_movies= []
    for i in movie_list:
        movie_id=i[0]

        recommended_movies.append((movies.iloc[i[0]].title))

    return recommended_movies

option= st.selectbox(
    'Select a movie', movies['title'].values)

if st.button('Recommend'):
    recommended_movies= recommend(option)
    for i in recommended_movies:
        st.write(i)