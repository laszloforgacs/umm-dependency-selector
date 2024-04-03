import asyncio
import os

from github.Repository import Repository

from data.repository.SourceRepositoryImpl import SOURCE_TEMP_DIR
from presentation.core.visitors.Visitor import Visitor


class ClocNumberOfCommentsVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            base_path = os.getcwd()
            path_to_repository = f"{base_path}/{SOURCE_TEMP_DIR}/{repository.name}"

            process = await asyncio.create_subprocess_shell(
                f"cloc {path_to_repository}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if stderr:
                raise Exception(stderr.decode())

            output_lines = stdout.decode().splitlines()
            previous_to_last_line = output_lines[-2] if output_lines else None
            if not previous_to_last_line:
                raise Exception("No output from cloc")

            split_previous_to_last_line = previous_to_last_line.split()
            number_of_comments = int(split_previous_to_last_line[-2])
            print(f"{repository.full_name}: {measure.name} is {number_of_comments}")

            return number_of_comments

        except Exception as e:
            raise Exception(str(e))