from abc import ABCMeta

from domain.model.Component import CompositeComponent


class QualityModel(CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, children: dict[str, 'Viewpoint']):
        self._parent = None
        self._name = name
        for child in children.values():
            child.parent = self
        self._children = children

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "viewpoints": [child.serialize() for child in self.children.values()]
        }

    def pretty_print(self) -> dict:
        values = list(self.children.values())
        vp = values[0]
        return {
            "name": self.name,
            "characteristics": vp.pretty_print()
        }
