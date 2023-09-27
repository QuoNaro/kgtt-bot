from bot.main import bot
from bot.data import keyboards
from bot.data import states
from bot.data import emoji
import os
from datetime import datetime,timedelta,timezone
from tiny_vk.utils import generate_keyboard


@bot.on.message('Начать', 'Начало', 'Старт', '/start', '/Начать',next_state = states.main)
def start(self):
    bot.utils.user_message('Добро пожаловать!', keyboard = keyboards.main())
    bot.utils.user_message('Подпишитесь на сообщество, чтобы не пропускать обновления',link=['https://vk.com/kgttbot'])

@bot.on.message('!сброс', '/сброс')
def reset(self):
    bot.db.delete_user()
    bot.utils.user_message('Все данные успешно удалены!', keyboard = keyboards.main())

@bot.on.message(emoji.red_circle, next_state = states.main)
def back(self):
    bot.utils.user_message('Главное меню', keyboard = keyboards.main())

@bot.on.empty("not self.state or not self.id")
def to_main_state(self):
    tz = timezone(timedelta(hours=7))
    hour = datetime.now(tz=tz).hour
    bot.db.set_state(states.main)
    choose = [f"вечер{emoji.moon}",f"день{emoji.sun}"]
    bot.utils.user_message(f'Добрый { choose[True if 13 <= hour <= 18 else False] }!\nДавайте начнем?', keyboard=generate_keyboard( ('Начать','positive') ))
    
@bot.on.empty('True')
def stop_mailing(self):
    if self.id == 435170678 and self.text == '!рофф':
        command = "sudo supervisorctl stop schedule_mailing"
        os.system(command)
        bot.utils.user_message('Рассылка отключена!',id = 435170678)

@bot.on.empty('True')
def start_mailing(self):
    if self.id == 435170678 and self.text == '!рон':
        command = "sudo supervisorctl start schedule_mailing"
        os.system(command)
        bot.utils.user_message('Рассылка запущена!', id = 435170678)

    