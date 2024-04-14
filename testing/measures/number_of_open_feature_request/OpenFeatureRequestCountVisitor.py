from presentation.core.visitors.Visitor import Visitor


class OpenFeatureRequestCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            open_feature_requests = repository.get_issues(labels=['feature-request'])
            print(f"{repository.full_name}: {measure.name} is {open_feature_requests.totalCount}")
            return open_feature_requests.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)