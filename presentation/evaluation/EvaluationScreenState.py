from dataclasses import dataclass


@dataclass
class EvaluationScreenState:
    pass


@dataclass
class AHPReport(EvaluationScreenState):
    report: dict


@dataclass
class Loading(EvaluationScreenState):
    pass


@dataclass
class Error(EvaluationScreenState):
    message: str

@dataclass
class NavigateBack():
    pass


EvaluationState = AHPReport | Loading | Error | NavigateBack
