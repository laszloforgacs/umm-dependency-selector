import os
from datetime import timezone, datetime

from dateutil.relativedelta import relativedelta
from github.Auth import Token

from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import AggregateVisitor
from source_temp.PyGithub.github import Github
from source_temp.PyGithub.github.Repository import Repository
from testing.measures.communitycapability.community_growth.NewContributors import NewContributors
from util.GithubRateLimiter import GithubRateLimiter


class ClosedIssuesPercentageByNewContributorsAggregator(AggregateVisitor[tuple[Measure, int]]):
    def __init__(self):
        super().__init__()

    def aggregate(self, normalized_measures: list[tuple[Measure, int]], repository: Repository) -> float:
        try:
            self._init()
            new_contributors = []
            contributors_closing_issues = set()

            for measure, measure_value in normalized_measures:
                if isinstance(measure, NewContributors):
                    new_contributors = new_contributors + measure_value

            new_contributors_closing_issues = set()
            end_date = datetime.now(timezone.utc)
            start_date = end_date - relativedelta(months=3)

            issues = self._github_rate_limiter.execute(
                repository.get_issues,
                state='closed',
                direction='desc'
            )
            filtered_issues = [
                issue for issue in issues
                if start_date <= issue.closed_at <= end_date
            ]

            for issue in filtered_issues:
                # The new contributors returned by the child measure are new ones
                # based on their contribution in the last 3 months
                if issue.closed_by and issue.closed_by.login in new_contributors:
                    new_contributors_closing_issues.add(issue.closed_by.login)

                if issue.closed_by:
                    contributors_closing_issues.add(issue.closed_by.login)

            total_issue_closers = len(contributors_closing_issues)
            count_new_contributors_closing_issues = len(new_contributors_closing_issues)
            if total_issue_closers == 0:
                print(f"Number of new contributors closing issues: {0}")
                return 0.0

            percentage = (count_new_contributors_closing_issues / total_issue_closers) * 100
            print(f"Percentage of new contributors closing issues: {percentage}")
            return percentage
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _init(self):
        auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
        github = Github(auth=auth, per_page=100)
        self._github_rate_limiter = GithubRateLimiter(github=github)
