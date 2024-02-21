from typing import Optional, TypeVar

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
