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
    email = input("請輸入 email：")
    password = input("請輸入 password：")
    password_confirm = input("請再次輸入 password：")
    if password == password_confirm:
        with session_scope() as session:
            Base.metadata.drop_all(session.bind)
            Base.metadata.create_all(session.bind)

        click.echo("資料庫初始化完成")

        data = {
            "cookie": {
                "expiry_days": 30,
                "key": "random_signature_key",
                "name": "random_cookie_name"
            },
            "credentials": {
                "usernames": {
                    "root": {
                        "email": email,
                        "name": "root",
                        "password": Hasher([password]).generate()[0]
                    }
                }
            },
            "preauthorized": {
                "emails": ["melsby@gmail.com"]
            }
        }
        with open('./credentials.yaml', 'w') as file:
            yaml.safe_dump(data, file)
        click.echo("超級使用者建立完成")

        if not os.path.exists(BASE_DIR / 'files'):
            os.mkdir(BASE_DIR / 'files')
    else:
        click.echo("兩次 password 不一致，請重新執行。")


cli.add_command(init_system)

if __name__ == '__main__':
    cli()
