import abc


def check_none(x):
    return x if x is not None else "null"


class DashboardComponent(abc.ABC):
    package_includes = []
    local_includes = []

    def __init__(self, location_col_idx=0, width=None, height=None) -> None:
        self.location_col_idx = location_col_idx
        self.width = check_none(width)
        self.height = check_none(height)

    @abc.abstractmethod
    def render(self, model):
        pass

    def reset(self):
        pass
