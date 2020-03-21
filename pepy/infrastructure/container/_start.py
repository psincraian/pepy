import logging
import os

from commandbus import CommandBus
from google.cloud import bigquery
from pymongo import MongoClient

from pepy.application.command import (
    ImportDownloadsFile,
    ImportDownloadsFileHandler,
    UpdateDownloads,
    UpdateDownloadsHandler,
    UpdateVersionDownloads, UpdateVersionDownloadsHandler)
from pepy.application.helper import AdminPasswordChecker
from pepy.application.query import BadgeProvider, ProjectProvider, DownloadsNumberFormatter
from pepy.domain.model import HashedPassword
from pepy.infrastructure.bq_downloads_extractor import BQDownloadsExtractor
from pepy.infrastructure.db_repository import MongoProjectRepository
from pepy.infrastructure.db_view import MongoProjectView
from ._config import BQ_CREDENTIALS_FILE, ADMIN_PASSWORD, LOGGING_FILE, LOGGING_DIR, MONGODB
from ...domain.pypi import StatsViewer, Result


class MockStatsViewer(StatsViewer):
    def __init__(self):
        self._rows = None

    def set_data(self, rows):
        self._rows = rows

    def get_version_downloads(self, date):
        return Result(len(self._rows), self._rows)


# Logger configuration
logger = logging.getLogger("pepy")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(pathname)s:%(funcName)s:%(lineno)d]: %(message)s")
file_handler = logging.FileHandler(LOGGING_FILE)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
mongo_client = MongoClient(MONGODB)
project_repository = MongoProjectRepository(mongo_client)
project_view = MongoProjectView(mongo_client)
stats_viewer = MockStatsViewer()
admin_password_checker = AdminPasswordChecker(HashedPassword(ADMIN_PASSWORD))
command_bus = CommandBus()
command_bus.subscribe(ImportDownloadsFile, ImportDownloadsFileHandler(project_repository))
command_bus.subscribe(UpdateVersionDownloads, UpdateVersionDownloadsHandler(project_repository, stats_viewer, admin_password_checker, logger))
downloads_formatter = DownloadsNumberFormatter()
badge_query = BadgeProvider(project_view, downloads_formatter)
project_provider = ProjectProvider(project_view)

# Directories configuration
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

environment = os.getenv("APPLICATION_ENV", None)
if environment == "prod":
    bq_client = bigquery.Client.from_service_account_json(BQ_CREDENTIALS_FILE)
    downloads_extractor = BQDownloadsExtractor(bq_client)
    command_bus.subscribe(
        UpdateDownloads, UpdateDownloadsHandler(project_repository, downloads_extractor, admin_password_checker, logger)
    )
