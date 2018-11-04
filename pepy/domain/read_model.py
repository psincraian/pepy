from datetime import date
from typing import List

from attr import attrs, attrib


@attrs()
class ProjectListProjection:
    name: str = attrib()
    total_downloads: int = attrib()


@attrs()
class DownloadProjection:
    date: date = attrib()
    downloads: int = attrib()


@attrs()
class ProjectProjection:
    name: str = attrib()
    total_downloads: int = attrib()
    last_downloads: List[DownloadProjection] = attrib()  # the last 30 days downloads
