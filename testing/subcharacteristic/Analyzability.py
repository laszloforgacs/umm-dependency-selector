from domain.model.MeasureableConcept import MeasurableConcept
from domain.model.Result import Result, Success
from domain.model.SubCharacteristic import SubCharacteristic


class Analyzability(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability", children)

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
