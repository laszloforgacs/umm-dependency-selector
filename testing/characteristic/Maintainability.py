from model.Characteristic import Characteristic
from model.Result import Result, Success
from model.SubCharacteristic import SubCharacteristic


class Maintainability(Characteristic):
    def __init__(self, children: dict[str, SubCharacteristic]):
        super().__init__("Maintainability", children)
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
