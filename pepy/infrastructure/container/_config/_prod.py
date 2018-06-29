import os

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get("PEPY_SECRET_KEY")

DATABASE = {
    "host": os.environ.get("PEPY_DATABASE_HOST"),
    "user": os.environ.get("PEPY_DATABASE_USER"),
    "password": os.environ.get("PEPY_DATABASE_PASSWORD"),
    "database": os.environ.get("PEPY_DATABASE_NAME"),
}

ADMIN_PASSWORD = os.environ.get("PEPY_ADMIN_PASSWORD")
BQ_CREDENTIALS_FILE = os.environ.get("PEPY_BIGQUERY_CREDENTIALS")
