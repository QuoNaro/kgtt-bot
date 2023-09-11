from .main import cli
import click
import toml
import subprocess

@cli.command
@click.option('-t',prompt="Токен для бота", help="Токен бота", type = str)
@click.option('-i',prompt="ID гугл таблицы", help="ID таблицы", type = str)
@click.option('-r',prompt="Период обновления расписания", help="table-reload-time",type = int)
@click.option('-d',prompt="Путь до базы данных", help="db-path", type = str)
@click.option('-j',prompt="Путь до json", help="json-path", type = str)
def make_config(t,i,r,d,j):
    
    """Первоначальная генерация config.toml"""
    dict_config = {'token': t,
                   'table-id': i,
                   'table-reload-time': r,
                   'db-path':d,
                   'json-path': j}
    subprocess.call(['mkdir','-r','~/.config'])
    with open('~/.config/kgttbotconfig.toml','w') as tml:
        toml.dump(dict_config,tml)

