from dataclasses import dataclass


@dataclass
class EvaluationScreenState:
    pass


@dataclass
class GetRepositories:
    repositories: list[str]


EvaluationState = GetRepositories
