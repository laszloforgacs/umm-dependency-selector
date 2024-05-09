import asyncio
import json
import os
from typing import Final

import aiofiles

from domain.model.Characteristic import Characteristic
from domain.model.QualityModel import QualityModel
from domain.model.Result import Result, Success, Failure
from domain.model.Viewpoint import Viewpoint
from domain.repository.QualityModelRepository import QualityModelRepository
from testing.characteristic.Cost import Cost
from testing.characteristic.CommunityAndAdoption import CommunityAndAdoption
from testing.characteristic.InteroperabilityCompatibility import InteroperabilityCompatibility
from testing.characteristic.Reliability import Reliability
from testing.characteristic.SupportAndService import SupportAndService
from testing.measurableconcepts.AbsenceOfLicenseFees import AbsenceOfLicenseFees
from testing.measurableconcepts.community_exists.CommunityInteractionMC import CommunityInteractionMC
from testing.measurableconcepts.community_exists.NewContributorsMC import NewContributorsMC
from testing.measurableconcepts.community_vitality.CommunityLifespan import CommunityLifespan
from testing.measurableconcepts.communitycapability.DurationToCloseIssuesMC import DurationToCloseIssuesMC
from testing.measurableconcepts.communitycapability.IssueThroughputMC import IssueThroughputMC
from testing.measurableconcepts.communitycapability.NumberOfContributors import NumberOfContributors
from testing.measurableconcepts.communitycapability.TimeToRespondToIssues import TimeToRespondToIssues
from testing.measurableconcepts.communitycapability.TruckFactorMC import TruckFactorMC
from testing.measurableconcepts.communitycapability.code_development_activity.ChangeRequestCommits import \
    ChangeRequestCommits
from testing.measurableconcepts.communitycapability.code_development_activity.ChangeRequestContributors import \
    ChangeRequestContributors
from testing.measurableconcepts.communitycapability.code_development_activity.CodeChangesCommits import \
    CodeChangesCommits
from testing.measurableconcepts.communitycapability.code_development_activity.CodeChangesLines import CodeChangesLines
from testing.measurableconcepts.communitycapability.code_development_efficiency.ChangeRequestAcceptanceRatio import \
    ChangeRequestAcceptanceRatio
from testing.measurableconcepts.communitycapability.code_development_efficiency.ChangeRequestsAcceptedCount import \
    ChangeRequestsAcceptedCount
from testing.measurableconcepts.communitycapability.code_development_efficiency.ChangeRequestsAcceptedRatio import \
    ChangeRequestsAcceptedRatio
from testing.measurableconcepts.communitycapability.code_development_efficiency.ChangeRequestsDeclinedCount import \
    ChangeRequestsDeclinedCount
from testing.measurableconcepts.communitycapability.code_development_efficiency.ChangeRequestsDeclinedRatio import \
    ChangeRequestsDeclinedRatio
from testing.measurableconcepts.communitycapability.code_development_process_quality.ChangeRequestReviews import \
    ChangeRequestReviews
from testing.measurableconcepts.communitycapability.issue_resolution.IssuesActiveCount import IssuesActiveCount
from testing.measurableconcepts.communitycapability.issue_resolution.IssuesActiveRatio import IssuesActiveRatio
from testing.measurableconcepts.communitycapability.issue_resolution.IssuesClosedCount import IssuesClosedCount
from testing.measurableconcepts.communitycapability.issue_resolution.IssuesClosedRatio import IssuesClosedRatio
from testing.measurableconcepts.communitycapability.issue_resolution.IssuesNewCount import IssuesNewCount
from testing.measurableconcepts.communitycapability.issue_resolution.IssuesNewRatio import IssuesNewRatio
from testing.measurableconcepts.complexity.CyclomaticComplexityMC import CyclomaticComplexityMC
from testing.measurableconcepts.contact_within_reasonable_time.AvgIssueResponseTimeMC import AvgIssueResponseTimeMC
from testing.measurableconcepts.maintainer_organization.MaintainerOrganizationMC import MaintainerOrganizationMC
from testing.measurableconcepts.numberofopenfeaturerequests.NumberOfOpenFeatureRequests import \
    NumberOfOpenFeatureRequests
