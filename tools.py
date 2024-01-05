import os
import click
import yaml
from streamlit_authenticator import Hasher
from env_settings import EnvSettings, BASE_DIR
from utils import session_scope
from databases.schemas import Base

env_settings = EnvSettings()


@click.group()
def cli():
    """系統應用小工具"""
    pass


@click.command()
def init_system():
    """初始化資料庫及建立 superuser"""
    if not os.path.exists(BASE_DIR / 'volumes'):
        os.mkdir(BASE_DIR / 'volumes')

    with session_scope() as session:
        Base.metadata.drop_all(session.bind)
        Base.metadata.create_all(session.bind)

    click.echo("資料庫初始化完成")

    data = {
        "cookie": {
            "expiry_days": 1,
            "key": "random_signature_key",
            "name": "random_cookie_name"
        },
        "credentials": {
            "usernames": {
                "root": {
                    "email": env_settings.ROOT_EMAIL,
                    "name": "root",
                    "password": Hasher([env_settings.ROOT_PASSWORD]).generate()[0]
                }
            }
        },
        "preauthorized": {
            "emails": ["melsby@gmail.com"]
        }
    }
    with open(BASE_DIR / 'volumes' / 'credentials.yaml', 'w') as file:
        yaml.safe_dump(data, file)
    click.echo("超級使用者建立完成")

    if not os.path.exists(BASE_DIR / 'files'):
        os.mkdir(BASE_DIR / 'files')
    else:
        for root, dirs, files in os.walk(BASE_DIR / 'files'):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(BASE_DIR / 'files')
        os.mkdir(BASE_DIR / 'files')


cli.add_command(init_system)

if __name__ == '__main__':
    cli()
