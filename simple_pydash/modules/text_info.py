import PIL.Image as Image
import os
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from simple_pydash.modules.dashboard_component import DashboardComponent
import abc
import PIL.Image


def check_none(x):
    return x if x is not None else "null"


class TextInfo(DashboardComponent):
    local_includes = [os.path.dirname(__file__) + "/TextInfo.js"]

    def __init__(self, id=None, replace=True, use_scroll=True, render=None, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.use_scroll = use_scroll
        self.trender = render

        if self.id is None:
            self.id = np.random.randint(0, 1000)

        new_element = (
            f"new TextInfo({self.width},"
            f"{self.height}, "
            f"{('true' if replace else 'false')}, "
            f"{('true' if use_scroll else 'false')}, "
            f"'{self.location_col_idx}')"
        )
        self.js_code = "elements.push(" + new_element + ")"

    def render(self, model) -> str:
        if self.trender:
            return self.trender(model)


import time

from collections import deque
from datetime import datetime


class GeneralTextInfo(TextInfo):
    local_includes = [os.path.dirname(__file__) + "/TextInfo.js"]
    previous_time = 0
    frame_times = deque(maxlen=50)  # Store times of last N=100 frames

    def render(self, model) -> str:
        current_time = time.time()
        frame_time = current_time - self.previous_time
        self.frame_times.append(frame_time)  # Append current frame time
        avg_fps = len(self.frame_times) / sum(
            self.frame_times
        )  # Average FPS over last N frames
        self.previous_time = current_time
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        text = f"{timestamp}: Iter. Num: {model.tot_steps}, Avg. FPS (last 50 frames): {avg_fps:.2f}\n"
        return text
