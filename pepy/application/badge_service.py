import logging
import math
from datetime import datetime, timedelta

from pybadges import badge

from pepy.domain.exception import ProjectNotFoundException
from pepy.domain.model import (
    Badge,
    Project,
    Downloads,
    PersonalizedBadge,
    ProjectName,
    BadgePeriod,
    BadgeStyle,
    BadgeColor,
    BadgeUnits,
)
from pepy.domain.repository import ProjectRepository


class DownloadsNumberFormatter:
    _METRIC_PREFIX = ["", "k", "M", "B", "T", "P"]
    _ABBREVIATION_PREFIX = ["", "k", "M", "B", "T", "Q"]

    def format(self, downloads: Downloads) -> str:
        if downloads.value == 0:
            return "0"
        digits = int(math.log10(abs(downloads.value)) if downloads else 0)
        millidx = max(0, min(len(self._METRIC_PREFIX) - 1, digits // 3))
        rounded_value = downloads.value // (10 ** (3 * millidx))
        return "{}{}".format(rounded_value, self._METRIC_PREFIX[millidx])

    def format_with_units(self, downloads: Downloads, units: BadgeUnits) -> str:
        if downloads.value == 0:
            return "0"
        if units == BadgeUnits.none:
            return str(downloads.value)
        digits = int(math.log10(abs(downloads.value)) if downloads else 0)
        millidx = max(0, min(len(self._METRIC_PREFIX) - 1, digits // 3))
        rounded_value = downloads.value // (10 ** (3 * millidx))
        if units == BadgeUnits.abbreviation:
            return "{}{}".format(rounded_value, self._ABBREVIATION_PREFIX[millidx])
        else:
            return "{}{}".format(rounded_value, self._METRIC_PREFIX[millidx])


class BadgeService:
    def __init__(self, project_repository: ProjectRepository, downloads_formatter: DownloadsNumberFormatter):
        self._project_repository = project_repository
        self._downloads_formatter = downloads_formatter

    def generate_badge(self, project_name: str) -> Badge:
        project = self._project_repository.get(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        downloads = self._downloads_formatter.format(project.total_downloads)
        s = badge(left_text="downloads", right_text=downloads, right_color="blue")
        return Badge(project_name, s)

    def generate_last_30_days_badge(self, project_name: str) -> Badge:
        project = self._project_repository.get(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        downloads = self._downloads_formatter.format(self._last_downloads(project, 30))
        s = badge(left_text="downloads/month", right_text=downloads, right_color="blue")
        return Badge(project_name, s)

    def generate_last_7_days_badge(self, project_name: str) -> Badge:
        project = self._project_repository.get(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        downloads = self._downloads_formatter.format(self._last_downloads(project, 7))
        s = badge(left_text="downloads/week", right_text=downloads, right_color="blue")
        return Badge(project_name, s)

    @staticmethod
    def _last_downloads(project: Project, days: int) -> Downloads:
        min_date = datetime.now().date() - timedelta(days=days)
        total_downloads = 0
        for d in project.last_downloads():
            if d.date >= min_date:
                total_downloads += d.downloads.value
        return Downloads(total_downloads)


class PersonalizedBadgeService:
    def __init__(
        self,
        project_repository: ProjectRepository,
        downloads_formatter: DownloadsNumberFormatter,
        logger: logging.Logger,
    ):
        self._logger = logger
        self._project_repository = project_repository
        self._downloads_formatter = downloads_formatter

    def generate(
        self, project_name: str, period: str, left_color: str, right_color: str, left_text: str, units: str
    ) -> Badge:
        project = self._project_repository.get(project_name)
        if project is None:
            raise ProjectNotFoundException(project_name)
        badge_data = PersonalizedBadge(
            ProjectName(project_name),
            BadgePeriod[period],
            BadgeStyle(
                left_color=BadgeColor(left_color),
                right_color=BadgeColor(right_color),
                left_text=left_text,
                units=BadgeUnits[units],
            ),
        )
        downloads = self._get_downloads(project, badge_data.period, badge_data.style.units)
        s = badge(
            left_text=badge_data.style.left_text,
            right_text=downloads,
            left_color=badge_data.style.left_color.value,
            right_color=badge_data.style.right_color.value,
        )

        return Badge(badge_data.name.name, s)

    def _get_downloads(self, project: Project, period: BadgePeriod, units: BadgeUnits) -> str:
        if period == BadgePeriod.total:
            downloads = project.total_downloads
        elif period == BadgePeriod.month:
            downloads = project.month_downloads()
        elif period == BadgePeriod.week:
            downloads = self._last_downloads(project, 7)
        else:
            raise Exception(f"{period} not valid")

        return self._downloads_formatter.format_with_units(downloads, units)

    @staticmethod
    def _last_downloads(project: Project, days: int) -> Downloads:
        min_date = datetime.now().date() - timedelta(days=days)
        total_downloads = 0
        for d in project.last_downloads():
            if d.date >= min_date:
                total_downloads += d.downloads.value
        return Downloads(total_downloads)
