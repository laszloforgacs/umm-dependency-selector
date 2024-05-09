from domain.model.MeasureableConcept import MeasurableConcept, Impact, OSSAspect


class IssueAgeAverage(MeasurableConcept[float]):
    def __init__(
            self,
            children,
            normalize_visitor=None,
            aggregate_visitor=None
    ):
        super().__init__(
            "Issue Age Average",
            children,
            Impact.NEGATIVE,
            "Repository issue tracker",
            "Calculation of how long issues have been open for",
            "Long open issue age affects product evolution negatively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )
