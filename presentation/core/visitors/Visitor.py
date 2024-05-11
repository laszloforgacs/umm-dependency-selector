import json
import os
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

import aiofiles
from github.Repository import Repository

from domain.model.ABCGenericMeta import ABCGenericMeta

T = TypeVar('T')
U = TypeVar('U')

CACHE_FOLDER = "cache"


class Visitor(Generic[T], metaclass=ABCGenericMeta):
    @abstractmethod
    def __init__(self):
        pass

    async def cache_result(self, measure: 'Measure', repository: 'Repository', value: T):
        quality_model = measure.get_quality_model()
        viewpoint = measure.get_viewpoint()
        path = os.path.join(CACHE_FOLDER, f"{repository.name}-{quality_model.name}-{viewpoint.name}-cache.json").replace(" ",
                                                                                                                    "_")

        key = f"{measure.name}_{self.__class__.__name__}".replace(" ", "_")
        data = {
            key: value
        }

        if not os.path.exists(path):
            await self._write_to_file(path, data)
            return

        content = await self._read_from_file(path)

        if not content:
            await self._write_to_file(path, data)
            return

        data = json.loads(content)
        data[key] = value

        await self._write_to_file(path, data)

    async def get_cached_result(self, measure: 'Measure', repository: 'Repository') -> Optional[T]:
        quality_model = measure.get_quality_model()
        viewpoint = measure.get_viewpoint()
        path = os.path.join(CACHE_FOLDER, f"{repository.name}-{quality_model.name}-{viewpoint.name}-cache.json").replace(" ",
                                                                                                                    "_")
        if not os.path.exists(path):
            return None

        content = await self._read_from_file(path)
        if not content:
            return None

        data = json.loads(content)
        key = f"{measure.name}_{self.__class__.__name__}".replace(" ", "_")
        return data.get(key, None)

    async def _write_to_file(self, path: str, data: dict):
        async with aiofiles.open(path, "w") as file:
            json_string = json.dumps(data, indent=4)
            await file.write(json_string)

    async def _read_from_file(self, path: str) -> str:
        async with aiofiles.open(path, "r") as file:
            content = await file.read()
            return content


class NormalizeVisitor(Visitor[T]):
    def __init__(self):
        pass

    @abstractmethod
    def normalize(self, measurements: list[T]) -> list[T]:
        pass


class AggregateVisitor(Visitor[T]):
    def __init__(self):
        pass

    @abstractmethod
    def aggregate(self, normalized_measures: list[T]) -> U:
        pass


class BaseMeasureVisitor(Visitor[T]):
    def __init__(self):
        pass

    @abstractmethod
    async def measure(self, measure: 'BaseMeasure', repository: Repository) -> T:
        pass
