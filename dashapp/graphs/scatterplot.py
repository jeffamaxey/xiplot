import json

import numpy as np
import pandas as pd
import plotly.express as px

from dash import html, dcc, Output, Input, State, MATCH

from dashapp.utils.layouts import layout_wrapper, delete_button
from dashapp.utils.dataframe import get_numeric_columns
from dashapp.graphs import Graph


class Scatterplot(Graph):
    @staticmethod
    def register_callbacks(app, df_from_store, df_to_store):
        @app.callback(
            Output({"type": "scatterplot", "index": MATCH}, "figure"),
            Output({"type": "jitter-slider", "index": MATCH}, "max"),
            Input({"type": "scatter_x_axis", "index": MATCH}, "value"),
            Input({"type": "scatter_y_axis", "index": MATCH}, "value"),
            Input({"type": "scatter_target_color", "index": MATCH}, "value"),
            Input({"type": "scatter_target_symbol", "index": MATCH}, "value"),
            Input({"type": "jitter-slider", "index": MATCH}, "value"),
            Input("clusters_column_store", "data"),
            State("data_frame_store", "data"),
            prevent_initial_call=True,
        )
        def tmp(x_axis, y_axis, color, symbol, jitter, kmeans_col, df):
            return Scatterplot.render_scatterplot(
                x_axis, y_axis, color, symbol, jitter, kmeans_col, df=df_from_store(df)
            )

    @staticmethod
    def render_scatterplot(x_axis, y_axis, color, symbol, jitter, kmeans_col, df):
        if len(kmeans_col) == df.shape[0]:
            df["Clusters"] = kmeans_col

        jitter_max = (df[x_axis].max() - df[x_axis].min()) * 0.05
        if jitter:
            jitter = float(jitter)
        if type(jitter) == float:
            if jitter > 0:
                Z = df[[x_axis, y_axis]].to_numpy("float64")
                Z = np.random.normal(Z, jitter)
                jitter_df = pd.DataFrame(Z, columns=[x_axis, y_axis])
                df[["jitter-x", "jitter-y"]] = jitter_df[[x_axis, y_axis]]
                x_axis, y_axis = "jitter-x", "jitter-y"

        fig = px.scatter(
            data_frame=df,
            x=x_axis,
            y=y_axis,
            color=color,
            symbol=symbol,
            color_discrete_map={
                "all": px.colors.qualitative.Plotly[0],
                **{
                    f"c{i+1}": c for i, c in enumerate(px.colors.qualitative.Plotly[1:])
                },
                "*": "#000000",
            },
            custom_data=["auxiliary"] if "auxiliary" in df.columns else None,
            hover_data={"Clusters": False},
            render_mode="webgl",
        )
        fig.update_layout(showlegend=False, uirevision=json.dumps([x_axis, y_axis]))
        fig.update(layout_coloraxis_showscale=False)

        return fig, jitter_max

    @staticmethod
    def create_new_layout(index, df, columns):
        x = None
        y = None
        num_columns = get_numeric_columns(df, columns)
        for c in num_columns:
            if "x-" in c or " 1" in c:
                x = c
            elif "y-" in c or " 2" in c:
                y = c
                break
        return html.Div(
            children=[
                delete_button("plot-delete", index),
                dcc.Graph(
                    id={"type": "scatterplot", "index": index},
                    figure=px.scatter(
                        df, x, y, custom_data=["auxiliary"], render_mode="webgl"
                    ),
                ),
                layout_wrapper(
                    component=dcc.Dropdown(
                        id={"type": "scatter_x_axis", "index": index},
                        options=num_columns,
                        value=x,
                        clearable=False,
                    ),
                    css_class="dd-double-left",
                    title="x",
                ),
                layout_wrapper(
                    component=dcc.Dropdown(
                        id={"type": "scatter_y_axis", "index": index},
                        options=num_columns,
                        value=y,
                        clearable=False,
                    ),
                    css_class="dd-double-right",
                    title="y",
                ),
                layout_wrapper(
                    component=dcc.Dropdown(
                        id={"type": "scatter_target_color", "index": index},
                        options=columns,
                        value="Clusters",
                    ),
                    css_class="dd-double-left",
                    title="target (color)",
                ),
                layout_wrapper(
                    component=dcc.Dropdown(
                        id={"type": "scatter_target_symbol", "index": index},
                        options=columns,
                    ),
                    css_class="dd-double-right",
                    title="target (symbol)",
                ),
                layout_wrapper(
                    component=dcc.Slider(
                        id={"type": "jitter-slider", "index": index},
                        min=0,
                        max=1,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    css_class="slider-single",
                    title="jitter",
                ),
            ],
            id={"type": "scatterplot-container", "index": index},
            className="graphs",
        )
