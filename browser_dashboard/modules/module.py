import abc

class Module(abc.ABC):
    package_includes = []
    local_includes = []

    @abc.abstractmethod
    def render(self, model):
        pass

    def reset(self):
        pass

