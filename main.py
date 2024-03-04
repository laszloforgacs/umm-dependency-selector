import asyncio

from ahpy import ahpy

from presentation.core.Dependencies import Dependencies
from presentation.core.NavigationController import NavigationController
from presentation.core.Navigator import Navigator
from presentation.util.Constants import QUALITY_MODEL_LIST_SCREEN


async def main():
    dependencies = Dependencies()

    asyncio.create_task(dependencies.shared_view_model.fetch_quality_models())
    await dependencies.navigator.navigate_to(QUALITY_MODEL_LIST_SCREEN)

    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    await asyncio.gather(*tasks)
    # preference_matrix_screen = PreferenceMatrixScreen(
    #    view_model=PreferenceMatrixViewModel(shared_view_model=shared_view_model),
    #    on_navigate_back=lambda: print("Navigate back")
    # )
    # preference_matrix_screen.on_created()


if __name__ == "__main__":
    asyncio.run(main())
