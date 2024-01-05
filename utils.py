from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from env_settings import EnvSettings, BASE_DIR
import yaml
import streamlit_authenticator as stauth
import hashlib
from typing import Union

env_settings = EnvSettings()


@contextmanager
def session_scope():
    db_path = BASE_DIR / 'volumes' / env_settings.DB_NAME
    engine = create_engine(f'sqlite:///{db_path}')
    session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_authenticator() -> stauth.Authenticate:
    with open(BASE_DIR / 'volumes' / './credentials.yaml') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    return stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )


def get_content_md5(content: Union[bytes, str]):
    m = hashlib.md5()
    m.update(content)
    h = m.hexdigest()

    return h
