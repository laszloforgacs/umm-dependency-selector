from domain.model.MeasureableConcept import Impact, OSSAspect, MeasurableConcept


class DelBiancoVulnerabilitiesMC(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "DelBianco Vulnerability",
            children,
            Impact.NEGATIVE,
            "Dependencies, source code",
            "Calculating the number of vulnerabilities",
            "Affects Risk Analysis/Security negatively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )