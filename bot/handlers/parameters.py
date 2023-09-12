from bot.logs.logging import *


from bot.main import bot

from bot.data import keyboards
from tiny_vk.utils import generate_keyboard
from bot.data import states
from bot.data import emoji


@bot.on.multiply([emoji.gear], [states.main], next_state=states.parameters)
def parameters(self):
    """Меню параметров с динамическими кнопками"""
    password = lambda x : '*' * len(x) if x != None else None
    mail_status = self.mail if self.mail != None else 0
    buttons = [(f"Логин : {self.ruobr_login}","secondary"),
                (f"Пароль : {password(self.ruobr_password)}","secondary"),
                None,
                (f"Группа : {self.object}","secondary"),
                None,
                ("Помощь","positive"),
                None,
                (emoji.red_circle,"negative")]

    if not self.ruobr_password and not self.ruobr_login :
      buttons.pop(0)
      buttons[0] = (f"Авторизация Ruobr","secondary")
    
    key = generate_keyboard(*buttons)
    bot.utils.user_message("Параметры", keyboard = key )
 

class Parameters:

  @bot.on.state(states.parameters)
  def ruobr_auth(self):
    if self.text == "Авторизация Ruobr" or "Пароль" in self.text or "Логин" in self.text:
      bot.db.set_state(states.ruobr_register[0])
      bot.utils.user_message('Введите логин от Ruobr', keyboard = keyboards.rcircle())
  
  @bot.on.state(states.parameters)
  def group_auth(self):
    if 'Группа' in self.text:
      bot.db.set_state(states.table_register)
      bot.utils.user_message('Введите свою учебную группу как в таблице', keyboard = keyboards.rcircle(), 
                            link=["https://docs.google.com/spreadsheets/d/1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU/edit#gid=0"])
  
  @bot.on.multiply(['Помощь'], [states.parameters])
  def helps(self):
    text = "Интересующие вопросы можете написать сюда :"
    bot.utils.user_message(text, link=['https://vk.com/topic-214878797_49282332'])
