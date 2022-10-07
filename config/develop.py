from .default import *

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.getenv('DEFAULT_DEVELOPMENT_DB')
