from measurableconcepts.ComplexityOfSourceCode import ComplexityOfSourceCode
from measures.CyclomaticComplexity import CyclomaticComplexity
from measures.LinesOfCode import LinesOfCode
from measures.NumberOfComplexFunctions import NumberOfComplexFunctions
from measures.NumberOfStatements import NumberOfStatements

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
