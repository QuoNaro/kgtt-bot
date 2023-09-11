import click
import vk_api
from tiny_vk.utils import user_message
from tiny_vk.database import Database

from console.main import cli
from config import config,global_dir


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
@click.option('--database',is_flag = True)
def messages(m,database):
    
    if database:
        db = Database(f'{global_dir}/{config["db-path"]}','Users')
        user_ids = db.get_users()
    
    else:
        vk_session = vk_api.VkApi(token=config['token'])
        vk = vk_session.get_api()

        # Получение списка бесед, в которых участвует ваш бот
        conversations = vk.messages.getConversations(filter='all')
        
        # Сбор ID пользователей
        user_ids = []
        for conversation in conversations['items']:
            peer = conversation['conversation']['peer']
            if peer['type'] == 'user':
                user_ids.append(peer['id'])

        
    for i in user_ids:
        try:
            user_message(config['token'],i,m)
        except Exception:
            print(i)
            pass
      
