WTF_CSRF_ENABLED = True
SECRET_KEY = "1234"

DATABASE = {"host": "pgsql", "user": "pepy", "password": "pepy", "database": "pepy"}
DATABASE_ORATOR = {
    "prope": {"driver": "postgres", "host": "pgsql", "user": "pepy", "password": "pepy", "database": "pepy"}
}

# password: pepyrocks
ADMIN_PASSWORD = "$pbkdf2-sha256$29000$uXcOobS2FiIkJCSkFGJszQ$TwCkC7lAIvOTrPjWmVr3LGDVAAK68CjWW7niKoI6dzo"
BQ_CREDENTIALS_FILE = None  # not used in development
LOGGING_FILE = "app.log"
