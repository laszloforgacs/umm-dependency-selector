from abc import ABC, abstractmethod

from testing.measures.community_vitality.RepositoryAgeMeasureVisitor import RepositoryAgeMeasureVisitor
from testing.measures.communitycapability.AvgNumberOfCommitsPerPRsVisitor import AvgNumberOfCommitsPerPRsVisitor
from testing.measures.communitycapability.AvgNumberOfContributorsPerPRsVisitor import \
    AvgNumberOfContributorsPerPRsVisitor
from testing.measures.communitycapability.LinesChangedCountVisitor import LinesChangedCountVisitor
from testing.measures.maintainer_organization.OrgCountMeasureVisitor import OrgCountMeasureVisitor
from testing.measures.number_of_open_feature_request.OpenFeatureRequestCountVisitor import \
    OpenFeatureRequestCountVisitor
from testing.measures.numberofreleases.ReleaseCountVisitor import ReleaseCountVisitor
from testing.measures.open_participation.NewContributorsVisitor import NewContributorsVisitor
from testing.measures.peer_influence.RepoMessagesVisitor import RepoMessagesVisitor
from testing.measures.popularity.AnnualCommitCountVisitor import AnnualCommitCountVisitor
from testing.measures.popularity.DownloadsCountVisitor import DownloadsCountVisitor
from testing.measures.popularity.ForksCountVisitor import ForksCountVisitor
from testing.measures.popularity.StarsCountVisitor import StarsCountVisitor
from testing.measures.popularity.WatchersCountVisitor import WatchersCountVisitor
from testing.measures.product_evolution.CommitCountVisitor import CommitCountVisitor
from testing.measures.product_evolution.declined_changes.ReviewsDeclinedCountVisitor import ReviewsDeclinedCountVisitor
from testing.measures.product_evolution.declined_changes.ReviewsDeclinedAggregator import ReviewsDeclinedAggregator
from testing.measures.product_evolution.issue_interactions.UpdatedIssuesCountVisitor import UpdatedIssuesCountVisitor
from testing.measures.product_evolution.opened_pull_requests.OpenedPullRequestCountVisitor import \
    OpenedPullRequestCountVisitor
from testing.measures.product_evolution.reviews_accepted.ReviewsAcceptedCountVisitor import ReviewsAcceptedCountVisitor
from testing.measures.product_evolution.reviews_accepted.ReviewsAcceptedRatioVisitor import ReviewsAcceptedRatioVisitor
from testing.measures.product_evolution.staleness.OpenIssueAgeVisitor import OpenIssueAgeVisitor
from testing.measures.product_evolution.updated_since.TimeSinceLastCommitVIsitor import TimeSinceLastCommitVisitor
from testing.subcharacteristic.communitycapability.AugurClosedIssuesCountVisitor import AugurClosedIssuesCountVisitor
from testing.subcharacteristic.communitycapability.AugurIssueThroughputVisitor import AugurIssueThroughputVisitor
from testing.subcharacteristic.communitycapability.AugurTotalIssuesCountVisitor import AugurTotalIssuesCountVisitor
from testing.visitors.StandardVisitors import MockMeasureVisitor, AverageAggregateVisitor, NoOpNormalizeVisitor, \
    AddAggregateVisitor
from testing.visitors.codecomplexity.AugurClosedIssueResolutionDurationVisitor import \
    AugurClosedIssueResolutionDurationVisitor
from testing.visitors.codecomplexity.IssueResponseTimeVisitor import IssueResponseTimeVisitor
from testing.visitors.codecomplexity.ClocNumberOfCommentsVisitor import ClocNumberOfCommentsVisitor
from testing.visitors.codecomplexity.CruzCodeQualityDerivedMeasureAggregator import \
    CruzCodeQualityDerivedMeasureAggregator
