import pandas as pd
import plotly.express as px

from dash import html, dcc, Output, Input, State, MATCH

from dashapp.utils.layouts import layout_wrapper, delete_button, cluster_dropdown
from dashapp.graphs import Graph


class Histogram(Graph):
    @staticmethod
    def register_callbacks(app, df_from_store, df_to_store):
        @app.callback(
            Output({"type": "histogram", "index": MATCH}, "figure"),
            Input({"type": "x_axis_histo", "index": MATCH}, "value"),
            Input({"type": "hg_selection_cluster_dropdown", "index": MATCH}, "value"),
            Input({"type": "hg_comparison_cluster_dropdown", "index": MATCH}, "value"),
            Input("clusters_column_store", "data"),
            State("data_frame_store", "data"),
            prevent_initial_call=True,
        )
        def render_histogram(x_axis, selection, comparison, kmeans_col, df):
            df = df_from_store(df)
            if len(kmeans_col) == df.shape[0]:
                df["Clusters"] = kmeans_col
            fig = make_fig_property(df, x_axis, selection, comparison, kmeans_col)

            return fig

    @staticmethod
    def create_new_layout(index, df, columns):
        return html.Div(
            [
                delete_button("plot-delete", index),
                dcc.Graph(
                    id={"type": "histogram", "index": index},
                    figure=px.histogram(df, columns[0]),
                ),
                layout_wrapper(
                    component=dcc.Dropdown(
                        id={"type": "x_axis_histo", "index": index},
                        value=columns[0],
                        clearable=False,
                        options=columns,
                    ),
                    css_class="dd-single",
                    title="x axis",
                ),
                cluster_dropdown(
                    "hg_selection_cluster_dropdown", index, selection=True
                ),
                cluster_dropdown(
                    "hg_comparison_cluster_dropdown", index, selection=False
                ),
            ],
            id={"type": "histogram-container", "index": index},
            className="graphs",
        )


def make_fig_property(df, property, cluster, comparison, clusters):
    props_a = []
    props_b = []

    for c, p in zip(clusters, df[property]):
        if c == cluster or cluster == "all":
            props_a.append(p)

        if c == comparison or comparison == "all":
            props_b.append(p)

    if cluster == comparison:
        props_b = []

    props = pd.DataFrame(
        {
            "Clusters": [cluster for _ in props_a] + [comparison for _ in props_b],
            property: props_a + props_b,
        }
    )

    fig_property = px.histogram(
        props,
        x=property,
        color="Clusters",
        hover_data={
            "Clusters": False,
            property: False,
        },
        color_discrete_map={
            "all": px.colors.qualitative.Plotly[0],
            **{f"c{i+1}": c for i, c in enumerate(px.colors.qualitative.Plotly[1:])},
        },
        opacity=0.75,
        histnorm="probability density",
    )

    fig_property.update_layout(
        hovermode="x unified",
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        barmode="overlay",
        yaxis=dict(
            tickformat=".2%",
        ),
    )

    return fig_property
