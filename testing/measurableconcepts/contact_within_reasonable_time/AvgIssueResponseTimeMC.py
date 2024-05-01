from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class AvgIssueResponseTimeMC(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Average Issue Response Time",
            children,
            Impact.POSITIVE,
            "First comment on issues",
            "Calculating the average time to respond to issues",
            "Affects 'Contact within reasonable time' positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor
        )