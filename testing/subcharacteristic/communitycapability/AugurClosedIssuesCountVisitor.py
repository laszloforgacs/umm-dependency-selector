from presentation.core.visitors.Visitor import Visitor


class AugurClosedIssuesCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            closed_issues = repository.get_issues(state='closed')
            print(f"{repository.full_name}: {measure.name} is {closed_issues.totalCount}")
            return closed_issues.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)