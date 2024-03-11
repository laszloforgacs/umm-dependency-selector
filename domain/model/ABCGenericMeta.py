from abc import ABCMeta
from typing import Generic, TypeVar

T = TypeVar('T')


class ABCGenericMeta(ABCMeta, type(Generic)):
    pass
