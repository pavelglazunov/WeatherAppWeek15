import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash
from dash.dependencies import Input, Output, State

from config.config import Config, load_config
from src.api import AccuWeatherApi
from src.exceptions import APIFetchException
from src.services import render

app = Dash(__name__)
app.layout = render.dom
colors = px.colors.qualitative.Plotly


@app.callback(
    Output('city-inputs', 'children'),
    Input('add-city-button', 'n_clicks'),
    State('city-inputs', 'children'),
)
def add_city_input(n_clicks, children):
    if n_clicks > 0:
        children.append(render.new_input(n_clicks))
    return children


@app.callback(
    Output("weather-graph", "figure"),
    Output("error-message", "children"),
    Input("submit-button", "n_clicks"),
    Input("city-inputs", "children"),
)
def update_graph(n_clicks, city_inputs):
    if n_clicks <= 0:
        return go.Figure(), ""

    dfs = []
    error_messages = []
    city_names = []
    for input_component in city_inputs:
        if input_component.get("props", {}).get("value"):
            city_names.append(input_component['props']['value'])
        else:
            input_id = input_component.get('props', {}).get('id', 'ID не найден')
            error_messages.append(f"Город {input_id} не найден")

    config: Config = load_config()
    api = AccuWeatherApi(config.api.key)

    for city_name in city_names:
        try:
            from_city_weathers = api.get_weather(city_name)
        except APIFetchException as err:
            error_messages.append(f"Ошибка для города '{city_name}': {err.message}")
            continue

        dfs.append(pd.DataFrame(from_city_weathers))

    fig = go.Figure()

    for i, (df, city) in enumerate(zip(dfs, city_names)):
        color = colors[i % len(colors)]
        fig.add_trace(render.new_scatter(
            df,
            "temperature_avg",
            f"Средняя температура в {city}",
            color,
        ))
        fig.add_trace(render.new_scatter(
            df,
            "temperature_max",
            f"Максимальная температура в {city}",
            color,
            is_dash=True,
        ))
        fig.add_trace(render.new_scatter(
            df,
            "temperature_min",
            f"Минимальная температура в {city}",
            color,
            is_dash=True,
        ))

    fig.update_layout(title="Прогноз погоды на 5 дней",
                      xaxis_title="Дата",
                      yaxis_title="Температура (°C)",
                      legend_title="Города")

    return fig, " и ".join(error_messages)
