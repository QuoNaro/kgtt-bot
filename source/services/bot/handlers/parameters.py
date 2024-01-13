from start import kgtt
from data import keyboards,states,emoji
from vk import Bot, generate_keyboard,dbutils


def parameters_keyboard(self : Bot):
  """Меню параметров с динамическими кнопками"""
  password = lambda x : '*' * len(x) if x != None else None
  mail_status = int(dbutils.check_mailing_status(self))
  buttons = [(f"Логин : {self.info.Login}","secondary"),
              (f"Пароль : {password(self.info.Password)}","secondary"),
              None,
              (f"Группа : {self.info.UserGroup}","secondary"),
              (f"{['Включить рассылку','Отключить рассылку'][mail_status]}",['positive','negative'][mail_status]),
              None,
              ("Помощь","positive"),
              None,
              (emoji.red_circle,"negative")]
  
  index_balance = 0
  if not self.info.Password and not self.info.Login :
    buttons.pop(0)
    index_balance+=1
    buttons[0] = ("Авторизация Ruobr","secondary")
    
  if not self.info.UserGroup:
    buttons.pop(4-index_balance)
    buttons[3-index_balance] = ("Группа не выбрана","secondary")
    
  return generate_keyboard(*buttons)
  
@kgtt.on.multiply([emoji.gear], [states.main])
def parameters(self : Bot):
    dbutils.set_state(self,states.parameters)
    kgtt.utils.user_message("Параметры", keyboard = parameters_keyboard(self))
    

class Parameters:

  @kgtt.on.state(states.parameters)
  def ruobr_auth(self : Bot):
    if self.message.text == "Авторизация Ruobr" or "Пароль" in self.message.text or "Логин" in self.message.text:
      dbutils.set_state(self,states.ruobr_register[0])
      kgtt.utils.user_message('Введите логин от Cabinet Ruobr', keyboard = keyboards.cancel())
  
  @kgtt.on.state(states.parameters)
  def group_auth(self : Bot):
    if 'Группа' in self.message.text:
      dbutils.set_state(self,states.table_register)
      kgtt.utils.user_message('Введите свою учебную группу как в таблице', keyboard = keyboards.cancel(), 
                            link=["https://clck.ru/psvfm"])
      

  @kgtt.on.state(states.parameters)
  def change_mailing(self : Bot):
    if 'рассылку' in self.message.text:
      if dbutils.check_mailing_status(self):
        dbutils.off_mailing_status(self)
      else:
        dbutils.on_mailing_status(self)
      kgtt.utils.user_message('Успешно',keyboard=keyboards.main())
      dbutils.set_state(self, states.main)
      
      
  
  @kgtt.on.multiply(['Помощь'], [states.parameters])
  def helps(self : Bot):
    text = "Интересующие вопросы можете написать сюда :"
    kgtt.utils.user_message(text, link=['https://vk.com/topic-214878797_49282332'])
