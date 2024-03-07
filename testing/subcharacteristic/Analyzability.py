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


class Analyzability2(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability2", children)

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


class Analyzability3(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability3", children)

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


class Analyzability4(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability4", children)

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


class Analyzability5(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability5", children)

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


class Analyzability6(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability6", children)

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


class Analyzability7(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability7", children)

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


class Analyzability8(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability8", children)

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


class Analyzability9(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability9", children)

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


class Analyzability10(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability10", children)

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


class Analyzability11(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability11", children)

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


class Analyzability12(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability12", children)

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


class Analyzability13(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability13", children)

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


class Analyzability14(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability14", children)

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


class Analyzability15(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability15", children)

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


class Analyzability16(SubCharacteristic):
    def __init__(self, children: dict[str, MeasurableConcept] = {}):
        super().__init__("Analyzability16", children)

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
