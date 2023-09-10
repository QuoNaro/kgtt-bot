from tiny_vk import Bot
import toml

# Открытие конфига
with open('config.toml','r') as tml:
  config = toml.load(tml)

bot = Bot(config['token'],dbfile=config['db-path'],table_name="Users", columns= {'object' : 'TEXT',
                                             'ruobr_login' : 'TEXT',
                                             'ruobr_password' : 'TEXT',
                                             'ruobr_tmp_login': 'TEXT',
                                             'ruobr_tmp_password' : 'TEXT',
                                             'mail' : 'INT'})


from bot.handlers.common import *
from bot.handlers.parameters import *
from bot.handlers.marks import *
from bot.handlers.table_mailing import *
from bot.handlers.table import *