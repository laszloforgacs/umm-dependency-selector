import asyncio
from concurrent.futures import ThreadPoolExecutor

from domain.model.Result import Failure, Success, Result
from presentation.core.QualityModelStateSubject import QualityModelStateSubject
from presentation.util.Observer import Observer
from presentation.util.Util import print_items_with_last


class QualityModelListStateObserver(Observer):
    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=1)

    async def update(self, subject: QualityModelStateSubject) -> None:
        state = subject.state

        if state.is_loading:
            print("Loading quality models...")
            return

        if state.error is not None:
            print(f"Error: {state.error.message}")
            return

        loop = asyncio.get_running_loop()
        while True:
            quality_model_list = [
                quality_model.name for quality_model in state.quality_model_list
            ]
            print_items_with_last(quality_model_list, "Exit")
            user_input = await loop.run_in_executor(self._executor, input, "Select a quality model: ")
            list_size = len(quality_model_list)
            result = self._handle_user_input(
                user_input=user_input,
                list_size=list_size
            )

            if isinstance(result, Success):
                if result.value == list_size + 1:
                    print("Exiting...")
                    break
                print("Selected quality model: ", quality_model_list[result.value - 1])
                break
            else:
                print(f"Error: {result.message}")
                print("Please try again")

    def _handle_user_input(self, user_input: str, list_size: int) -> Result[int]:
        try:
            value = int(user_input)
            if value == list_size + 1:
                return Success(
                    value=list_size + 1
                )
            if 1 <= value <= list_size:
                return Success(
                    value=value
                )
            else:
                error_message = f"Input can only be 1 or you can exit" if list_size == 1 else f"Input must be between 1 and {list_size}"
                return Failure(
                    error_message=error_message
                )
        except ValueError as e:
            return Failure(error_message=str(e))

    def dispose(self):
        self.executor.shutdown(wait=True)
