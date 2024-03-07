from domain.model.Characteristic import Characteristic
from domain.model.Result import Result, Success
from domain.model.SubCharacteristic import SubCharacteristic
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix


class Maintainability(Characteristic):
    def __init__(self, children: dict[str, SubCharacteristic] = {}, preference_matrix: PrefMatrix = {}):
        super().__init__("Maintainability", children, preference_matrix=preference_matrix)
        self._weight = 0.0

    def run(self) -> Result:
        measurements = [result.value for result in self.measure()]
        aggregated = self.aggregate(measurements)
        return aggregated

    def measure(self) -> list[Result]:
        return [
            child.run() for child in self.children.values()
        ]

    def aggregate(self, measuredResults: list[float]) -> Result:
        return Success(
            value=sum(measuredResults) / len(measuredResults)
        )

class Maintainability2(Characteristic):
    def __init__(self, children: dict[str, SubCharacteristic] = {}, preference_matrix: PrefMatrix = {}):
        super().__init__("Maintainability2", children, preference_matrix=preference_matrix)
        self._weight = 0.0

    def run(self) -> Result:
        measurements = [result.value for result in self.measure()]
        aggregated = self.aggregate(measurements)
        return aggregated

    def measure(self) -> list[Result]:
        return [
            child.run() for child in self.children.values()
        ]

    def aggregate(self, measuredResults: list[float]) -> Result:
        return Success(
            value=sum(measuredResults) / len(measuredResults)
        )

class Maintainability3(Characteristic):
    def __init__(self, children: dict[str, SubCharacteristic] = {}, preference_matrix: PrefMatrix = {}):
        super().__init__("Maintainability3", children, preference_matrix=preference_matrix)
        self._weight = 0.0

    def run(self) -> Result:
        measurements = [result.value for result in self.measure()]
        aggregated = self.aggregate(measurements)
        return aggregated

    def measure(self) -> list[Result]:
        return [
            child.run() for child in self.children.values()
        ]

    def aggregate(self, measuredResults: list[float]) -> Result:
        return Success(
            value=sum(measuredResults) / len(measuredResults)
        )

class Maintainability4(Characteristic):
    def __init__(self, children: dict[str, SubCharacteristic] = {}, preference_matrix: PrefMatrix = {}):
        super().__init__("Maintainability4", children, preference_matrix=preference_matrix)
        self._weight = 0.0

    def run(self) -> Result:
        measurements = [result.value for result in self.measure()]
        aggregated = self.aggregate(measurements)
        return aggregated

    def measure(self) -> list[Result]:
        return [
            child.run() for child in self.children.values()
        ]

    def aggregate(self, measuredResults: list[float]) -> Result:
        return Success(
            value=sum(measuredResults) / len(measuredResults)
        )