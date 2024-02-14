from testing.measurableconcepts.ComplexityOfSourceCode import ComplexityOfSourceCode
from testing.measures.CyclomaticComplexity import CyclomaticComplexity
from testing.measures.LinesOfCode import LinesOfCode
from testing.measures.NumberOfComplexFunctions import NumberOfComplexFunctions
from testing.measures.NumberOfStatements import NumberOfStatements
from testing.subcharacteristic.Analyzability import Analyzability

if __name__ == "__main__":
    print("Hello, world!")

    linesOfCode = LinesOfCode()
    numberOfComplexFunctions = NumberOfComplexFunctions()
    cyclomaticComplexity = CyclomaticComplexity()
    cyclomaticComplexity.add_component(linesOfCode)
    cyclomaticComplexity.add_component(numberOfComplexFunctions)
    numberOfStatements = NumberOfStatements()

    resultCyclomaticComplexity = [
        component.measure().value
        for component in cyclomaticComplexity.children.values()
    ]

    resultNumberOfStatements = numberOfStatements.measure().value

    print(resultCyclomaticComplexity)
    print(resultNumberOfStatements)

    complexityOfSourceCode = ComplexityOfSourceCode()
    complexityOfSourceCode.add_component(cyclomaticComplexity)
    complexityOfSourceCode.add_component(numberOfStatements)
    codeComplexity = complexityOfSourceCode.run().value
    print(codeComplexity)

    analyzability = Analyzability({})
    analyzability.add_component(complexityOfSourceCode)
    print(analyzability.run().value)

