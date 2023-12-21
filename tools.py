import click
from utils import session_scope
from schemas import Base, User
from streamlit_authenticator import Hasher
from env_settings import EnvSettings

env_settings = EnvSettings()


@click.group()
def cli():
    """系統應用小工具"""
    pass


@click.command()
def setup():
    """初始化系統設置"""
    with session_scope() as session:
        Base.metadata.drop_all(session.bind)
        Base.metadata.create_all(session.bind)

        new_user = User(
            username=env_settings.ROOT_NAME,
            email=env_settings.ROOT_EMAIL,
            password=Hasher([env_settings.ROOT_PASSWORD]).generate()[0],
            is_superuser=True
        )
        session.add(new_user)
        session.commit()

    click.echo("系統初始化完成，包括資料庫和超級用戶的創建。")


cli.add_command(setup)

if __name__ == '__main__':
    cli()
