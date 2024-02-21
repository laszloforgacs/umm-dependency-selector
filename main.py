import asyncio

from data.repository.QualityModelRepositoryImpl import QualityModelRepositoryImpl
from presentation.core.SharedViewModel import SharedViewModel
from presentation.quality_model_list.QualityModelListScreen import QualityModelListScreen
from presentation.quality_model_list.QualityModelListViewModel import QualityModelListViewModel


async def main():
    quality_model_repository = QualityModelRepositoryImpl()
    shared_view_model = SharedViewModel(quality_model_repository=quality_model_repository)
    quality_model_list_view_model = QualityModelListViewModel(shared_view_model=shared_view_model)
    quality_model_list_screen = QualityModelListScreen(
        view_model=quality_model_list_view_model,
        on_navigate_back=lambda: print("Navigate back")
    )
    quality_model_list_screen.on_created()
    # preference_matrix_screen = PreferenceMatrixScreen(
    #    view_model=PreferenceMatrixViewModel(shared_view_model=shared_view_model),
    #    on_navigate_back=lambda: print("Navigate back")
    # )
    # preference_matrix_screen.on_created()


if __name__ == "__main__":
    asyncio.run(main())
