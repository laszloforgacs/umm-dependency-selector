from abc import ABCMeta

from domain.model.Viewpoint import Viewpoint
from domain.model.components.Component import CompositeComponent


class QualityModel(CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, children: dict[str, Viewpoint]):
        self._name = name
        self._children = children