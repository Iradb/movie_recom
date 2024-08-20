import dash
from dash import html, Input, Output, dcc, dash_table,Dash,State
from flask import send_from_directory
from app.utils.utils import prep_genre
from flask import url_for,redirect
from app.callback.callback import get_callbacks
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os

movie = pd.read_csv("dataset/movies.csv")
rating = pd.read_csv("dataset/ratings.csv")
tags = prep_genre(movie)
# print(movie)

app = dash.Dash(__name__,use_pages=True)

@app.server.route('/assests/css/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'assests/css')
    return send_from_directory(static_folder, path)


@app.server.route('/')
def index():
    return redirect("/plots")

app.layout = html.Div([
    html.Div([
        html.Link(
            rel='stylesheet',
            href='/assets/css/style.css'
        ),
        html.Link(
            rel='stylesheet',
            href='/assets/css/analytics_style.css'
        ),
   html.Header(children=[dcc.Location(id='url', refresh=False),
    html.Div(
        html.Ul(
            children=[
            dcc.Link(html.Li("Графики"),href="/",className="header_LI"),
            dcc.Link(html.Li("Рекомендации"),href="/recomm",className="header_LI"),
            dcc.Link(html.Li("Пользователи"),href="/score",className="header_LI")],
        className="Header__ul")
        ,
        className="Header__container",
    )],
className="Header",id="Header"),
    dash.page_container
]),])


# app.layout = html.Div(children=[layout_header])
get_callbacks(app,movie,tags,rating)
if __name__ == '__main__':
    # app.callback()
    app.run_server(debug=True)