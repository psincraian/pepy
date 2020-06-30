import datetime
from collections import defaultdict, OrderedDict
from itertools import islice
from typing import List, Set
import re
import attr


@attr.s
class ProjectName:
    name: str = attr.ib()
    MIN_LENGTH = 1
    MAX_LENGTH = 512

    @name.validator
    def _check(self, attribute, value):
        if len(value) < self.MIN_LENGTH or len(value) > self.MAX_LENGTH:
            from pepy.domain.exception import ProjectNameLengthIsNotValidException

            raise ProjectNameLengthIsNotValidException(value, self.MIN_LENGTH, self.MAX_LENGTH)

    def __attrs_post_init__(self):
        self.name = re.sub(r"[-_.]+", "-", self.name).strip().lower()


@attr.s
class HashedPassword:
    password: str = attr.ib()


@attr.s
class Password:
    password: str = attr.ib()


@attr.s
class Badge:
    project: str = attr.ib()
    image = attr.ib()


@attr.s
class Downloads:
    value: int = attr.ib()

    def __add__(self, o):
        return Downloads(self.value + o.value)

    def __sub__(self, o):
        return Downloads(self.value - o.value)


@attr.s
class ProjectVersionDownloads:
    date: datetime.date = attr.ib()
    version: str = attr.ib()
    downloads: Downloads = attr.ib()


class Project:
    MAX_RETENTION_DAYS = 180

    def __init__(self, name: ProjectName, total_downloads: Downloads):
        self.name = name
        self.total_downloads = total_downloads
        self._latest_downloads = defaultdict(lambda: defaultdict())
        self._versions = set()
        self.min_date = None

    def add_downloads(self, date: datetime.date, version: str, downloads: Downloads):
        if self.min_date is None:
            self.min_date = date
        elif date < self.min_date:
            raise Exception("Date should be greater than min date")
        elif date - self.min_date > datetime.timedelta(days=Project.MAX_RETENTION_DAYS):
            self._latest_downloads.pop(self.min_date)
            self.min_date = self._find_next_min_date(date)

        # if we already had the downloads let's update it
        if date in self._latest_downloads and version in self._latest_downloads[date]:
            self.total_downloads -= self._latest_downloads[date][version]

        self._latest_downloads[date][version] = downloads
        self.total_downloads += downloads
        self._versions.add(version)

    def _find_next_min_date(self, max_date):
        min_date = self.min_date + datetime.timedelta(days=1)
        while min_date not in self._latest_downloads and min_date < max_date:
            min_date = min_date + datetime.timedelta(days=1)
        return min_date

    def last_downloads(self, gte_date: datetime.date = None) -> List[ProjectVersionDownloads]:
        result = []
        for date, version_downloads in self._latest_downloads.items():
            if gte_date is None or date >= gte_date:
                for version, downloads in version_downloads.items():
                    result.append(ProjectVersionDownloads(date, version, downloads))
        return result

    def versions(self) -> Set[str]:
        return self._versions


@attr.s
class ProjectDownloads:
    name: ProjectName = attr.ib()
    downloads: Downloads = attr.ib()
    day: datetime.date = attr.ib()


@attr.s
class BQDownloads:
    project: ProjectName = attr.ib()
    version: str = attr.ib()
    date: datetime.date = attr.ib()
    downloads: Downloads = attr.ib()
