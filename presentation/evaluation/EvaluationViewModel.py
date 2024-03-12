import itertools

from presentation.core.AHPReportStateSubject import AHPReportStateSubject
from presentation.core.navigation.SourceStateSubject import SourceStateSubject
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
            repositories: list[str],
            comparisons: list[str, dict],
            viewpoint: 'Viewpoint',
            characteristics: list['Characteristic']
    ):
        matrix = [
            [] for _ in repositories
        ]

        for i, repo in enumerate(repositories):
            measures = [
                await characteristic.measure(repo)
                for characteristic in characteristics
            ]
            matrix[i] = list(itertools.chain.from_iterable(measures))

        print(matrix)
