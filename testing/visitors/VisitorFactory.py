from abc import ABC, abstractmethod

from testing.visitors.StandardVisitors import MockMeasureVisitor, AverageAggregateVisitor, NoOpNormalizeVisitor, \
    AddAggregateVisitor
from testing.visitors.codecomplexity.ClocNumberOfCommentsVisitor import ClocNumberOfCommentsVisitor
from testing.visitors.codecomplexity.CruzCodeQualityDerivedMeasureAggregator import \
    CruzCodeQualityDerivedMeasureAggregator
from testing.visitors.codecomplexity.LizardCyclomaticComplexityVisitor import LizardCyclomaticComplexityVisitor
from testing.visitors.codecomplexity.LizardLinesOfCodeVisitor import LizardLinesOfCodeVisitor
from testing.visitors.communitycapability.PyGithubCommunityCountVisitor import PyGithubCommunityCountVisitor
from testing.visitors.license.OSSAQMLicenseVisitor import OSSAQMLicenseVisitor
from testing.visitors.risk.DelBiancoSnykRiskMeasureVisitor import DelBiancoSnykRiskMeasureVisitor


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
            "ContributorCount": PyGithubCommunityCountVisitor,
            "DelBiancoRiskMeasure": DelBiancoSnykRiskMeasureVisitor,
            "License": OSSAQMLicenseVisitor,
            "CruzNumberOfCommentsBaseMeasure": ClocNumberOfCommentsVisitor,
            "LinesOfCode": LizardLinesOfCodeVisitor,
            "NumberOfComplexFunctions": MockMeasureVisitor,
            "NumberOfStatements": MockMeasureVisitor,
            "CruzCyclomaticComplexityBaseMeasure": LizardCyclomaticComplexityVisitor
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
            "CyclomaticComplexity": (NoOpNormalizeVisitor, AverageAggregateVisitor),
            "CruzCodeQualityDerivedMeasure": (NoOpNormalizeVisitor, CruzCodeQualityDerivedMeasureAggregator)
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
            "DelBiancoVulnerabilitiesMC": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "AbsenceOfLicenseFees": (NoOpNormalizeVisitor, AverageAggregateVisitor),
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
