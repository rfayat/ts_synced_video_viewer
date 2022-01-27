"""Time series plotting component.

Author: Romain Fayat, January 2022
"""
import plotly.graph_objects as go
import pandas as pd


class Figure(go.Figure):
    "Extend ploty Figure to make the instantiation easier."

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, trace_kwargs=None):
        "Create a figure and add columns of a dataframe as traces."
        self = cls()
        if trace_kwargs is None:
            trace_kwargs = {}
        # Create a trace for each column in the dataframe
        # The index is used as x values
        for col_name in df:
            # Additional kw arguments for the trace
            kw = trace_kwargs.get(col_name, {})
            trace = go.Scattergl(
                x=df.index.values,
                y=df[col_name].values,
                name=col_name,
                mode="lines",
                hoverinfo="skip",
                **kw)
            self.add_trace(trace)
        self.update_xaxes(rangeslider_visible=True)
        return self

    @classmethod
    def from_csv(cls, *args, trace_kwargs=None, **kwargs):
        "Create a figure using data stored as a csv."
        df = pd.read_csv(*args, **kwargs)
        return cls.from_dataframe(df=df, trace_kwargs=trace_kwargs)
