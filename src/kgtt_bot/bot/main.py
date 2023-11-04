"""Файл инициализации экземпляра бота и хэндлеров для взаимодействия с пользователем"""

from kgtt_bot.vk import Bot
from config import config
kgtt = Bot(config['token'],database=config["db-path"])
from kgtt_bot.bot.handlers import *