import abc
import time
import sty
import numpy as np
import random
import datetime


class Model(abc.ABC):
    gfx = False

    def __init__(self, seed=None, gfx=True, print_seed=True):
        now = datetime.datetime.now()
        self.seed = int(time.time()) % (2**32 - 1) if seed is None else seed

        self.gfx = gfx
        print(sty.fg.red + f"SEED : {self.seed}" + sty.rs.fg) if print_seed else None
        np.random.seed(self.seed)
        print(self.seed)
        random.seed(self.seed)

    @abc.abstractmethod
    def __iter__(self):
        while True:
            yield None

    @abc.abstractmethod
    def stop(self):
        pass
