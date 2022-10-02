import abc


class Model(abc.ABC):
    @abc.abstractmethod
    def step(self):
        while True:
            yield None

    @abc.abstractmethod
    def stop(self):
        pass
