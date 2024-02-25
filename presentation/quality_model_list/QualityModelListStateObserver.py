from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from domain.model.Result import Failure, Success, Result
from presentation.core.QualityModelStateSubject import QualityModelStateSubject
from presentation.util.Observer import Observer
from presentation.util.Util import print_items_with_last


class QualityModelListStateObserver(Observer):

    def __init__(self, on_update: Callable[[bool], None] = None):
        self._on_update = on_update

    async def update(self, subject: QualityModelStateSubject) -> None:
        state = subject.state

        if state.is_loading:
            print("Loading quality models...")
            return None

        if state.error is not None:
            print(f"Error: {state.error.message}")
            return None

        if len(state.quality_model_list) > 0:
            quality_model_list = [
                quality_model.name for quality_model in state.quality_model_list
            ]

            print_items_with_last(quality_model_list, "Exit")
            await self._on_update(True)
