from domain.model.MeasureableConcept import MeasurableConcept, Impact


class NumberOfReleases(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Number of releases",
            children,
            Impact.POSITIVE,
            "Release",
            "Calculation of the number of releases",
            "Number of releases affects reliability positively",
            normalize_visitor,
            aggregate_visitor
        )