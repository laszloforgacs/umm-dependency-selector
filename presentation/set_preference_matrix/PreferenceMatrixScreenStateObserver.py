from domain.model.Result import Failure, Success, Result
from presentation.set_preference_matrix import PreferenceMatrixScreenStateSubject
from presentation.util.Constants import INPUT_SET_PREFERENCE, ERROR_SET_PREFERENCE_VALUE_INVALID
from presentation.util.Observer import Observer
from presentation.util.Util import is_pref_matrix_valid


class PreferenceMatrixScreenStateObserver(Observer):
    def update(self, subject: PreferenceMatrixScreenStateSubject) -> None:
        state = subject.state

        if isinstance(state, Failure):
            print(f"Error: {state.message}")
            return

        if state.preferences_shown_to_user is not None and is_pref_matrix_valid(state.matrix):
            while True:
                try:
                    user_input = input(INPUT_SET_PREFERENCE)
                    result = self._sanitize_preference_input(user_input)
                    if isinstance(result, Success):
                        print("preference: ", result.value)
                        break
                    else:
                        subject.set_state(state.copy(message=result.message))
                except ValueError as e:
                    subject.set_state(state.copy(message=str(e)))

    def _sanitize_preference_input(self, input: str) -> Result:
        try:
            value = float(input)
            if 1 <= value <= 9:
                return Success(value)
            else:
                return Failure(error_message=ERROR_SET_PREFERENCE_VALUE_INVALID)
        except ValueError as e:
            return Failure(error_message=str(e))