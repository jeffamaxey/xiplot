from dash import html, dcc

from dashapp.services.data_frame import get_data_files

import dash_uploader as du


TABS = [
    dcc.Tab(label="Data", value="control-data-tab"),
    dcc.Tab(label="Plots", value="control-plots-tab"),
    dcc.Tab(label="Clusters", value="control-clusters-tab"),
]


def app_logo():
    layout = html.Div(
        [html.H1("Dash App 2022")], style={"text-align": "center", "margin": 20}
    )
    return layout


def control():
    layout = html.Div(
        [
            app_logo(),
            dcc.Tabs(id="control-tabs", value="control-data-tab", children=TABS),
            control_data_content(),
            control_plots_content(),
            control_clusters_content(),
        ],
        style={
            "width": "25%",
            "display": "inline-block",
            "float": "right",
            "background-color": "#dffcde",
            "height": "600px",
            "border-radius": "8px",
        },
    )

    return layout


def control_data_content():
    layout = html.Div(
        [
            layout_wrapper(
                component=dcc.Dropdown(
                    get_data_files(), id="data_files", clearable=False
                ),
                title="Choose a data file",
                style={"width": "98%"},
            ),
            html.Div(
                [
                    html.Button(
                        "Load the data file",
                        id="submit-button",
                        n_clicks=0,
                        className="btn btn-primary",
                    ),
                ],
                style={
                    "padding-top": "2%",
                },
            ),
            html.Div(
                [html.H4(id="data_file_load_message")],
                id="data_file_load_message-container",
                style={"display": "none"},
            ),
            html.Div([du.Upload(id="file_uploader")], style={"padding-top": "2%"}),
        ],
        id="control_data_content-container",
        style={"display": "none"},
    )

    return layout


def control_plots_content():
    layout = html.Div(
        [
            layout_wrapper(
                component=dcc.Dropdown(
                    options=["Scatterplot", "Histogram", "Heatmap"], id="plot_type"
                ),
                title="Select a plot type",
                style={"width": "98%"},
            ),
            html.Button("Add", id="new_plot-button"),
        ],
        id="control_plots_content-container",
        style={"display": "none"},
    )

    return layout


def control_clusters_content():
    layout = html.Div(
        [
            layout_wrapper(
                component=dcc.Dropdown(
                    options=[i for i in range(2, 11)], id="cluster_amount"
                ),
                title="cluster amount",
                style={"width": "23%", "display": "inline-block", "padding-left": "2%"},
            ),
            layout_wrapper(
                component=dcc.Dropdown(id="cluster_feature", multi=True),
                title="features",
                style={"width": "50%", "display": "inline-block", "padding-left": "2%"},
            ),
            html.Div(
                [html.Button("Run", id="cluster-button")],
                style={"padding-left": "2%", "padding-top": "2%"},
            ),
            html.Div(
                [html.H4(id="clusters_created_message")],
                id="clusters_created_message-container",
                style={"display": "none"},
            ),
        ],
        id="control_clusters_content-container",
        style={"display": "none"},
    )

    return layout


def smiles():
    layout = html.Div([html.Div(id="smiles_image")], style={"float": "left"})

    return layout


def layout_wrapper(component, id="", style=None, css_class=None, title=None):
    layout = html.Div(
        children=[html.Div(title), component],
        id=id,
        style=style
        if style
        else {
            "width": "40%",
            "display": "inline-block",
            "padding-left": "2%",
        },
        className=css_class,
    )

    return layout
