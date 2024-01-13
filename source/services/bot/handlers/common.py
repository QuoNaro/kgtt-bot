from start import kgtt
from data import keyboards,states,emoji
from vk import Bot, generate_keyboard,dbutils

@kgtt.on.empty('self.info.State == None and self.message.text != "Начать"')
def main_menu(self : Bot):
    self.utils.user_message('Давайте начнем!',keyboard=generate_keyboard(
        ("Начать",'positive')
    ))
    
@kgtt.on.message('Начать')
def start(self : Bot):
    dbutils.set_state(self, states.main)
    self.utils.user_message('Добро пожаловать!',keyboard=keyboards.main())

@kgtt.on.message('!сброс')
def reset(self : Bot):
    dbutils.delete_user_information(self)
    self.utils.user_message('Все данные успешно удалены!', keyboard = keyboards.main())

@kgtt.on.message(emoji.red_circle)
def back(self : Bot):
    dbutils.set_state(self,states.main)
    self.utils.user_message('Главное меню', keyboard = keyboards.main())

@kgtt.on.message('Из таблицы', 'Рассылка')
def old_commands(self : Bot):
    dbutils.set_state(self,states.main)
    self.utils.user_message('Данной функции больше не существует, возвращаемся в главное меню', keyboard = keyboards.main())
    

    