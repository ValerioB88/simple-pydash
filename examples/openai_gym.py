from simple_pydash.server import CustomAPI
import uvicorn
from simple_pydash.modules.canvas import (
    RenderGymEnv,
    StaticImage,
)
from simple_pydash.modules.inject_html import Inject_HTML
from simple_pydash.modules.plotlyplot import AppendScatterPlot, HeatMap

from simple_pydash.modules.text_info import GeneralTextInfo, TextInfo
from matplotlib import colors
import gym
import numpy as np
from simple_pydash.model import Model
import PIL.Image as Image

newgym = int(gym.__version__.split(".")[1]) > 25


class DummyGymModel(Model):
    action = 0
    tot_steps = 0

    def __init__(self, env, **kwargs):
        super().__init__(**kwargs)
        self.env = env
        self.obs = self.env.reset()[0] if newgym else self.env.reset()

    def __iter__(self):
        while True:
            self.action = np.random.randint(0, 2)
            self.obs, _, termination, *_ = self.env.step(self.action)
            self.tot_steps += 1
            if termination:
                self.obs = self.env.reset()[0] if newgym else self.env.reset()
            yield None

    def stop(self):
        self.env.reset()


server = CustomAPI(
    model_obj=DummyGymModel,
    dash_comps=[
        GeneralTextInfo(
            location_col_idx=0,
            use_scroll=False,
            width=480,
        ),
        RenderGymEnv(width=480, height=320, location_col_idx=0),
        HeatMap(
            title="Random Matrix",
            get_new_data_fun=lambda m: np.random.randn(10, 10),
            width=400,
            height=400,
            clr_min=-1,
            clr_max=1,
            location_col_idx=1,
            show_colormap=False,
        ),
        StaticImage(img=Image.open("assets/panzi.jpg"), location_col_idx=0),
        AppendScatterPlot(
            legends=["Cart Pos", "Cart Vel", "Pole Angle", "Pole Angle Vel"],
            get_new_data_fun=lambda m: [[i] for i in m.obs.tolist()],
            location_col_idx=1,
            width=500,
            height=200,
        ),
        AppendScatterPlot(
            legends=["Action"],
            get_new_data_fun=lambda m: [[m.action]],
            location_col_idx=1,
            width=500,
            height=150,
        ),
    ],
    model_params=dict(env=gym.make("CartPole-v1", render_mode="rgb_array")),
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
