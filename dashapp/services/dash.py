from dash import html, dcc

from dashapp.graphs.scatterplot import Scatterplot
from dashapp.graphs.histogram import Histogram
from dashapp.graphs.heatmap import Heatmap
from dashapp.graphs.barplot import Barplot
from dashapp.services import dash_layouts
from dashapp.ui.dash_callbacks import Callbacks


class DashApp:
    def __init__(self, app, df_from_store, df_to_store) -> None:
        self.app = app

        try:
            import dash_uploader as du

            du.configure_upload(app=self.app, folder="uploads", use_upload_id=False)
        except ImportError:
            pass

        PLOT_TYPES = {p.name(): p for p in [Scatterplot, Histogram, Heatmap, Barplot]}

        self.app.layout = html.Div(
            [
                dash_layouts.control(PLOT_TYPES),
                dcc.Store(id="data_frame_store"),
                dcc.Store(id="clusters_column_store"),
                dcc.Store(id="uploaded_data_file_store"),
            ],
            id="main",
        )

        self.cb = Callbacks(PLOT_TYPES)
        self.cb.init_callbacks(
            self.app, df_from_store=df_from_store, df_to_store=df_to_store
        )

        for plot_name, plot_type in PLOT_TYPES.items():
            plot_type.register_callbacks(
                app, df_from_store=df_from_store, df_to_store=df_to_store
            )
