import abc

class Module(abc.ABC):
    @abc.abstractmethod
    def render(self):
        pass