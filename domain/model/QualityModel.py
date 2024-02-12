from domain.model.Viewpoint import Viewpoint
from domain.model.components.CompositeComponent import CompositeComponent


class QualityModel(CompositeComponent):

    def __init__(self, name: str, children: dict[str, Viewpoint]):
        self._name = name
        self._children = children
