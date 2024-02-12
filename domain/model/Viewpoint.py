from domain.model.components.CompositeComponent import CompositeComponent


class Viewpoint(CompositeComponent):
    def __init__(self, name: str, children: dict[str, QualityCharacteristic]):
        self._name = name
        self._children = children
