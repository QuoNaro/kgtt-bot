from vk_api.keyboard import VkKeyboard,VkKeyboardColor
from emoji import emojize as emj

def selection():
  keyboard = VkKeyboard()
  keyboard.add_button(emj(':thumbs_up:'), color=VkKeyboardColor.POSITIVE)
  keyboard.add_button(emj(':thumbs_down:'), color=VkKeyboardColor.NEGATIVE)
  keyboard.add_line()
  keyboard.add_button(emj(':hollow_red_circle:'),color=VkKeyboardColor.SECONDARY)
  return keyboard.get_keyboard()

def main():
    keyboard = VkKeyboard()
    keyboard.add_button("Расписание", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Оценки", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(emj(':gear:'), color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def schedule():
  keyboard = VkKeyboard()
  keyboard.add_button("Из таблицы", color=VkKeyboardColor.SECONDARY)
  keyboard.add_button("Рассылка", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button(emj(':hollow_red_circle:'),color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

def mailing():
  keyboard = VkKeyboard()
  keyboard.add_button("Отписаться", color=VkKeyboardColor.SECONDARY)
  keyboard.add_button("Подписаться", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button(emj(':hollow_red_circle:'),color=VkKeyboardColor.NEGATIVE)
  
  
  return keyboard.get_keyboard()

def parameters():
  keyboard = VkKeyboard()
  keyboard.add_button("Изменить логин и пароль Ruobr", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button("Изменить объект", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button("Помощь", color=VkKeyboardColor.POSITIVE)
  keyboard.add_line()
  keyboard.add_button(emj(':hollow_red_circle:'),color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

def prediction():
  keyboard = VkKeyboard()
  keyboard.add_button("На завтра", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button(emj(':hollow_red_circle:'),color=VkKeyboardColor.NEGATIVE)
  
  return keyboard.get_keyboard()

def marks():
  keyboard = VkKeyboard()
  keyboard.add_button("На сегодня", color=VkKeyboardColor.SECONDARY)
  keyboard.add_button("За месяц", color=VkKeyboardColor.SECONDARY)
  keyboard.add_button("За год", color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button('Таблица оценок',color=VkKeyboardColor.POSITIVE)
  keyboard.add_line()
  keyboard.add_button(emj(':hollow_red_circle:'),color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

def ok():
  keyboard = VkKeyboard()
  keyboard.add_button(emj(':OK_button:'), color=VkKeyboardColor.POSITIVE)
  return keyboard.get_keyboard()

def cancel():
  keyboard = VkKeyboard()
  keyboard.add_button(emj(':hollow_red_circle:'), color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

def empty():
  VkKeyboard().get_empty_keyboard()

def excel():
  keyboard = VkKeyboard()
  keyboard.add_button('За этот учебный год',color=VkKeyboardColor.SECONDARY)
  keyboard.add_line()
  keyboard.add_button(emj(':hollow_red_circle:'), color=VkKeyboardColor.NEGATIVE)
  return keyboard.get_keyboard()

def rcircle():
    keyboard = VkKeyboard()
    keyboard.add_button(emj(':hollow_red_circle:'), color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()