from dataclasses import dataclass

PrefMatrix = dict[tuple[str, str], int | float | None]


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
class SetOSSAspectPreferences(ComponentPreferencesState):
    oss_aspect_combination: tuple[str, str]

    def copy(self, **kwargs):
        return SetOSSAspectPreferences(
            oss_aspect_combination=kwargs.get('oss_aspect_combination', self.oss_aspect_combination)
        )


@dataclass
class Refetch(ComponentPreferencesState):
    pass

    def copy(self, **kwargs):
        return Refetch()


@dataclass
class UrlInput(ComponentPreferencesState):
    comparisons: dict[str, 'Compare']
    viewpoint: 'Viewpoint'
    characteristics: list['Characteristic']

    def copy(self, **kwargs):
        return UrlInput(
            comparisons=kwargs.get('comparisons', self.comparisons),
            viewpoint=kwargs.get('viewpoint', self.viewpoint),
            characteristics=kwargs.get('characteristics', self.characteristics)
        )


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


ComponentPrefState = ComponentsState | SetPreferences | SetOSSAspectPreferences | Refetch | UrlInput | Error | Loading | NavigateBack
