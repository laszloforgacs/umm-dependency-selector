from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
CHAOSS measurable concept.
A higher ratio suggests that a larger proportion of contributions meet the project's requirements
or expectations, indicating either high-quality submissions or less stringent review
standards. A lower ratio would indicate a more rigorous or selective review process.
CATEGORY 1
"""


class ChangeRequestAcceptanceRatio(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Change Request Acceptance Ratio",
            children,
            Impact.POSITIVE,
            "version control history",
            "Calculating the ratio of accepted pull requests to declined pull requests",
            "Affects Community Capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
