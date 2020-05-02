WTF_CSRF_ENABLED = True
SECRET_KEY = "1234"

MONGODB = "mongodb://pepy:pepy@mongodb"

# password: pepyrocks
ADMIN_PASSWORD = "$pbkdf2-sha256$29000$uXcOobS2FiIkJCSkFGJszQ$TwCkC7lAIvOTrPjWmVr3LGDVAAK68CjWW7niKoI6dzo"
BQ_CREDENTIALS_FILE = "bigquery.json"  # not used in development
LOGGING_DIR = "logs"
LOGGING_FILE = f"{LOGGING_DIR}/app.log"
