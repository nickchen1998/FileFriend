from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    DB_NAME: str = "file_friend"

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
