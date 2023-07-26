import os
from io import BytesIO
from simple_pydash.modules.dashboard_component import DashboardComponent
import abc


def check_none(x):
    return x if x is not None else "null"


class Inject_HTML(DashboardComponent):
    local_includes = [os.path.dirname(__file__) + "/InjectHTML.js"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        new_element = f"new InjectHTML('{self.location_col_idx}')"
        self.js_code = "elements.push(" + new_element + ")"

    @abc.abstractmethod
    def render(self, model) -> str:
        html = "<p> oh hi mark </p>"
        return html
