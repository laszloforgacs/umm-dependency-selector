import asyncio
import os

from data.repository.SourceRepositoryImpl import SOURCE_TEMP_DIR
from presentation.core.visitors.Visitor import Visitor
from source_temp.PyGithub.github.Repository import Repository


class DelBiancoSnykRiskMeasureVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            base_path = os.getcwd()
            path_to_repository = f"{base_path}/{SOURCE_TEMP_DIR}/{repository.name}"
            process = await asyncio.create_subprocess_shell(
                f"snyk test --all-projects {path_to_repository}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if stderr:
                raise Exception(stderr.decode())

            output_lines = stdout.decode().splitlines()
            previous_to_last_line = output_lines[-2] if output_lines else None
            if not previous_to_last_line:
                raise Exception("No output from snyk")

            split_previous_to_last_line = previous_to_last_line.split()
            total_vulnerabilities = split_previous_to_last_line[0]
            print(f"{repository.full_name}: {measure.name} is {total_vulnerabilities}")

            return int(total_vulnerabilities)
        except Exception as e:
            raise Exception(str(e))