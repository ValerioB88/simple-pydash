import PIL.Image as Image
import os
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from gym_browser_dashboard.modules.module import Module
import abc
import PIL.Image

def check_none(x):
    return x if x is not None else 'null'

class TextInfo(Module):
    local_includes = [os.path.dirname(__file__) + '/TextInfo.js']

    def __init__(self, id=None, width=None, height=None, replace=True, use_scroll=True, location='left', render=None):
        self.id = id
        self.location = location
        self.width = width
        self.height = height
        self.use_scroll = use_scroll
        self.trender = render

        if self.id is None:
            self.id = np.random.randint(0, 1000)

        new_element = f"new TextInfo({check_none(self.id)}," \
                      f"{check_none(self.width)}," \
                      f"{check_none(self.height)}, " \
                      f"{('true' if replace else 'false')}, " \
                      f"{('true' if use_scroll else 'false')}, " \
                      f"'{self.location}')"
        self.js_code = "elements.push(" + new_element + ")";
        super().__init__()

    def render(self, model) -> str:
        if self.trender:
            return self.trender(model)

