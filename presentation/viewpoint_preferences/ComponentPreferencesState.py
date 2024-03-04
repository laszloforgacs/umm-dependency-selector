from dataclasses import dataclass

PrefMatrix = dict[tuple[str, str], float | None]


@dataclass
class ComponentPreferencesState:
    pass


@dataclass
class ComponentsState(ComponentPreferencesState):
    viewpoint: 'Viewpoint'
    characteristics: list['Characteristic']
    sub_characteristics: list['SubCharacteristic']

    def copy(self, **kwargs):
        return ComponentsState(
            components=kwargs.get(
                'viewpoint', self.viewpoint,
                'characteristics', self.characteristics,
                'sub_characteristics', self.sub_characteristics
            )
        )


@dataclass
class SetPreferences(ComponentPreferencesState):
    preference_combination: tuple['CompositeComponent', 'CompositeComponent']

    def copy(self, **kwargs):
        return SetPreferences(
            preference_combination=kwargs.get('preference_combination', self.preference_combination)
        )


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
