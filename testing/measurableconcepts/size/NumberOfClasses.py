from domain.model.MeasureableConcept import OSSAspect, Impact, MeasurableConcept

"""
Category 2. It is measured by Sonar but that does not decide how the number of classes affect the project.
Is it good or bad to have a lot of classes? Does it depend on the size of the project?
We can select an optimal value and the value returned by the Visitor will be an "efficiency" value.
That is, the closer to the optimal value, the better.
"""


class NumberOfClasses(MeasurableConcept[float]):
    def __init__(self, children, normalize_visitor=None, aggregate_visitor=None):
        super().__init__(
            "Number of Classes",
            children,
            Impact.POSITIVE,
            "source code",
            "Calculating the efficiency of the number of classes in the repository",
            "Affects project size negatively",
            OSSAspect.CODE,
            normalize_visitor,
            aggregate_visitor
        )
