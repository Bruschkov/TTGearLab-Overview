import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


COLOR_SCALE = px.colors.qualitative.Plotly
TYPE_COLORS = {
    '5-Ply': COLOR_SCALE[0],
    '7-Ply': COLOR_SCALE[1],
    'Carbon Inner': COLOR_SCALE[2],
    'Carbon Outer': COLOR_SCALE[3],
}


class Plot:
    def __init__(
            self,
            title: str,
            raw_data: pd.DataFrame,
            x_dim: str,
            y_dim: str,
            size_dim: str,
            type_colors: dict[str, str] = TYPE_COLORS,
            marker_size_function=lambda x: x,
            legend_marker_size_function=lambda x: x,
    ):
        self.title = title
        self.raw_data = raw_data
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.size_dim = size_dim
        self.type_colors = type_colors
        self._marker_size = marker_size_function
        self._legend_marker_size_function = legend_marker_size_function

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
                    marker=dict(
                        color=self.type_colors.get(type, 'grey'),
                        size=self._marker_size(type_data[self.size_dim]),
                        sizemode='area',
                        sizeref=2. * max(self._marker_size(self.raw_data[self.size_dim])) / (40. ** 2),
                        sizemin=4,
                    ),
                    legend="legend",
                    showlegend=True,
                    customdata=list(type_data[['Brand', 'Name', 'Type', self.size_dim]].to_numpy()),
                    name=type,
                ),
            )
        fig.update_traces(
            hovertemplate=
            '''
        <b>%{customdata[0]} %{customdata[1]}</b> <br>
        Vp = %{x} <br>
        Vl/Vp = %{y:.2f} <br>
        Ep = %{customdata[3]} <br>
        Type = %{customdata[2]}
        <extra></extra>
            '''
        )

        legend_marker_sizes = np.array([1, 1.5, 2])
        for legend_marker_size in legend_marker_sizes:
            fig.add_scatter(
                x=[0],
                y=[0],
                mode='markers',
                name=f'{legend_marker_size}',
                marker=dict(
                    color='black',
                    size=self._legend_marker_size_function(legend_marker_size),
                    line={
                        'width': 1,
                        'color': 'black'
                    },
                    sizeref=2. * max(self._legend_marker_size_function(legend_marker_sizes)) / (40. ** 2),
                    sizemin=4,

                ),
                visible='legendonly',
                legend="legend2",
            )
        fig.update_layout(
            title=self.title,
            legend={
                "title": "Blade Type",
                'itemsizing': 'constant',
                'itemclick': False,
                'itemdoubleclick': False,
            },
            legend2={
                "title": self.size_dim,
                "y": 0.0,
                'itemclick': False,
                'itemdoubleclick': False,
            }
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
