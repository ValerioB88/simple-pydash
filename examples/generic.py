from simple_pydash.modules.plotlyplot import AppendLinePlot, HeatMap
from simple_pydash.server import CustomAPI
import uvicorn
from simple_pydash.modules.text_info import GeneralTextInfo, TextInfo
import numpy as np
from simple_pydash.model import Model
import PIL.Image as Image


class DummyModel(Model):
    tot_steps = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rnd_values = np.random.randn(3, 2)

    def __iter__(self):
        while True:
            self.rnd_values = np.random.randn(3, 2)
            self.tot_steps += 1
            yield None

    def stop(self):
        pass


model = DummyModel

model_params = dict()  # add any other initialization parameters here

server = CustomAPI(
    model_obj=model,
    dash_comps=[
        GeneralTextInfo(location_col_idx=0, use_scroll=False),
        HeatMap(
            get_new_data_fun=lambda m: m.rnd_values,
            # width=500,
            # height=300,
            clr_min=-1,
            clr_max=1,
            location_col_idx=1,
        ),
        AppendLinePlot(
            legends=[
                "Rnd",
                "Rnd2",
            ],  # notice that the number of legends provided doen't need to match the number of lines plotted. This will be handled automatically
            get_new_data_fun=lambda m: m.rnd_values.tolist(),
            location_col_idx=2,
            width=500,
            height=350,
        ),
        AppendLinePlot(
            get_new_data_fun=lambda m: [np.random.randn(3, 2).tolist()],
            location_col_idx=2,
        ),
    ],
    model_params=model_params,
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
