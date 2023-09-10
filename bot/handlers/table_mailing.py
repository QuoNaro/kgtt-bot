from bot.main import bot

from bot.data import keyboards
from bot.data import states
from bot.data import emoji

@bot.on.multiply(['Рассылка'], [states.schedule])
def mailing(self):
    if self.object:
        bot.db.set_state(states.mailing)
        bot.utils.user_message('Всё окей!', keyboard =keyboards.mailing())

    else:
        bot.utils.user_message(f'Вы не зарегистрированы\nПуть для регистрации : {emoji.red_circle} → {emoji.gear} → Группа')

class Mailing:
    
    
    @bot.on.multiply(['Подписаться'],[states.mailing])
    def on(self):
        bot.db.update_field(category="mail",new=1)
        bot.utils.user_message('Вы подписались на рассылку!')
        
    
    @bot.on.multiply(['Отписаться'],[states.mailing])
    def off(self):
        bot.db.update_field(category="mail",new=0)
        bot.utils.user_message('Вы отписались от рассылки!')
        
        



