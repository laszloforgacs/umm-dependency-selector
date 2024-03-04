import asyncio
import json
import os
from copy import deepcopy
from typing import Final

import aiofiles

from domain.model.Characteristic import Characteristic
from domain.model.QualityModel import QualityModel
from domain.model.Result import Result, Success
from domain.model.Viewpoint import Viewpoint
from domain.repository.QualityModelRepository import QualityModelRepository
from presentation.util.Util import convert_tuple_keys_to_string, convert_string_keys_to_tuple
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix
from testing.characteristic.Maintainability import Maintainability
from testing.measurableconcepts.ComplexityOfSourceCode import ComplexityOfSourceCode
from testing.measures.CyclomaticComplexity import CyclomaticComplexity
from testing.measures.LinesOfCode import LinesOfCode
from testing.measures.NumberOfComplexFunctions import NumberOfComplexFunctions
from testing.measures.NumberOfStatements import NumberOfStatements
from testing.qualitymodels.TestQualityModel import TestQualityModel
from testing.subcharacteristic.Analyzability import Analyzability
from testing.viewpoints.DeveloperViewpoint import DeveloperViewpoint

QM_FOLDER: Final = "config"
JSON_EXTENSION: Final = ".json"


class QualityModelRepositoryImpl(QualityModelRepository):
    def __init__(self):
        pass

    async def fetch_quality_models(self) -> Result[list[QualityModel]]:
        linesOfCode = LinesOfCode()
        numberOfComplexFunctions = NumberOfComplexFunctions()
        cyclomaticComplexity = CyclomaticComplexity()
        cyclomaticComplexity.add_component(linesOfCode)
        cyclomaticComplexity.add_component(numberOfComplexFunctions)
        numberOfStatements = NumberOfStatements()

        resultCyclomaticComplexity = [
            component.measure().value
            for component in cyclomaticComplexity.children.values()
        ]

        resultNumberOfStatements = numberOfStatements.measure().value

        # print(resultCyclomaticComplexity)
        # print(resultNumberOfStatements)

        complexityOfSourceCode = ComplexityOfSourceCode()
        complexityOfSourceCode.add_component(cyclomaticComplexity)
        complexityOfSourceCode.add_component(numberOfStatements)
        codeComplexity = complexityOfSourceCode.run().value
        # print(codeComplexity)

        analyzability = Analyzability()
        analyzability.add_component(complexityOfSourceCode)
        # print(analyzability.run().value)

        analyzability2 = deepcopy(analyzability)
        analyzability3 = deepcopy(analyzability)
        analyzability4 = deepcopy(analyzability)
        analyzability2.name = "Analyzability2"
        analyzability3.name = "Analyzability3"
        analyzability4.name = "Analyzability4"

        maintainability = Maintainability(children={
            analyzability.name: analyzability,
            analyzability2.name: analyzability2,
            analyzability3.name: analyzability3,
            analyzability4.name: analyzability4
        })
        # maintainability.add_component(analyzability)
        # print(maintainability.run().value)

        maintainability2 = deepcopy(maintainability)
        maintainability3 = deepcopy(maintainability)
        maintainability4 = deepcopy(maintainability)
        maintainability2.name = "Maintainability2"
        maintainability3.name = "Maintainability3"
        maintainability4.name = "Maintainability4"

        developer_viewpoint = DeveloperViewpoint(children={
            maintainability.name: maintainability,
            maintainability2.name: maintainability2,
            maintainability3.name: maintainability3,
            maintainability4.name: maintainability4
        })
        # print(developer_viewpoint.run().value)
        # print(developer_viewpoint.is_valid_preference_matrix)
        # print(developer_viewpoint.preference_matrix)

        test_quality_model = TestQualityModel(
            children={
                developer_viewpoint.name: developer_viewpoint
            }

        )

        tasks = []

        for viewpoint in test_quality_model.children.values():
            viewpoint.preference_matrix = await self._init_viewpoint_pref_matrix(
                quality_model=test_quality_model.name,
                viewpoint=viewpoint
            )

        for characteristic in viewpoint.children.values():
            characteristic.preference_matrix = await self._init_characteristic_pref_matrix(
                quality_model=test_quality_model.name,
                viewpoint=viewpoint.name,
                characteristic=characteristic
            )

        await asyncio.gather(*tasks)
        await asyncio.sleep(5)
        return Success(
            [
                test_quality_model
            ]
        )

    async def set_preference(
            self,
            filename: str,
            characteristic_tuple: tuple[str, str],
            preference: str
    ):
        path = os.path.join(QM_FOLDER, filename + JSON_EXTENSION)
        data = {
            "preference_matrix": {}
        }

        if os.path.exists(path):
            async with aiofiles.open(path, "r") as file:
                content = await file.read()
                if content:
                    data = json.loads(content)

        key = f"{characteristic_tuple[0].name}, {characteristic_tuple[1].name}"
        data["preference_matrix"][key] = preference

        async with aiofiles.open(path, "w") as file:
            json_string = json.dumps(data, indent=4)
            await file.write(json_string)

    async def _init_viewpoint_pref_matrix(
            self,
            quality_model: str,
            viewpoint: Viewpoint
    ) -> PrefMatrix:
        path = os.path.join(QM_FOLDER, f"{quality_model}-{viewpoint.name}.json").replace(" ", "_")

        return await self._read_write_pref_matrix(
            path=path,
            preference_matrix=viewpoint.preference_matrix
        )

    async def _init_characteristic_pref_matrix(
            self,
            quality_model: str,
            viewpoint: str,
            characteristic: Characteristic
    ) -> PrefMatrix:
        path = os.path.join(QM_FOLDER, f"{quality_model}-{viewpoint}-{characteristic.name}.json").replace(" ", "_")

        return await self._read_write_pref_matrix(
            path=path,
            preference_matrix=characteristic.preference_matrix
        )

    async def _read_write_pref_matrix(
            self,
            path: str,
            preference_matrix: PrefMatrix
    ):
        if not os.path.exists(path):
            async with aiofiles.open(path, "w") as file:
                data = {
                    "preference_matrix": convert_tuple_keys_to_string(preference_matrix)
                }

                json_string = json.dumps(data, indent=4)
                await file.write(json_string)
                return preference_matrix
        else:
            async with aiofiles.open(path, "r") as file:
                content = await file.read()
                if content:
                    data = json.loads(content)
                    return convert_string_keys_to_tuple(data["preference_matrix"])
