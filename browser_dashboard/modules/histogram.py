from typing import Callable
import json
import os
from browser_dashboard.modules.module import Module
import abc
from typing import List
import numpy as np
from matplotlib import colors as col


def check_none(x):
    return x if x is not None else 'null'


class Histogram(Module, abc.ABC):
    package_includes = ["chartjs-plugin-zoom.min.js"] # ["Chart.min.js"]
    local_includes = [os.path.dirname(__file__) + "/Histogram.js"]

    def __init__(
            self,
            series=None,
            names=None,
            colors=None,
            replace=None,
            num_bins=20,
            height=200,
            # xmax=None,
            width=500,
            location='left',
            title=''
    ):
        self.num_bins = num_bins
        assert series or names, "Please specify either the series or the name tags"
        if series is None:
            if replace is None:
                replace = ['false'] * (len(series) if series else len(names))
            if colors is None:
                colors = col.BASE_COLORS.values()
            self.series = [{'Label': n, 'Color': col.to_hex(cc), 'Replace': rr} for n, cc, rr in zip(names, colors, replace)]
        else:
            self.series = series
        series_json = json.dumps(self.series)
        new_element = f"new Histogram({series_json}, {width}, {height}, '{location}', '{title}')"

        self.js_code = "elements.push(" + new_element + ");"
