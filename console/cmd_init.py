import click
from loguru import logger
import toml

from bot.utils.schedule import get_global_dictionary,write_json,TableParser
from tiny_vk.database import Database
from console.main import cli

# Загрузка конфигурации
with open('config.toml','r') as tml:
    config = toml.load(tml)

@cli.command
@click.option('--database',help="db-path",is_flag = True)
@click.option('--schedule',help="json-path", is_flag= True)
def init(database,schedule):
    """Инициализация базы данных и таблицы"""

    
    if schedule:
        global_dictionary = get_global_dictionary(TableParser(config['table-id']))
        write_json(config['json-path'],global_dictionary)
        logger.info('Данные из гугл таблицы получены!')
        
    if database:
        Database(config['db-path'],'Users').create_table({'id': "INT",
                                                "state" : "TEXT",
                                                'object' : 'TEXT',
                                                'ruobr_login' : 'TEXT',
                                                'ruobr_password' : 'TEXT',
                                                'ruobr_tmp_login': 'TEXT',
                                                'ruobr_tmp_password' : 'TEXT',
                                                'mail' : 'INT'})
        logger.info('Пустая таблица инициализирована!')
