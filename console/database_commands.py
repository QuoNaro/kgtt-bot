
import click

from tiny_vk.database import Database
from config.cfg import current_dir

from console.main import cli

@cli.group
def database():
    """Получение данных из БД"""
    pass

@database.command()
def users():
    """Получение списка пользователей"""
    db = Database('kgtt.db','Users')
    click.echo(db.get_users())

@database.command()
@click.option('-i', prompt="Введите ID пользователя",  help="ID пользователя",type = int)
def info(i):
    """Получение списка пользователей"""
    db = Database(f'{current_dir}/kgtt.db','Users')
    click.echo(db.get_information(i))


@database.command()
def mailing_users():
    """Получение списка рассылки"""
    db = Database('kgtt.db','Users')
    click.echo(db.get_mailing_ids('mail'))