from dataclasses import dataclass


@dataclass
class SourceState:
    pass


@dataclass
class Loading(SourceState):
    pass

    def copy(self, **kwargs):
        return Loading()


@dataclass
class Error(SourceState):
    message: str

    def copy(self, **kwargs):
        return Error(
            message=kwargs.get('message', self.message)
        )


@dataclass
class Loaded(SourceState):
    repositories: list[str]

    def copy(self, **kwargs):
        return Loaded()


RepositoryState = Loaded | Loading | Error
