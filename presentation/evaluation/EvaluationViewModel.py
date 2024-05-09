import asyncio
import itertools
from pprint import pprint

import skcriteria
from github.Repository import Repository
from skcriteria.agg import similarity
from skcriteria.pipeline import mkpipe
from skcriteria.preprocessing import invert_objectives, scalers

from domain.model.MeasureableConcept import OSSAspect, Impact
from presentation.core.AHPReportStateSubject import AHPReportStateSubject
from presentation.core.navigation.SourceStateSubject import SourceStateSubject
from presentation.evaluation.EvaluationScreenState import Error as EvaluationError
from presentation.evaluation.EvaluationStateSubject import EvaluationStateSubject


class EvaluationViewModel:
    _evaluation_state_subject: EvaluationStateSubject = EvaluationStateSubject()

    def __init__(self, shared_view_model: 'SharedViewModel'):
        self._shared_view_model = shared_view_model

    @property
    def evaluation_state_subject(self) -> 'EvaluationStateSubject':
        return self._evaluation_state_subject

    @property
    def ahp_report_state_subject(self) -> AHPReportStateSubject:
        return self._shared_view_model.ahp_report_state_subject

    @property
    def source_state_subject(self) -> SourceStateSubject:
        return self._shared_view_model.source_state_subject

    async def fetch_repositories(self, urls: list[str]):
        await self._shared_view_model.clone_repositories(urls)
        await self._shared_view_model.fetch_repositories(urls)

    async def create_topsis_matrix(
            self,
            repositories: list[Repository],
            comparisons: dict[str, 'Compare'],
            viewpoint: 'Viewpoint',
            characteristics: list['Characteristic']
    ):
        try:
            aspects = [aspect.name for aspect in OSSAspect]
            top_comparison = comparisons[viewpoint.name]
            matrix = [
                [] for _ in repositories
            ]

            measurable_concepts = []
            weights = []
            impacts = []
            criteria = []

            for characteristic in characteristics:
                for child in characteristic.children.values():
                    for aspect in aspects:
                        mcs = list(itertools.chain.from_iterable([
                            child.get_children_by_aspect(aspect)
                        ]))
                        measurable_concepts = measurable_concepts + mcs

            for i, repo in enumerate(repositories):
                for mc in measurable_concepts:
                    result = await mc.measure(repo)
                    if 0 <= result < 1:
                        result = 2
                    print(f"{repo.full_name}: {mc.name} Measurable Concept - {result}")
                    matrix[i].append(result)

            for mc in measurable_concepts:
                if mc.impact == Impact.POSITIVE:
                    impacts.append(max)
                else:
                    impacts.append(min)

                weight = top_comparison.target_weights[mc.parent.name] * top_comparison.global_weights[
                    mc.relevant_oss_aspect.name
                ]
                weights.append(weight)
                criteria.append(f"{mc.name} - {mc.relevant_oss_aspect.name}")

            dm = skcriteria.mkdm(
                matrix=matrix,
                objectives=impacts,
                weights=weights,
                alternatives=[repo.full_name for repo in repositories],
                criteria=criteria
            )

            pipe = mkpipe(
                invert_objectives.NegateMinimize(),
                scalers.VectorScaler(target="matrix"),
                scalers.SumScaler(target="weights"),
                similarity.TOPSIS()
            )
            rankings = pipe.evaluate(dm)
            pprint(rankings)

            quality_model_list = self._shared_view_model.quality_model_state_subject.state.quality_model_list
            filtered_quality_model_list = [qm for qm in quality_model_list if qm.name == viewpoint.parent.name]
            if len(filtered_quality_model_list) == 0:
                raise Exception("Unable to write measurement tree to JSON. Quality model not found.")
            selected_quality_model = filtered_quality_model_list[0]
            tasks = []
            for repo in repositories:
                tasks.append(
                    asyncio.create_task(
                        self._write_measurement_tree_to_json(selected_quality_model, viewpoint, repo.name)
                    )
                )
            await asyncio.gather(*tasks)
        except Exception as e:
            await self.evaluation_state_subject.set_state(
                state=EvaluationError(
                    message=str(e) + self.__class__.__name__
                )
            )

    async def _write_measurement_tree_to_json(self, quality_model: 'QualityModel', viewpoint: 'Viewpoint', repository_name: str):
        await self._shared_view_model.write_measurement_result_tree_to_json(quality_model, viewpoint, repository_name)

    async def dispose(self):
        await self._shared_view_model.dispose()
