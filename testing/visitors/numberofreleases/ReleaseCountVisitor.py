import os
from datetime import datetime, timedelta, timezone

from github.Repository import Repository

from presentation.core.visitors.Visitor import Visitor


class ReleaseCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            releases = repository.get_releases()
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=365)
            release_count = 0

            for release in releases:
                release_date = release.created_at
                if start_date <= release_date <= end_date:
                    release_count += 1
                else:
                    break

            print(f"{repository.full_name}: {measure.name} is {release_count}")

            await self.cache_result(measure, repository, release_count)
            return release_count
        except Exception as e:
            raise Exception(str(e))