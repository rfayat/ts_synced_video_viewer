"""Time series plotting component.

Author: Romain Fayat, January 2022
"""
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class Figure(go.Figure):
    "Extend ploty Figure to make the instantiation easier."

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, trace_kwargs,
                       range_slider_visible=False):
        "Create a figure and add columns of a dataframe as traces."
        self = cls()
        # Create a trace for each column in the dataframe
        # The index is used as x values
        for col_name, kwargs in trace_kwargs.items():
            if col_name not in df:
                break
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
        if range_slider_visible:
            self.update_xaxes(rangeslider_visible=True)
        return self

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
