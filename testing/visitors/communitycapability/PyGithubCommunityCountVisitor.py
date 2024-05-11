from presentation.core.visitors.Visitor import Visitor


class PyGithubCommunityCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            contributors = repository.get_contributors()
            contributors_count = sum(1 for _ in contributors)
            print(f"{repository.full_name}: {measure.name} is {contributors_count}")

            await self.cache_result(measure, repository, contributors_count)
            return contributors_count
        except Exception as e:
            raise Exception(str(e))