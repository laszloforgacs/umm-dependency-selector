from typing import Optional


class ViewpointListViewModel:
    def __init__(self, shared_view_model: 'SharedViewModel'):
        self._shared_view_model = shared_view_model

    def viewpoints(self, selected_quality_model: str) -> Optional[dict[str, 'Viewpoint']]:
        return self._shared_view_model.viewpoints(
            selected_quality_model=selected_quality_model
        )
