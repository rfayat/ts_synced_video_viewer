"""Graphical User Interface for visualizing video synced with time series.

Author: Romain Fayat, January 2022
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from video_viewer.plots import Figure
from video_viewer.video import VideoCamera
from quart import Quart, websocket
from dash.dependencies import Output, Input, State
from dash_extensions import WebSocket
import threading
import asyncio
import base64

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

current_frame = 0  #  WARNING: GLOBAL variable for selecting the diplayed frame

# Create the app and the layout
server = Quart(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Synced Video Viewer"

# Top navigation bar
navbar = dbc.Navbar(
    [html.A([dbc.NavbarBrand("Synced Video Viewer")]), ],
    color="#37393d", dark=True,
)
# Time series
fig = Figure.from_csv(**config["trace"])
range_slider = dcc.Slider(id="center_slider", min=0, max=1800, step=1, value=0)
# Size of the window
input_width = dbc.InputGroup([
    dbc.InputGroupAddon("Size of the window", addon_type="prepend"),
    dbc.Input(min=10, max=1800, value=300, type="number", id="input_width")],
    className="mb-1",
)


async def stream(camera, delay=None):
    "Grab the current frame and send it to the websocket every delay seconds."
    global current_frame
    while True:
        if delay is not None:
            await asyncio.sleep(delay)  # add delay if CPU usage is too high
        frame = camera.get_frame(current_frame)
        await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")  # noqa E501


@server.websocket("/stream0")
async def stream0():
    "Websocket for streaming frames."
    camera = VideoCamera("data/video.avi")
    # The delay is introduced here to limit CPU usage
    await stream(camera, delay=1/100)


# Global layout of the app
app.layout = html.Div([
    navbar,
    html.Img(style={'width': '40%', 'padding': 10}, id="v0"),
    WebSocket(url="ws://127.0.0.1:5000/stream0", id="ws0"),
    dcc.Graph(id="data_graph", figure=fig),
    html.Div([range_slider], style={"padding": 10}),
    input_width,
    html.Div(["coucou"], id="debugging_text")
])

app.clientside_callback(
    """
    function(m){
        return m? m.data : '';
    }
    """,
    Output("v0", "src"),
    Input("ws0", "message")
)


@app.callback(Output("debugging_text", "children"),
              Output("data_graph", "figure"),
              Input("center_slider", "value"),
              Input("input_width", "value"))
def get_current_frame(center, width):
    "When interacting with the figure, update the current xaxis location."
    global fig
    global current_frame
    range_plot = [center - width / 2, center + width / 2]
    fig['layout']['xaxis'].update(range=range_plot)
    current_frame = center
    return [f"Center: {center}, Width: {width}"],  fig


if __name__ == "__main__":
    threading.Thread(target=app.run_server).start()
    server.run()
