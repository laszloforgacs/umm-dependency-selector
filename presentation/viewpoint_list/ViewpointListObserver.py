from presentation.util.Observer import Observer
from presentation.util.Util import print_items_with_last
from presentation.viewpoint_list import ViewpointListStateSubject


class ViewpointListObserver(Observer):
    def update(self, subject: ViewpointListStateSubject) -> None:
        viewpoints = subject.state.viewpoints
        print_items_with_last(viewpoints, "Go back")
