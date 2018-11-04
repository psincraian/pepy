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

    @property
    def total_downloads_last_30_days(self) -> int:
        downloads = 0
        for d in self.last_downloads:
            downloads += d.downloads
        return downloads

    @property
    def total_downloads_last_7_days(self) -> int:
        downloads = 0
        for d in self.last_downloads[:7]:
            downloads += d.downloads
        return downloads
