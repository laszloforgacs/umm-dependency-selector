import asyncio
import json
import os
from typing import Final

import aiofiles

from domain.model.Characteristic import Characteristic
from domain.model.QualityModel import QualityModel
from domain.model.Result import Result, Success, Failure
from domain.model.Viewpoint import Viewpoint
from domain.repository.QualityModelRepository import QualityModelRepository
from presentation.core.visitors.VisitorFactory import MeasureVisitorFactory, DerivedMeasureVisitorFactory, \
    MeasurableConceptVisitorFactory
from presentation.util.Util import convert_tuple_keys_to_string, convert_string_keys_to_tuple
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix
from testing.characteristic.Maintainability import Maintainability, Maintainability2, Maintainability3, Maintainability4
from testing.measurableconcepts.ComplexityOfSourceCode import ComplexityOfSourceCode, ComplexityOfSourceCode2
from testing.measures.CyclomaticComplexity import CyclomaticComplexity
from testing.measures.LinesOfCode import LinesOfCode
from testing.measures.NumberOfComplexFunctions import NumberOfComplexFunctions
from testing.measures.NumberOfStatements import NumberOfStatements
from testing.qualitymodels.TestQualityModel import TestQualityModel
from testing.subcharacteristic.Analyzability import Analyzability, Analyzability2, Analyzability3, Analyzability4, \
    Analyzability5, Analyzability6, Analyzability7, Analyzability8, Analyzability9, Analyzability10, Analyzability11, \
    Analyzability12, Analyzability13, Analyzability14, Analyzability15, Analyzability16
from testing.viewpoints.DeveloperViewpoint import DeveloperViewpoint

QM_FOLDER: Final = "config"
JSON_EXTENSION: Final = ".json"


