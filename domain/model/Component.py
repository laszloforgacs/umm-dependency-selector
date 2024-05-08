from abc import abstractmethod, ABCMeta, ABC

from domain.model.Result import Result


class Component(ABC):

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    @abstractmethod
    def children(self) -> dict[str, 'Component'] | None:
        pass

    @abstractmethod
    def serialize(self) -> dict:
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


class CompositeComponent(Component, metaclass=ABCMeta):
    @property
    def children(self) -> dict[str, 'Component'] | None:
        return self._children

    def add_component(self, component: Component):
        self._children[component.name] = component
        component.parent = self

    def remove_component(self, component: Component):
        del self.children[component.name]
        component.parent = None


class LeafComponent(Component, metaclass=ABCMeta):
    def __init__(self):
        pass

    @property
    def children(self) -> dict[str, 'Component'] | None:
        return None

    def measure(self) -> Result:
        pass
