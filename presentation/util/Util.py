from typing import Optional, TypeVar

from domain.model.Result import Result, Success, Failure
from presentation.util.Constants import AHP_COMMON_RATINGS, AHP_INTERMEDIATE_RATINGS

T = TypeVar('T')


def is_pref_matrix_valid(matrix: dict[tuple[str, str], float]) -> bool:
    return all(
        value is not None
        for value in matrix.values()
    )


def print_items_with_last(items, last_string=""):
    for i, item in enumerate(items, start=1):
        print(f"{i}. {item}")

    if last_string:
        print(f"{len(items) + 1}. {last_string}")


def get_item_by_numerical_position(items: list[T], position) -> Optional[T]:
    return items[position - 1] if 0 < position <= len(items) else None


def handle_user_input(user_input: str, list_size: int, error_message: str) -> Result[int]:
    try:
        value = int(user_input)
        if value == list_size + 1:
            return Success(
                value=list_size + 1
            )
        if 1 <= value <= list_size:
            return Success(
                value=value
            )
        else:
            error_message = error_message
            return Failure(
                error_message=error_message
            )
    except ValueError as e:
        return Failure(error_message=str(e))


def print_ahp_ratings(comparisons: tuple[str, str]):
    print(f"How many times more, or how strongly more is {comparisons[0]} preferred over {comparisons[1]}?")
    print(AHP_COMMON_RATINGS)
    print(AHP_INTERMEDIATE_RATINGS)
    print(
        f"Enter a number from 1 to 9. If {comparisons[1]} is preferred over {comparisons[0]}, enter the reciprocal of the number.\nFor example, 1/3, 1/5, 1/7, 1/9, or the reciprocal of the intermediate values.\nIf the two elements are equally important, enter 1")


def accepted_ahp_values() -> list[float]:
    return [
        "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "1/2", "1/3", "1/4", "1/5", "1/6", "1/7", "1/8", "1/9"
    ]


def reversed_ahp_values() -> dict[str, float]:
    return {
        "1": "1",
        "2": "1/2",
        "3": "1/3",
        "4": "1/4",
        "5": "1/5",
        "6": "1/6",
        "7": "1/7",
        "8": "1/8",
        "9": "1/9",
        "1/2": "2",
        "1/3": "3",
        "1/4": "4",
        "1/5": "5",
        "1/6": "6",
        "1/7": "7",
        "1/8": "8",
        "1/9": "9"
    }


def convert_tuple_keys_to_string(data):
    if isinstance(data, dict):
        return {', '.join(key): value for key, value in data.items()}
    else:
        return data


def convert_string_keys_to_tuple(data):
    if isinstance(data, dict):
        return {tuple(key.split(', ')): value for key, value in data.items()}
    else:
        return data
