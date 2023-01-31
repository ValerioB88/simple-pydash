import abc


class Model(abc.ABC):
    @abc.abstractmethod
    def __iter__(self):
        while True:
            yield None

    @abc.abstractmethod
    def stop(self):
        pass
