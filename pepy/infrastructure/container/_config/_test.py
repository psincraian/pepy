WTF_CSRF_ENABLED = True
SECRET_KEY = "1234"
DEBUG = True

DATABASE = {"host": "pgsql", "user": "pepy", "password": "pepy", "database": "pepy_test"}
DATABASE_ORATOR = {
    "prope": {"driver": "postgres", "host": "pgsql", "user": "pepy", "password": "pepy", "database": "pepy_test"}
}

# password: pepyrocks
ADMIN_PASSWORD = "$pbkdf2-sha256$29000$uXcOobS2FiIkJCSkFGJszQ$TwCkC7lAIvOTrPjWmVr3LGDVAAK68CjWW7niKoI6dzo"
BQ_CREDENTIALS_FILE = None  # not used in development
LOGGING_FILE = "test_app.log"
