from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config.default import ENV


if ENV == 'development':
    from config.develop import *
elif ENV == 'testing':
    from config.testing import *
elif ENV == 'production':
    from config.production import *
else:
    raise Exception(f'Unknown environment "{ENV}"')

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    max_identifier_length=30
)

db = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db.query_property()


def init_db() -> None:
    from ..database import models
    Base.metadata.create_all(bind=engine)
