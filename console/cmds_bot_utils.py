import click

from tiny_vk.utils import user_message
from tiny_vk.database import Database

from console.main import cli

import toml

with open('~/.config/kgttbotconfig.toml','r') as tml:
    config = toml.load(tml)


@cli.group
def utils():
    """Утилиты бота"""
    pass

@utils.command()
@click.option('-i', prompt="Введите ID пользователя",  help="ID пользователя",type = int)
@click.option('-m',prompt="Введите сообщение пользователю", help="Сообщение пользователю", type = str)
def message(i,m):
    user_message(config['token'],i,m)

@utils.command()
@click.option('-m',prompt="Введите сообщение пользователям", help="Сообщение пользователям", type = str)
def messages(m):
    db = Database(config['db-path'],'Users')
    for i in db.get_users():
        try:
            user_message(config['token'],i,m)
        except Exception:
            pass
