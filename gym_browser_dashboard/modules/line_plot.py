from typing import Callable
import json
import os
from gym_browser_dashboard.modules.module import Module
import abc
from typing import List
import numpy as np
from matplotlib import colors as col


def check_none(x):
    return x if x is not None else 'null'


class LinePlot(Module, abc.ABC):
    package_includes = ["chartjs-plugin-zoom.min.js"]  # ["Chart.min.js"]
    local_includes = [os.path.dirname(__file__) + "/LinePlot.js"]

    def __init__(
            self,
            series=None,
            names=None,
            show_lines=None,
            colors=None,  # a string 'red'
            replace=None,
            height=200,
            xmax=50,
            width=500,
            location='left',
            title=''
    ):
        assert series or names, "Please specify either the series or the name tags"
        if series is None:
            if show_lines is None:
                show_lines = ['true'] * (len(series) if series else len(names))
            if replace is None:
                replace = ['false'] * (len(series) if series else len(names))
            if colors is None:
                colors = col.BASE_COLORS.values()
            self.series = [{'Label': n, 'Color': col.to_hex(cc), 'ShowLine': ss, 'Replace': rr} for n, cc, ss, rr in zip(names, colors, show_lines, replace)]
        else:
            self.series = series
        series_json = json.dumps(self.series)
        new_element = f"new LinePlot({series_json}, {width}, {height}, '{location}', {check_none(xmax)}, '{title}')"
        self.dataset_indexes = [0 for i in range(len(self.series))]

        self.js_code = "elements.push(" + new_element + ");"

    def index_render(self, values):
        """
        Method used for converting list of values for each dataset in proper datapoints for chart_js. That is, values can be in this format (e.g. for 3 datasets):
         [[1,2,3],[4,5],[10,200,10,-1]]
         It will automatically update the indexes x for each dataset separately.
        """
        idx_values = [[{'x': didx + idx, 'y': v} for idx, v in enumerate(dv)] for didx, dv in zip(self.dataset_indexes, values)]
        if len(idx_values) != 0:
            self.dataset_indexes = [v[-1]['x'] + 1 for v in idx_values]
        return idx_values

    @staticmethod
    def reformat_values(values):
        """
        Values will be reformatted tobe in the format [DATASETS [LINEPLOTS [NUMBERS]].
        E.g.
        values = [0, 1] => [[0], [1]]
        values = 0 => [[0]]
        values = [[0, 1, 2], [3, 1]] => (unchanged)
        """
        if isinstance(values, np.ndarray):
            values = values.tolist()
        if not isinstance(values, list):
            values = [[values]]
        for idx, v in enumerate(values):
            if not isinstance(v, list):
                values[idx] = [v]
        return values


class AddLineChart(LinePlot):
    """
    Use a simplified
    [DATASETS [LINEPLOTS [VALUES] ] ]
    action_chart = AddLineChart(series=[{"Label": "A1", "Color": colors.to_hex("blue")}, {"Label": "A2", "Color": colors.to_hex("red")}], render=lambda model: [[1, 2, 20], [1, 2]], title='Action')
    lambda model: [1, 2, 3, 4], title='Hi') also works, for 4 datasets
    e.g.
    """

    def __init__(self, render: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trender = render

    def render(self, model):
        values = self.reformat_values(self.trender(model))
        return self.index_render(values)

#
