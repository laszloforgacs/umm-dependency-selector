from abc import ABC, abstractmethod

from testing.visitors.LizardCyclomaticComplexityVisitor import LizardCyclomaticComplexityVisitor
from testing.visitors.StandardVisitors import MockMeasureVisitor, AverageAggregateVisitor, NoOpNormalizeVisitor


class MeasureCreationError(Exception):
    pass


class VisitorFactory(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def instantiate_with_visitor(self, type, **kwargs):
        pass


class MeasureVisitorFactory(VisitorFactory):
    def __init__(self):
        self.visitor_mappings = {
            # Key needs to be the exact name of the class, not the class property "name"
            # Add more mappings as needed
            "LinesOfCode": MockMeasureVisitor,
            "NumberOfComplexFunctions": MockMeasureVisitor,
            "NumberOfStatements": MockMeasureVisitor,
            "CyclomaticComplexityBaseMeasure": LizardCyclomaticComplexityVisitor
        }

    def instantiate_with_visitor(self, measure_type, **kwargs):
        try:
            measure = measure_type(**kwargs)
            visitor_type = self.visitor_mappings.get(measure_type.__name__)
            if visitor_type:
                measure.accept_visitor(visitor_type())
            return measure
        except KeyError as e:
            raise MeasureCreationError(f"Visitor mapping not found for {measure_type.__name__}.") from e
        except TypeError as e:
            raise MeasureCreationError(f"Failed to instantiate {measure_type.__name__} with provided arguments.") from e
        except Exception as e:
            raise MeasureCreationError(f"Unexpected error occurred while creating measure with visitor.") from e


class DerivedMeasureVisitorFactory(VisitorFactory):
    def __init__(self):
        self.visitor_mappings = {
            # Key needs to be the exact name of the class, not the class property "name"
            # Add more mappings as needed
            "CyclomaticComplexity": (NoOpNormalizeVisitor, AverageAggregateVisitor)
        }

    def instantiate_with_visitor(self, derived_measure_type, **kwargs):
        try:
            derived_measure = derived_measure_type(**kwargs)
            visitors = self.visitor_mappings.get(derived_measure_type.__name__)
            if visitors:
                normalize_visitor, aggregate_visitor = visitors
                derived_measure.accept_visitors(normalize_visitor(), aggregate_visitor())
            return derived_measure
        except KeyError as e:
            raise MeasureCreationError(f"Visitor mapping not found for {derived_measure_type.__name__}.") from e
        except TypeError as e:
            raise MeasureCreationError(
                f"Failed to instantiate {derived_measure_type.__name__} with provided arguments.") from e
        except Exception as e:
            raise MeasureCreationError(f"Unexpected error occurred while creating measure with visitor.") from e


class MeasurableConceptVisitorFactory(VisitorFactory):
    def __init__(self):
        self.visitor_mappings = {
            # Key needs to be the exact name of the class, not the class property "name"
            # Add more mappings as needed
            "ComplexityOfSourceCode": (NoOpNormalizeVisitor, AverageAggregateVisitor),
            "ComplexityOfSourceCode2": (NoOpNormalizeVisitor, AverageAggregateVisitor)
        }

    def instantiate_with_visitor(self, derived_measure_type, **kwargs):
        try:
            derived_measure = derived_measure_type(**kwargs)
            visitors = self.visitor_mappings.get(derived_measure_type.__name__)
            if visitors:
                normalize_visitor, aggregate_visitor = visitors
                derived_measure.accept_visitors(normalize_visitor(), aggregate_visitor())
            return derived_measure
        except KeyError as e:
            raise MeasureCreationError(f"Visitor mapping not found for {derived_measure_type.__name__}.") from e
        except TypeError as e:
            raise MeasureCreationError(
                f"Failed to instantiate {derived_measure_type.__name__} with provided arguments.") from e
        except Exception as e:
            raise MeasureCreationError(f"Unexpected error occurred while creating measure with visitor.") from e
