from typing import Final

INPUT_SET_PREFERENCE: Final = "Please enter the blabla how much do you rate this and that"

ERROR_SET_PREFERENCE_VALUE_INVALID: Final = "Preference value must be between 1 and 9 (inclusive)"
ERROR_INVALID_INPUT: Final = "Invalid input. Please try again"

QUALITY_MODEL_USER_INPUT: Final = "Select a quality model by entering a number: "

VIEWPOINT_LIST_PRESENTATION: Final = "The following viewpoints are available: "
VIEWPOINT_LIST_INPUT: Final = "Select a Viewpoint or go back by entering a number: "

VIEWPOINT_WANT_TO_SET_PREFERENCES: Final = "There are no preferences set for this item, or it is incomplete. Do you want to set preferences now? (y/n): "
VIEWPOINT_PREFERENCES_EVALUATE_OR_RESET_INPUT: Final = "Would you like to evaluate repositories, or set the preference matrix again? "

PREFERENCES_NOT_ENOUGH_CHARACTERISTICS_OR_SUB_CHARACTERISTICS: Final = f"You need to add more characteristics or sub-characteristics for the AHP calculation by editing the appropriate preference matrix in the config folder"

QUALITY_MODEL_LIST_SCREEN: Final = "QualityModelListScreen"
VIEWPOINT_LIST_SCREEN: Final = "ViewpointListScreen"
VIEWPOINT_PREFERENCES_SCREEN: Final = "ViewpointPreferencesScreen"

AHP_COMMON_RATINGS: Final = "1: Equal importance\n3: Moderately more important\n5: Strongly more important\n7: Very strongly more important\n9: Extremely more important"
AHP_INTERMEDIATE_RATINGS: Final = "2, 4, 6, 8: Intermediate values between two adjacent judgments"
