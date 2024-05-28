import asyncio
import json
import os
from typing import Final

import aiofiles

from domain.model.Characteristic import Characteristic
from domain.model.Model import QualityModelSchema
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
from testing.measurableconcepts.communitycapability.IssueResolutionDurationAverage import IssueResolutionDurationAverage
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
from testing.measurableconcepts.communitycapability.code_development_efficiency.ChangeRequestsDurationAverage import \
    ChangeRequestsDurationAverage
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
from testing.measures.communitycapability.DurationToResolveIssues import DurationToResolveIssues
from testing.measures.communitycapability.ClosedIssuesCount import ClosedIssuesCount
from testing.measures.communitycapability.ContributorCount import ContributorCount
from testing.measures.communitycapability.IssueResponseTime import IssueResponseTime
from testing.measures.communitycapability.IssueThroughput import IssueThroughput
from testing.measures.communitycapability.LinesChangedCount import LinesChangedCount
from testing.measures.communitycapability.TotalIssuesCount import TotalIssuesCount
from testing.measures.communitycapability.TruckFactor import TruckFactor
from testing.measures.communitycapability.change_request_reviews.PercentageOfPRsReviewed import PercentageOfPRsReviewed
from testing.measures.communitycapability.change_requests_duration.DurationToResolvePullRequests import \
    DurationToResolvePullRequests
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
MODELS_FOLDER: Final = f"{QM_FOLDER}/models"
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
            read_json_files = await self._read_json_files_from_config_dir(MODELS_FOLDER)
            quality_models = []
            for data in read_json_files:
                qm_schema = QualityModelSchema()
                quality_models.append(qm_schema.load(data))

            return Success(
                quality_models
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

    async def _read_json_files_from_config_dir(self, dir: str) -> list[str]:
        base_path = os.getcwd()
        config_path = os.path.join(base_path, dir)
        files = os.listdir(config_path)
        data = []
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(config_path, file)
                async with aiofiles.open(file_path, "r") as f:
                    try:
                        content = await f.read()
                        data.append(json.loads(content))
                    except json.JSONDecodeError:
                        print(f"Error reading file {file}")
        return data

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
