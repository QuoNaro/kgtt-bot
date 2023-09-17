from tiny_vk import Bot
from config import config,global_dir

bot = Bot(config['token'],dbfile=f'{global_dir}/{config["db-path"]}',table_name="Users", columns= {'object' : 'TEXT',
                                             'ruobr_login' : 'TEXT',
                                             'ruobr_password' : 'TEXT',
                                             'ruobr_tmp_login': 'TEXT',
                                             'ruobr_tmp_password' : 'TEXT',
                                             'mail' : 'INT'})


from bot.handlers import *  # noqa: F403, E402