class QualityModelRepositoryImpl(QualityModelRepository):
    def __init__(
            self,
            base_measure_visitor_factory: MeasureVisitorFactory,
            derived_measure_visitor_factory: DerivedMeasureVisitorFactory,
            measurable_concept_visitor_factory: MeasurableConceptVisitorFactory
    ):
        self._base_measure_visitor_factory = base_measure_visitor_factory
        self._derived_measure_visitor_factory = derived_measure_visitor_factory
        self._measurable_concept_visitor_factory = measurable_concept_visitor_factory

    async def fetch_quality_models(self) -> Result[list[QualityModel]]:
        try:
            linesOfCode = self._base_measure_visitor_factory.instantiate_with_visitor(LinesOfCode)
            numberOfComplexFunctions = self._base_measure_visitor_factory.instantiate_with_visitor(
                NumberOfComplexFunctions
            )
            cyclomaticComplexity = self._derived_measure_visitor_factory.instantiate_with_visitor(
                CyclomaticComplexity,
                children={
                    linesOfCode.name: linesOfCode,
                    numberOfComplexFunctions.name: numberOfComplexFunctions
                }
            )
            numberOfStatements = self._base_measure_visitor_factory.instantiate_with_visitor(NumberOfStatements)
            complexityOfSourceCode = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ComplexityOfSourceCode,
                children={
                    cyclomaticComplexity.name: cyclomaticComplexity,
                    numberOfStatements.name: numberOfStatements
                }
            )

            complexityOfSourceCode2 = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ComplexityOfSourceCode2,
                children={
                    cyclomaticComplexity.name: cyclomaticComplexity.copy(
                        children={
                            linesOfCode.name: linesOfCode.copy(),
                            numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                        }
                    ),
                    numberOfStatements.name: numberOfStatements.copy()
                }
            )

            analyzability = Analyzability(
                children={
                    complexityOfSourceCode.name: complexityOfSourceCode.copy(
                        children={
                            cyclomaticComplexity.name: cyclomaticComplexity.copy(
                                children={
                                    linesOfCode.name: linesOfCode.copy(),
                                    numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                                }
                            ),
                            numberOfStatements.name: numberOfStatements.copy()
                        }
                    )
                }
            )

            analyzability2 = Analyzability2(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability3 = Analyzability3(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability4 = Analyzability4(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability5 = Analyzability5(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability6 = Analyzability6(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability7 = Analyzability7(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability8 = Analyzability8(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability9 = Analyzability9(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability10 = Analyzability10(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability11 = Analyzability11(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity,
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability12 = Analyzability12(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability13 = Analyzability13(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability14 = Analyzability14(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability15 = Analyzability15(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                )
            })
            analyzability16 = Analyzability16(children={
                complexityOfSourceCode.name: complexityOfSourceCode.copy(
                    children={
                        cyclomaticComplexity.name: cyclomaticComplexity.copy(
                            children={
                                linesOfCode.name: linesOfCode.copy(),
                                numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                            }
                        ),
                        numberOfStatements.name: numberOfStatements.copy()
                    }
                ),
                complexityOfSourceCode2.name: complexityOfSourceCode2
            })

            maintainability = Maintainability(children={
                analyzability.name: analyzability,
                analyzability2.name: analyzability2,
                analyzability3.name: analyzability3,
                analyzability4.name: analyzability4
            })

            maintainability2 = Maintainability2(children={
                analyzability5.name: analyzability5,
                analyzability6.name: analyzability6,
                analyzability7.name: analyzability7,
                analyzability8.name: analyzability8
            })

            maintainability3 = Maintainability3(children={
                analyzability9.name: analyzability9,
                analyzability10.name: analyzability10,
                analyzability11.name: analyzability11,
                analyzability12.name: analyzability12
            })

            maintainability4 = Maintainability4(children={
                analyzability13.name: analyzability13,
                analyzability14.name: analyzability14,
                analyzability15.name: analyzability15,
                analyzability16.name: analyzability16
            })

            developer_viewpoint = DeveloperViewpoint(children={
                maintainability.name: maintainability,
                maintainability2.name: maintainability2,
                maintainability3.name: maintainability3,
                maintainability4.name: maintainability4
            })

            test_quality_model = TestQualityModel(
                children={
                    developer_viewpoint.name: developer_viewpoint
                }

            )

            for viewpoint in test_quality_model.children.values():
                viewpoint.preference_matrix = await self._init_viewpoint_pref_matrix(
                    quality_model=test_quality_model.name,
                    viewpoint=viewpoint
                )
                viewpoint.oss_aspect_preference_matrix = await self._init_oss_aspect_pref_matrix(
                    quality_model=test_quality_model.name,
                    viewpoint=viewpoint
                )

                for characteristic in viewpoint.children.values():
                    characteristic.preference_matrix = await self._init_characteristic_pref_matrix(
                        quality_model=test_quality_model.name,
                        viewpoint=viewpoint.name,
                        characteristic=characteristic
                    )

            await asyncio.sleep(1)
            return Success(
                [
                    test_quality_model
                ]
            )
        except Exception as e:
            return Failure(
                error_message=str(e)
            )

    async def set_preference(
            self,
            filename: str,
            key: str,
            matrix_key: str,
            preference: str
    ) -> PrefMatrix:
        path = os.path.join(QM_FOLDER, filename + JSON_EXTENSION)
        data = {
            matrix_key: {}
        }

        if os.path.exists(path):
            async with aiofiles.open(path, "r") as file:
                content = await file.read()
                if content:
                    data = json.loads(content)

        data[matrix_key][key] = preference

        async with aiofiles.open(path, "w") as file:
            json_string = json.dumps(data, indent=4)
            await file.write(json_string)
            return convert_string_keys_to_tuple(data.get(matrix_key, {}))

    async def _init_viewpoint_pref_matrix(
            self,
            quality_model: str,
            viewpoint: 'Viewpoint'
    ) -> PrefMatrix:
        path = os.path.join(QM_FOLDER, f"{quality_model}-{viewpoint.name}.json").replace(" ", "_")

        return await self._read_write_pref_matrix(
            path=path,
            preference_matrix=viewpoint.preference_matrix,
            key="preference_matrix"
        )

    async def _init_characteristic_pref_matrix(
            self,
            quality_model: str,
            viewpoint: str,
            characteristic: 'Characteristic'
    ) -> PrefMatrix:
        path = os.path.join(QM_FOLDER, f"{quality_model}-{viewpoint}-{characteristic.name}.json").replace(" ", "_")

        return await self._read_write_pref_matrix(
            path=path,
            preference_matrix=characteristic.preference_matrix,
            key="preference_matrix"
        )

    async def _init_oss_aspect_pref_matrix(
            self,
            quality_model: str,
            viewpoint: 'Viewpoint'
    ) -> PrefMatrix:
        path = os.path.join(QM_FOLDER, f"{quality_model}-{viewpoint.name}.json").replace(" ", "_")

        return await self._read_write_pref_matrix(
            path=path,
            preference_matrix=viewpoint.oss_aspect_preference_matrix,
            key="oss_aspect_preference_matrix"
        )

    async def _read_write_pref_matrix(
            self,
            path: str,
            preference_matrix: PrefMatrix,
            key: str
    ):
        if not os.path.exists(path):
            await self._write_pref_matrix(
                path=path,
                data={key: convert_tuple_keys_to_string(preference_matrix)}
            )
            return preference_matrix

        async with aiofiles.open(path, "r") as file:
            content = await file.read()

        if not content:
            await self._write_pref_matrix(
                path=path,
                data={key: convert_tuple_keys_to_string(preference_matrix)}
            )
            return preference_matrix

        data = json.loads(content)
        if key not in data:
            data[key] = convert_tuple_keys_to_string(preference_matrix)
            await self._write_pref_matrix(
                path=path,
                data=data
            )
            return preference_matrix

        pref_matrix_data = data[key]
        return convert_string_keys_to_tuple(pref_matrix_data)

    async def _write_pref_matrix(
            self,
            path: str,
            data: dict
    ):
        async with aiofiles.open(path, "w") as file:
            json_string = json.dumps(data, indent=4)
            await file.write(json_string)
