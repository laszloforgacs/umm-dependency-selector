from dataclasses import dataclass

PrefMatrix = dict[tuple[str, str], float | None]


@dataclass
class ComponentPreferencesState:
    pass


@dataclass
class ComponentsState(ComponentPreferencesState):
    components: list['CompositeComponent']

    def copy(self, **kwargs):
        return ComponentsState(components=kwargs.get('components', self.components))


@dataclass
class SetPreferences(ComponentPreferencesState):
    components: list['CompositeComponent']

    def copy(self, **kwargs):
        return SetPreferences(components=kwargs.get('components', self.components))


@dataclass
class UserInput(ComponentPreferencesState):
    characteristics: tuple[str, str]

    def copy(self, **kwargs):
        return UserInput(characteristics=kwargs.get('characteristics', self.characteristics))


@dataclass
class Error(ComponentPreferencesState):
    message: str

    def copy(self, **kwargs):
        return Error(message=kwargs.get('message', self.message))


@dataclass
class Loading(ComponentPreferencesState):
    pass

    def copy(self, **kwargs):
        return Loading()


@dataclass
class NavigateBack(ComponentPreferencesState):
    pass

    def copy(self, **kwargs):
        return NavigateBack()


ComponentPrefState = ComponentsState | SetPreferences | UserInput | Error | Loading | NavigateBack
