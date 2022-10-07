from .default import *

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.getenv('DEFAULT_PRODUCTION_DB')
