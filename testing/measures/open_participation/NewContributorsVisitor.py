from datetime import timezone, datetime

from dateutil.relativedelta import relativedelta

from presentation.core.visitors.Visitor import Visitor
from util.GithubRateLimiter import GithubRateLimiter

"""
Augur measure: Time series of number of new contributors
1. Fetching pull requests
2. Fetching comments
3. Collecting commenters/contributors
4. Determining new contributors
In the last 3 months.
"""


class NewContributorsVisitor(Visitor[int]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        self._github_rate_limiter = github_rate_limiter


async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> int:
    try:
        new_contributor_count = 0
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

        pr_comments = self._github_rate_limiter.execute(
            repository.get_pulls_comments,
            sort='updated',
            direction='desc',
            since=start_date
        )
        for comment in pr_comments:
            commenters.add(comment.user.login)

        for commenter in commenters:
            first_contribution_date = None
            events = self._github_rate_limiter.execute(
                self._github_rate_limiter.github_client.get_user,
                login=commenter
            )
            for event in events:
                if event.created_at < start_date:
                    break

                if event.type in user_event_types:
                    if not first_contribution_date or event.created_at < first_contribution_date:
                        first_contribution_date = event.created_at

            if first_contribution_date and first_contribution_date >= start_date:
                new_contributor_count += 1

        print(f"{repository.full_name}: {measure.name} is {new_contributor_count}")
        return new_contributor_count
    except Exception as e:
        raise Exception(str(e) + self.__class__.__name__)
