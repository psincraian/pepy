import logging
import os
import psycopg2
from commandbus import CommandBus
from google.cloud import bigquery
from orator import DatabaseManager

from pepy.application.command import (
    ImportDownloadsFile,
    ImportDownloadsFileHandler,
    UpdateDownloads,
    UpdateDownloadsHandler,
)
from pepy.application.helper import AdminPasswordChecker
from pepy.application.query import BadgeProvider, ProjectProvider, DownloadsNumberFormatter
from pepy.domain.model import HashedPassword
from pepy.infrastructure.bq_downloads_extractor import BQDownloadsExtractor
from pepy.infrastructure.db_repository import DBProjectRepository
from pepy.infrastructure.db_view import DBProjectView
from ._config import DATABASE, BQ_CREDENTIALS_FILE, ADMIN_PASSWORD, LOGGING_FILE, DATABASE_ORATOR, LOGGING_DIR

db_connection = psycopg2.connect(**DATABASE)
db_orator = DatabaseManager(DATABASE_ORATOR)
project_repository = DBProjectRepository(db_connection)
db_project_view = DBProjectView(db_orator)
command_bus = CommandBus()
command_bus.subscribe(ImportDownloadsFile, ImportDownloadsFileHandler(project_repository))
downloads_formatter = DownloadsNumberFormatter()
badge_query = BadgeProvider(db_project_view, downloads_formatter)
project_provider = ProjectProvider(project_repository, db_project_view)

# Directories configuration
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

# Logger configuration
logger = logging.getLogger("pepy")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(pathname)s:%(funcName)s:%(lineno)d]: %(message)s")
file_handler = logging.FileHandler(LOGGING_FILE)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

environment = os.getenv("APPLICATION_ENV", None)
if environment == "prod":
    bq_client = bigquery.Client.from_service_account_json(BQ_CREDENTIALS_FILE)
    downloads_extractor = BQDownloadsExtractor(bq_client)
    admin_password_checker = AdminPasswordChecker(HashedPassword(ADMIN_PASSWORD))
    command_bus.subscribe(
        UpdateDownloads, UpdateDownloadsHandler(project_repository, downloads_extractor, admin_password_checker, logger)
    )
