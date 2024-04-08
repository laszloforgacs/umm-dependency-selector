from presentation.core.visitors.Visitor import Visitor


class AugurIssueResponseTimeVisitor(Visitor[float]):
    def __init__(self):
        pass

    async def measure(self, measure: 'BaseMeasure', repository: 'Repository') -> float:
        try:
            issues = repository.get_issues()
            time_differences = []
            for issue in issues:
                comments = issue.get_comments()
                if comments.totalCount > 0:
                    first_comment = comments[0]

                    if first_comment and issue.created_at:
                        time_difference = first_comment.created_at - issue.created_at
                        time_differences.append(time_difference)

            if not time_differences:
                # returning 30 days in seconds as an appropriately high value.
                print(f"{repository.full_name}: {measure.name} is {30 * 24 * 60 * 60}")
                return 30 * 24 * 60 * 60
            else:
                total_time_difference_seconds = sum(
                    [time_difference.total_seconds() for time_difference in time_differences])
                average_time_difference_seconds = total_time_difference_seconds / len(time_differences)
                print(f"{repository.full_name}: {measure.name} is {average_time_difference_seconds}")
                return average_time_difference_seconds
        except Exception as e:
            raise Exception(str(e) + self.__class__.__name__)
