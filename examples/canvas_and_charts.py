from gym_browser_dashboard.server import CustomAPI
import uvicorn
from gym_browser_dashboard.modules.canvas import RenderGymEnv, RenderRandomMatrix, StaticImage
from gym_browser_dashboard.modules.line_plot import InputObservationChart, DiscreteActionChart
from matplotlib import colors
import gym
import numpy as np
from gym_browser_dashboard.model import Model
import PIL.Image as Image
newgym = int(gym.__version__.split('.')[1]) > 25


class DummyGymModel(Model):
    action = 0
    def __init__(self, env):
        self.env = env
        self.obs = self.env.reset()[0] if newgym else self.env.reset()

    def step(self):
        while True:
            self.action = np.random.randint(0, 2)
            self.obs, _, termination, *_ = env.step(self.action)
            if termination:
                self.obs = env.reset()[0] if newgym else self.env.reset()

            yield None

    def stop(self):
        env.reset()


model = DummyGymModel

env = gym.make("CartPole-v1", render_mode='rgb_array')

######################## Declare Modules #########################
obs_chart = InputObservationChart(
    [{"Label": "Cart Pos", "Color": colors.to_hex("red")},
     {"Label": "Cart Vel", "Color": colors.to_hex("green")},
     {"Label": "Pol Angl", "Color": colors.to_hex("yellow")},
     {"Label": "Pol Angl Vel", "Color": colors.to_hex("blue")}]
)

action_chart = DiscreteActionChart(
    [{"Label": "Action", "Color": colors.to_hex("red")}])
render_img = StaticImage(img=Image.open('panzi.jpg'), location='left', width=160, height=110)

render_gym_canvas = RenderGymEnv()
random_matrix = RenderRandomMatrix()

##################################################################

model_params = dict(env=env)  # add any other initialization parameters here
server = CustomAPI(model, [render_gym_canvas,  random_matrix, render_img, obs_chart, action_chart], model_params)

if __name__ == "__main__":
    connected = False
    port = 8000
    while not connected:
        try:
            uvicorn.run("__main__:server", host="localhost", port=port)
            connected = True
        except:
            port += 1

