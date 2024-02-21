from abc import ABC, abstractmethod
from dataclasses import dataclass

from presentation.util.ErrorState import ErrorState


@dataclass
class PreferenceMatrixScreenState():
    matrix: dict[tuple[str, str], float]
    preferences_shown_to_user: list[tuple[str, str]]
    error: ErrorState | None

    def copy(self, **kwargs):
        # Create a copy of the current instance with updated attributes
        return PreferenceMatrixScreenState(matrix=kwargs.get('matrix', self.matrix),
                                           preferences_shown_to_user=kwargs.get('preferences_shown_to_user',
                                                                                self.preferences_shown_to_user),
                                           error=kwargs.get('error', self.error))
