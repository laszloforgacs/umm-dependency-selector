import asyncio
from typing import Optional

from domain.model.QualityModel import QualityModel
from domain.model.Result import Result, Success
from domain.repository.QualityModelRepository import QualityModelRepository
from presentation.core.QualityModelStateSubject import QualityModelStateSubject
from presentation.util.ErrorState import ErrorState
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix


class SharedViewModel():
    _quality_model_state_subject: QualityModelStateSubject = None

    def __init__(self, quality_model_repository: QualityModelRepository):
        self._quality_model_state_subject = QualityModelStateSubject()
        self._quality_model_repository = quality_model_repository

    @property
    def quality_model_state_subject(self) -> QualityModelStateSubject:
        return self._quality_model_state_subject

    def viewpoints(self, selected_quality_model: str) -> dict[str, 'Viewpoint']:
        selected_quality_model = next(
            (quality_model for quality_model in self._quality_model_state_subject.state.quality_model_list if
             quality_model.name == selected_quality_model),
            {}
        )
        return selected_quality_model.children

    def viewpoint(self, selected_quality_model: str, selected_viewpoint: str) -> 'Viewpoint':
        viewpoints = self.viewpoints(selected_quality_model)
        return viewpoints.get(selected_viewpoint, {})

    def characteristics(self, selected_quality_model: str, selected_viewpoint: str) -> dict[str, 'Characteristic']:
        selected_viewpoint = self.viewpoints(selected_quality_model).get(selected_viewpoint, {})
        return selected_viewpoint.children

    def preference_matrix(self, selected_quality_model: str, selected_viewpoint: str) -> PrefMatrix:
        selected_viewpoint = self.viewpoints(selected_quality_model).get(selected_viewpoint, {})
        return selected_viewpoint.preference_matrix

    async def fetch_quality_models(self):
        await self._quality_model_state_subject.set_state(self._quality_model_state_subject.state.copy(is_loading=True))
        result = await self._quality_model_repository.fetch_quality_models()
        await self._quality_model_state_subject.set_state(self._quality_model_state_subject.state.copy(
            quality_model_list=result.value if result.is_valid else [],
            is_loading=False,
            error=ErrorState(message=result.message) if not result.is_valid else None
        ))

    async def set_preference(
            self,
            filename: str,
            component: 'CompositeComponent',
            characteristic_tuple: tuple[str, str],
            preference: str
    ):
        await self._quality_model_repository.set_preference(
            filename=filename,
            component=component,
            characteristic_tuple=characteristic_tuple,
            preference=preference
        )