import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import random

def prepare_df(df: pd.DataFrame) -> pd.DataFrame:
    movie = df.copy()
    movie['year'] = movie['title'].str.extract(r'[(](?P<first>\d{4})')
    movie['year'].fillna(0, inplace=True)
    movie['year'] = movie['year'].astype(int)
    movie.index = movie['movieId']
    return movie

def check_and_rating(rating:pd.DataFrame,movie:pd.DataFrame,userid:int) -> pd.DataFrame:
    data_rating = rating[rating["userId"] == userid]
    moive_check = pd.merge(data_rating, movie, on="movieId")
    # print(moive_check)
    return moive_check[['title','genres','rating']]

def count_genre_on_user(value:int,rating:pd.DataFrame,tags:pd.DataFrame)->pd.DataFrame:
    graph_val = rating[rating["userId"] == value]
    graph_val = graph_val[["movieId","rating"]]
    genre_val = tags[tags["movieId"].isin(graph_val["movieId"])]
    # genre_val = genre_val[['split_genre']].value_counts().to_dict("records")
    genre_val = genre_val.groupby(by="split_genre").count()
    return genre_val

def get_movie_on_recommend_user(rating:pd.DataFrame,movie:pd.DataFrame,userid:int):
    pivot = rating.pivot(index='userId',columns='userId',values='rating')
    pivot.fillna(0,inplace=True)
    

def recomen_movie_on_score_movie(rating:pd.DataFrame,movie:pd.DataFrame,userid:int) -> pd.DataFrame:
    pivot = rating.pivot(index='movieId',columns='userId',values='rating')
    pivot.fillna(0,inplace=True)
    neighbour_ids = []
    rating_high_movie = rating[rating['userId']==userid]
    rating_high_movie = rating_high_movie[rating_high_movie['rating']==rating_high_movie['rating'].max()]['movieId']
    random_film = np.random.randint(0,len(rating_high_movie))
    rand_film_id = rating_high_movie.iloc[random_film]
    rating_pivot_value = pivot[pivot.index==rand_film_id]
    k = 8
    kNN = NearestNeighbors(n_neighbors=8, algorithm="brute", metric='cosine')
    kNN.fit(pivot)
    movie_vec = rating_pivot_value
    neighbour = kNN.kneighbors(movie_vec,n_neighbors=k ,return_distance=False)
    for i in range(0,k):
        n = neighbour.item(i)
        neighbour_ids.append(n)
    movie_name_film = movie[movie['movieId'].isin(neighbour_ids)][['title','genres']]
    title_based = movie[movie['movieId']==rand_film_id]['title'].values[0]
    return movie_name_film,title_based

def unique_val(df:pd.DataFrame)->list:
    df['split_genre'] = df["genres"].str.split("|")
    df = df.explode('split_genre')
    return df['split_genre'].unique()
def uniq_val_user(df:pd.DataFrame)->list:
    return df['userId'].unique()

def prep_genre(df:pd.DataFrame)->pd.DataFrame:
    df['split_genre'] = df["genres"].str.split("|")
    df = df.explode('split_genre')
    return df

def check_count_movie(df:pd.DataFrame,year:int=None,year_1:int=None)->pd.DataFrame:
    df = df["year"].copy()
    df = df[df>0] #Убираем из выборки фильмы без даты
    # print(df)
    if year is not None:
        df = df[(df>=year)&(df<=year_1)]
    groupby = df.groupby(by=df).count()
    return groupby
    # groupby.plot(ylabel='Кол-во фильмов в год',legend=True)

def high_score_movie(rating:pd.DataFrame,df:pd.DataFrame,year:int=None,year_1:int=None,type_agg:str="mean") -> pd.DataFrame:
    df = df["year"].copy()
    df = df[df>0]
    if year is not None:
        df = df[(df>=year)&(df<=year_1)]
    # print(df.index)
    # print(rating[rating["movieId"]==7815])
    rating = rating[rating["movieId"].isin(df.index)]
    # print(rating)
    # rating = rating.groupby(by='movieId').agg({"rating":[type_agg,"count"]})
    
    return rating.groupby(by='movieId').agg({"rating":[type_agg,"count"]})
    
def recomen_movie_on_genre(df:pd.DataFrame,df_2:pd.DataFrame,genre:list=[]):
    if len(genre) != 0:
        df['one'] = [1]* df.shape[0]
        pivot_data = df.pivot(index='movieId',values='one',columns='split_genre')
        pivot_data.fillna(0,inplace=True)
        test_data_input = pd.DataFrame(columns=pivot_data.columns)
        # input_genre = ['action','scifi','adventure']

        prepare_date = [1  if i in genre else 0 for i in pivot_data.columns]

        test_data_input.loc[0] = prepare_date
        test_val = test_data_input.values.reshape(1,-1)
        # corr_values = np.array([cosine_similarity(pivot_data.values[i].reshape(1,-1),test_val)[0,0] for i in range(len(pivot_data.values))]) # Предпочитаемый выброр
        corr_values = np.array([np.corrcoef(pivot_data.values[i], test_val)[0, 1] for i in range(len(pivot_data.values))]) # Предпочитаемый выброр
        indices = np.argpartition(corr_values, -30)[-30:]
        # arr = np.random.permutation(0, len(indices), 5,replace=False)
        arr = random.sample(range(len(indices)), 10)
        indices_rand = indices[arr]
        print(arr)
    # print(df_2.loc[indices].columns)
        return df_2.loc[indices_rand]
    if len(genre) == 0:
        return []