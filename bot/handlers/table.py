from bot.main import bot
from bot.utils.schedule import read_json,get_text
from bot.data import keyboards
from bot.data import states
from bot.data import emoji
import toml
from bot.utils.schedule import exceptions
from bot.logs.logging import *
from loguru import logger

with open('~/.config/kgttbotconfig.toml','r') as tml:
    config = toml.load(tml)

@bot.on.multiply(['Расписание'], [states.main], next_state=states.schedule)
def schedule(self):
    bot.utils.user_message('Раздел с расписанием', keyboard = keyboards.schedule())

 

class Authentification:
    @bot.on.state(states.table_register)
    def reg(self):
        if self.text != emoji.red_circle:
            bot.db.update_field(category="object",new=self.text)
            bot.db.set_state(states.main)
            bot.utils.user_message("Приятного использования!", keyboard=keyboards.main())

@bot.on.multiply(['Из таблицы'], [states.schedule])
def from_table(self):
    if self.object:
      try:
        group_dictionary_table = read_json(config['json-path'])[self.object]
        schedule = get_text(group_dictionary_table)
        bot.utils.user_message(schedule)
      except FileNotFoundError as e:
        logger.exception(e)
        bot.utils.user_message('Произошла внутренняя ошибка, попробуйте позже')
      except KeyError:
        logger.exception(f'Группы {self.object} нет в таблице')
        bot.utils.user_message('Группа не найдена!')
      except exceptions.GroupNotFoundError:
        logger.exception(f'Группы {self.object} нет в таблице')
        bot.utils.user_message('Группа не найдена!')
    else:
      bot.utils.user_message(f'Вы не зарегистрированы\nПуть для регистрации : {emoji.red_circle} → {emoji.gear} → Группа')