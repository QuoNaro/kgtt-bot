from bot.main import bot

from bot.data import keyboards
from bot.data import states
from bot.data import emoji



@bot.on.message('Начать', 'Начало', 'Старт', '/start', '/Начать',next_state = states.main)
def start(self):
    bot.utils.user_message('За работу!', keyboard = keyboards.main())

@bot.on.message('!сброс', '/сброс')
def reset(self):
    bot.db.delete_user()
    bot.utils.user_message('Все данные успешно удалены!', keyboard = keyboards.main())

@bot.on.message(emoji.red_circle, next_state = states.main)
def back(self):
    bot.utils.user_message('Главное меню', keyboard = keyboards.main())

@bot.on.empty(f"not self.state")
def to_main_state(self):
    bot.db.set_state(states.main)