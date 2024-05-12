from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
CHAOSS measurable concept.
Belongs to Community Growth. Category 1 measure
"""


class NumberOfDownloads(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Number Of Downloads",
            children,
            Impact.POSITIVE,
            "release assets",
            "Number of Downloads measures the relative and absolute traffic to a project’s repository on the frequency of downloaded or cloned software artifacts",
            "Increasing download numbers indicates interest in the project",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
