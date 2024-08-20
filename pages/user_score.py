import dash
from dash import html, Input, Output, dcc, dash_table,Dash,State
from app.utils.utils import uniq_val_user
from run import rating

dash.register_page(__name__, path="/score",title="Оценки пользователей")

layout = html.Div(
    [html.Div(
        dcc.Dropdown(options=[{"label":i,"value":i} for i in uniq_val_user(rating)],
                     className="dropdown_score",placeholder="Выберите id пользователя",id="dropdown_score_id"),
    ),
    html.Div(
        [html.Div(id="genre_plot",className="Genre_plot_container"),
         html.Div([
       
                  ],id="recomm_system_user",className="recomm_system_user_container")],
    className="Genre_plot"),
    html.Div([
        dash_table.DataTable(id="table_1",
                                            data=None,
                                            columns=[{"name":"Наименование","id":"title"},
                                                     {"name":"Жанры","id":"genres"},
                                                     {"name":"Оценка","id":"rating"}],
                                            style_header={'textAlign': 'left'},
                                            style_cell={'textAlign': 'left'},page_size=10)
    ],className="recomm_system_user")],

    className="Body",
)