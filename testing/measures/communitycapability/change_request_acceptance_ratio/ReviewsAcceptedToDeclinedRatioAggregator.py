from domain.model.Measure import Measure
from presentation.core.visitors.Visitor import AggregateVisitor
from testing.measures.product_evolution.declined_changes.ReviewsDeclinedCount import ReviewsDeclinedCount
from testing.measures.product_evolution.reviews_accepted.ReviewsAcceptedCount import ReviewsAcceptedCount
from util.GithubRateLimiter import GithubRateLimiter


class ReviewsAcceptedToDeclinedRatioAggregator(AggregateVisitor[tuple[Measure, float]]):
    def __init__(self, github_rate_limiter: GithubRateLimiter):
        super().__init__()
        self._github_rate_limiter = github_rate_limiter

    def aggregate(self, normalized_measures: list[tuple[Measure, float]]) -> float:
        try:
            accepted_reviews = 0
            declined_reviews = 0

            for measure, measure_value in normalized_measures:
                if isinstance(measure, ReviewsAcceptedCount):
                    accepted_reviews += measure_value
                if isinstance(measure, ReviewsDeclinedCount):
                    declined_reviews += measure_value

        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
