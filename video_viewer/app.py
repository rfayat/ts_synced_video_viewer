"""Graphical User Interface for visualizing video synced with time series.

Author: Romain Fayat, January 2022
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from video_viewer.plots import Figure
from video_viewer.video import RandomImageGenerator
from quart import Quart, websocket
from dash.dependencies import Output, Input
from dash_extensions import WebSocket
import threading
import asyncio
import base64


COLORS = {"navbar": "#17A2B8"}

# Create the app and the layout
server = Quart(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Synced Video Viewer"

# Top navigation bar
navbar = dbc.Navbar(
    [html.A([dbc.NavbarBrand("Synced Video Viewer")]), ],
    color=COLORS["navbar"],
    dark=True,
)
# Time series
trace_kwargs = {
  "x": {"line": {"color": "red"}},
  "y": {"line": {"color": "green"}},
  "z": {"line": {"color": "blue"}},
}
fig = Figure.from_csv("data/time_series.csv",
                      index_col="fnum",
                      trace_kwargs=trace_kwargs)


async def stream(camera, delay=None):
    while True:
        if delay is not None:
            await asyncio.sleep(delay)  # add delay if CPU usage is too high
        frame = camera.get_frame()
        await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")  # noqa E501


@server.websocket("/stream0")
async def stream0():
    camera = RandomImageGenerator()
    await stream(camera, delay=1/30)


# Global layout of the app
app.layout = html.Div([
    navbar,
    html.Img(style={'width': '40%', 'padding': 10}, id="v0"),
    WebSocket(url="ws://127.0.0.1:5000/stream0", id="ws0"),
    dcc.Graph(id="data_graph", figure=fig),
])

app.clientside_callback("function(m){return m? m.data : '';}",
                        Output("v0", "src"), Input("ws0", "message"))

if __name__ == "__main__":
    # app.run_server(host="127.0.0.1", debug=True)
    threading.Thread(target=app.run_server).start()
    server.run()
