from presentation.core.visitors.Visitor import Visitor


class OpenFeatureRequestCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            feature_labels = self._get_feature_labels(repository)
            total_count = 1
            open_feature_requests = repository.get_issues(labels=feature_labels, state='open')
            total_count += open_feature_requests.totalCount
            print(f"{repository.full_name}: {measure.name} is {total_count}")
            return total_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _get_feature_labels(self, repository: 'Repository') -> list[str]:
        try:
            labels = repository.get_labels()
            feature_labels = [label.name for label in labels if 'feature' in label.name.lower()]
            return feature_labels
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)