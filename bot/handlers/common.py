from bot.main import bot

from bot.data import keyboards
from bot.data import states
from bot.data import emoji
import subprocess
import os



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


@bot.on.message('!рофф')
@bot.on.empty('self.id == 435170678')
def stop_mailing(self):
    command = "sudo supervisorctl stop schedule_mailing"
    os.system(command)
    bot.utils.user_message('Рассылка отключена!',id = 435170678)
    
    
    
@bot.on.message('!рон')
@bot.on.empty('self.id == 435170678')
def start_mailing(self):
    command = "sudo supervisorctl start schedule_mailing"
    os.system(command)
    bot.utils.user_message('Рассылка запущена!', id = 435170678)

    