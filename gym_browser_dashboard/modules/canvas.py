import PIL.Image as Image
import os
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from gym_browser_dashboard.modules.module import Module
import abc

def fig2PIL(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


def PIL2base64(image):
    buffered = BytesIO()
    image.convert('RGB').save(buffered, format="PNG")  # JPEG doesn't render well (flashy)
    b64img = base64.b64encode(buffered.getvalue())
    image = str(b64img)[2:-2].replace('=', '')
    return image


class Canvas(Module, abc.ABC):
    local_includes = [os.path.dirname(__file__) + "/Canvas.js"]
    package_includes = []
    portrayal_method = None

    def __init__(self, id=None, width=120, height=80):
        self.id = id
        if self.id is None:
            self.id = np.random.randint(0, 1000)
        self.canvas_width, self.canvas_height = width, height
        new_element = f"new Canvas({self.id},{self.canvas_width}, {self.canvas_height})"
        self.js_code = "elements.push(" + new_element + ");"
        super().__init__()

    @abc.abstractmethod
    def render(self) -> str:
        pass

class RenderGymEnv(Canvas):
    def render(self, model):
        canvas = model.env.render()
        canvas = Image.fromarray(canvas)
        return PIL2base64(canvas)


class RenderRandomMatrix(Canvas):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fig, ax = plt.subplots(1, 2)
        m1 = np.random.rand(10, 10)
        m2 = np.random.rand(20, 3)
        self.im1 = ax[0].imshow(m1)
        ax[0].set_title("rnd M1")
        self.im2 = ax[1].imshow(m2)
        ax[1].set_title("rnd M2")
        [axx.axis('off') for axx in ax]


    def render(self, model):
        m1 = np.random.rand(10, 10)
        m2 = np.random.rand(20, 3)
        self.im1.set_data(m1)
        self.im2.set_data(m2)

        canvas = fig2PIL(self.fig)
        return PIL2base64(canvas)