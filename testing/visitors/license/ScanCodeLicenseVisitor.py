import asyncio
import json
import os

from data.repository.SourceRepositoryImpl import SOURCE_TEMP_DIR
from presentation.core.visitors.Visitor import Visitor
from source_temp.PyGithub.github.Repository import Repository


class ScanCodeLicenseVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            base_path = os.getcwd()
            path_to_repository = f"{base_path}/{SOURCE_TEMP_DIR}/{repository.name}"
            process = await asyncio.create_subprocess_shell(
                f"scancode --license --json-pp - {SOURCE_TEMP_DIR}/{repository.name}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if stderr:
                raise Exception(stderr.decode())

            scan_results = json.loads(stdout)
            print(scan_results)
            return 1
        except Exception as e:
            raise Exception(str(e))
