import dash
from dash import callback
from dash import html, Input, Output, dcc, dash_table,Dash,State
from dash import html,dcc
import plotly.graph_objects as go
from app.utils.utils import unique_val,recomen_movie_on_genre
import plotly.express as px
from app.utils.utils import prepare_df,check_count_movie,high_score_movie,count_genre_on_user,recomen_movie_on_score_movie,check_and_rating
import pandas as pd
# from run import movie,tags
# from app.query.query import take_group,take_data_TCP
def get_callbacks(app:dash.Dash,movie:pd.DataFrame,tags:pd.DataFrame,rating:pd.DataFrame):
    @app.callback(
            Output("genre_plot","children"),
            Output("recomm_system_user","children"),
            Output("table_1","data"),
            Input("dropdown_score_id","value"),
    )
    def update_graph(value):
        print(value)
        if value is not None:
            take_data_rating = check_and_rating(rating,movie,value)
            genre_val = count_genre_on_user(value,rating,tags)
            figure = {'data': [go.Pie(values=genre_val['genres'].values,labels=genre_val.index.values)],
                        'layout': {'title': f'Просмотренные жанры у пользователя {value}',"height": "auto"}
                        }
            data_back,title_based = recomen_movie_on_score_movie(rating,movie,value)
            print(data_back['title'].values.tolist())
            back_html_table = [html.P(f"Рекомендуемые фильмы основаясь на оценке фильма {title_based}",className="recomm_system_user_title"),html.Div(
            html.Ul(
                    children=[html.Li(i) for i in data_back['title'].values.tolist()]
                   ,className="recomm_system_user_ul")
                )]
            return dcc.Graph(figure=figure),back_html_table,take_data_rating.to_dict("records")
        return html.Div(),html.Div(),[]

    @app.callback(
        Output("table","data"),
        Input("check","value")
    )
    def take_check_val(value) -> pd.DataFrame:
        if value != None:
            print(value)
            val_return = recomen_movie_on_genre(tags,movie,value)
            if type(val_return) is pd.DataFrame:
                return val_return[['title','genres']].to_dict('records')
            else:
                return []
                # return pd.DataFrame(columns=['title','genres'])
        pass
    @app.callback(
     Output("graph","children") ,
     Input("dropdown","value"),
     Input("dropdown_1","value"),
     Input("dropdown_2","value")
    )
    def update_graph(value,value_1:int,value_2:int):
        if value is not None:
            movie = pd.read_csv("dataset/movies.csv")
            if value_1 == "None":
                value_1 = None
            movie = prepare_df(movie)
            plot_graph = check_count_movie(movie,value_1,value_2)
            if value == 1:
                figure = {'data': [go.Scatter(y= plot_graph.values,x=plot_graph.index)],
                        'layout': {'title': f'Кол-во фильмов за {value_1} - {value_2}',"height": "auto"}
                        }
            elif value == 2:
                rating = pd.read_csv("dataset/ratings.csv")
                high_n = high_score_movie(rating=rating,df=movie,year=value_1,year_1=value_2,type_agg='mean')['rating']
                high_n = high_n[high_n["count"] > high_n.quantile(0.9).values[1]]
                high_n = high_n.nlargest(10,'mean')
                high_score_with_name = movie[movie["movieId"].isin(high_n.index)]
                figure = {'data': [go.Bar(x =high_score_with_name["title"], y =high_n["mean"])],
                        'layout': {'title': f'Популярные фильмы {value_1} - {value_2}', }
                        }
                
            
            return dcc.Graph(figure=figure)