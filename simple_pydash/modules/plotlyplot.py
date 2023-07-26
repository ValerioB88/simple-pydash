import json
import os
from typing import Callable, List
import plotly
from simple_pydash.modules.dashboard_component import DashboardComponent
import abc
import plotly.graph_objects as go


class PlotlyComponents(DashboardComponent, abc.ABC):
    local_includes = [os.path.dirname(__file__) + "/PlotlyPlot.js"]

    def __init__(
        self, location_col_idx, title="", width=None, height=None, **init_figure_args
    ):
        super().__init__(location_col_idx, width=width, height=height)
        new_element = (
            f"new PlotlyPlot('{self.location_col_idx}', {self.width}, {self.height})"
        )
        self.js_code = "elements.push(" + new_element + ")"
        self.layout = go.Layout(
            title={
                "text": title,
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            margin=dict(
                l=5,
                r=5,
                b=5,
                t=5,
                pad=0,
            ),
        )
        self.init_figure(**init_figure_args)

    @abc.abstractmethod
    def init_figure(self):
        # self.fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
        pass

    @abc.abstractmethod
    def render(self, model) -> str:
        pass


class ScatterPlot(PlotlyComponents, abc.ABC):
    def init_figure(self, mode="lines", legends: List[str] = None, range_x=50):
        """_summary_

        Args:
            mode (str, optional): 'lines', 'markers', 'text'. Defaults to "lines".
            legends (List[str], optional): A list of legends. Defaults to None.
            range_x (int, optional): The range to show on the horizontal axis. Defaults to 50.
        """
        self.mode = mode

        self.layout.update(
            dict(
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                shapes=[
                    dict(
                        type="rect",
                        xref="paper",
                        yref="paper",
                        x0=0,
                        y0=0,
                        x1=1,
                        y1=1,
                        line=dict(
                            color="Black",
                            width=1,
                        ),
                    )
                ],
            )
        )
        self.range_x = range_x
        self.legends = legends
        self.data = [[]] * len(legends)
        self.traces = [
            go.Scatter(y=self.data[idx], mode=self.mode, name=l)
            for idx, l in enumerate(legends)
        ]
        self.fig = go.Figure(data=self.traces, layout=self.layout)

    def reset(self):
        self.init_figure(self.mode, self.legends, self.range_x)


class AppendScatterPlot(ScatterPlot):
    """
    Appends data to existing plot lines. The user needs to provide `get_new_data_fun`, a function that returns a nested list of data points. Each sublist represents a separate line on the plot, corresponding to the legends. The number of elements (data points) in each sublist may vary.
    """

    def __init__(self, get_new_data_fun: Callable, **kwargs):
        """
        Args:
            get_new_data_fun (Callable): a Callable that returns a set of point to append to the plot.

        """
        self.get_new_data_fun = get_new_data_fun
        legends = ["Line 1"] if "legends" not in kwargs else kwargs.pop("legends")

        self.data_counts = [0] * len(legends)
        super().__init__(legends=legends, **kwargs)

    def render(self, model) -> str:
        new_data = self.get_new_data_fun(model)
        if len(new_data) > len(self.legends):
            for i in range(len(new_data) - len(self.legends)):
                self.legends.append(f"Line {len(self.legends) + i + 1}")
                self.data_counts.append(0)
                self.fig.add_trace(
                    go.Scatter(y=[], mode=self.mode, name=self.legends[-1])
                )

        # If new_data has fewer traces, fill up the remainder with None
        if len(new_data) < len(self.legends):
            new_data += [[None]] * (len(self.legends) - len(new_data))

        for i in range(len(self.legends)):
            self.data_counts[i] += len(new_data[i])  # Update the count for each line

            updated_y_data = list(self.fig.data[i].y) + new_data[i]
            if len(updated_y_data) > self.range_x:
                updated_y_data = updated_y_data[-self.range_x :]

            # Update the x-values as well
            updated_x_data = list(
                range(self.data_counts[i] - len(updated_y_data), self.data_counts[i])
            )
            self.fig.data[i].x = updated_x_data  # Set the x-values
            self.fig.data[i].y = updated_y_data  # Set the y-values

        fig_json = json.dumps(self.fig, cls=plotly.utils.PlotlyJSONEncoder)
        return fig_json

    def reset(self):
        self.data_counts = [0] * len(self.legends)
        super().reset()


class HeatMap(PlotlyComponents):
    def __init__(self, get_new_data_fun, **kwargs):
        self.get_new_data_fun = get_new_data_fun
        super().__init__(**kwargs)

    def init_figure(
        self,
        clr_min=None,
        clr_max=None,
        x_legends=None,
        y_legends=None,
        show_colormap=True,
    ):
        self.layout.update(
            margin=dict(
                l=15,
                r=15,
                b=15,
                t=35,
                pad=0,
            )
        )
        self.show_colormap = show_colormap
        self.x_legends, self.y_legends = x_legends, y_legends
        self.clr_min, self.clr_max = clr_min, clr_max
        self.fig = go.Figure(
            data=go.Heatmap(
                z=[[]],
                x=x_legends,
                showscale=show_colormap,
                y=y_legends,
                zmin=clr_min,
                zmax=clr_max,
                hoverongaps=False,
                colorbar=dict(
                    thickness=10,
                    len=1,
                    xpad=0,
                    ypad=0,
                ),
            ),
            layout=self.layout,
        )

    def render(self, model) -> str:
        new_data = self.get_new_data_fun(model)
        self.fig.data[0].z = new_data

        fig_json = json.dumps(self.fig, cls=plotly.utils.PlotlyJSONEncoder)
        return fig_json

    def reset(self):
        self.init_figure(
            self.clr_min,
            self.clr_max,
            self.x_legends,
            self.y_legends,
            self.show_colormap,
        )
