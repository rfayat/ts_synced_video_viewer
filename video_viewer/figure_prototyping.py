"""Prototyping GUI for designing the figure layout.

Author: Romain Fayat, January 2022
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from video_viewer.plots import Figure
import threading
import pandas as pd
import numpy as np

config = {
    "figure": {
        "filepath_or_buffer": "data/time_series.csv",
        "index_col": "fnum",
        "trace_kwargs": {
            "x": {
                "mode": "lines",
                "hoverinfo": "skip",
                "line": {"color": "red"}
            },
            "y": {
                "mode": "lines",
                "hoverinfo": "skip",
                "line": {"color": "green"}
            },
            "z": {
                "mode": "lines",
                "hoverinfo": "skip",
                "line": {"color": "blue"}
            },
        },
        "fill_kwargs": {
            "cluster": {
                "y_b": -1,
                "y_t": 1,
            },
        },
    }
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Time series
n_points = 1800
df = pd.DataFrame(np.random.random((n_points, 3)) - .5,
                  columns=["x", "y", "z"])
cluster = np.zeros(n_points, dtype=int)
cluster[:100] = 1
cluster[300:600] = 1
cluster[1600:] = 1
cluster[100:300] = 2
cluster[1200:1400] = 2
df["cluster"] = cluster

fig = Figure.from_dataframe(
    df=df,
    trace_kwargs=config["figure"]["trace_kwargs"],
    fill_kwargs=config["figure"]["fill_kwargs"],
    range_slider_visible=True)

# Layout of the app
app.layout = html.Div([
    dcc.Graph(id="data_graph", figure=fig),
    html.Div(["coucou"], id="debugging_text")
])

if __name__ == "__main__":
    app.run_server(debug=True)
