"""Time series plotting component.

Author: Romain Fayat, January 2022
"""
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex


def map_values_to_colormap(values, cmap="viridis"):
    "Map a discrete set of values to a colormap."
    # Attribute each unique value to a number between 0 and 256
    values_unique = np.sort(np.unique(values))
    n_colors = len(values_unique)
    gradient = np.linspace(0, 256, n_colors).astype(int)

    # Grab the selected color map
    cmap_callable = plt.get_cmap(cmap)

    # Use the values to select a color and store it as hex in color_mapping
    color_mapping = {}
    for v, c in zip(values_unique, gradient):
        color = cmap_callable(c)
        color_hex = to_hex(color)
        color_mapping[v] = color_hex
    return color_mapping


class Figure(go.Figure):
    "Extend ploty Figure to make the instantiation easier."

    @classmethod
    def from_dataframe(cls,
                       df: pd.DataFrame,
                       trace_kwargs=None,
                       fill_kwargs=None,
                       range_slider_visible=False):
        "Create a figure and add columns of a dataframe as traces."
        self = cls()
        if trace_kwargs is not None:
            self.traces_from_dataframe(df, trace_kwargs)
        if fill_kwargs is not None:
            self.fill_from_dataframe(df, fill_kwargs)
        if range_slider_visible:
            self.update_xaxes(rangeslider_visible=True)
        return self

    def traces_from_dataframe(self, df, trace_kwargs):
        "Create traces for selected columns in a dataframe."
        # Create a trace for each column in the dataframe
        # The index is used as x values
        for col_name, kwargs in trace_kwargs.items():
            if col_name not in df:
                continue
            # Default kwargs if missing in kwargs
            default_kwargs = {"mode": "lines", "hoverinfo": "skip"}
            kw = {**default_kwargs, **kwargs}
            # Create the trace and add it to the figure
            trace = go.Scattergl(
                x=df.index.values,
                y=df[col_name].values,
                name=col_name,
                **kw)
            self.add_trace(trace)

    def fill_from_dataframe(self, df, fill_kwargs):
        "Fill areas of the plot depending on selected columns in a dataframe."
        x = df.index.values
        for col_name, kwargs in fill_kwargs.items():
            if col_name not in df:
                continue
            values = df[col_name].values
            values_unique = np.unique(np.sort(values))
            color_mapping = map_values_to_colormap(values_unique)
            for v in values_unique:
                color = color_mapping[v]
                self.fill_areas(x, where=values == v, color=color, **kwargs)

    @classmethod
    def from_csv(cls, *args, trace_kwargs=None,
                 range_slider_visible=False,
                 **kwargs):
        "Create a figure using data stored as a csv."
        df = pd.read_csv(*args, **kwargs)
        return cls.from_dataframe(df=df,
                                  range_slider_visible=range_slider_visible,
                                  trace_kwargs=trace_kwargs)

    def fill_areas(self, x, where, y_t=1, y_b=0, color="blue", opacity=.2):
        """Shade rectangles along the x axis.

        x: array
            x coordinates matching the x axis.

        where: array of boolean, same length as x
            Booleans indicating the x coordinates that must be shaded.

        y_t, y_b, scalars
            Top and bottom bounds of the shaded areas.
        """
        x_l_all = np.argwhere(np.append(where[0], ~where[:-1] & where[1:]))
        x_r_all = np.argwhere(np.append(where[:-1] & ~where[1:], where[-1]))
        for x_l, x_r in np.c_[x_l_all, x_r_all]:
            rectangle = go.Scattergl(
                x=[x_l, x_r, x_r, x_l, x_l],
                y=[y_t, y_t, y_b, y_b, y_t],
                mode="lines",
                fill="toself",
                hoverinfo="skip",
                showlegend=False,
                line_color=color,
                fillcolor=color,
                opacity=opacity,
            )
            self.add_trace(rectangle)
        return self
