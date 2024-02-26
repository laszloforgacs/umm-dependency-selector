import asyncio
from typing import Callable

from data.repository.QualityModelRepositoryImpl import QualityModelRepositoryImpl
from presentation.core.NavigationController import NavigationController
from presentation.core.SharedViewModel import SharedViewModel
from presentation.quality_model_list.QualityModelListScreen import QualityModelListScreen
from presentation.quality_model_list.QualityModelListViewModel import QualityModelListViewModel
from presentation.viewpoint_list.ViewpointListScreen import ViewpointListScreen


async def main():
    navigation_controller = NavigationController()
    quality_model_repository = QualityModelRepositoryImpl()
    shared_view_model = SharedViewModel(quality_model_repository=quality_model_repository)
    asyncio.create_task(shared_view_model.fetch_quality_models())
    quality_model_list_view_model = QualityModelListViewModel(shared_view_model=shared_view_model)

    navigation_controller.navigate_to(
        _provide_quality_model_list_screen(
            view_model=quality_model_list_view_model,
            on_navigate_back=lambda: print("Navigate back")
        )
    )

    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    await asyncio.gather(*tasks)
    # preference_matrix_screen = PreferenceMatrixScreen(
    #    view_model=PreferenceMatrixViewModel(shared_view_model=shared_view_model),
    #    on_navigate_back=lambda: print("Navigate back")
    # )
    # preference_matrix_screen.on_created()


def _provide_quality_model_list_screen(
        view_model: QualityModelListViewModel,
        on_navigate_back: Callable[[None], None]
):
    return lambda: QualityModelListScreen(
        view_model=view_model,
        on_navigate_back=on_navigate_back
    )


def _provide_viewpoint_list_screen(
        on_navigate_back: Callable[[None], None]
):
    return lambda: ViewpointListScreen(
        on_navigate_back=on_navigate_back
    )


if __name__ == "__main__":
    asyncio.run(main())
