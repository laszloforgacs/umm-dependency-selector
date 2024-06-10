import os
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from github import Github
from github.Repository import Repository

from presentation.core.visitors.Visitor import BaseMeasureVisitor
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
Cruz Measure. Limited to the last 3 months.
"""


class NumberOfTestersVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result} {measure.unit}")
                return cached_result

            self._init()

            people_submitting_bugs = set()
            end_date = datetime.now(timezone.utc)
            start_date = end_date - relativedelta(months=3)

            bug_labels = self._get_bug_labels(repository)
            issues_tagged_with_bug_label = self._github_rate_limiter.execute(
                repository.get_issues,
                labels=bug_labels,
                state='all',
                since=start_date
            )

            tester_event_types = [
                "IssuesEvent",
            ]

            developer_event_types = [
                "PullRequestEvent",
                "PullRequestReviewEvent",
                "PullRequestReviewCommentEvent",
                "PullRequestReviewThreadEvent",
                "ReleaseEvent"
            ]

            for issue in issues_tagged_with_bug_label:
                if issue.user.login:
                    people_submitting_bugs.add(issue.user.login)

            testers = set()
            for bug_submitter in people_submitting_bugs:
                user = self._github_rate_limiter.execute(
                    self._github_rate_limiter.github_client.get_user,
                    login=bug_submitter
                )

                events = self._github_rate_limiter.execute(
                    user.get_events
                )

                contains_issue_creation = any(
                    event.type in tester_event_types and event.payload.get('action') == 'opened'
                    for event in events
                )

                contains_developer_action = any(
                    event.type in developer_event_types
                    for event in events
                )

                if contains_issue_creation and not contains_developer_action:
                    testers.add(bug_submitter)

            testers_count = len(testers)
            print(f"{repository.full_name}: {measure.name} is {testers_count} {measure.unit}")

            await self.cache_result(measure, repository, testers_count)
            return testers_count
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)

    def _init(self):
        auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
        github = Github(auth=auth, per_page=100)
        self._github_rate_limiter = GithubRateLimiter(github=github)

    def _get_bug_labels(self, repository: 'Repository') -> list[str]:
        try:
            labels = self._github_rate_limiter.execute(
                repository.get_labels
            )
            bug_labels = [label.name for label in labels if 'bug' in label.name.lower()]
            return bug_labels
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