from testing.measurableconcepts.numberofreleases.NumberOfReleases import NumberOfReleases
from testing.measurableconcepts.popularity.PopularityMC import PopularityMC
from testing.measurableconcepts.product_evolution.CommitFrequency import CommitFrequency
from testing.measurableconcepts.product_evolution.DeclinedChanges import DeclinedChanges
from testing.measurableconcepts.product_evolution.IssueInteractions import IssueInteractions
from testing.measurableconcepts.product_evolution.OpenedPullRequests import OpenedPullRequests
from testing.measurableconcepts.product_evolution.ReviewsAccepted import ReviewsAccepted
from testing.measurableconcepts.product_evolution.IssueAgeAverage import IssueAgeAverage
from testing.measurableconcepts.risk.DelBiancoVulnerabilitiesMC import DelBiancoVulnerabilitiesMC
from testing.measurableconcepts.product_evolution.UpdatedSince import UpdatedSince
from testing.measurableconcepts.support_community.OpenParticipation import OpenParticipation
from testing.measurableconcepts.support_community.PeerInfluence import PeerInfluence
from testing.measures.CruzCodeQualityDerivedMeasure import CruzCodeQualityDerivedMeasure
from testing.measures.CruzCyclomaticComplexityBaseMeasure import CruzCyclomaticComplexityBaseMeasure
from testing.measures.CruzNumberOfCommentsBaseMeasure import CruzNumberOfCommentsBaseMeasure
from testing.measures.License import License
from testing.measures.community_vitality.RepositoryAgeMeasure import RepositoryAgeMeasure
from testing.measures.communitycapability.change_request_acceptance_ratio.ReviewsAcceptedToDeclinedRatio import \
    ReviewsAcceptedToDeclinedRatio
from testing.measures.communitycapability.change_request_commits.AvgNumberOfCommitsPerPRs import \
    AvgNumberOfCommitsPerPRs
from testing.measures.communitycapability.change_request_contributors.AvgNumberOfContributorsPerPRs import \
    AvgNumberOfContributorsPerPRs
from testing.measures.communitycapability.ClosedIssueResolutionDuration import ClosedIssueResolutionDuration
from testing.measures.communitycapability.ClosedIssuesCount import ClosedIssuesCount
from testing.measures.communitycapability.ContributorCount import ContributorCount
from testing.measures.communitycapability.IssueResponseTime import IssueResponseTime
from testing.measures.communitycapability.IssueThroughput import IssueThroughput
from testing.measures.communitycapability.LinesChangedCount import LinesChangedCount
from testing.measures.communitycapability.TotalIssuesCount import TotalIssuesCount
from testing.measures.communitycapability.TruckFactor import TruckFactor
from testing.measures.communitycapability.change_request_reviews.PercentageOfPRsReviewed import PercentageOfPRsReviewed
from testing.measures.communitycapability.issue_resolution.issues_active.ActiveIssuesRatio import ActiveIssuesRatio
from testing.measures.communitycapability.issue_resolution.issues_closed.ClosedIssuesRatio import ClosedIssuesRatio
from testing.measures.communitycapability.issue_resolution.issues_new.NewIssuesCount import NewIssuesCount
from testing.measures.communitycapability.issue_resolution.issues_new.NewIssuesRatio import NewIssuesRatio
from testing.measures.maintainer_organization.OrgCountMeasure import OrgCountMeasure
from testing.measures.number_of_open_feature_request.OpenFeatureRequestCount import OpenFeatureRequestCount
from testing.measures.numberofreleases.ReleaseCount import ReleaseCount
from testing.measures.open_participation.NewContributors import NewContributors
from testing.measures.peer_influence.RepoMessages import RepoMessages
from testing.measures.popularity.AnnualCommitCount import AnnualCommitCount
from testing.measures.popularity.ForksCount import ForksCount
from testing.measures.popularity.StarsCount import StarsCount
from testing.measures.popularity.WatchersCount import WatchersCount
from testing.measures.product_evolution.CommitCount import CommitCount
from testing.measures.product_evolution.declined_changes.ReviewsDeclinedCount import ReviewsDeclinedCount
from testing.measures.product_evolution.declined_changes.ReviewsDeclinedRatio import ReviewsDeclinedRatio
from testing.measures.product_evolution.issue_interactions.UpdatedIssuesCount import UpdatedIssuesCount
from testing.measures.product_evolution.opened_pull_requests.OpenedPullRequestCount import OpenedPullRequestCount
from testing.measures.product_evolution.reviews_accepted.ReviewsAcceptedCount import ReviewsAcceptedCount
from testing.measures.product_evolution.reviews_accepted.ReviewsAcceptedRatio import ReviewsAcceptedRatio
from testing.measures.product_evolution.staleness.OpenIssueAge import OpenIssueAge
from testing.measures.product_evolution.updated_since.TimeSinceLastCommit import TimeSinceLastCommit
from testing.measures.risk.DelBiancoRiskMeasure import DelBiancoRiskMeasure
from testing.subcharacteristic.ReturnOnInvestment import ReturnOnInvestment
from testing.subcharacteristic.community_exists.CommunityExists import CommunityExists
from testing.subcharacteristic.community_vitality.CommunityVitality import CommunityVitality
from testing.subcharacteristic.communitycapability.CommunityCapability import CommunityCapability
from testing.subcharacteristic.complexity.Complexity import Complexity
from testing.subcharacteristic.contact_within_reasonable_time.ContactWithinReasonableTime import \
    ContactWithinReasonableTime
