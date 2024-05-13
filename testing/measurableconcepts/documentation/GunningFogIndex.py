from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept


class GunningFogIndex(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Average Gunning Fog Index of files",
            children,
            Impact.NEGATIVE,
            "text files in the repository",
            "Calculating the average Gunning Fog Index of files in the repository",
            "Smaller Gunning Fog Index affects the readability of documentation positively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )
