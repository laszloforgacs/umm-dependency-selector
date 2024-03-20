from dataclasses import dataclass

from github.Repository import Repository


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
    repositories: list[Repository]

    def copy(self, **kwargs):
        return Loaded(
            repositories=kwargs.get('repositories', self.repositories)
        )


RepositoryState = Loaded | Loading | Error
