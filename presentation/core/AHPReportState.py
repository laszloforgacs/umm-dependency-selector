from dataclasses import dataclass

from domain.model.Viewpoint import Viewpoint


@dataclass
class AHPReportState:
    comparisons: list[str, dict]
    viewpoint: 'Viewpoint'
    characteristics: list['Characteristic']

    def copy(self, **kwargs):
        return AHPReportState(
            report=kwargs.get(
                'comparisons', self.comparisons,
                'viewpoint', self.viewpoint,
                'characteristics', self.characteristics
            )
        )
