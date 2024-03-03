import asyncio
from copy import deepcopy

from domain.model.QualityModel import QualityModel
from domain.model.Result import Result, Success
from domain.repository.QualityModelRepository import QualityModelRepository
from testing.characteristic.Maintainability import Maintainability
from testing.measurableconcepts.ComplexityOfSourceCode import ComplexityOfSourceCode
from testing.measures.CyclomaticComplexity import CyclomaticComplexity
from testing.measures.LinesOfCode import LinesOfCode
from testing.measures.NumberOfComplexFunctions import NumberOfComplexFunctions
from testing.measures.NumberOfStatements import NumberOfStatements
from testing.qualitymodels.TestQualityModel import TestQualityModel
from testing.subcharacteristic.Analyzability import Analyzability
from testing.viewpoints.DeveloperViewpoint import DeveloperViewpoint


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

        maintainability = Maintainability({})
        maintainability.add_component(analyzability)
        # print(maintainability.run().value)

        maintainability2 = deepcopy(maintainability)
        maintainability3 = deepcopy(maintainability)

        developer_viewpoint = DeveloperViewpoint(children={
            maintainability.name: maintainability,
        },
            preference_matrix={
                (maintainability.name, maintainability2.name): None,
                (maintainability.name, maintainability3.name): None,
            }
        )
        # print(developer_viewpoint.run().value)
        # print(developer_viewpoint.is_valid_preference_matrix)
        # print(developer_viewpoint.preference_matrix)

        test_quality_model = TestQualityModel(
            children={
                developer_viewpoint.name: developer_viewpoint
            }
        )

        await asyncio.sleep(5)
        return Success(
            [
                test_quality_model
            ]
        )
