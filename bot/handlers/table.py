from bot.main import bot
from bot.utils.schedule import read_json,get_text
from bot.data import keyboards
from bot.data import states
from bot.data import emoji
from config import config,global_dir
from bot.utils.schedule import exceptions
from bot.logs.logging import *  # noqa: F403
from loguru import logger



@bot.on.multiply(['Расписание'], [states.main])
def schedule(self):
    if self.object:
      try:
        group_dictionary_table = read_json(f'{global_dir}/{config["json-path"]}')[self.object.lower()]
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

class Authentification:
    @bot.on.state(states.table_register)
    def reg(self):
        if self.text != emoji.red_circle:
            bot.db.update_field(category="object",new=self.text)
            bot.db.set_state(states.main)
            bot.db.update_field(category="mail",new=1)
            bot.utils.user_message("Приятного использования! Рассылка включена !", keyboard=keyboards.main())
            