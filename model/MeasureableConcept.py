from abc import ABCMeta, abstractmethod
from enum import Enum

from model.Result import Result
from model.components.Component import CompositeComponent
from model.measurement.Measure import Measure


class Impact(Enum):
    POSITIVE = 1
    NEGATIVE = 2


class OSSAspect(Enum):
    COMMUNITY = 1
    CODE = 2


class MeasurableConcept(CompositeComponent, metaclass=ABCMeta):
    def __init__(self, name: str, children: dict[str, Measure], impact: Impact, entity: str,
                 relevant_oss_aspect: OSSAspect, information_need: str, quality_requirement: str):
        self._name = name
        self._children = children
        self._impact = impact
        self._entity = entity
        self._relevant_oss_aspect = relevant_oss_aspect
        self._information_need = information_need
        self._quality_requirement = quality_requirement

    @property
    def impact(self) -> Impact:
        return self._impact

    @property
    def entity(self) -> str:
        return self._entity

    @property
    def relevant_oss_aspect(self) -> OSSAspect:
        return self._relevant_oss_aspect

    @property
    def information_need(self) -> str:
        return self._information_need

    @property
    def quality_requirement(self) -> str:
        return self._quality_requirement

    @abstractmethod
    def run(self) -> Result:
        pass

    @abstractmethod
    def measure(self) -> Result:
        pass
