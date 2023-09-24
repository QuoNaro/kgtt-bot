from bot.main import bot
from bot.data import keyboards
from bot.data import states
from bot.data import emoji
import os





@bot.on.message('Начать', 'Начало', 'Старт', '/start', '/Начать',next_state = states.main)
def start(self):
    bot.utils.user_message('Добро пожаловать!', keyboard = keyboards.main())
    bot.utils.user_message('Подпишитесь на сообщество :)',link=['https://vk.com/widget_community.php?act=a_subscribe_box&oid=-214878797&state=1'])

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

    