from abc import ABCMeta

from domain.model.Viewpoint import Viewpoint
from domain.model.Component import CompositeComponent


class QualityModel(CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, children: dict[str, Viewpoint]):
        self._name = name
        for child in children.values():
            child.parent = self
        self._children = children

    def serialize(self) -> dict:
        return {
            "class_name": self.__class__.__name__,
            "name": self.name,
            "viewpoints": [child.serialize() for child in self.children.values()]
        }
