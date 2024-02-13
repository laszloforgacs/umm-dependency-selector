from model.CyclomaticComplexity import CyclomaticComplexity
from model.LinesOfCode import LinesOfCode
from model.NumberOfComplexFunctions import NumberOfComplexFunctions
from model.measurement.Measure import BaseMeasure, MeasurementMethod, DerivedMeasure

if __name__ == "__main__":
    print("Hello, world!")

    baseMeasure1 = LinesOfCode()
    print(baseMeasure1.name)
    print(baseMeasure1.children)
    baseMeasure2 = NumberOfComplexFunctions()
    derivedMeasure1 = CyclomaticComplexity()
    derivedMeasure1.add_component(baseMeasure1)
    derivedMeasure1.add_component(baseMeasure2)
    print(derivedMeasure1.name)
    print(derivedMeasure1.children)
    results = [success.value for success in derivedMeasure1.measure()]
    print(results)



