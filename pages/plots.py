import dash
from dash import html, Input, Output, dcc, dash_table,Dash,State
from pages.header import layout_header


body_content = html.Div(
    children=[html.Div(
                    children=[dcc.Dropdown(id='dropdown',placeholder="Выберите график",
                                options=[{'label': 'Кол-во фильмов за год(а)', 'value': 1},
                                         {'label': 'Популярные фильмы', 'value': 2}],
                                            className="dropdown_graph"),
                              dcc.Dropdown(id='dropdown_1',placeholder="Выберите начала период",
                                options=[{"label":i,"value":i} for i in range(1910,2021)]+[{"label":"За весь период","value":"None"}],
                                            className="dropdown_graph_1",value=1910),
                              dcc.Dropdown(id='dropdown_2',placeholder="Выберите конец период",
                                options=[{"label":i,"value":i} for i in range(1910,2021)]+[{"label":"За весь период","value":"None"}],
                                            className="dropdown_graph_1",value=2020)],
        className="Body__container"),
              html.Div(
               className="Graph__container", 
              id="graph")],
    className="Body",
)


# layout = html.Div([body_content])

dash.register_page(__name__, path="/",title="Графики",layout=body_content)