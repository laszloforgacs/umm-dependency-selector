import asyncio
import os

from github.Repository import Repository

from data.repository.SourceRepositoryImpl import SOURCE_TEMP_DIR
from presentation.core.visitors.Visitor import Visitor


class LizardLinesOfCodeVisitor(Visitor[float]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> float:
        try:
            return 50.0
            base_path = os.getcwd()
            path_to_repository = f"{base_path}/{SOURCE_TEMP_DIR}/{repository.name}"
            process = await asyncio.create_subprocess_shell(
                f"lizard {path_to_repository}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if stderr:
                raise Exception(stderr.decode())

            output_lines = stdout.decode().splitlines()
            last_line = output_lines[-1] if output_lines else None
            if not last_line:
                raise Exception("No output from lizard")
            split_last_line = last_line.split()
            total_nloc = split_last_line[0]
            avg_nloc = split_last_line[1]
            avg_ccn = split_last_line[2]
            avg_token = split_last_line[3]
            method_count = split_last_line[4]
            warning_count = split_last_line[5]
            fun_rt = split_last_line[6]
            nloc_rt = split_last_line[7]

            analysis = {
                "total_nloc": total_nloc,
                "avg_nloc": avg_nloc,
                "avg_ccn": avg_ccn,
                "avg_token": avg_token,
                "method_count": method_count,
                "warning_count": warning_count,
                "fun_rt": fun_rt,
                "nloc_rt": nloc_rt
            }
            lines_of_code = float(analysis["total_nloc"])
            print(f"{repository.full_name}: {measure.name} is {lines_of_code}")

            return lines_of_code

        except Exception as e:
            raise Exception(str(e))
