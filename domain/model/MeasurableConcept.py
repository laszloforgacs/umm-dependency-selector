from enum import Enum

from domain.model.components.CompositeComponent import CompositeComponent
from domain.model.measure.Measure import Measure


class Impact(Enum):
    POSITIVE = 1
    NEGATIVE = 2


class RelevantOSSAspect(Enum):
    COMMUNITY = 1
    CODE = 2


class MeasurableConcept(CompositeComponent):
    def __init__(self, name: str, children: dict[str, Measure], impact: Impact, entity: str,
                 relevant_oss_aspect: RelevantOSSAspect, quality_requirement: str):
        self._name = name
        self._children = children
        self._impact = impact
        self._entity = entity
        self._relevant_oss_aspect = relevant_oss_aspect
        self._quality_requirement = quality_requirement
