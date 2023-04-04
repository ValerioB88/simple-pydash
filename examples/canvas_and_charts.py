from browser_dashboard.server import CustomAPI
import uvicorn
from browser_dashboard.modules.canvas import RenderGymEnv, RenderRandomMatrix, StaticImage
from browser_dashboard.modules.line_plot import AddLineChart
from browser_dashboard.modules.text_info import TextInfo
import gym
import numpy as np
from browser_dashboard.model import Model
import PIL.Image as Image
newgym = int(gym.__version__.split('.')[1]) > 25


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

env = gym.make("CartPole-v1", render_mode='rgb_array')


model_params = dict(env=env)  # add any other initialization parameters here
server = CustomAPI(model, [RenderGymEnv(width=480, height=320),
                           TextInfo(width=None, height=None, location='right', render=lambda m: m.tot_steps, use_scroll=False),
                           RenderRandomMatrix(width=480, height=320),
                           StaticImage(img=Image.open('panzi.jpg'), location='right',  height=110),
                           AddLineChart(names=['Cart Pos', 'Cart Vel', 'Pole Angle', 'Pole Angle Vel'],
                                        render=lambda m: m.obs.tolist(), location='right'),
                           AddLineChart(names=['action'], render=lambda m: [m.action], location='right')
                           ], model_params, update_gfx_every_x_steps=1)

if __name__ == "__main__":
    connected = False
    port = 8000
    while not connected:
        try:
            uvicorn.run("__main__:server", host="localhost", port=port)
            connected = True
        except:
            port += 1

