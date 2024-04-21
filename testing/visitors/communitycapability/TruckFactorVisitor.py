import os

from truckfactor.compute import main

from data.repository.SourceRepositoryImpl import SOURCE_TEMP_DIR
from presentation.core.visitors.Visitor import Visitor


class TruckFactorVisitor(Visitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
        try:
            base_path = os.getcwd()
            path_to_repository = f"{base_path}/{SOURCE_TEMP_DIR}/{repository.name}"
            #tf, commit_shas, authors = main(path_to_repository)
            #print(f"{repository.full_name}: {measure.name} is {tf}")
            return 1
        except Exception as e:
            raise Exception(str(e))