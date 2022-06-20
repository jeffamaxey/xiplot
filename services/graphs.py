from re import sub
from dash import html, dcc
from matplotlib.pyplot import bar
import plotly.express as px
import services.dash_layouts as dash_layouts


class Scatterplot:
    def __init__(self, df, x_axis=None, y_axis=None, color=None, symbol=None, subset_points=None):
        self.__df = df
        self.__x_axis = x_axis
        self.__y_axis = y_axis
        self.__color = color
        self.__symbol = symbol
        self.__subset_points = subset_points

    def set_axes(self, x_axis, y_axis):
        self.__x_axis = x_axis
        self.__y_axis = y_axis

    def set_color(self, variable):
        self.__color = variable

    def set_subset_points(self, subset_points):
        self.__subset_points = subset_points

    def set_symbol(self, variable):
        self.__symbol = variable

    def create_plot(self):
        fig = px.scatter(self.__df, self.__x_axis,
                         self.__y_axis, self.__color, self.__symbol)
        return fig

    def render(self):
        fig = self.create_plot()
        fig.show()

    def get_layout(self):
        layout = dash_layouts.scatterplot()
        return layout


class Histogram:
    def __init__(self, df, x_axis=None, y_axis=None, color=None, color_dicrete_sequence=None, barmode=None, subset_points=None):
        self.__df = df
        self.__x_axis = x_axis
        self.__y_axis = y_axis
        self.__color = color
        self.__color_discrete_sequence = color_dicrete_sequence
        self.__barmode = barmode
        self.__subset_points = subset_points

    def set_axes(self, x_axis, y_axis=None):
        self.__x_axis = x_axis
        self.__y_axis = y_axis

    def set_color(self, variable):
        self.__color = variable

    def set_color_discrete_sequence(self, value):
        self.__color_discrete_sequence = value

    def set_subset_points(self, subset_points):
        self.__subset_points = subset_points

    def set_barmode(self, value):
        self.__barmode = value

    def create_plot(self):
        fig = px.histogram(self.__df, self.__x_axis,
                           self.__y_axis, self.__color, color_discrete_sequence=self.__color_discrete_sequence, barmode=self.__barmode)
        return fig

    def add_trace(self, fig, fig_2):
        fig.add_trace(fig_2)

        #px.histogram(data_frame=selected_df, x=x_axis, color_discrete_sequence=px.colors.qualitative.Dark2).data[0]
        # fig.show()

        return fig

    def render(self):
        fig = self.create_plot()
        fig.show()

    def get_layout(self):
        layout = dash_layouts.histogram()
        return layout
