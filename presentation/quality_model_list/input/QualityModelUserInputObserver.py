from typing import Callable

import aioconsole

from domain.model.Result import Success, Failure, Result
from presentation.quality_model_list.QualityModelListStateSubject import QualityModelListStateSubject
from presentation.quality_model_list.input.QualityModelUserInputSubject import QualityModelUserInputSubject
from presentation.util.Observer import Observer


class QualityModelUserInputObserver(Observer):

    def __init__(self, quality_model_list_state_subject: QualityModelListStateSubject,
                 on_update: Callable[[bool], None] = None):
        self._quality_model_list_state_subject = quality_model_list_state_subject
        self._on_update = on_update

    async def update(self, subject: QualityModelUserInputSubject):
        state = subject.state

        if state.should_wait_for_user_input:
            while True:
                user_input = await aioconsole.ainput("Select a quality model: ")
                quality_model_list = self._quality_model_list_state_subject.state.quality_model_list
                list_size = len(quality_model_list)
                result = self._handle_user_input(
                    user_input=user_input,
                    list_size=list_size
                )

                if isinstance(result, Success):
                    if result.value == list_size + 1:
                        print("Exiting...")
                        await self._on_update(True)
                        break
                    print("Selected quality model: ", quality_model_list[result.value - 1].name)
                    await self._on_update(True)
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
