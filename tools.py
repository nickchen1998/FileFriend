import click
import yaml
from streamlit_authenticator import Hasher
from env_settings import EnvSettings
from utils import session_scope
from databases.schemas import Base

env_settings = EnvSettings()


@click.group()
def cli():
    """系統應用小工具"""
    pass


@click.command()
def encrypt_password():
    """加密使用者密碼"""
    # 讀取 YAML 文件
    with open('./credentials.yaml', 'r') as file:
        data = yaml.safe_load(file)

    # 遍歷用戶名並更改密碼
    for username in data['credentials']['usernames']:
        if not data['credentials']['usernames'][username].get("is_encrypt"):
            data['credentials']['usernames'][username]['password'] = Hasher([
                data['credentials']['usernames'][username]['password']
            ]).generate()[0]
            data['credentials']['usernames'][username]['is_encrypt'] = True

    # 將更新後的數據寫回 YAML 文件
    with open('./credentials.yaml', 'w') as file:
        yaml.safe_dump(data, file)

    click.echo("使用者密碼加密完成")


@click.command()
def init_database():
    """資料庫初始化"""
    with session_scope() as session:
        Base.metadata.drop_all(session.bind)
        Base.metadata.create_all(session.bind)
        click.echo("資料庫初始化完成")


cli.add_command(init_database)
cli.add_command(encrypt_password)

if __name__ == '__main__':
    cli()
