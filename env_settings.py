from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    DB_NAME: str = "file_friend"
    ROOT_NAME: str = "root"
    ROOT_EMAIL: str = None
    ROOT_PASSWORD: str = None

    # cookies settings
    COOKIES_EXPIRY_DAYS: int = 30
    COOKIES_KEY: str = "random_signature_key"
    COOKIES_NAME: str = "random_cookie_name"

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
