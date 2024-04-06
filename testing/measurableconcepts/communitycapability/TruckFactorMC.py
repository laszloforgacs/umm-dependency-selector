from domain.model.MeasureableConcept import MeasurableConcept, OSSAspect, Impact


class TruckFactorMC(MeasurableConcept[int]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Truck Factor",
            children,
            Impact.POSITIVE,
            "Developers",
            "Calculating the Truck Factor of a repository",
            "Affects Community Capability positively",
            OSSAspect.COMMUNITY,
            normalize_visitor,
            aggregate_visitor,
        )