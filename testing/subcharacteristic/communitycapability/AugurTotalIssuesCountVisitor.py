from presentation.core.visitors.Visitor import Visitor


class AugurTotalIssuesCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            issues = repository.get_issues()
            print(f"{repository.full_name}: {measure.name} is {issues.totalCount}")
            return issues.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)