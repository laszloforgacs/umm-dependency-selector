from model.Characteristic import Characteristic
from model.Result import Result, Success
from model.Viewpoint import Viewpoint


class DeveloperViewpoint(Viewpoint):
    def __init__(self, children: dict[str, Characteristic] = {}, preference_matrix: dict[tuple[str, str], float] = {}):
        super().__init__("Developer Viewpoint", children, preference_matrix)

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
