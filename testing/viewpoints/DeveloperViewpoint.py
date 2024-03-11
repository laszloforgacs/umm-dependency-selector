from domain.model.Characteristic import Characteristic
from domain.model.Result import Result, Success
from domain.model.Viewpoint import Viewpoint


class DeveloperViewpoint(Viewpoint):
    def __init__(self, children: dict[str, Characteristic] = {}, preference_matrix: dict[tuple[str, str], float] = {}):
        super().__init__("Developer Viewpoint", children, preference_matrix)

    def get_characteristics(self) -> list[str]:
        return [
            "Analyzability",
            "Changeability",
            "Stability",
            "Testability",
            "Maintainability",
            "Reusability",
            "Understandability",
            "Compatibility"
        ]