from testing.subcharacteristic.maintainer_organization.MaintainerOrganization import MaintainerOrganization
from testing.subcharacteristic.number_of_contributors.NumberOfContributorsSubChar import NumberOfContributorsSubChar
from testing.subcharacteristic.openfeaturerequests.CruzOpenFeatureRequests import CruzOpenFeatureRequests
from testing.subcharacteristic.popularity.Popularity import Popularity
from testing.subcharacteristic.product_evolution.ProductEvolution import ProductEvolution
from testing.subcharacteristic.regularupdates.RegularUpdates import RegularUpdates
from testing.subcharacteristic.risk.DelBiancoRiskAnalysis import DelBiancoRiskAnalysis
from testing.subcharacteristic.short_term_support.ShortTermSupport import ShortTermSupport
from testing.subcharacteristic.support_community.SupportCommunity import SupportCommunity
from testing.visitors.VisitorFactory import MeasureVisitorFactory, DerivedMeasureVisitorFactory, \
    MeasurableConceptVisitorFactory
from presentation.util.Util import convert_tuple_keys_to_string, convert_string_keys_to_tuple
from presentation.viewpoint_preferences.ComponentPreferencesState import PrefMatrix
from testing.characteristic.Maintainability import Maintainability
from testing.measurableconcepts.ComplexityOfSourceCode import ComplexityOfSourceCode, ComplexityOfSourceCode2
from testing.measures.CyclomaticComplexity import CyclomaticComplexity
from testing.measures.LinesOfCode import LinesOfCode
from testing.measures.NumberOfComplexFunctions import NumberOfComplexFunctions
from testing.measures.NumberOfStatements import NumberOfStatements
from testing.qualitymodels.TestQualityModel import TestQualityModel
from testing.viewpoints.DeveloperViewpoint import DeveloperViewpoint
from util.GithubRateLimiter import GithubRateLimiter

QM_FOLDER: Final = "config"
RESULTS_FOLDER: Final = "results"
JSON_EXTENSION: Final = ".json"


