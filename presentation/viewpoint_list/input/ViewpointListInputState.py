from dataclasses import dataclass
from typing import Optional


@dataclass
class ViewpointListInputState:
    should_wait_for_input: Optional[bool] = None
