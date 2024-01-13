"""Файл инициализации экземпляра бота и хэндлеров для взаимодействия с пользователем"""

from vk import Bot
import os
kgtt = Bot(os.getenv('TOKEN'),database='database/kgtt.sqlite')
from handlers import *

if __name__ == '__main__':
    kgtt.start()