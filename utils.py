from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from env_settings import EnvSettings

env_settings = EnvSettings()


@contextmanager
def session_scope():
    engine = create_engine(f'sqlite:///{env_settings.DB_NAME}.sqlite3')
    session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
