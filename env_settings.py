from pydantic_settings import BaseSettings, SettingsConfigDict
import pathlib

BASE_DIR = pathlib.Path(__file__).parent


class EnvSettings(BaseSettings):
    DB_NAME: str = "ffd.sqlite3"
    ROOT_EMAIL: str = None
    ROOT_PASSWORD: str = None

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
