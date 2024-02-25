from dataclasses import dataclass


@dataclass
class QualityModelUserInputState:
    should_wait_for_user_input: bool = False
