import base64
import abc
from io import BytesIO
from pathlib import Path
import random
from PIL import Image
import PIL
import io

from matplotlib import pyplot as plt
from simple_pydash.modules.dashboard_component import DashboardComponent


def fig2PIL(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


def PIL2base64(image):
    """Converts a PIL Image into base64 string for HTML rendering."""
    buffered = BytesIO()
    image.convert("RGB").save(buffered, format="PNG")  # PNG renders well
    b64img = base64.b64encode(buffered.getvalue())
    img_base64 = str(b64img)[2:-2].replace("=", "")
    return img_base64


class Canvas(DashboardComponent, abc.ABC):
    local_includes = [str(Path(__file__).parent / "Canvas.js")]

    def __init__(self, **kwargs):
        add_checkbox = False
        super().__init__(**kwargs)

        new_element = (
            f"new Canvas({self.width},"
            f"{self.height}, "
            f"'{self.location_col_idx}', {'true' if add_checkbox else 'false'})"
        )
        self.js_code = "elements.push(" + new_element + ");"

    @abc.abstractmethod
    def render(self, model) -> str:
        pass


class RenderGymEnv(Canvas):
    def render(self, model):
        canvas = model.env.render()
        canvas = Image.fromarray(canvas)
        return PIL2base64(canvas)


class StaticImage(Canvas):
    rendered = False

    def __init__(self, img: PIL.Image, **kwargs):
        self.img = img
        super().__init__(**kwargs)

    def render(self, model):
        if not self.rendered:
            self.rendered = True
            return PIL2base64(self.img)


# This is just an example of how one would render a matplotlib plot. Notice that this is discouraged, and Plotly will be almost always faster.
class MatplotlibPlot(Canvas):
    def render(self, model):
        fig = plt.figure()
        plt.bar(
            ["pippo", "paperino", "pluto"], [random.randint(0, 10) for _ in range(3)]
        )
        plt.tight_layout()
        b64 = PIL2base64(fig2PIL(fig))
        plt.close(fig)
        return b64
