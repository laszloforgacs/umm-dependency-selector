import json
import os
from typing import Final

import aiofiles

from domain.model.Characteristic import Characteristic
from domain.model.Model import QualityModelSchema
from domain.model.QualityModel import QualityModel
from domain.model.Result import Result, Success, Failure
from domain.model.Viewpoint import Viewpoint
from domain.repository.QualityModelRepository import QualityModelRepository
from testing.visitors.VisitorFactory import MeasureVisitorFactory, DerivedMeasureVisitorFactory, \
    MeasurableConceptVisitorFactory
from presentation.util.Util import convert_tuple_keys_to_string, convert_string_keys_to_tuple
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix
from util.GithubRateLimiter import GithubRateLimiter

QM_FOLDER: Final = "config"
MODELS_FOLDER: Final = f"{QM_FOLDER}/models"
RESULTS_FOLDER: Final = "results"
JSON_EXTENSION: Final = ".json"


class QualityModelRepositoryImpl(QualityModelRepository):
    def __init__(
            self,
            github_rate_limiter: GithubRateLimiter,
            base_measure_visitor_factory: MeasureVisitorFactory,
            derived_measure_visitor_factory: DerivedMeasureVisitorFactory,
            measurable_concept_visitor_factory: MeasurableConceptVisitorFactory
    ):
        self._github_rate_limiter = github_rate_limiter
        self._base_measure_visitor_factory = base_measure_visitor_factory
        self._derived_measure_visitor_factory = derived_measure_visitor_factory
        self._measurable_concept_visitor_factory = measurable_concept_visitor_factory

    async def fetch_quality_models(self) -> Result[list[QualityModel]]:
        try:
            read_json_files = await self._read_json_files_from_config_dir(MODELS_FOLDER)
            quality_models = []
            for data in read_json_files:
                qm_schema = QualityModelSchema()
                quality_models.append(qm_schema.load(data))

            for quality_model in quality_models:
                for viewpoint in quality_model.children.values():
                    viewpoint.preference_matrix = await self._init_viewpoint_pref_matrix(
                        quality_model=quality_model.name,
                        viewpoint=viewpoint
                    )
                    viewpoint.oss_aspect_preference_matrix = await self._init_oss_aspect_pref_matrix(
                        quality_model=quality_model.name,
                        viewpoint=viewpoint
                    )

                    for characteristic in viewpoint.children.values():
                        characteristic.preference_matrix = await self._init_characteristic_pref_matrix(
                            quality_model=quality_model.name,
                            viewpoint=viewpoint.name,
                            characteristic=characteristic
                        )

            return Success(
                quality_models
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

    async def write_measurement_result_tree_to_json(self, quality_model: 'QualityModel', viewpoint: 'Viewpoint',
                                                    repository_name: str):
        path = os.path.join(RESULTS_FOLDER, f"{repository_name}-{quality_model.name}-{viewpoint.name}.json").replace(
            " ", "_")
        data = quality_model.serialize()

        async with aiofiles.open(path, "w") as file:
            json_string = json.dumps(data, indent=4)
            await file.write(json_string)

    async def _read_json_files_from_config_dir(self, dir: str) -> list[str]:
        base_path = os.getcwd()
        config_path = os.path.join(base_path, dir)
        files = os.listdir(config_path)
        data = []
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(config_path, file)
                async with aiofiles.open(file_path, "r") as f:
                    try:
                        content = await f.read()
                        data.append(json.loads(content))
                    except json.JSONDecodeError:
                        print(f"Error reading file {file}")
        return data

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
