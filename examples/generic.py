from simple_pydash.modules.canvas import MatplotlibPlot
from simple_pydash.modules.plotlyplot import AppendScatterPlot, HeatMap
from simple_pydash.server import CustomAPI
import uvicorn
from simple_pydash.modules.text_info import GeneralTextInfo, TextInfo
import numpy as np
from simple_pydash.model import Model
import PIL.Image as Image


class DummyModel(Model):
    tot_steps = 0

    def __init__(self, num_lines, **kwargs):
        self.num_lines = num_lines
        super().__init__(**kwargs)
        # self.rnd_matrix = np.random.randn(10, 10)
        # self.rnd_lines = np.random.randint(-3, 3, (3, 1))

    def __iter__(self):
        while True:
            self.rnd_matrix = np.random.randn(10, 10)
            self.rnd_lines = np.random.randint(-3, 3, (self.num_lines, 1))

            self.tot_steps += 1
            yield None

    def stop(self):
        pass


server = CustomAPI(
    model_obj=DummyModel,
    dash_comps=[
        GeneralTextInfo(location_col_idx=0, use_scroll=False),
        MatplotlibPlot(location_col_idx=0, width=500),
        AppendScatterPlot(
            get_new_data_fun=lambda m: np.random.randn(2, 2).tolist(),
            location_col_idx=0,
            mode="markers",
            width=500,
            height=350,
        ),
        HeatMap(
            get_new_data_fun=lambda m: m.rnd_matrix,
            clr_min=-1,
            clr_max=1,
            location_col_idx=2,
            height=420,
        ),
        AppendScatterPlot(
            legends=[
                "Rnd",
                "Rnd2",
            ],  # notice that the number of legends provided doen't need to match the number of lines plotted. This will be handled automatically
            get_new_data_fun=lambda m: m.rnd_lines.tolist(),
            location_col_idx=1,
            width=500,
            height=350,
        ),
    ],
    model_params=dict(num_lines=3),
    wide_page=True,
)

if __name__ == "__main__":
    connected = False
    port = 8000
    while not connected:
        try:
            uvicorn.run("__main__:server", host="localhost", port=port)
            connected = True
        except:
            port += 1
