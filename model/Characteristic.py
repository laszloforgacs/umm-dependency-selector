from abc import abstractmethod, ABCMeta

from model.Result import Result
from model.SubCharacteristic import SubCharacteristic
from model.components.Component import CompositeComponent


class Characteristic(CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, children: dict[str, SubCharacteristic]):
        self._name = name
        self._children = children
        self._weight = 0

    @property
    def weight(self) -> float:
        return self._weight

    @abstractmethod
    def run(self) -> Result:
        pass