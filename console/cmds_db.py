
import click
import toml
from tiny_vk.database import Database
from console.main import cli



# Открытие конфига
with open('config.toml','r') as tml:
        config = toml.load(tml)

db = Database(config['db-path'],'Users')

# Создание группы database
@cli.group
def database():
    """Получение данных из БД"""
    pass


@database.command()
def users():
    """Получение списка пользователей"""
    click.echo(db.get_users())

@database.command()
@click.option('-i', prompt="Введите ID пользователя",  help="ID пользователя",type = int)
def user_info(i):
    """Получение списка пользователей"""
    click.echo(db.get_information(i))


@database.command()
def mailing_users():
    """Получение списка рассылки"""
    click.echo(db.get_mailing_ids('mail'))