import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html

dom = html.Div([
    html.H1("Погода в городах"),
    dcc.Dropdown(
        id='days-count-dropdown',
        options=[
            {'label': '1 день', 'value': 'days_1'},
            {'label': '2 дня', 'value': 'days_2'},
            {'label': '3 дня', 'value': 'days_3'},
            {'label': '4 дня', 'value': 'days_4'},
            {'label': '5 дней', 'value': 'days_5'},
        ],
        value='days_3',
        clearable=False,
        style={'width': '50%', 'margin': 'auto'}
    ),
    html.Div(id='city-inputs', children=[
        dcc.Input(id='city-0', type='text', placeholder='Введите город'),
        dcc.Input(id='city-1', type='text', placeholder='Введите город'),
    ]),
    html.Button("Добавить город", id='add-city-button', n_clicks=0),
    html.Button("Удалить город", id='remove-city-button', n_clicks=0),
    html.Button("Получить погоду", id="submit-button", n_clicks=0),
    html.Div(id='error-message', style={'color': 'red'}),

    html.Div(
        style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '20px'},
        children=[
            dcc.Graph(id="weather-graph-temperature"),
            dcc.Graph(id="weather-graph-wind"),
            dcc.Graph(id="weather-graph-humidity"),
            dcc.Graph(id="weather-graph-rain"),
        ]
    ),
    html.Div([
        html.H1("Интерактивная карта городов"),
        dcc.Graph(id="weather-map")
    ])
])


def new_input(input_id: int) -> dcc.Input:
    return dcc.Input(
        id=f'city-{input_id}',
        type='text',
        placeholder='Введите город',
    )


def new_scatter(df: pd.DataFrame, y: str, title: str, color, is_dash: bool = False):
    line = dict(color=color)
    if is_dash:
        line["dash"] = "dash"

    return go.Scatter(
        x=df["date"],
        y=df[y],
        mode="lines+markers",
        name=title,
        line=line,
    )
