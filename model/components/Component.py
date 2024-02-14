from abc import abstractmethod, ABCMeta, ABC

from model.Result import Result


class Component(ABC):
    @property
    def name(self) -> str:
        return self._name

    @property
    @abstractmethod
    def children(self) -> dict[str, 'Component'] | None:
        pass

    def add_component(self, component: 'Component'):
        """
        add_component adds a component to the component map
        """
        pass

    def remove_component(self, component: 'Component'):
        """
        remove_component removes a component from the component map
        """
        pass

    def measure(self) -> list[Result]:
        pass

    def aggregate(self) -> list[Result]:
        pass

    def normalize(self) -> list[Result]:
        pass

    def run(self) -> Result:
        pass


class CompositeComponent(Component, metaclass=ABCMeta):
    @property
    def children(self) -> dict[str, 'Component'] | None:
        return self._children

    def add_component(self, component: Component):
        self._children[component.name] = component

    def remove_component(self, component: Component):
        del self.children[component.name]


class LeafComponent(Component, metaclass=ABCMeta):
    def __init__(self):
        pass

    @property
    def children(self) -> dict[str, 'Component'] | None:
        return None
