import pytest
import sqlalchemy
from async_generator import yield_, async_generator
from app.database import db, init_db


@pytest.fixture(scope='module')
def sa_engine():
    engine = sqlalchemy.create_engine('sqlite:///:memory:')
    db.metadata.create_all(engine)
    yield engine
    db.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
@async_generator
async def bind(sa_engine):
    async with db.with_bind('sqlite:///:memory:', echo=True) as e:
        await yield_(e)
    sa_engine.execute("DELETE FROM gino_user_settings")
    sa_engine.execute("DELETE FROM gino_users")
