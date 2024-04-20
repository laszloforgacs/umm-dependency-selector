import time

from github import Github

from source_temp.PyGithub.github import RateLimitExceededException


class GithubRateLimiter():
    def __init__(self, github: Github):
        self._github = github

    @property
    def github_client(self) -> Github:
        return self._github

    def execute(self, function, *args, **kwargs):
        try:
            self._check_rate_limit()
            result = function(*args, **kwargs)
            return result
        except RateLimitExceededException:
            # Adding a 5-minute sleep as a fallback
            self._throttle(time.time() + 300)
            return self.execute(function, *args, **kwargs)

    def _check_rate_limit(self):
        rate_limit = self.github_client.get_rate_limit().core
        self.last_remaining = rate_limit.remaining
        print(f"API requests remaining: {self.last_remaining}")
        if self.last_remaining < 500:  # Adjust threshold as necessary
            self._throttle(rate_limit.reset)

    def _throttle(self, reset_time):
        current_time = time.time()
        if reset_time > current_time:
            sleep_time = reset_time - current_time + 10  # Adding 10 seconds buffer
            print(f"Rate limit exceeded. Sleeping for {sleep_time:.2f} seconds.")
            time.sleep(sleep_time)
        else:
            print("Rate limit reset time has passed. Continuing without sleep.")
