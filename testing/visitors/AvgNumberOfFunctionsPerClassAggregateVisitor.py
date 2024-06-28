from github.Repository import Repository

from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import AggregateVisitor


class AvgNumberOfFunctionsPerClassAggregateVisitor(AggregateVisitor[tuple[Measure, int]]):
    def __init__(self):
        super().__init__()

    async def aggregate(self, normalized_measures: list[tuple[Measure, int]], repository: Repository) -> float:
        number_of_functions = 0
        number_of_classes = 0

        for measure, measure_value in normalized_measures:
            if measure.name.lower() == "number of functions":
                number_of_functions += measure_value
            if measure.name.lower() == "number of classes":
                number_of_classes += measure_value

        if number_of_classes == 0:
            # or a high threshold might be preferable
            print(f"Avg number of functions per class: {number_of_functions}")
            return number_of_functions

        ratio = number_of_functions / number_of_classes
        print(f"Number of functions: {number_of_functions}, Number of classes: {number_of_classes}, Ratio: {ratio}")
        return ratio
