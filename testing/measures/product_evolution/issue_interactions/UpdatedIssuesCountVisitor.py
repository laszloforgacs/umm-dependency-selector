from presentation.core.visitors.Visitor import Visitor


class UpdatedIssuesCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            updated_issues = repository.get_issues(state='updated')
            total_count = 1
            total_count += updated_issues.totalCount
            print(f"{repository.full_name}: {measure.name} is {total_count}")
            return total_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)