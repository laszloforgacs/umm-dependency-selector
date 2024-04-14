import os
from datetime import datetime, timedelta, timezone

from data.repository.SourceRepositoryImpl import SOURCE_TEMP_DIR
from presentation.core.visitors.Visitor import Visitor
from source_temp.PyGithub.github.Repository import Repository


class ReleaseCountVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            releases = repository.get_releases()
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=365)
            release_count = 1

            for release in releases:
                release_date = release.created_at
                if start_date <= release_date <= end_date:
                    release_count += 1
                else:
                    break

            print(f"{repository.full_name}: {measure.name} is {release_count}")
            return release_count
        except Exception as e:
            raise Exception(str(e))