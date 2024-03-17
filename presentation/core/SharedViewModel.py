from domain.model.Result import Success
from domain.repository.QualityModelRepository import QualityModelRepository
from domain.repository.SourceRepository import SourceRepository
from presentation.core.AHPReportStateSubject import AHPReportStateSubject
from presentation.core.QualityModelStateSubject import QualityModelStateSubject
from presentation.core.SourceState import Loading, Loaded, Error
from presentation.core.navigation.SourceStateSubject import SourceStateSubject
from presentation.util.ErrorState import ErrorState
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix


class SharedViewModel:
    _quality_model_state_subject: QualityModelStateSubject = None
    _ahp_report_state_subject: AHPReportStateSubject = None
    _source_state_subject: SourceStateSubject = None

    def __init__(self, quality_model_repository: QualityModelRepository, source_repository: SourceRepository):
        self._quality_model_state_subject = QualityModelStateSubject()
        self._ahp_report_state_subject = AHPReportStateSubject()
        self._source_state_subject = SourceStateSubject()
        self._quality_model_repository = quality_model_repository
        self._source_repository = source_repository

    @property
    def quality_model_state_subject(self) -> QualityModelStateSubject:
        return self._quality_model_state_subject

    @property
    def ahp_report_state_subject(self) -> AHPReportStateSubject:
        return self._ahp_report_state_subject

    @property
    def source_state_subject(self) -> SourceStateSubject:
        return self._source_state_subject

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

    async def fetch_repositories(self, urls: list[str]):
        await self._source_state_subject.set_state(
            state=Loading()
        )
        result = await self._source_repository.fetch_repositories(urls)
        if isinstance(result, Success):
            results = result.value
            await self._source_state_subject.set_state(
                state=Loaded(
                    repositories=results
                )
            )
        else:
            await self._source_state_subject.set_state(
                state=Error(
                    message=result.message
                )
            )


    async def set_preference(
            self,
            selected_quality_model: str,
            selected_viewpoint: str,
            filename: str,
            characteristic_tuple: tuple['CompositeComponent', 'CompositeComponent'],
            preference: str
    ):
        new_pref_matrix = await self._quality_model_repository.set_preference(
            filename=filename,
            key=f"{characteristic_tuple[0].name}, {characteristic_tuple[1].name}",
            matrix_key="preference_matrix",
            preference=preference
        )

        self._quality_model_state_subject.set_preference(
            selected_quality_model=selected_quality_model,
            selected_viewpoint=selected_viewpoint,
            component=characteristic_tuple[0],
            pref_matrix=new_pref_matrix
        )

    async def set_oss_aspect_preference(
            self,
            selected_quality_model: str,
            selected_viewpoint: str,
            filename: str,
            oss_aspect_combination: tuple['OSSAspect', 'OSSAspect'],
            preference: str
    ):
        new_oss_aspect_pref_matrix = await self._quality_model_repository.set_preference(
            filename=filename,
            key=f"{oss_aspect_combination[0]}, {oss_aspect_combination[1]}",
            matrix_key="oss_aspect_preference_matrix",
            preference=preference
        )

        self._quality_model_state_subject.set_oss_aspect_preference(
            selected_quality_model=selected_quality_model,
            selected_viewpoint=selected_viewpoint,
            pref_matrix=new_oss_aspect_pref_matrix
        )

    def dispose(self):
        self._source_repository.dispose()