class QualityModelRepositoryImpl(QualityModelRepository):
    def __init__(
            self,
            github_rate_limiter: GithubRateLimiter,
            base_measure_visitor_factory: MeasureVisitorFactory,
            derived_measure_visitor_factory: DerivedMeasureVisitorFactory,
            measurable_concept_visitor_factory: MeasurableConceptVisitorFactory
    ):
        self._github_rate_limiter = github_rate_limiter
        self._base_measure_visitor_factory = base_measure_visitor_factory
        self._derived_measure_visitor_factory = derived_measure_visitor_factory
        self._measurable_concept_visitor_factory = measurable_concept_visitor_factory

    async def fetch_quality_models(self) -> Result[list[QualityModel]]:
        try:
            linesOfCode = self._base_measure_visitor_factory.instantiate_with_visitor(LinesOfCode)
            numberOfComplexFunctions = self._base_measure_visitor_factory.instantiate_with_visitor(
                NumberOfComplexFunctions
            )
            cyclomaticComplexity = self._derived_measure_visitor_factory.instantiate_with_visitor(
                CyclomaticComplexity,
                children={
                    linesOfCode.name: linesOfCode,
                    numberOfComplexFunctions.name: numberOfComplexFunctions
                }
            )
            lizard_cyclomatic_complexity = self._base_measure_visitor_factory.instantiate_with_visitor(
                CruzCyclomaticComplexityBaseMeasure
            )
            numberOfStatements = self._base_measure_visitor_factory.instantiate_with_visitor(NumberOfStatements)
            complexityOfSourceCode = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ComplexityOfSourceCode,
                children={
                    cyclomaticComplexity.name: cyclomaticComplexity,
                    numberOfStatements.name: numberOfStatements
                }
            )

            complexityOfSourceCode2 = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ComplexityOfSourceCode2,
                children={
                    cyclomaticComplexity.name: cyclomaticComplexity.copy(
                        children={
                            linesOfCode.name: linesOfCode.copy(),
                            numberOfComplexFunctions.name: numberOfComplexFunctions.copy()
                        }
                    ),
                    numberOfStatements.name: numberOfStatements.copy()
                }
            )

            cruz_number_of_comments = self._base_measure_visitor_factory.instantiate_with_visitor(
                CruzNumberOfCommentsBaseMeasure
            )
            cruz_code_quality_derived_measure = self._derived_measure_visitor_factory.instantiate_with_visitor(
                CruzCodeQualityDerivedMeasure,
                children={
                    linesOfCode.name: linesOfCode.copy(),
                    cruz_number_of_comments.name: cruz_number_of_comments
                }
            )

            license_measure = self._base_measure_visitor_factory.instantiate_with_visitor(
                License
            )
            delbianco_risk_measure = self._base_measure_visitor_factory.instantiate_with_visitor(
                DelBiancoRiskMeasure
            )
            community_count_measure = self._base_measure_visitor_factory.instantiate_with_visitor(
                ContributorCount
            )
            truck_factor_measure = self._base_measure_visitor_factory.instantiate_with_visitor(
                TruckFactor
            )
            closed_issue_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                ClosedIssuesCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )
            total_issue_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                TotalIssuesCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )
            issue_throughput = self._derived_measure_visitor_factory.instantiate_with_visitor(
                IssueThroughput,
                children={
                    closed_issue_count.name: closed_issue_count,
                    total_issue_count.name: total_issue_count
                }
            )
            closed_issue_resolution_duration = self._base_measure_visitor_factory.instantiate_with_visitor(
                ClosedIssueResolutionDuration
            )
            issue_response_time = self._base_measure_visitor_factory.instantiate_with_visitor(
                IssueResponseTime,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            absence_of_license_fees = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                AbsenceOfLicenseFees,
                children={
                    license_measure.name: license_measure
                }
            )
            return_on_investment = ReturnOnInvestment(
                children={
                    absence_of_license_fees.name: absence_of_license_fees
                }
            )
            delbianco_vulnerabilities_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                DelBiancoVulnerabilitiesMC,
                children={
                    delbianco_risk_measure.name: delbianco_risk_measure
                }
            )
            delbianco_risk_analysis = DelBiancoRiskAnalysis(
                children={
                    delbianco_vulnerabilities_mc.name: delbianco_vulnerabilities_mc
                }
            )

            number_of_contributors_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                NumberOfContributors,
                children={
                    community_count_measure.name: community_count_measure
                }
            )

            truck_factor_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                TruckFactorMC,
                children={
                    truck_factor_measure.name: truck_factor_measure
                }
            )

            issue_throughput_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                IssueThroughputMC,
                children={
                    issue_throughput.name: issue_throughput
                }
            )

            duration_to_close_issues_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                DurationToCloseIssuesMC,
                children={
                    closed_issue_resolution_duration.name: closed_issue_resolution_duration
                }
            )

            time_to_respond_to_issues = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                TimeToRespondToIssues,
                children={
                    issue_response_time.name: issue_response_time
                }
            )

            total_lines_changed_over_time = self._base_measure_visitor_factory.instantiate_with_visitor(
                LinesChangedCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            community_capability = CommunityCapability(
                children={
                    number_of_contributors_mc.name: number_of_contributors_mc,
                    truck_factor_mc.name: truck_factor_mc,
                    issue_throughput_mc.name: issue_throughput_mc,
                    duration_to_close_issues_mc.name: duration_to_close_issues_mc,
                    time_to_respond_to_issues.name: time_to_respond_to_issues
                }
            )

            interoperability_compatibility = InteroperabilityCompatibility()
            cost = Cost(
                children={
                    return_on_investment.name: return_on_investment,
                    # delbianco_risk_analysis.name: delbianco_risk_analysis
                    community_capability.name: community_capability,
                }
            )

            release_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                ReleaseCount
            )
            number_of_releases = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                NumberOfReleases,
                children={
                    release_count.name: release_count
                }
            )
            regular_updates = RegularUpdates(
                children={
                    number_of_releases.name: number_of_releases
                }
            )
            reliability = Reliability(
                children={
                    regular_updates.name: regular_updates
                }
            )

            open_feature_request_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                OpenFeatureRequestCount
            )

            commit_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                CommitCount
            )

            number_of_open_feature_requests_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                NumberOfOpenFeatureRequests,
                children={
                    open_feature_request_count.name: open_feature_request_count
                }
            )

            commit_frequency_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                CommitFrequency,
                children={
                    commit_count.name: commit_count
                }
            )

            time_since_last_commit = self._base_measure_visitor_factory.instantiate_with_visitor(
                TimeSinceLastCommit
            )
            updated_since_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                UpdatedSince,
                children={
                    time_since_last_commit.name: time_since_last_commit
                }
            )

            open_feature_requests = CruzOpenFeatureRequests(
                children={
                    number_of_open_feature_requests_mc.name: number_of_open_feature_requests_mc
                }
            )

            updated_issues_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                UpdatedIssuesCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            issue_interactions_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                IssueInteractions,
                children={
                    updated_issues_count.name: updated_issues_count,
                    closed_issue_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        ClosedIssuesCount,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    )
                }
            )

            open_issue_age = self._base_measure_visitor_factory.instantiate_with_visitor(
                OpenIssueAge,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            issue_age_average_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                IssueAgeAverage,
                children={
                    open_issue_age.name: open_issue_age
                }
            )

            reviews_declined_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                ReviewsDeclinedCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            reviews_declined_ratio = self._derived_measure_visitor_factory.instantiate_with_visitor(
                ReviewsDeclinedRatio,
                children={
                    reviews_declined_count.name: reviews_declined_count,
                    total_issue_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        TotalIssuesCount,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    )
                }
            )

            declined_changes_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                DeclinedChanges,
                children={
                    reviews_declined_ratio.name: reviews_declined_ratio
                }
            )

            opened_pull_request_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                OpenedPullRequestCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            opened_pull_request_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                OpenedPullRequests,
                children={
                    opened_pull_request_count.name: opened_pull_request_count
                }
            )

            reviews_accepted_ratio = self._base_measure_visitor_factory.instantiate_with_visitor(
                ReviewsAcceptedRatio,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            reviews_accepted_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                ReviewsAcceptedCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            reviews_accepted_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ReviewsAccepted,
                children={
                    reviews_accepted_ratio.name: reviews_accepted_ratio,
                    reviews_accepted_count.name: reviews_accepted_count
                }
            )

            product_evolution = ProductEvolution(
                children={
                    commit_frequency_mc.name: commit_frequency_mc,
                    updated_since_mc.name: updated_since_mc,
                    issue_interactions_mc.name: issue_interactions_mc,
                    issue_age_average_mc.name: issue_age_average_mc,
                    declined_changes_mc.name: declined_changes_mc,
                    opened_pull_request_mc.name: opened_pull_request_mc,
                    reviews_accepted_mc.name: reviews_accepted_mc
                }
            )

            new_contributors = self._base_measure_visitor_factory.instantiate_with_visitor(
                NewContributors,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            open_participation = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                OpenParticipation,
                children={
                    new_contributors.name: new_contributors
                }
            )

            repo_messages = self._base_measure_visitor_factory.instantiate_with_visitor(
                RepoMessages,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            peer_influence = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                PeerInfluence,
                children={
                    repo_messages.name: repo_messages
                }
            )

            support_community = SupportCommunity(
                children={
                    open_participation.name: open_participation,
                    peer_influence.name: peer_influence
                }
            )

            short_term_support = ShortTermSupport(
                children={
                    time_to_respond_to_issues.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                        TimeToRespondToIssues,
                        children={
                            issue_response_time.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                IssueResponseTime,
                                visitor_kwargs={
                                    "github_rate_limiter": self._github_rate_limiter
                                }
                            )
                        }
                    ),
                    number_of_contributors_mc.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                        NumberOfContributors,
                        children={
                            community_count_measure.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                ContributorCount
                            )
                        }
                    ),
                    number_of_releases.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                        NumberOfReleases,
                        children={
                            release_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                ReleaseCount
                            )
                        }
                    )
                }
            )

            new_contributors_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                NewContributorsMC,
                children={
                    new_contributors.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        NewContributors,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    )
                }
            )

            community_interaction_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                CommunityInteractionMC,
                children={
                    repo_messages.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        RepoMessages,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    )
                }
            )

            community_exists = CommunityExists(
                children={
                    new_contributors_mc.name: new_contributors_mc,
                    community_interaction_mc.name: community_interaction_mc,
                    issue_throughput_mc.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                        IssueThroughputMC,
                        children={
                            issue_throughput.name: self._derived_measure_visitor_factory.instantiate_with_visitor(
                                IssueThroughput,
                                children={
                                    closed_issue_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                        ClosedIssuesCount,
                                        visitor_kwargs={
                                            "github_rate_limiter": self._github_rate_limiter
                                        }
                                    ),
                                    total_issue_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                        TotalIssuesCount,
                                        visitor_kwargs={
                                            "github_rate_limiter": self._github_rate_limiter
                                        }
                                    )
                                }
                            )
                        }
                    )
                }
            )

            avg_issue_response_time_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                AvgIssueResponseTimeMC,
                children={
                    issue_response_time.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        IssueResponseTime,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    )
                }
            )

            contact_within_reasonable_time = ContactWithinReasonableTime(
                children={
                    avg_issue_response_time_mc.name: avg_issue_response_time_mc
                }
            )

            cyclomatic_complexity_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                CyclomaticComplexityMC,
                children={
                    lizard_cyclomatic_complexity.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        CruzCyclomaticComplexityBaseMeasure
                    )
                }
            )

            complexity = Complexity(
                children={
                    cyclomatic_complexity_mc.name: cyclomatic_complexity_mc
                }
            )

            repository_age = self._base_measure_visitor_factory.instantiate_with_visitor(
                RepositoryAgeMeasure,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            community_lifespan_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                CommunityLifespan,
                children={
                    repository_age.name: repository_age
                }
            )

            community_vitality = CommunityVitality(
                children={
                    community_lifespan_mc.name: community_lifespan_mc
                }
            )

            org_count_measure = self._base_measure_visitor_factory.instantiate_with_visitor(
                OrgCountMeasure,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            maintainer_org_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                MaintainerOrganizationMC,
                children={
                    org_count_measure.name: org_count_measure
                }
            )

            maintainer_org = MaintainerOrganization(
                children={
                    maintainer_org_mc.name: maintainer_org_mc
                }
            )

            support_and_service = SupportAndService(
                children={
                    open_feature_requests.name: open_feature_requests,
                    product_evolution.name: product_evolution,
                    support_community.name: support_community,
                    short_term_support.name: short_term_support,
                    community_exists.name: community_exists,
                    contact_within_reasonable_time.name: contact_within_reasonable_time,
                    complexity.name: complexity,
                    community_vitality.name: community_vitality,
                    maintainer_org.name: maintainer_org
                }
            )

            watchers_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                WatchersCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            stars_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                StarsCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            forks_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                ForksCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            annual_commit_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                AnnualCommitCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            popularity_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                PopularityMC,
                children={
                    watchers_count.name: watchers_count,
                    stars_count.name: stars_count,
                    forks_count.name: forks_count,
                    community_count_measure.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        ContributorCount
                    ),
                    annual_commit_count.name: annual_commit_count
                }
            )

            popularity = Popularity(
                children={
                    popularity_mc.name: popularity_mc
                }
            )

            number_of_contributors_subchar = NumberOfContributorsSubChar(
                children={
                    number_of_contributors_mc.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                        NumberOfContributors,
                        children={
                            community_count_measure.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                ContributorCount
                            )
                        }
                    )
                }
            )

            code_changes_commits_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                CodeChangesCommits,
                children={
                    annual_commit_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        AnnualCommitCount,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    )
                }
            )

            lines_changed_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                LinesChangedCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            code_changes_lines_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                CodeChangesLines,
                children={
                    lines_changed_count.name: lines_changed_count
                }
            )

            avg_commits_per_pr = self._base_measure_visitor_factory.instantiate_with_visitor(
                AvgNumberOfCommitsPerPRs,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            change_request_commits_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ChangeRequestCommits,
                children={
                    avg_commits_per_pr.name: avg_commits_per_pr
                }
            )

            avg_contributors_per_pr = self._base_measure_visitor_factory.instantiate_with_visitor(
                AvgNumberOfContributorsPerPRs,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            change_request_contributors_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ChangeRequestContributors,
                children={
                    avg_contributors_per_pr.name: avg_contributors_per_pr
                }
            )

            change_requests_accepted_count = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ChangeRequestsAcceptedCount,
                children={
                    reviews_accepted_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        ReviewsAcceptedCount,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    )
                }
            )

            change_requests_accepted_ratio = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ChangeRequestsAcceptedRatio,
                children={
                    reviews_accepted_ratio.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        ReviewsAcceptedRatio,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    )
                }
            )

            change_requests_declined_count = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ChangeRequestsDeclinedCount,
                children={
                    reviews_declined_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        ReviewsDeclinedCount,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    )
                }
            )

            change_requests_declined_ratio = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ChangeRequestsDeclinedRatio,
                children={
                    reviews_declined_ratio.name: self._derived_measure_visitor_factory.instantiate_with_visitor(
                        ReviewsDeclinedRatio,
                        children={
                            reviews_declined_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                ReviewsDeclinedCount,
                                visitor_kwargs={
                                    "github_rate_limiter": self._github_rate_limiter
                                }
                            ),
                            total_issue_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                TotalIssuesCount,
                                visitor_kwargs={
                                    "github_rate_limiter": self._github_rate_limiter
                                }
                            )
                        }
                    )
                }
            )

            reviews_accepted_to_declined_ratio = self._derived_measure_visitor_factory.instantiate_with_visitor(
                ReviewsAcceptedToDeclinedRatio,
                aggregate_visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                },
                children={
                    reviews_accepted_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        ReviewsAcceptedCount,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    ),
                    reviews_declined_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        ReviewsDeclinedCount,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    )
                }
            )

            change_request_acceptance_ratio = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ChangeRequestAcceptanceRatio,
                children={
                    reviews_accepted_to_declined_ratio.name: reviews_accepted_to_declined_ratio
                }
            )

            percentage_of_prs_reviewed = self._base_measure_visitor_factory.instantiate_with_visitor(
                PercentageOfPRsReviewed,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            change_request_reviews = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                ChangeRequestReviews,
                children={
                    percentage_of_prs_reviewed.name: percentage_of_prs_reviewed
                }
            )

            new_issues_count = self._base_measure_visitor_factory.instantiate_with_visitor(
                NewIssuesCount,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            issues_new_count_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                IssuesNewCount,
                children={
                    new_issues_count.name: new_issues_count
                }
            )

            new_issues_ratio = self._base_measure_visitor_factory.instantiate_with_visitor(
                NewIssuesRatio,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            issues_new_ratio_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                IssuesNewRatio,
                children={
                    new_issues_ratio.name: new_issues_ratio
                }
            )

            issues_active_count_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                IssuesActiveCount,
                children={
                    updated_issues_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        UpdatedIssuesCount,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    )
                }
            )

            active_issues_ratio = self._base_measure_visitor_factory.instantiate_with_visitor(
                ActiveIssuesRatio,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            issues_active_ratio_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                IssuesActiveRatio,
                children={
                    active_issues_ratio.name: active_issues_ratio
                }
            )

            issues_closed_count_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                IssuesClosedCount,
                children={
                    closed_issue_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                        ClosedIssuesCount,
                        visitor_kwargs={
                            "github_rate_limiter": self._github_rate_limiter
                        }
                    )
                }
            )

            closed_issues_ratio = self._base_measure_visitor_factory.instantiate_with_visitor(
                ClosedIssuesRatio,
                visitor_kwargs={
                    "github_rate_limiter": self._github_rate_limiter
                }
            )

            issues_closed_ratio_mc = self._measurable_concept_visitor_factory.instantiate_with_visitor(
                IssuesClosedRatio,
                children={
                    closed_issues_ratio.name: closed_issues_ratio
                }
            )

            community_and_adoption = CommunityAndAdoption(
                children={
                    community_exists.name: CommunityExists(
                        children={
                            new_contributors_mc.name: new_contributors_mc,
                            community_interaction_mc.name: community_interaction_mc,
                            issue_throughput_mc.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                                IssueThroughputMC,
                                children={
                                    issue_throughput.name: self._derived_measure_visitor_factory.instantiate_with_visitor(
                                        IssueThroughput,
                                        children={
                                            closed_issue_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                                ClosedIssuesCount,
                                                visitor_kwargs={
                                                    "github_rate_limiter": self._github_rate_limiter
                                                }
                                            ),
                                            total_issue_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                                TotalIssuesCount,
                                                visitor_kwargs={
                                                    "github_rate_limiter": self._github_rate_limiter
                                                }
                                            )
                                        }
                                    )
                                }
                            )
                        }
                    ),
                    popularity.name: popularity,
                    number_of_contributors_subchar.name: number_of_contributors_subchar,
                    community_capability.name: CommunityCapability(
                        children={
                            number_of_contributors_mc.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                                NumberOfContributors,
                                children={
                                    community_count_measure.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                        ContributorCount
                                    )
                                }
                            ),
                            truck_factor_mc.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                                TruckFactorMC,
                                children={
                                    truck_factor_measure.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                        TruckFactor
                                    )
                                }
                            ),
                            issue_throughput_mc.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                                IssueThroughputMC,
                                children={
                                    closed_issue_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                        ClosedIssuesCount,
                                        visitor_kwargs={
                                            "github_rate_limiter": self._github_rate_limiter
                                        }
                                    ),
                                    total_issue_count.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                        TotalIssuesCount,
                                        visitor_kwargs={
                                            "github_rate_limiter": self._github_rate_limiter
                                        }
                                    )
                                }
                            ),
                            duration_to_close_issues_mc.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                                DurationToCloseIssuesMC,
                                children={
                                    closed_issue_resolution_duration.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                        ClosedIssueResolutionDuration
                                    )
                                }
                            ),
                            time_to_respond_to_issues.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                                TimeToRespondToIssues,
                                children={
                                    issue_response_time.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                        IssueResponseTime,
                                        visitor_kwargs={
                                            "github_rate_limiter": self._github_rate_limiter
                                        }
                                    )
                                }
                            ),
                            code_changes_commits_mc.name: code_changes_commits_mc,
                            code_changes_lines_mc.name: code_changes_lines_mc,
                            change_request_commits_mc.name: change_request_commits_mc,
                            change_request_contributors_mc.name: change_request_contributors_mc,
                            change_requests_accepted_count.name: change_requests_accepted_count,
                            change_requests_accepted_ratio.name: change_requests_accepted_ratio,
                            change_requests_declined_count.name: change_requests_declined_count,
                            change_requests_declined_ratio.name: change_requests_declined_ratio,
                            change_request_acceptance_ratio.name: change_request_acceptance_ratio,
                            opened_pull_request_mc.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                                OpenedPullRequests,
                                children={
                                    opened_pull_request_count.name: opened_pull_request_count
                                }
                            ),
                            change_request_reviews.name: change_request_reviews,
                            issues_new_count_mc.name: issues_new_count_mc,
                            issues_new_ratio_mc.name: issues_new_ratio_mc,
                            issues_active_count_mc.name: issues_active_count_mc,
                            issues_active_ratio_mc.name: issues_active_ratio_mc,
                            issues_closed_count_mc.name: issues_closed_count_mc,
                            issues_closed_ratio_mc.name: issues_closed_ratio_mc,
                            issue_age_average_mc.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                                IssueAgeAverage,
                                children={
                                    open_issue_age.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                        OpenIssueAge,
                                        visitor_kwargs={
                                            "github_rate_limiter": self._github_rate_limiter
                                        }
                                    )
                                }
                            )
                        }
                    ),
                    contact_within_reasonable_time.name: ContactWithinReasonableTime(
                        children={
                            avg_issue_response_time_mc.name: self._measurable_concept_visitor_factory.instantiate_with_visitor(
                                AvgIssueResponseTimeMC,
                                children={
                                    issue_response_time.name: self._base_measure_visitor_factory.instantiate_with_visitor(
                                        IssueResponseTime,
                                        visitor_kwargs={
                                            "github_rate_limiter": self._github_rate_limiter
                                        }
                                    )
                                }
                            )
                        }
                    )
                }
            )

            maintainability = Maintainability(children={

            })

            developer_viewpoint = DeveloperViewpoint(children={
                # maintainability.name: maintainability,
                cost.name: cost,
                reliability.name: reliability,
                support_and_service.name: support_and_service,
                community_and_adoption.name: community_and_adoption
            })

            test_quality_model = TestQualityModel(
                children={
                    developer_viewpoint.name: developer_viewpoint
                }
            )

            for viewpoint in test_quality_model.children.values():
                viewpoint.preference_matrix = await self._init_viewpoint_pref_matrix(
                    quality_model=test_quality_model.name,
                    viewpoint=viewpoint
                )
                viewpoint.oss_aspect_preference_matrix = await self._init_oss_aspect_pref_matrix(
                    quality_model=test_quality_model.name,
                    viewpoint=viewpoint
                )

                for characteristic in viewpoint.children.values():
                    characteristic.preference_matrix = await self._init_characteristic_pref_matrix(
                        quality_model=test_quality_model.name,
                        viewpoint=viewpoint.name,
                        characteristic=characteristic
                    )

            await asyncio.sleep(1)
            return Success(
                [
                    test_quality_model
                ]
            )
        except Exception as e:
            return Failure(
                error_message=str(e)
            )

    async def set_preference(
            self,
            filename: str,
            key: str,
            matrix_key: str,
            preference: str
    ) -> PrefMatrix:
        path = os.path.join(QM_FOLDER, filename + JSON_EXTENSION)
        data = {
            matrix_key: {}
        }

        if os.path.exists(path):
            async with aiofiles.open(path, "r") as file:
                content = await file.read()
                if content:
                    data = json.loads(content)

        data[matrix_key][key] = preference

        async with aiofiles.open(path, "w") as file:
            json_string = json.dumps(data, indent=4)
            await file.write(json_string)
            return convert_string_keys_to_tuple(data.get(matrix_key, {}))

    async def write_measurement_result_tree_to_json(self, quality_model: 'QualityModel', viewpoint: 'Viewpoint',
                                                    repository_name: str):
        path = os.path.join(RESULTS_FOLDER, f"{repository_name}-{quality_model.name}-{viewpoint.name}.json").replace(
            " ", "_")
        data = quality_model.serialize()

        async with aiofiles.open(path, "w") as file:
            json_string = json.dumps(data, indent=4)
            await file.write(json_string)

    async def _init_viewpoint_pref_matrix(
            self,
            quality_model: str,
            viewpoint: 'Viewpoint'
    ) -> PrefMatrix:
        path = os.path.join(QM_FOLDER, f"{quality_model}-{viewpoint.name}.json").replace(" ", "_")

        return await self._read_write_pref_matrix(
            path=path,
            preference_matrix=viewpoint.preference_matrix,
            key="preference_matrix"
        )

    async def _init_characteristic_pref_matrix(
            self,
            quality_model: str,
            viewpoint: str,
            characteristic: 'Characteristic'
    ) -> PrefMatrix:
        path = os.path.join(QM_FOLDER, f"{quality_model}-{viewpoint}-{characteristic.name}.json").replace(" ", "_")

        return await self._read_write_pref_matrix(
            path=path,
            preference_matrix=characteristic.preference_matrix,
            key="preference_matrix"
        )

    async def _init_oss_aspect_pref_matrix(
            self,
            quality_model: str,
            viewpoint: 'Viewpoint'
    ) -> PrefMatrix:
        path = os.path.join(QM_FOLDER, f"{quality_model}-{viewpoint.name}.json").replace(" ", "_")

        return await self._read_write_pref_matrix(
            path=path,
            preference_matrix=viewpoint.oss_aspect_preference_matrix,
            key="oss_aspect_preference_matrix"
        )

    async def _read_write_pref_matrix(
            self,
            path: str,
            preference_matrix: PrefMatrix,
            key: str
    ):
        if not os.path.exists(path):
            await self._write_pref_matrix(
                path=path,
                data={key: convert_tuple_keys_to_string(preference_matrix)}
            )
            return preference_matrix

        async with aiofiles.open(path, "r") as file:
            content = await file.read()

        if not content:
            await self._write_pref_matrix(
                path=path,
                data={key: convert_tuple_keys_to_string(preference_matrix)}
            )
            return preference_matrix

        data = json.loads(content)
        if key not in data:
            data[key] = convert_tuple_keys_to_string(preference_matrix)
            await self._write_pref_matrix(
                path=path,
                data=data
            )
            return preference_matrix

        pref_matrix_data = data[key]
        return convert_string_keys_to_tuple(pref_matrix_data)

    async def _write_pref_matrix(
            self,
            path: str,
            data: dict
    ):
        async with aiofiles.open(path, "w") as file:
            json_string = json.dumps(data, indent=4)
            await file.write(json_string)
