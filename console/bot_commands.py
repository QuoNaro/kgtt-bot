import click
from loguru import logger

from tiny_vk.utils import user_message
from tiny_vk.database import Database

from config.cfg import current_dir,token,database_abs_path,tableid
from bot.utils.schedule import write_json,TableParser,get_global_dictionary
from console.main import cli



@cli.group
def bot():
    """Управление ботом"""
    pass


@bot.command()
@click.option('-i', prompt="Введите ID пользователя",  help="ID пользователя",type = int)
@click.option('-m',prompt="Введите сообщение пользователю", help="Сообщение пользователю", type = str)
def message_user(i,m):
    db = Database(database_abs_path,'Users')
    print(db.get_users())
    user_message(token,m,user_id=i)

@bot.command()
@click.option('-m',prompt="Введите сообщение пользователям", help="Сообщение пользователям", type = str)
def message_users(m):
    db = Database(database_abs_path,'Users')
    for i in db.get_users():
        try:
            user_message(token,m,i)
        except Exception:
            pass

@bot.command()
@click.option('-t',prompt="Введите токен для бота", help="Токен бота", type = str)
@click.option('-i',prompt="Введите ID гугл таблицы", help="Период обновления расписнаия", type = str)
@click.option('-r',prompt="Введите период обновления расписания (в секундах)", help="Период обновления расписнаия", type = int)
def config(t,r,i):
    with open(f'{current_dir}/config/.env','w') as file:
        file.write(f'TOKEN={t}')
    with open(f'{current_dir}/config/cfg.py','r') as cfg:
        base_config = cfg.read()
    for parameter in base_config.splitlines():
        if 'event_reload_time' in parameter:
            base_config = base_config.replace(parameter, f'event_reload_time = {r}') 
        if 'tableid' in parameter :
            base_config = base_config.replace(parameter, f'tableid = "{i}" ')
    with open(f'{current_dir}/config/cfg.py','w') as cfg:
        cfg.write(base_config)
        
        
@bot.command()
def generate_schedule():
    tableparser = TableParser(tableid)
    json = get_global_dictionary(tableparser)
    write_json(f'{current_dir}/schedule.json',json)
    logger.info('Создан файл с расписанием')