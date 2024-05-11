from presentation.core.visitors.Visitor import Visitor


class OpenFeatureRequestCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            feature_labels = self._get_feature_labels(repository)
            open_feature_requests = repository.get_issues(labels=feature_labels, state='open')
            print(f"{repository.full_name}: {measure.name} is {open_feature_requests.totalCount}")

            await self.cache_result(measure, repository, open_feature_requests.totalCount)
            return open_feature_requests.totalCount
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _get_feature_labels(self, repository: 'Repository') -> list[str]:
        try:
            labels = repository.get_labels()
            feature_labels = [label.name for label in labels if 'feature' in label.name.lower()]
            return feature_labels
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)