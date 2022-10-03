import json
import os
from gym_browser_dashboard.modules.module import Module
import abc
from typing import List

class LinePlot(Module, abc.ABC):
    package_includes = ["Chart.min.js"]
    local_includes = [os.path.dirname(__file__) + "/LinePlot.js"]

    def __init__(
        self,
        series,
        canvas_height=200,
        canvas_width=500,
    ):
        self.series = series
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width

        series_json = json.dumps(self.series)
        new_element = f"new LinePlot({series_json}, {canvas_width}, {canvas_height})"

        self.js_code = "elements.push(" + new_element + ");"

    @abc.abstractmethod
    def render(self) -> List:
        pass

class InputObservationChart(LinePlot):
    def render(self, model):
        return model.obs.tolist()

class DiscreteActionChart(LinePlot):
    def render(self, model):
        return [model.action]
