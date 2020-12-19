import datetime
from abc import abstractmethod, ABC
from typing import Iterable

import attr


@attr.s
class Row:
    project: str = attr.ib()
    version: str = attr.ib()
    date: datetime.date = attr.ib()
    downloads: int = attr.ib()
    pip_downloads: int = attr.ib()


@attr.s
class Result:
    total_rows: int = attr.ib()
    rows: Iterable[Row] = attr.ib()


class StatsViewer(ABC):
    @abstractmethod
    def get_version_downloads(self, date: datetime.date) -> Result:
        pass
