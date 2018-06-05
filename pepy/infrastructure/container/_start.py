import os
import psycopg2
from commandbus import CommandBus
from google.cloud import bigquery

from pepy.application.command import ImportDownloadsFile, ImportDownloadsFileHandler, UpdateDownloads, \
    UpdateDownloadsHandler
from pepy.application.helper import AdminPasswordChecker
from pepy.application.query import BadgeProvider, ProjectProvider, DownloadsNumberFormatter
from pepy.domain.model import HashedPassword
from pepy.infrastructure.bq_downloads_extractor import BQDownloadsExtractor
from pepy.infrastructure.db_repository import DBProjectRepository
from ._config import DATABASE, BQ_CREDENTIALS_FILE, ADMIN_PASSWORD

db_connection = psycopg2.connect(**DATABASE)
project_repository = DBProjectRepository(db_connection)
command_bus = CommandBus()
command_bus.subscribe(ImportDownloadsFile, ImportDownloadsFileHandler(project_repository))
downloads_formatter = DownloadsNumberFormatter()
badge_query = BadgeProvider(project_repository, downloads_formatter)
project_provider = ProjectProvider(project_repository)

environment = os.getenv('APPLICATION_ENV', None)
if environment == 'prod':
    bq_client = bigquery.Client.from_service_account_json(BQ_CREDENTIALS_FILE)
    downloads_extractor = BQDownloadsExtractor(bq_client)
    admin_password_checker = AdminPasswordChecker(HashedPassword(ADMIN_PASSWORD))
    command_bus.subscribe(UpdateDownloads, UpdateDownloadsHandler(project_repository, downloads_extractor,
                                                                  admin_password_checker))
