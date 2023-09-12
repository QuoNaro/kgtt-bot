from bot.main import bot

from bot.data import keyboards
from bot.data import states
from bot.data import emoji

@bot.on.multiply(['Рассылка'], [states.schedule])
def mailing(self):
    if self.object:
        bot.db.set_state(states.mailing)
        mailing_status = 0 if self.mail is None else self.mail
        bot.utils.user_message(f'Рассылка : {["Отключена","Включена"][mailing_status]}', keyboard =keyboards.mailing())

    else:
        bot.utils.user_message(f'Вы не зарегистрированы\nПуть для регистрации : {emoji.red_circle} → {emoji.gear} → Группа')

class Mailing:
    
    
    @bot.on.multiply(['Подписаться'],[states.mailing])
    def on(self):
        bot.db.update_field(category="mail",new=1)
        mailing_status = 0 if self.mail is None else self.mail
        bot.utils.user_message(f'Рассылка : {["Отключена","Включена"][mailing_status]}')
        
    
    @bot.on.multiply(['Отписаться'],[states.mailing])
    def off(self):
        bot.db.update_field(category="mail",new=0)
        mailing_status = 0 if self.mail is None else self.mail
        bot.utils.user_message(f'Рассылка : {["Отключена","Включена"][mailing_status]}')
        
        



