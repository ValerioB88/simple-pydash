import abc
import sty
import numpy as np
import random
class Model(abc.ABC):
    gfx = False
    def __init__(self, seed=0, gfx=True):
        self.seed = seed
        self.gfx = gfx
        print(sty.fg.red + f"SEED : {self.seed}" + sty.rs.fg)
        np.random.seed(seed)
        random.seed(seed)

    @abc.abstractmethod
    def __iter__(self):
        while True:
            yield None

    @abc.abstractmethod
    def stop(self):
        pass
