import os
from datetime import timezone, datetime

from dateutil.relativedelta import relativedelta

from presentation.core.visitors.Visitor import BaseMeasureVisitor, T
from source_temp.PyGithub.github.Repository import Repository
from source_temp.PyGithub.github import Github
from util.GithubRateLimiter import GithubRateLimiter
from github.Auth import Token

"""
Augur measure: Time series of number of new contributors
1. Fetching pull requests
2. Fetching comments
3. Collecting commenters/contributors
4. Determining new contributors
In the last 3 months.
"""


class NewContributorsVisitor(BaseMeasureVisitor[int]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> int:
        try:
            cached_result = await self.get_cached_result(measure, repository)
            if cached_result is not None:
                print(f"{repository.full_name}: {measure.name} is {cached_result}")
                return cached_result

            auth = Token(os.getenv('UMM_DEPENDENCY_SELECTOR_GITHUB_TOKEN'))
            github = Github(auth=auth, per_page=100)
            github_rate_limiter = GithubRateLimiter(github=github)

            new_contributors = []
            commenters = set()
            end_date = datetime.now(timezone.utc)
            start_date = end_date - relativedelta(months=3)
            user_event_types = [
                "IssueCommentEvent",
                "GollumEvent",
                "IssuesEvent",
                "PullRequestEvent",
                "PullRequestReviewEvent",
                "PullRequestReviewCommentEvent",
                "PullRequestReviewThreadEvent",
                "ReleaseEvent"
            ]

            pr_comments = github_rate_limiter.execute(
                repository.get_pulls_comments,
                sort='updated',
                direction='desc',
                since=start_date
            )
            for comment in pr_comments:
                commenters.add(comment.user.login)

            for commenter in commenters:
                first_contribution_date = None
                user = github_rate_limiter.execute(
                    github_rate_limiter.github_client.get_user,
                    login=commenter
                )
                events = github_rate_limiter.execute(
                    user.get_events,
                )

                for event in events:
                    if event.created_at < start_date:
                        break

                    if event.type in user_event_types:
                        if not first_contribution_date or event.created_at < first_contribution_date:
                            first_contribution_date = event.created_at

                if first_contribution_date and first_contribution_date >= start_date:
                    new_contributors.append(commenter)

            print(f"{repository.full_name}: {measure.name} is {new_contributors}")

            await self.cache_result(measure, repository, new_contributors)
            return new_contributors
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
