from domain.model.Characteristic import Characteristic
from domain.model.SubCharacteristic import SubCharacteristic
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix


class CommunityAndAdoption(Characteristic[float]):
    def __init__(self, children: dict[str, SubCharacteristic] = {}, preference_matrix: PrefMatrix = {}):
        super().__init__("Community and Adoption", children, preference_matrix=preference_matrix)
