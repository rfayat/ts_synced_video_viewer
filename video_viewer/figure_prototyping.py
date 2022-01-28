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
    "trace": {
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
        }
    }
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Time series
n_points = 1800
df = pd.DataFrame(np.random.random((n_points, 3)), columns=["x", "y", "z"])
fig = Figure.from_dataframe(
    df=df,
    trace_kwargs=config["trace"]["trace_kwargs"],
    range_slider_visible=True)
to_fill = np.zeros(n_points, dtype=bool)
to_fill[:100] = True
to_fill[500:600] = True
to_fill[1000:1800] = True
fig = fig.fill_areas(df.index.values, to_fill, y_b=-1, color="blue")
fig = fig.fill_areas(df.index.values, ~to_fill, y_b=-1, color="red")

# Layout of the app
app.layout = html.Div([
    dcc.Graph(id="data_graph", figure=fig),
    html.Div(["coucou"], id="debugging_text")
])

if __name__ == "__main__":
    app.run_server(debug=True)
