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
        return await self._shared_view_model.fetch_repositories(urls)

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
            #pprint(dm.matrix)
            rankings = pipe.evaluate(dm)
            pprint(rankings)
            #print(dir(rankings))
            #print(rankings.rank_)
            #print(rankings.alternatives)
            #print(rankings.values)
        except Exception as e:
            await self.evaluation_state_subject.set_state(
                state=EvaluationError(
                    message=str(e)
                )
            )

    def dispose(self):
        self._shared_view_model.dispose()
