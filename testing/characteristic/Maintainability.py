from domain.model.Characteristic import Characteristic
from domain.model.SubCharacteristic import SubCharacteristic
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix


class Maintainability(Characteristic[float]):
    def __init__(self, children: dict[str, SubCharacteristic] = {}, preference_matrix: PrefMatrix = {}):
        super().__init__("Maintainability", children, preference_matrix=preference_matrix)
        self._weight = 0.0


class Maintainability2(Characteristic[float]):
    def __init__(self, children: dict[str, SubCharacteristic] = {}, preference_matrix: PrefMatrix = {}):
        super().__init__("Maintainability2", children, preference_matrix=preference_matrix)
        self._weight = 0.0


class Maintainability3(Characteristic[float]):
    def __init__(self, children: dict[str, SubCharacteristic] = {}, preference_matrix: PrefMatrix = {}):
        super().__init__("Maintainability3", children, preference_matrix=preference_matrix)
        self._weight = 0.0


class Maintainability4(Characteristic[float]):
    def __init__(self, children: dict[str, SubCharacteristic] = {}, preference_matrix: PrefMatrix = {}):
        super().__init__("Maintainability4", children, preference_matrix=preference_matrix)
        self._weight = 0.0
