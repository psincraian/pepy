import logging
import os
from pathlib import Path

from commandbus import CommandBus
from google.cloud import bigquery
from pymongo import MongoClient

from pepy.application.admin_password_checker import AdminPasswordChecker
from pepy.application.badge_service import BadgeService, DownloadsNumberFormatter, PersonalizedBadgeService
from pepy.application.command import (
    UpdateVersionDownloads,
    UpdateVersionDownloadsHandler,
    ImportTotalDownloads,
    ImportTotalDownloadsHandler,
)
from pepy.domain.model import HashedPassword
from pepy.infrastructure.db_repository import MongoProjectRepository
from ._config import BQ_CREDENTIALS_FILE, ADMIN_PASSWORD, LOGGING_FILE, LOGGING_DIR, MONGODB, environment, Environment
from ..bq_stats_viewer import BQStatsViewer
from ...domain.pypi import StatsViewer, Result


class MockStatsViewer(StatsViewer):
    def __init__(self):
        self._rows = None

    def set_data(self, rows):
        self._rows = rows

    def get_version_downloads(self, date):
        return Result(len(self._rows), self._rows)


# Directories configuration
Path(LOGGING_DIR).mkdir(parents=True, exist_ok=True)

# Logger configuration
logger = logging.getLogger("pepy")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(pathname)s:%(funcName)s:%(lineno)d]: %(message)s")
file_handler = logging.FileHandler(LOGGING_FILE)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
mongo_client = MongoClient(MONGODB)

if environment == Environment.test:
    project_repository = MongoProjectRepository(mongo_client.pepy_test)
else:
    project_repository = MongoProjectRepository(mongo_client.pepy)

bq_client = None
if environment == Environment.prod:
    bq_client = bigquery.Client.from_service_account_json(BQ_CREDENTIALS_FILE)

if environment == Environment.test:
    stats_viewer = MockStatsViewer()
else:
    stats_viewer = BQStatsViewer(bq_client)

admin_password_checker = AdminPasswordChecker(HashedPassword(ADMIN_PASSWORD))
command_bus = CommandBus()
command_bus.subscribe(
    UpdateVersionDownloads,
    UpdateVersionDownloadsHandler(project_repository, stats_viewer, admin_password_checker, logger),
)
command_bus.subscribe(ImportTotalDownloads, ImportTotalDownloadsHandler(project_repository, logger))
downloads_formatter = DownloadsNumberFormatter()
badge_service = BadgeService(project_repository, downloads_formatter)
personalized_badge_service = PersonalizedBadgeService(project_repository, downloads_formatter, logger)
