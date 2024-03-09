from dataclasses import dataclass

from domain.model.Viewpoint import Viewpoint


@dataclass
class AHPReportState:
    report: dict
    viewpoint: 'Viewpoint'
    characteristics: list['Characteristic']

    def copy(self, **kwargs):
        return AHPReportState(
            report=kwargs.get(
                'report', self.report,
                'viewpoint', self.viewpoint,
                'characteristics', self.characteristics
            )
        )
