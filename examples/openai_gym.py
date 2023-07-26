from simple_pydash.server import CustomAPI
import uvicorn
from simple_pydash.modules.canvas import (
    RenderGymEnv,
    StaticImage,
)
from simple_pydash.modules.inject_html import Inject_HTML
from simple_pydash.modules.plotlyplot import AppendLinePlot, HeatMap

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
            self.obs, _, termination, *_ = env.step(self.action)
            self.tot_steps += 1
            if termination:
                self.obs = env.reset()[0] if newgym else self.env.reset()
            yield None

    def stop(self):
        env.reset()


model = DummyGymModel

env = gym.make("CartPole-v1", render_mode="rgb_array")


model_params = dict(env=env)  # add any other initialization parameters here
server = CustomAPI(
    model_obj=model,
    dash_comps=[
        GeneralTextInfo(
            location_col_idx=0,
            use_scroll=False,
            width=480,
        ),
        RenderGymEnv(width=480, height=320),
        HeatMap(
            get_new_data_fun=lambda m: np.random.randn(10, 10),
            width=500,
            clr_min=-1,
            clr_max=1,
            height=300,
            location_col_idx=2,
        ),
        StaticImage(img=Image.open("panzi.jpg"), location_col_idx=2),
        AppendLinePlot(
            legends=["Cart Pos", "Cart Vel", "Pole Angle", "Pole Angle Vel"],
            get_new_data_fun=lambda m: [[i] for i in m.obs.tolist()],
            location_col_idx=1,
            width=500,
            height=200,
        ),
        AppendLinePlot(
            legends=["Action"],
            get_new_data_fun=lambda m: [[m.action]],
            location_col_idx=1,
            width=500,
            height=150,
        ),
    ],
    model_params=model_params,
    num_widget_columns=3,
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
