from domain.model.MeasurableConcept import MeasurableConcept
from domain.model.components.CompositeComponent import CompositeComponent


class SubCharacteristic(CompositeComponent):
    def __init__(self, name: str, children: dict[str, MeasurableConcept]):
        self._name = name
        self._children = children
