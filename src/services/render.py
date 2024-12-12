import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html

dom = html.Div([
    html.H1("Погода в городах"),
    html.Div(id='city-inputs', children=[
        dcc.Input(id='city-0', type='text', placeholder='Введите город'),
        dcc.Input(id='city-1', type='text', placeholder='Введите город'),
    ]),
    html.Button("Добавить город", id='add-city-button', n_clicks=0),
    html.Button("Получить погоду", id="submit-button", n_clicks=0),
    dcc.Graph(id="weather-graph"),
    html.Div(id='error-message', style={'color': 'red'})
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
