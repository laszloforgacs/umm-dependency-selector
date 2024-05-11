from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import AggregateVisitor
from source_temp.PyGithub.github.Repository import Repository
from testing.measures.product_evolution.declined_changes.ReviewsDeclinedCount import ReviewsDeclinedCount
from testing.measures.product_evolution.reviews_accepted.ReviewsAcceptedCount import ReviewsAcceptedCount
from util.GithubRateLimiter import GithubRateLimiter


class ReviewsAcceptedToDeclinedRatioAggregator(AggregateVisitor[tuple[Measure, float]]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        super().__init__()
        self._github_rate_limiter = github_rate_limiter

    def aggregate(self, normalized_measures: list[tuple[Measure, float]], repository: Repository) -> float:
        try:
            accepted_reviews = 0
            declined_reviews = 0

            for measure, measure_value in normalized_measures:
                if isinstance(measure, ReviewsAcceptedCount):
                    accepted_reviews += measure_value
                if isinstance(measure, ReviewsDeclinedCount):
                    declined_reviews += measure_value

            if declined_reviews == 0:
                print(
                    f"Reviews Accepted: {accepted_reviews}, Reviews Declined: {declined_reviews}, Ratio: {accepted_reviews}")
                return accepted_reviews

            ratio = accepted_reviews / declined_reviews
            print(f"Reviews Accepted: {accepted_reviews}, Reviews Declined: {declined_reviews}, Ratio: {ratio}")
            return ratio
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
