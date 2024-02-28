from dataclasses import dataclass
from typing import Optional

PrefMatrix = dict[tuple[str, str], float | None]


@dataclass
class ViewpointPreferencesState:
    pass


@dataclass
class ViewpointState(ViewpointPreferencesState):
    value: Optional['Viewpoint']

    def copy(self, **kwargs):
        return ViewpointState(value=kwargs.get('value', self.value))


@dataclass
class UserInput(ViewpointPreferencesState):
    characteristics: tuple[str, str]

    def copy(self, **kwargs):
        return UserInput(characteristics=kwargs.get('characteristics', self.characteristics))


@dataclass
class Error(ViewpointPreferencesState):
    message: str

    def copy(self, **kwargs):
        return Error(message=kwargs.get('message', self.message))


@dataclass
class Loading(ViewpointPreferencesState):
    pass

    def copy(self, **kwargs):
        return Loading()


ViewpointPrefState = ViewpointState | UserInput | Error | Loading
