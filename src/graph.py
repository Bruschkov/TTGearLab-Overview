import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

from src.util import sort_unique


COLOR_SCALE = px.colors.qualitative.Plotly


class Plot:
    def __init__(
            self,
            title: str,
            raw_data: pd.DataFrame,
            x_dim: str,
            y_dim: str,
            type_colors_scale=COLOR_SCALE,
    ):
        self.title = title
        self.raw_data = raw_data
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.type_colors = self._get_type_colors(type_colors_scale, raw_data)

    def _get_type_colors(self, type_colors_scale, raw_data):
        return {
            t: type_colors_scale[i]
            for i, t in enumerate(sort_unique(raw_data['Type']))
        }

    def _marker_config(self, type: str, type_data: pd.DataFrame) -> dict:
        return dict(
            color=self.type_colors.get(type, 'grey'),
        )

    def _custom_data_cols(self) -> list:
        return ['Brand', 'Name', 'Type']

    def _hover_template(self) -> str:
        return f'''
        <b>%{{customdata[0]}} %{{customdata[1]}}</b> 
        <br>Type = %{{customdata[2]}} 
        <br>{self.x_dim} = %{{x}}
        <br>{self.y_dim} = %{{y:.2f}}
        '''

    def plot(self, filtered_data: pd.DataFrame):
        fig = go.Figure()

        fig.add_hline(y=1, line_width=1.5, line_dash="dash", line_color="grey", opacity=.4)
        fig.add_vline(x=1, line_width=1.5, line_dash="dash", line_color="grey", opacity=.4)

        for type in filtered_data.Type.unique():
            type_data = filtered_data[filtered_data['Type'] == type]
            fig.add_trace(
                go.Scatter(
                    x=type_data[self.x_dim],
                    y=type_data[self.y_dim],
                    mode='markers',
                    marker=self._marker_config(type, type_data),
                    legend="legend",
                    showlegend=True,
                    customdata=list(type_data[self._custom_data_cols()].to_numpy()),
                    name=type,
                ),
            )

        fig.update_traces(hovertemplate=self._hover_template() + "<extra></extra>")

        fig.update_layout(
            title=self.title,
            legend={
                "title": "Blade Type",
                'itemsizing': 'constant',
                'itemclick': False,
                'itemdoubleclick': False,
            },
        )
        fig.update_xaxes(
            title_text=self.x_dim,
            autorangeoptions=dict(
                include=1
            )
        )
        fig.update_yaxes(
            title_text=self.y_dim,
            autorangeoptions=dict(
                include=1
            )
        )
        return fig


class SizeDimPlot(Plot):
    def __init__(
            self,
            title: str,
            raw_data: pd.DataFrame,
            x_dim: str,
            y_dim: str,
            size_dim: str,
            type_colors_scale=COLOR_SCALE,
            marker_size_function=lambda x: x,
            legend_marker_size_function=lambda x: x,
            max_marker_size: int = 25.,
    ):
        super().__init__(title, raw_data, x_dim, y_dim, type_colors_scale)
        self.size_dim = size_dim
        self._marker_size = marker_size_function
        self._legend_marker_size = legend_marker_size_function
        self.max_marker_size = max_marker_size

    def _marker_config(self, type: str, type_data: pd.DataFrame) -> dict:
        basic_marker_config = super()._marker_config(type, type_data)
        size_specific_marker_config = dict(
            size=self._marker_size(type_data[self.size_dim]),
            sizemode='area',
            sizeref=2. * max(self._marker_size(self.raw_data[self.size_dim])) / (self.max_marker_size ** 2),
            sizemin=4,
        )
        return dict(**basic_marker_config, **size_specific_marker_config)

    def _custom_data_cols(self) -> list:
        return super()._custom_data_cols() + [self.size_dim]

    def _hover_template(self) -> str:
        base_template = super()._hover_template()
        return base_template + f"<br>{self.size_dim} = %{{customdata[3]}}"

    def plot(self, filtered_data: pd.DataFrame):
        fig = super().plot(filtered_data)

        legend_marker_sizes = np.array([1, 1.5, 2])
        for legend_marker_size in legend_marker_sizes:
            fig.add_scatter(
                x=[0],
                y=[0],
                mode='markers',
                name=f'{legend_marker_size}',
                marker=dict(
                    color='black',
                    size=self._legend_marker_size(legend_marker_size),
                    line={
                        'width': 1,
                        'color': 'black'
                    },
                    sizeref=2. * max(self._legend_marker_size(legend_marker_sizes)) / (40. ** 2),
                    sizemin=4,

                ),
                visible='legendonly',
                legend="legend2",
            )

        fig.update_layout(
            legend2={
                "title": self.size_dim,
                "y": 0.0,
                'itemclick': False,
                'itemdoubleclick': False,
            }
        )
        return fig


class TrendLinePlot(Plot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trend_line = self._fit_trend_line_regression(self.raw_data)

    def _fit_trend_line_regression(self, raw_data):
        return LinearRegression().fit(
            raw_data[self.x_dim].values.reshape(-1, 1),
            raw_data[self.y_dim],
        )

    def plot(self, filtered_data: pd.DataFrame):
        fig = super().plot(filtered_data)

        x_start = min(filtered_data[self.x_dim].min(), 1)
        x_end = filtered_data[self.x_dim].max()
        y_start, y_end = self.trend_line.predict([[x_start], [x_end]])

        fig.add_trace(go.Scatter(
            x=[x_start, x_end],
            y=[y_start, y_end],
            mode='lines',
            opacity=0.2,
            line=dict(
                color='red',
                width=2,
                dash='dash'
            ),
            legend="legend2",
            name="Trend Line"
        ))

        fig.update_layout(
            legend2={
                "y": 0.0,
                'itemclick': False,
                'itemdoubleclick': False,
            }
        )

        return fig