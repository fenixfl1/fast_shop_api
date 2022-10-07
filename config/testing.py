from .default import *

TESTING = True
ENV = 'testing'
SQLALCHEMY_DATABASE_URI = os.getenv('DEFAULT_TESTING_DB')
