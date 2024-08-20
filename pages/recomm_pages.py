import dash,dash_table
import flask
import pandas as pd
from dash import dcc, html, Input, Output, State
from app.utils.utils import unique_val,recomen_movie_on_genre
from run import movie,tags

dash.register_page(__name__, path="/recomm",title="Рекомендательная система")
layout  = html.Div(children=[
    html.Div(children=[html.Div("Выберите жанры для рекомендации фильмов",className="recom_P"),
                       dcc.Checklist(id="check",options=[{"label":i,"value":i} for i in unique_val(movie) if i != "(no genres listed)"],className="recomm_check")],
                                            className="recomm_checkout"),
                       dash_table.DataTable(id="table",
                                            data=None,
                                            columns=[{"name":"Наименование","id":"title"},{"name":"Жанры","id":"genres"}],
                                            style_header={'textAlign': 'left'},
                                            style_cell={'textAlign': 'left'}),
],className="Body")