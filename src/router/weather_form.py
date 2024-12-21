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
    Output('city-inputs', 'children', allow_duplicate=True),
    Input('add-city-button', 'n_clicks'),
    State('city-inputs', 'children'),
    prevent_initial_call=True,
)
def add_city_input(n_clicks_add, children):
    if n_clicks_add > 0:
        children.append(render.new_input(n_clicks_add))

    return children


@app.callback(
    Output('city-inputs', 'children', allow_duplicate=True),
    Input('remove-city-button', 'n_clicks'),
    State('city-inputs', 'children'),
    prevent_initial_call=True,
)
def remove_city_input(n_clicks_add, children):
    if n_clicks_add > 0:
        children.pop(-1)

    return children


cache = {}


@app.callback(
    Output("weather-graph-temperature", "figure"),
    Output("weather-graph-wind", "figure"),
    Output("weather-graph-humidity", "figure"),
    Output("weather-graph-rain", "figure"),
    Output("weather-map", "figure"),
    Output("error-message", "children"),
    Input("submit-button", "n_clicks"),
    Input("city-inputs", "children"),
    Input("days-count-dropdown", "value"),
)
def update_graph(n_clicks, city_inputs, days_count):
    if n_clicks <= 0:
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), ""

    days = int(days_count.split("_")[1])

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

    map_data = []

    for city_name in city_names:
        try:
            if city_name in cache:
                from_city_weathers = cache[city_name]

            else:
                from_city_weathers = api.get_weather(city_name)
                cache[city_name] = from_city_weathers
            map_data.append({
                "lat": cache[city_name][-1]["locations_lat"],
                "lot": cache[city_name][-1]["locations_lot"],
                "city": city_name,
            })

        except APIFetchException as err:
            error_messages.append(f"Ошибка для города '{city_name}': {err.message}")
            continue

        dfs.append(pd.DataFrame(from_city_weathers))

    map_df = pd.DataFrame(map_data)

    temperature_fig = go.Figure()
    wind_fig = go.Figure()
    humidity_fig = go.Figure()
    rain_fig = go.Figure()

    for i, (base_df, city) in enumerate(zip(dfs, city_names)):
        df = base_df[:days]
        color = colors[i % len(colors)]
        temperature_fig.add_trace(render.new_scatter(
            df,
            "temperature_avg",
            f"Средняя температура в {city}",
            color,
        ))
        wind_fig.add_trace(render.new_scatter(
            df,
            "wind_speed",
            f"Средняя скорость в {city}",
            color,
        ))
        humidity_fig.add_trace(render.new_scatter(
            df,
            "humidity_avg",
            f"Влажность в {city}",
            color,
        ))
        rain_fig.add_trace(render.new_scatter(
            df,
            "rain_probability",
            f"Вероятность дождя в {city}",
            color,
        ))

    temperature_fig.update_layout(title=f"Прогноз температуры на {days} дней",
                                  xaxis_title="Дата",
                                  yaxis_title="Температура (°C)",
                                  legend_title="Города")
    wind_fig.update_layout(title=f"Прогноз ветра на {days} дней",
                           xaxis_title="Дата",
                           yaxis_title="Скорость (км/час)",
                           legend_title="Города")
    humidity_fig.update_layout(title=f"Прогноз влажности на {days} дней",
                               xaxis_title="Дата",
                               yaxis_title="Влажность (%)",
                               legend_title="Города")
    rain_fig.update_layout(title=f"Прогноз вероятности дождя на {days} дней",
                           xaxis_title="Дата",
                           yaxis_title="Вероятность (%)",
                           legend_title="Города")
    map_df = pd.concat(dfs)
    map_fig = px.scatter_mapbox(
        map_df,
        lat='locations_lat',
        lon='locations_lot',
        hover_name='city',
        mapbox_style='carto-positron',
        hover_data=["city", "temperature_avg", "wind_speed", "rain_probability", "humidity_avg"],
        zoom=5,
    )

    return temperature_fig, wind_fig, humidity_fig, rain_fig, map_fig, " и ".join(error_messages)