from testing.visitors.codecomplexity.LizardCyclomaticComplexityVisitor import LizardCyclomaticComplexityVisitor
from testing.visitors.codecomplexity.LizardLinesOfCodeVisitor import LizardLinesOfCodeVisitor
from testing.visitors.communitycapability.PyGithubCommunityCountVisitor import PyGithubCommunityCountVisitor
from testing.visitors.communitycapability.TruckFactorVisitor import TruckFactorVisitor
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
            "ReviewsAcceptedCount": ReviewsAcceptedCountVisitor,
            "AvgNumberOfContributorsPerPRs": AvgNumberOfContributorsPerPRsVisitor,
            "AvgNumberOfCommitsPerPRs": AvgNumberOfCommitsPerPRsVisitor,
            "LinesChangedCount": LinesChangedCountVisitor,
            "DownloadsCount": DownloadsCountVisitor,
            "AnnualCommitCount": AnnualCommitCountVisitor,
            "ForksCount": ForksCountVisitor,
            "StarsCount": StarsCountVisitor,
            "WatchersCount": WatchersCountVisitor,
            "OrgCountMeasure": OrgCountMeasureVisitor,
            "RepositoryAgeMeasure": RepositoryAgeMeasureVisitor,
            "RepoMessages": RepoMessagesVisitor,
            "NewContributors": NewContributorsVisitor,
            "ReviewsAcceptedRatio": ReviewsAcceptedRatioVisitor,
            "OpenedPullRequestCount": OpenedPullRequestCountVisitor,
            "ReviewsDeclinedCount": ReviewsDeclinedCountVisitor,
            "OpenIssueAge": OpenIssueAgeVisitor,
            "UpdatedIssuesCount": UpdatedIssuesCountVisitor,
            "TimeSinceLastCommit": TimeSinceLastCommitVisitor,
            "CommitCount": CommitCountVisitor,
            "OpenFeatureRequestCount": OpenFeatureRequestCountVisitor,
            "ReleaseCount": ReleaseCountVisitor,
            "IssueResponseTime": IssueResponseTimeVisitor,
            "ClosedIssueResolutionDuration": AugurClosedIssueResolutionDurationVisitor,
            "TotalIssuesCount": AugurTotalIssuesCountVisitor,
            "ClosedIssuesCount": AugurClosedIssuesCountVisitor,
            "TruckFactor": TruckFactorVisitor,
            "ContributorCount": PyGithubCommunityCountVisitor,
            "DelBiancoRiskMeasure": DelBiancoSnykRiskMeasureVisitor,
            "License": OSSAQMLicenseVisitor,
            "CruzNumberOfCommentsBaseMeasure": ClocNumberOfCommentsVisitor,
            "LinesOfCode": LizardLinesOfCodeVisitor,
            "NumberOfComplexFunctions": MockMeasureVisitor,
            "NumberOfStatements": MockMeasureVisitor,
            "CruzCyclomaticComplexityBaseMeasure": LizardCyclomaticComplexityVisitor
        }

    def instantiate_with_visitor(self, measure_type, visitor_kwargs=None, **measure_kwargs):
        try:
            measure = measure_type(**measure_kwargs)
            visitor_type = self.visitor_mappings.get(measure_type.__name__)
            if visitor_type:
                if visitor_kwargs is None:
                    visitor_kwargs = {}
                visitor = visitor_type(**visitor_kwargs)
                measure.accept_visitor(visitor)
            print(f"Created measure {measure.name} with visitor {visitor_type.__name__}")
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
            "ReviewsDeclinedRatio": (NoOpNormalizeVisitor, ReviewsDeclinedAggregator),
            "IssueThroughput": (NoOpNormalizeVisitor, AugurIssueThroughputVisitor),
            "CyclomaticComplexity": (NoOpNormalizeVisitor, AverageAggregateVisitor),
            "CruzCodeQualityDerivedMeasure": (NoOpNormalizeVisitor, CruzCodeQualityDerivedMeasureAggregator)
        }

    def instantiate_with_visitor(
            self,
            derived_measure_type,
            normalize_visitor_kwargs=None,
            aggregate_visitor_kwargs=None,
            **measure_kwargs
    ):
        try:
            derived_measure = derived_measure_type(**measure_kwargs)
            visitors = self.visitor_mappings.get(derived_measure_type.__name__)
            if visitors:
                normalize_visitor, aggregate_visitor = visitors
                if normalize_visitor_kwargs is None:
                    normalize_visitor_kwargs = {}
                if aggregate_visitor_kwargs is None:
                    aggregate_visitor_kwargs = {}
                derived_measure.accept_visitors(
                    normalize_visitor(**normalize_visitor_kwargs),
                    aggregate_visitor(**aggregate_visitor_kwargs)
                )

            print(
                f"Created derived measure {derived_measure.name} with visitors {normalize_visitor.__name__} and {aggregate_visitor.__name__}")
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
            "ChangeRequestsDeclinedRatio": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "ChangeRequestsDeclinedCount": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "ChangeRequestsAcceptedRatio": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "ChangeRequestsAcceptedCount": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "ChangeRequestContributors": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "ChangeRequestCommits": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "CodeChangesLines": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "CodeChangesCommits": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "PopularityMC": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "MaintainerOrganizationMC": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "CommunityLifespan": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "CyclomaticComplexityMC": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "AvgIssueResponseTimeMC": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "CommunityInteractionMC": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "NewContributorsMC": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "PeerInfluence": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "OpenParticipation": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "ReviewsAccepted": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "OpenedPullRequests": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "DeclinedChanges": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "Staleness": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "IssueInteractions": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "UpdatedSince": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "CommitFrequency": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "NumberOfOpenFeatureRequests": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "NumberOfReleases": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "TimeToRespondToIssues": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "DurationToCloseIssuesMC": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "IssueThroughputMC": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "TruckFactorMC": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "NumberOfContributors": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "DelBiancoVulnerabilitiesMC": (NoOpNormalizeVisitor, AddAggregateVisitor),
            "AbsenceOfLicenseFees": (NoOpNormalizeVisitor, AverageAggregateVisitor),
            "ComplexityOfSourceCode": (NoOpNormalizeVisitor, AverageAggregateVisitor),
            "ComplexityOfSourceCode2": (NoOpNormalizeVisitor, AverageAggregateVisitor)
        }

    def instantiate_with_visitor(
            self,
            measurable_concept_type,
            normalize_visitor_kwargs=None,
            aggregate_visitor_kwargs=None,
            **measure_kwargs
    ):
        try:
            measurable_concept = measurable_concept_type(**measure_kwargs)
            visitors = self.visitor_mappings.get(measurable_concept_type.__name__)
            if visitors:
                normalize_visitor, aggregate_visitor = visitors
                if normalize_visitor_kwargs is None:
                    normalize_visitor_kwargs = {}
                if aggregate_visitor_kwargs is None:
                    aggregate_visitor_kwargs = {}
                measurable_concept.accept_visitors(
                    normalize_visitor(**normalize_visitor_kwargs),
                    aggregate_visitor(**aggregate_visitor_kwargs)
                )

            print(
                f"Created measurable concept {measurable_concept.name} with visitors {normalize_visitor.__name__} and {aggregate_visitor.__name__}")
            return measurable_concept
        except KeyError as e:
            raise MeasureCreationError(f"Visitor mapping not found for {measurable_concept_type.__name__}.") from e
        except TypeError as e:
            raise MeasureCreationError(
                f"Failed to instantiate {measurable_concept_type.__name__} with provided arguments.") from e
        except Exception as e:
            raise MeasureCreationError(f"Unexpected error occurred while creating measure with visitor.") from e
