from presentation.core.AHPReportStateSubject import AHPReportStateSubject
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
