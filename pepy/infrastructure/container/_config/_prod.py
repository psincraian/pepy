import logging
import os

MONGODB = "mongodb://pepy-mongo:27017"

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get("PEPY_SECRET_KEY")

ADMIN_PASSWORD = os.environ.get("PEPY_ADMIN_PASSWORD")
BQ_CREDENTIALS_FILE = os.environ.get("PEPY_BIGQUERY_CREDENTIALS")
LOGGING_DIR = "logs"
LOGGING_FILE = os.environ.get("PEPY_LOGGING_FILE")
LOGGING_LEVEL = logging.DEBUG