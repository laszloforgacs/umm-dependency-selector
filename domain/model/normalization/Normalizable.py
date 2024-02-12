from abc import ABC, abstractmethod

from domain.model.Result import Result
from domain.model.normalization.Normalizer import Normalizer


class Normalizable(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def normalize(self, normalizer: Normalizer) -> Result:
        pass
