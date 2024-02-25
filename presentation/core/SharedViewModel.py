import asyncio

from domain.model.QualityModel import QualityModel
from domain.model.Result import Result, Success
from domain.repository.QualityModelRepository import QualityModelRepository
from presentation.core.QualityModelStateSubject import QualityModelStateSubject
from presentation.util.ErrorState import ErrorState


class SharedViewModel():
    _quality_model_state_subject: QualityModelStateSubject = None

    def __init__(self, quality_model_repository: QualityModelRepository):
        self._quality_model_state_subject = QualityModelStateSubject()
        self._quality_model_repository = quality_model_repository

    @property
    def quality_model_state_subject(self) -> QualityModelStateSubject:
        return self._quality_model_state_subject

    async def fetch_quality_models(self):
        await self._quality_model_state_subject.set_state(self._quality_model_state_subject.state.copy(is_loading=True))
        result = await self._quality_model_repository.fetch_quality_models()
        await self._quality_model_state_subject.set_state(self._quality_model_state_subject.state.copy(
            quality_model_list=result.value if result.is_valid else [],
            is_loading=False,
            error=ErrorState(message=result.message) if not result.is_valid else None
        ))
