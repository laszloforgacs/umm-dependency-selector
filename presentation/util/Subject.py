from abc import abstractmethod, ABC


class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: 'Observer'):
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: 'Observer'):
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self):
        """
        Notify all observers about an event.
        """
        pass