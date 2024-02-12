from domain.model.SubCharacteristic import SubCharacteristic
from domain.model.components.CompositeComponent import CompositeComponent


class QualityCharacteristic(CompositeComponent):
    def __init__(self, name: str, children: dict[str, SubCharacteristic]):
        self._name = name
        self._children = children
