from github.Repository import Repository

from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import AggregateVisitor


class AugurIssueThroughputVisitor(AggregateVisitor[tuple[Measure, int]]):
    def __init__(self):
        super().__init__()

    async def aggregate(self, normalized_measures: list[tuple[Measure, int]], repository: Repository) -> float:
        try:
            closed_issues_count = 0
            total_issues_count = 0
            for measure, measure_value in normalized_measures:
                if measure.name.lower() == "number of total issues":
                    total_issues_count += measure_value
                elif measure.name.lower() == "number of closed issues":
                    closed_issues_count += measure_value

            if total_issues_count == 0:
                print(f"{repository.full_name}: Issue Throughput is 0.0")
                return 0.0

            throughput = closed_issues_count / total_issues_count
            print(f"{repository.full_name}: Issue Throughput is {throughput}")
            return throughput
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)